import {authenticated} from './content-release.js';

const API = '/api/music';
const PREFIX = 'site-music/v1/';
const CATALOG = PREFIX + 'catalog.json';
const MAX_BYTES = 32 * 1024 * 1024;
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
async function catalog(bucket) {
  const object=await bucket.get(CATALOG);
  return {data:object ? await object.json() : empty(),etag:object?.etag || null};
}
async function writeCatalog(bucket,data,etag) {
  const object=await bucket.put(CATALOG,JSON.stringify(data),{httpMetadata:{contentType:'application/json'},onlyIf:etag ? {etagMatches:etag}:{etagDoesNotMatch:'*'}});
  if (!object) fail(409,'The playlist changed. Refresh and retry.');
  return object.etag;
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
  if (declared>limit) fail(413,'The file exceeds 32 MB.');
  if (!request.body) fail(422,'Empty upload.');
  const reader=request.body.getReader(),chunks=[];let size=0;
  while (true) {
    const {done,value}=await reader.read();if(done)break;
    size+=value.byteLength;if(size>limit){await reader.cancel();fail(413,'The file exceeds 32 MB.');}chunks.push(value);
  }
  const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
  return bytes;
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
      return json({...state.data,active:state.data.enabled,etag:state.etag});
    }
    const owner=musicOwner(request,env),publisher=await authenticated(request,env);
    if(path===API+'/session' && request.method==='GET')return json({canManage:owner||publisher,signIn:'/signin-with-chatgpt?return_to=%2Fmusic%2Fmanage%2F'});
    if(!owner&&!publisher)return json({error:'Only the site owner can manage music.'},401);
    if(!publisher && request.headers.get('origin')!==url.origin)return json({error:'Invalid request origin.'},403);
    if(request.headers.get('origin') && request.headers.get('origin')!==url.origin)return json({error:'Invalid request origin.'},403);
    const trackRoute=path.match(/^\/api\/music\/tracks\/([a-f0-9-]+)$/);
    if(trackRoute && ID.test(trackRoute[1])){
      const id=trackRoute[1],key=PREFIX+'audio/'+id;
      if(request.method==='PUT'){
        let meta;try{meta=JSON.parse(decodeURIComponent(request.headers.get('x-music-details')||''));}catch{fail(422,'Invalid track details.');}
        const title=text(meta.title),artist=text(meta.artist||'');if(!title)fail(422,'A track title is required.');
        let state=await catalog(bucket);
        if(state.data.tracks.some(t=>t.id===id))return json({track:state.data.tracks.find(t=>t.id===id),etag:state.etag});
        if(state.data.tracks.length>=200)fail(422,'The playlist limit is 200 tracks.');
        const bytes=await bodyBytes(request,MAX_BYTES),contentType=audioType(bytes);
        const object=await bucket.put(key,bytes,{httpMetadata:{contentType},onlyIf:{etagDoesNotMatch:'*'}});
        if(!object)fail(409,'This upload identifier is already in use.');
        const track={id,title,artist,bytes:bytes.byteLength,contentType,src:'/media/music/'+id};
        try {
          for(let attempt=0;attempt<3;attempt++){
            state=await catalog(bucket);
            if(state.data.tracks.some(t=>t.id===id))return json({track,etag:state.etag});
            if(state.data.tracks.length>=200)fail(422,'The playlist limit is 200 tracks.');
            const data={...state.data,defaultTrack:state.data.defaultTrack||id,tracks:[...state.data.tracks,track]};
            try{return json({track,etag:await writeCatalog(bucket,data,state.etag)},201);}catch(e){if(e.status!==409||attempt===2)throw e;}
          }
        } catch(e) {
          // Reconcile an uncertain write before removing this upload's object.
          const current=await catalog(bucket);
          if(current.data.tracks.some(t=>t.id===id))return json({track,etag:current.etag});
          await bucket.delete(key);throw e;
        }
      }
      if(request.method==='DELETE'){
        const state=await catalog(bucket);
        if(request.headers.get('if-match')!==state.etag)fail(409,'The playlist changed. Refresh and retry.');
        const tracks=state.data.tracks.filter(t=>t.id!==id);
        const data={...state.data,tracks,defaultTrack:state.data.defaultTrack===id?(tracks[0]?.id||null):state.data.defaultTrack};
        const etag=await writeCatalog(bucket,data,state.etag);await bucket.delete(key);return json({etag});
      }
    }
    if(path===API+'/catalog' && request.method==='PUT'){
      const bytes=await bodyBytes(request,128*1024);let next;try{next=JSON.parse(new TextDecoder().decode(bytes));}catch{fail(422,'Invalid playlist.');}
      const state=await catalog(bucket);
      if(request.headers.get('if-match')!==(state.etag||'empty'))fail(409,'The playlist changed. Refresh and retry.');
      if(typeof next.enabled!=='boolean'||!Array.isArray(next.tracks)||next.tracks.length!==state.data.tracks.length)fail(422,'Invalid playlist.');
      const byId=new Map(state.data.tracks.map(t=>[t.id,t]));
      const tracks=next.tracks.map(t=>{if(!byId.has(t.id))fail(422,'Invalid track.');const original=byId.get(t.id);byId.delete(t.id);const title=text(t.title);if(!title)fail(422,'A track title is required.');return {...original,title,artist:text(t.artist||'')};});
      if(next.defaultTrack!==null&&!tracks.some(t=>t.id===next.defaultTrack))fail(422,'Invalid default track.');
      const data={enabled:next.enabled,tracks,defaultTrack:next.defaultTrack||tracks[0]?.id||null};
      return json({etag:await writeCatalog(bucket,data,state.etag)});
    }
    return json({error:'Not found'},404);
  }catch(e){return json({error:e.status?e.message:'Music operation failed. Refresh before retrying.'},e.status||503);}
}
