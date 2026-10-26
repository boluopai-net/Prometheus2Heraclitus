import {authenticated} from './content-release.js';
import {musicIdentity} from './music-identity.js';

const API = '/api/music';
const PREFIX = 'site-music/v1/';
const CATALOG = PREFIX + 'catalog.json';
const MAX_BYTES = 32 * 1024 * 1024;
const PART_BYTES = 8 * 1024 * 1024;
const MAX_TRACK_BYTES = 512 * 1024 * 1024;
// A completion may contend with every other job in the supported upload batch.
const WRITE_ATTEMPTS = 32;
const ID = /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/;
const HEADERS = {'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','X-Robots-Tag':'noindex, nofollow'};
const json = (data,status=200,headers={}) => new Response(JSON.stringify(data),{status,headers:{...HEADERS,'Content-Type':'application/json; charset=utf-8',...headers}});
const fail = (status,message) => {throw Object.assign(new Error(message),{status});};
const empty = () => ({enabled:true,defaultTrack:null,tracks:[]});

export function musicOwner(request,env) {
  const id=request.headers.get('oai-authenticated-user-id'), email=request.headers.get('oai-authenticated-user-email');
  if (!id || !email) return false;
  return env.OWNER_USER_ID ? id===env.OWNER_USER_ID : !!env.OWNER_EMAIL && email.toLowerCase()===env.OWNER_EMAIL.toLowerCase();
}
async function catalog(bucket,key=CATALOG) {
  const object=await bucket.get(key);
  return {data:object ? await object.json() : empty(),etag:object?.etag || null};
}
async function writeCatalog(bucket,data,etag,key=CATALOG) {
  const object=await bucket.put(key,JSON.stringify(data),{httpMetadata:{contentType:'application/json'},onlyIf:etag ? {etagMatches:etag}:{etagDoesNotMatch:'*'}});
  if (!object) fail(409,'The playlist changed. Refresh and retry.');
  return object.etag;
}
const defaultIds=data=>data.defaultIds || data.tracks.map(track=>track.id);
function playlistView(data,library) {
  const byId=new Map(library.tracks.map(track=>[track.id,track]));
  const tracks=data.ids.map(id=>byId.get(id)).filter(Boolean);
  return {enabled:data.enabled,tracks,defaultTrack:tracks.some(track=>track.id===data.defaultTrack)?data.defaultTrack:tracks[0]?.id||null};
}
const defaults=data=>playlistView({enabled:data.enabled,ids:defaultIds(data),defaultTrack:data.defaultTrack},data);
const personalKey=user=>PREFIX+'playlists/github/'+user.id+'.json';
async function personalCatalog(bucket,user,library) {
  const object=await bucket.get(personalKey(user));
  return {data:object?await object.json():{enabled:library.enabled,ids:defaultIds(library),defaultTrack:defaults(library).defaultTrack},etag:object?.etag||null};
}
async function appendPersonal(bucket,user,track) {
  for(let attempt=0;attempt<WRITE_ATTEMPTS;attempt++){
    const library=(await catalog(bucket)).data,state=await personalCatalog(bucket,user,library);
    const included=state.data.ids.includes(track.id);
    if(included&&state.etag)return state.etag;
    if(!included&&state.data.ids.length>=200)fail(422,'The playlist limit is 200 tracks.');
    const data={...state.data,ids:included?state.data.ids:[...state.data.ids,track.id],defaultTrack:state.data.defaultTrack||track.id};
    try{return await writeCatalog(bucket,data,state.etag,personalKey(user));}catch(e){if(e.status!==409||attempt===WRITE_ATTEMPTS-1)throw e;}
  }
}
function text(value,max=200) {
  if (typeof value!=='string' || value.length>max || /[\u0000-\u001f]/.test(value)) fail(422,'Invalid track details.');
  return value.trim();
}
function audioType(bytes) {
  const start=new TextDecoder().decode(bytes.slice(0,12));
  if (start.startsWith('ID3') || (bytes[0]===255 && (bytes[1]&224)===224)) return 'audio/mpeg';
  if (start.startsWith('OggS')) return 'audio/ogg';
  if (start.startsWith('fLaC')) return 'audio/flac';
  if (start.startsWith('RIFF') && start.slice(8)==='WAVE') return 'audio/wav';
  if (start.slice(4,8)==='ftyp') return 'audio/mp4';
  fail(415,'Use MP3, M4A, OGG, FLAC or WAV audio. NCM is not a browser audio format.');
}
async function bodyBytes(request,limit) {
  const declared=Number(request.headers.get('content-length'));
  if (declared>limit) fail(413,'The request body is too large.');
  if (!request.body) fail(422,'Empty upload.');
  const reader=request.body.getReader(),chunks=[];let size=0;
  while (true) {
    const {done,value}=await reader.read();if(done)break;
    size+=value.byteLength;if(size>limit){await reader.cancel();fail(413,'The request body is too large.');}chunks.push(value);
  }
  const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
  return bytes;
}
async function bodyJson(request,limit=16*1024) {
  const bytes=await bodyBytes(request,limit);
  try{const data=JSON.parse(new TextDecoder().decode(bytes));if(!data||typeof data!=='object'||Array.isArray(data))throw new Error();return data;}catch{fail(422,'Invalid upload details.');}
}
async function uploadState(bucket,id,uploadId,actor='owner') {
  const object=await bucket.get(PREFIX+'uploads/'+id+'.json');
  if(!object)fail(404,'Upload not found.');
  const data=await object.json();
  if((data.actor||'owner')!==actor)fail(403,'This upload belongs to another account.');
  if(data.uploadId!==uploadId)fail(409,'Invalid upload identifier.');
  return {data,etag:object.etag};
}
async function audioDigest(bucket,id) {
  const object=await bucket.get(PREFIX+'audio/'+id);
  if(!object)fail(409,'Audio changed. Refresh and retry.');
  // Hash stored decoded audio, independent of multipart boundaries or filenames.
  // DigestStream retains no audio bytes, including for the 512 MiB upload path.
  const stream=new crypto.DigestStream('SHA-256');
  await object.body.pipeTo(stream);
  return [...new Uint8Array(await stream.digest)].map(byte=>byte.toString(16).padStart(2,'0')).join('');
}
async function addTrack(bucket,track,ownerDefault=true) {
  const fingerprints=new Map();
  try {
    track={...track,sha256:await audioDigest(bucket,track.id)};
    for(let attempt=0;attempt<WRITE_ATTEMPTS;attempt++){
      const state=await catalog(bucket);
      const existing=state.data.tracks.find(t=>t.id===track.id);
      if(existing){
        if(ownerDefault&&!defaultIds(state.data).includes(existing.id)){
          const data={...state.data,defaultIds:[...defaultIds(state.data),existing.id],defaultTrack:state.data.defaultTrack||existing.id};
          try{return json({track:existing,etag:await writeCatalog(bucket,data,state.etag)});}catch(e){if(e.status!==409||attempt===WRITE_ATTEMPTS-1)throw e;continue;}
        }
        return json({track:existing,etag:state.etag});
      }
      const ids=[...defaultIds(state.data)];
      const tracks=[];let duplicate;
      for(const candidate of state.data.tracks){
        let current=candidate;
        if(candidate.bytes===track.bytes){
          let digest=candidate.sha256;
          if(!digest){
            digest=fingerprints.get(candidate.id)||await audioDigest(bucket,candidate.id);
            fingerprints.set(candidate.id,digest);
            current={...candidate,sha256:digest};
          }
          if(digest===track.sha256&&!duplicate)duplicate=current;
        }
        tracks.push(current);
      }
      if(duplicate){
        try{
          // CAS also protects a match against concurrent playlist edits. Never
          // remove an existing recording; discard only this unreferenced upload.
          if(ownerDefault&&!ids.includes(duplicate.id))ids.push(duplicate.id);
          const etag=await writeCatalog(bucket,{...state.data,tracks,defaultIds:ids,defaultTrack:ownerDefault?(state.data.defaultTrack||duplicate.id):state.data.defaultTrack},state.etag);
          // Personal completion retains its temporary object until its own
          // playlist CAS succeeds, so a failed attachment can safely retry.
          if(ownerDefault)await bucket.delete(PREFIX+'audio/'+track.id);
          return json({track:duplicate,etag,duplicate:true});
        }catch(e){if(e.status!==409||attempt===WRITE_ATTEMPTS-1)throw e;continue;}
      }
      if(state.data.tracks.length>=200)fail(422,'The playlist limit is 200 tracks.');
      if(ownerDefault)ids.push(track.id);
      const data={...state.data,defaultIds:ids,defaultTrack:ownerDefault?(state.data.defaultTrack||track.id):state.data.defaultTrack,tracks:[...tracks,track]};
      try{return json({track,etag:await writeCatalog(bucket,data,state.etag)},201);}catch(e){if(e.status!==409||attempt===WRITE_ATTEMPTS-1)throw e;}
    }
  } catch(e) {
    // Reconcile an uncertain write before removing this upload's object.
    const current=await catalog(bucket),existing=current.data.tracks.find(t=>t.id===track.id);
    if(existing)return json({track:existing,etag:current.etag});
    await bucket.delete(PREFIX+'audio/'+track.id);throw e;
  }
}
async function multipartResponse(request,bucket,id,action,partNumber,user=null) {
  const key=PREFIX+'audio/'+id,stateKey=PREFIX+'uploads/'+id+'.json';
  const actor=user?'github:'+user.id:'owner';
  if(!action && request.method==='POST'){
    const meta=await bodyJson(request),title=text(meta.title),artist=text(meta.artist||'');
    if(!title)fail(422,'A track title is required.');
    if(!Number.isSafeInteger(meta.bytes)||meta.bytes<12||meta.bytes>MAX_TRACK_BYTES)fail(422,'Audio must be between 12 bytes and 512 MiB.');
    const current=await catalog(bucket);
    if(current.data.tracks.some(t=>t.id===id)||await bucket.head(key)||await bucket.head(stateKey))fail(409,'This upload identifier is already in use.');
    const token=crypto.randomUUID();
    const upload=await bucket.createMultipartUpload(key,{httpMetadata:{contentType:'application/octet-stream'},customMetadata:{musicUpload:token}});
    try {
      const state={uploadId:upload.uploadId,token,actor,title,artist,bytes:meta.bytes,parts:[],contentType:null};
      const stored=await bucket.put(stateKey,JSON.stringify(state),{onlyIf:{etagDoesNotMatch:'*'}});
      if(!stored)fail(409,'This upload identifier is already in use.');
    } catch(e){await upload.abort();throw e;}
    return json({uploadId:upload.uploadId,partBytes:PART_BYTES,maxBytes:MAX_TRACK_BYTES,parts:Math.ceil(meta.bytes/PART_BYTES)},201);
  }
  if(!action && request.method==='DELETE'){
    const {data}=await uploadState(bucket,id,request.headers.get('x-music-upload-id'),actor);
    await bucket.resumeMultipartUpload(key,data.uploadId).abort();
    await bucket.delete(stateKey);
    return json({aborted:true});
  }
  if(action==='parts' && request.method==='PUT'){
    const {data,etag}=await uploadState(bucket,id,request.headers.get('x-music-upload-id'),actor);
    const totalParts=Math.ceil(data.bytes/PART_BYTES);
    if(!Number.isSafeInteger(partNumber)||partNumber<1||partNumber>totalParts||partNumber!==data.parts.length+1)fail(409,'Upload parts in order.');
    const expected=Math.min(PART_BYTES,data.bytes-(partNumber-1)*PART_BYTES);
    const bytes=await bodyBytes(request,expected);
    if(bytes.byteLength!==expected)fail(422,'Upload part size does not match the declared audio size.');
    if(partNumber===1)data.contentType=audioType(bytes);
    const part=await bucket.resumeMultipartUpload(key,data.uploadId).uploadPart(partNumber,bytes);
    data.parts.push({partNumber:part.partNumber,etag:part.etag});
    const stored=await bucket.put(stateKey,JSON.stringify(data),{onlyIf:{etagMatches:etag}});
    if(!stored)fail(409,'The upload changed. Abort and retry.');
    return json({partNumber:part.partNumber,etag:part.etag});
  }
  if(action==='complete' && request.method==='POST'){
    const meta=await bodyJson(request),{data}=await uploadState(bucket,id,meta.uploadId,actor);
    if(data.parts.length!==Math.ceil(data.bytes/PART_BYTES)||!data.contentType)fail(422,'Upload all audio parts before completing.');
    // A successful completion can precede a lost response; reconcile its object.
    let object=await bucket.head(key);
    if(!object){await bucket.resumeMultipartUpload(key,data.uploadId).complete(data.parts);object=await bucket.head(key);}
    if(!object||object.customMetadata?.musicUpload!==data.token)fail(409,'The uploaded audio does not match this upload.');
    if(object.size!==data.bytes){await bucket.delete(key);fail(422,'The completed audio size does not match the declared size.');}
    const track={id,title:data.title,artist:data.artist,bytes:object.size,contentType:data.contentType,src:'/media/music/'+id};
    let response=await addTrack(bucket,track,!user);
    if(user){
      const result=await response.json();
      result.etag=await appendPersonal(bucket,user,result.track);
      if(result.duplicate)await bucket.delete(key);
      response=json(result,response.status);
    }
    await bucket.delete(stateKey);
    return response;
  }
  return json({error:'Method not allowed'},405);
}
async function mediaResponse(request,bucket,id) {
  const state=await catalog(bucket),track=state.data.tracks.find(track=>track.id===id);
  if (!track) return json({error:'Not found'},404);
  const key=PREFIX+'audio/'+id,head=await bucket.head(key);
  if (!head) return json({error:'Not found'},404);
  const headers={...HEADERS,'Content-Type':track.contentType,'Accept-Ranges':'bytes',ETag:head.httpEtag,'Content-Length':String(head.size)};
  if(request.headers.get('if-none-match')===head.httpEtag)return new Response(null,{status:304,headers});
  let range;
  const raw=request.headers.get('range');
  if(raw && (!request.headers.get('if-range') || request.headers.get('if-range')===head.httpEtag)){
    const m=/^bytes=(\d*)-(\d*)$/.exec(raw);
    if(!m || (!m[1]&&!m[2]))return new Response(null,{status:416,headers:{...headers,'Content-Range':`bytes */${head.size}`,'Content-Length':'0'}});
    const start=m[1]?Number(m[1]):Math.max(0,head.size-Number(m[2]));
    const end=m[1]&&m[2]?Math.min(Number(m[2]),head.size-1):head.size-1;
    if(!Number.isSafeInteger(start)||!Number.isSafeInteger(end)||start>end||start>=head.size)return new Response(null,{status:416,headers:{...headers,'Content-Range':`bytes */${head.size}`,'Content-Length':'0'}});
    range={offset:start,length:end-start+1};headers['Content-Range']=`bytes ${start}-${end}/${head.size}`;headers['Content-Length']=String(range.length);
  }
  if(request.method==='HEAD')return new Response(null,{status:range?206:200,headers});
  const object=await bucket.get(key,range?{range}:{});
  return new Response(object.body,{status:range?206:200,headers});
}
async function personalResponse(request,bucket,path,user) {
  if(path===API+'/personal/session'&&request.method==='GET')return json({canManage:!!user,user,signIn:'/auth/github?returnTo=/music/'});
  if(!user)return json({error:'Sign in with GitHub to manage your playlist.'},401);
  if(request.method!=='GET'&&request.headers.get('origin')!==new URL(request.url).origin)return json({error:'Invalid request origin.'},403);
  const upload=path.match(/^\/api\/music\/personal\/tracks\/([a-f0-9-]+)\/upload(?:\/(complete)|\/parts\/([1-9]\d*))?$/);
  if(upload&&ID.test(upload[1]))return multipartResponse(request,bucket,upload[1],upload[2]||(upload[3]?'parts':null),Number(upload[3]),user);
  const library=(await catalog(bucket)).data,state=await personalCatalog(bucket,user,library);
  if(path===API+'/personal/catalog'){
    if(request.method==='GET')return json({...playlistView(state.data,library),active:state.data.enabled,etag:state.etag,profileKey:'github:'+user.id});
    if(request.method==='PUT'){
      if(request.headers.get('if-match')!==(state.etag||'empty'))fail(409,'The playlist changed. Refresh and retry.');
      const next=await bodyJson(request,128*1024);
      if(typeof next.enabled!=='boolean'||!Array.isArray(next.tracks)||next.tracks.length>200)fail(422,'Invalid playlist.');
      const known=new Set(library.tracks.map(track=>track.id)),ids=[];
      for(const track of next.tracks){
        if(!track||!known.has(track.id)||ids.includes(track.id))fail(422,'Invalid track.');
        ids.push(track.id);
      }
      if(next.defaultTrack!==null&&!ids.includes(next.defaultTrack))fail(422,'Invalid default track.');
      const data={enabled:next.enabled,ids,defaultTrack:next.defaultTrack||ids[0]||null};
      return json({etag:await writeCatalog(bucket,data,state.etag,personalKey(user))});
    }
    return json({error:'Method not allowed'},405);
  }
  const track=path.match(/^\/api\/music\/personal\/tracks\/([a-f0-9-]+)$/);
  if(track&&ID.test(track[1])&&request.method==='DELETE'){
    if(request.headers.get('if-match')!==(state.etag||'empty'))fail(409,'The playlist changed. Refresh and retry.');
    if(!state.data.ids.includes(track[1]))fail(404,'Track not found in your playlist.');
    const ids=state.data.ids.filter(id=>id!==track[1]);
    const data={...state.data,ids,defaultTrack:state.data.defaultTrack===track[1]?(ids[0]||null):state.data.defaultTrack};
    return json({etag:await writeCatalog(bucket,data,state.etag,personalKey(user))});
  }
  return json({error:'Not found'},404);
}

export async function siteMusic(request,env) {
  const url=new URL(request.url),path=url.pathname;
  const media=path.match(/^\/media\/music\/([a-f0-9-]+)$/);
  if(!path.startsWith(API+'/') && !media)return null;
  try {
    if(!env.BUCKET)return json({error:'Music storage unavailable'},503);
    const bucket=env.BUCKET;
    if(media){if(!ID.test(media[1]))return json({error:'Not found'},404);if(!['GET','HEAD'].includes(request.method))return json({error:'Method not allowed'},405);return await mediaResponse(request,bucket,media[1]);}
    if(path===API+'/catalog' && request.method==='GET'){
      const state=await catalog(bucket);
      return json({...defaults(state.data),active:state.data.enabled,etag:state.etag});
    }
    if(path===API+'/library'&&request.method==='GET'){
      const state=await catalog(bucket);return json({tracks:state.data.tracks,etag:state.etag});
    }
    if(path===API+'/playback'&&request.method==='GET'){
      const library=await catalog(bucket),user=await musicIdentity(request,env);
      if(!user)return json({...defaults(library.data),active:library.data.enabled,etag:library.etag,profileKey:'default'});
      const state=await personalCatalog(bucket,user,library.data),view=playlistView(state.data,library.data);
      return json({...view,active:view.enabled,etag:state.etag,profileKey:'github:'+user.id});
    }
    if(path.startsWith(API+'/personal/'))return await personalResponse(request,bucket,path,await musicIdentity(request,env));
    const owner=musicOwner(request,env),publisher=await authenticated(request,env);
    if(path===API+'/session' && request.method==='GET')return json({canManage:owner||publisher,signIn:'/signin-with-chatgpt?return_to=%2Fmusic%2Fmanage%2F'});
    if(!owner&&!publisher)return json({error:'Only the site owner can manage music.'},401);
    if(!publisher && request.headers.get('origin')!==url.origin)return json({error:'Invalid request origin.'},403);
    if(request.headers.get('origin') && request.headers.get('origin')!==url.origin)return json({error:'Invalid request origin.'},403);
    const uploadRoute=path.match(/^\/api\/music\/tracks\/([a-f0-9-]+)\/upload(?:\/(complete)|\/parts\/([1-9]\d*))?$/);
    if(uploadRoute && ID.test(uploadRoute[1]))return await multipartResponse(request,bucket,uploadRoute[1],uploadRoute[2]||(uploadRoute[3]?'parts':null),Number(uploadRoute[3]));
    const trackRoute=path.match(/^\/api\/music\/tracks\/([a-f0-9-]+)$/);
    if(trackRoute && ID.test(trackRoute[1])){
      const id=trackRoute[1],key=PREFIX+'audio/'+id;
      if(request.method==='PUT'){
        let meta;try{meta=JSON.parse(decodeURIComponent(request.headers.get('x-music-details')||''));}catch{fail(422,'Invalid track details.');}
        const title=text(meta.title),artist=text(meta.artist||'');if(!title)fail(422,'A track title is required.');
        let state=await catalog(bucket);
        if(state.data.tracks.some(t=>t.id===id))return await addTrack(bucket,state.data.tracks.find(t=>t.id===id));
        if(await bucket.head(PREFIX+'uploads/'+id+'.json'))fail(409,'A multipart upload is using this identifier.');
        const bytes=await bodyBytes(request,MAX_BYTES),contentType=audioType(bytes);
        const object=await bucket.put(key,bytes,{httpMetadata:{contentType},onlyIf:{etagDoesNotMatch:'*'}});
        if(!object)fail(409,'This upload identifier is already in use.');
        const track={id,title,artist,bytes:bytes.byteLength,contentType,src:'/media/music/'+id};
        return await addTrack(bucket,track);
      }
      if(request.method==='DELETE'){
        const state=await catalog(bucket);
        if(request.headers.get('if-match')!==state.etag)fail(409,'The playlist changed. Refresh and retry.');
        if(!defaultIds(state.data).includes(id))fail(404,'Track not found in the default playlist.');
        const ids=defaultIds(state.data).filter(trackId=>trackId!==id);
        const data={...state.data,defaultIds:ids,defaultTrack:state.data.defaultTrack===id?(ids[0]||null):state.data.defaultTrack};
        return json({etag:await writeCatalog(bucket,data,state.etag)});
      }
    }
    if(path===API+'/catalog' && request.method==='PUT'){
      const bytes=await bodyBytes(request,128*1024);let next;try{next=JSON.parse(new TextDecoder().decode(bytes));}catch{fail(422,'Invalid playlist.');}
      const state=await catalog(bucket);
      if(request.headers.get('if-match')!==(state.etag||'empty'))fail(409,'The playlist changed. Refresh and retry.');
      const originalDefaults=defaults(state.data).tracks;
      if(typeof next.enabled!=='boolean'||!Array.isArray(next.tracks)||next.tracks.length!==originalDefaults.length)fail(422,'Invalid playlist.');
      const byId=new Map(originalDefaults.map(t=>[t.id,t]));
      const tracks=next.tracks.map(t=>{if(!byId.has(t.id))fail(422,'Invalid track.');const original=byId.get(t.id);byId.delete(t.id);const title=text(t.title);if(!title)fail(422,'A track title is required.');return {...original,title,artist:text(t.artist||'')};});
      if(next.defaultTrack!==null&&!tracks.some(t=>t.id===next.defaultTrack))fail(422,'Invalid default track.');
      const edited=new Map(tracks.map(track=>[track.id,track]));
      const data={...state.data,enabled:next.enabled,tracks:state.data.tracks.map(track=>edited.get(track.id)||track),defaultIds:tracks.map(track=>track.id),defaultTrack:next.defaultTrack||tracks[0]?.id||null};
      return json({etag:await writeCatalog(bucket,data,state.etag)});
    }
    return json({error:'Not found'},404);
  }catch(e){return json({error:e.status?e.message:'Music operation failed. Refresh before retrying.'},e.status||503);}
}
