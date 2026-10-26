import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {randomUUID,createHash,createHmac} from 'node:crypto';
const require=createRequire(process.env.MUSIC_TEST_PACKAGE || new URL('../package.json',import.meta.url));
const {build}=require('esbuild'),{Miniflare}=require('miniflare');

test('music API deduplicates exact decoded audio across upload paths and concurrent jobs',async t=>{
  const built=await build({stdin:{contents:"import {siteMusic} from './lib/site-music.js';export default {fetch:siteMusic};",resolveDir:process.cwd()},bundle:true,write:false,format:'esm',platform:'browser'});
  const mf=new Miniflare({modules:true,script:built.outputFiles[0].text,compatibilityDate:'2026-05-15',r2Buckets:['BUCKET'],bindings:{OWNER_EMAIL:'owner@example.invalid'}});
  t.after(()=>mf.dispose());
  const bucket=await mf.getR2Bucket('BUCKET');
  const owner={'oai-authenticated-user-id':'owner','oai-authenticated-user-email':'owner@example.invalid',Origin:'https://music.invalid'};
  const call=(path,method='GET',body,headers={})=>mf.dispatchFetch('https://music.invalid/api/music/'+path,{method,body,headers:{...owner,...headers}});
  const catalog=async()=> (await call('catalog')).json();
  const audio=Buffer.alloc(100);audio.write('RIFF');audio.write('WAVE',8);
  const direct=async(bytes,title='Same title')=>{
    const id=randomUUID(),response=await call('tracks/'+id,'PUT',bytes,{'x-music-details':encodeURIComponent(JSON.stringify({title}))});
    assert.ok([200,201].includes(response.status),await response.clone().text());
    return {id,...await response.json()};
  };
  async function multipart(bytes){
    const id=randomUUID(),path='tracks/'+id+'/upload';
    let response=await call(path,'POST',JSON.stringify({title:'Renamed NCM conversion',bytes:bytes.length}));assert.equal(response.status,201);
    const upload=await response.json();
    for(let offset=0,part=1;offset<bytes.length;offset+=upload.partBytes,part++){
      response=await call(path+'/parts/'+part,'PUT',bytes.subarray(offset,offset+upload.partBytes),{'x-music-upload-id':upload.uploadId});assert.equal(response.status,200,await response.clone().text());
    }
    response=await call(path+'/complete','POST',JSON.stringify({uploadId:upload.uploadId}));
    assert.ok([200,201].includes(response.status),await response.clone().text());
    return {id,...await response.json()};
  }
  assert.equal((await mf.dispatchFetch('https://music.invalid/api/music/tracks/'+randomUUID(),{method:'PUT',body:audio})).status,401);
  const first=await direct(audio);
  const duplicate=await multipart(audio);
  assert.equal(duplicate.duplicate,true);assert.equal(duplicate.track.id,first.id);
  assert.equal(first.track.sha256,createHash('sha256').update(audio).digest('hex'));
  assert.equal(await bucket.head('site-music/v1/audio/'+duplicate.id),null);
  assert.ok(await bucket.head('site-music/v1/audio/'+first.id));
  const different=Buffer.from(audio);different[99]=1;
  const second=await direct(different);assert.notEqual(second.track.id,first.id);
  assert.equal((await catalog()).tracks.length,2,'Same title with different bytes remains distinct');
  // Simulate a pre-fingerprint catalog; retain both existing entries unchanged.
  let state=await catalog();for(const track of state.tracks)delete track.sha256;
  delete state.etag;delete state.active;
  await bucket.put('site-music/v1/catalog.json',JSON.stringify(state));
  const legacy=await direct(audio,'Different filename');assert.equal(legacy.duplicate,true);assert.equal(legacy.track.id,first.id);
  assert.equal((await catalog()).tracks.length,2);
  // Equal bytes uploaded under 32 independent UUIDs must converge to one entry.
  const fresh=Buffer.from(audio);fresh[99]=2;
  const concurrent=await Promise.all(Array.from({length:32},()=>direct(fresh)));
  assert.equal(new Set(concurrent.map(result=>result.track.id)).size,1);
  assert.equal((await catalog()).tracks.length,3);
  assert.equal((await bucket.list({prefix:'site-music/v1/audio/'})).objects.length,3,'No duplicate audio objects retained');
  // Cross multipart boundaries rather than relying on multipart ETags.
  const large=Buffer.alloc(8*1024*1024+12);large.write('RIFF');large.write('WAVE',8);
  const largeFirst=await multipart(large),largeDuplicate=await direct(large);
  assert.equal(largeDuplicate.duplicate,true);assert.equal(largeDuplicate.track.id,largeFirst.id);
  const current=await catalog();
  const reordered={enabled:true,defaultTrack:current.defaultTrack,tracks:current.tracks.map(({id,title,artist})=>({id,title,artist}))};
  assert.equal((await call('catalog','PUT',JSON.stringify(reordered),{'if-match':'stale'})).status,409);
  assert.equal((await call('catalog','PUT',JSON.stringify(reordered),{'if-match':current.etag})).status,200);
  assert.ok((await catalog()).tracks.every(track=>track.sha256),'Editing metadata preserves server fingerprints');
  const legacyDuplicateId=randomUUID(),legacyState=await catalog();
  await bucket.put('site-music/v1/audio/'+legacyDuplicateId,audio);
  legacyState.tracks.push({...legacyState.tracks[0],id:legacyDuplicateId,src:'/media/music/'+legacyDuplicateId});
  delete legacyState.etag;delete legacyState.active;
  await bucket.put('site-music/v1/catalog.json',JSON.stringify(legacyState));
  assert.equal((await direct(audio)).duplicate,true);
  assert.equal((await catalog()).tracks.length,5,'Existing duplicate entries are preserved');
  assert.ok(await bucket.head('site-music/v1/audio/'+legacyDuplicateId),'Existing duplicate audio is preserved');
});

test('GitHub playlists isolate account references and preserve shared audio and owner defaults',async t=>{
  const built=await build({stdin:{contents:"import {siteMusic} from './lib/site-music.js';export default {fetch:siteMusic};",resolveDir:process.cwd()},bundle:true,write:false,format:'esm',platform:'browser'});
  const secret='test-only-github-music-session-secret-0123456789';
  const mf=new Miniflare({modules:true,script:built.outputFiles[0].text,compatibilityDate:'2026-05-15',r2Buckets:['BUCKET'],bindings:{OWNER_EMAIL:'owner@example.invalid',MUSIC_SESSION_SECRET:secret}});
  t.after(()=>mf.dispose());
  const bucket=await mf.getR2Bucket('BUCKET'),origin='https://music.invalid';
  const cookie=(id,login)=>{
    const iat=Math.floor(Date.now()/1000),body=Buffer.from(JSON.stringify({id,login,origin,iat,exp:iat+7*24*60*60})).toString('base64url');
    return '__Host-music-session='+body+'.'+createHmac('sha256',secret).update('session.'+body).digest('base64url');
  };
  const owner={'oai-authenticated-user-id':'owner','oai-authenticated-user-email':'owner@example.invalid',Origin:origin};
  const a={Cookie:cookie('101','alice'),Origin:origin},b={Cookie:cookie('202','bob'),Origin:origin};
  const call=(path,method='GET',body,headers={})=>mf.dispatchFetch(origin+'/api/music/'+path,{method,body,headers});
  const get=async(path,headers={})=>{const response=await call(path,'GET',undefined,headers);assert.equal(response.status,200,await response.clone().text());return response.json();};
  const put=async(next,etag,headers=a)=>call('personal/catalog','PUT',JSON.stringify(next),{...headers,'if-match':etag||'empty'});
  const audio=Buffer.alloc(100);audio.write('RIFF');audio.write('WAVE',8);
  const defaultId=randomUUID();
  assert.equal((await call('tracks/'+defaultId,'PUT',audio,{...owner,'x-music-details':encodeURIComponent(JSON.stringify({title:'Owner default'}))})).status,201);
  assert.equal((await get('personal/session')).canManage,false);
  assert.deepEqual((await get('personal/session',a)).user,{id:'101',login:'alice'});
  assert.equal((await call('personal/catalog')).status,401);
  const inherited=await get('personal/catalog',a);assert.equal(inherited.tracks[0].id,defaultId);assert.equal(inherited.etag,null);
  assert.equal((await get('playback')).profileKey,'default');
  assert.equal((await get('playback',a)).profileKey,'github:101');
  const cleared=await put({enabled:true,defaultTrack:null,tracks:[]},null);assert.equal(cleared.status,200);
  assert.equal((await get('personal/catalog',{Cookie:cookie('101','alice-new-device')})).tracks.length,0,'An explicit empty playlist survives another signed device session');
  assert.equal((await get('playback',a)).tracks.length,0);
  assert.equal((await get('playback',b)).tracks.length,1);
  assert.equal((await get('playback')).tracks.length,1);
  // Bob saves inherited references; future owner-default changes cannot edit them.
  assert.equal((await put({enabled:true,defaultTrack:defaultId,tracks:[{id:defaultId,title:'forged title'}]},null,b)).status,200);
  assert.equal((await get('personal/catalog',b)).tracks[0].title,'Owner default');
  async function begin(bytes,headers=a){
    const id=randomUUID(),path='personal/tracks/'+id+'/upload';
    const response=await call(path,'POST',JSON.stringify({title:'Community upload',artist:'Uploader',bytes:bytes.length}),headers);
    assert.equal(response.status,201,await response.clone().text());return {id,path,...await response.json()};
  }
  async function finish(job,bytes,headers=a){
    let response=await call(job.path+'/parts/1','PUT',bytes,{...headers,'x-music-upload-id':job.uploadId});assert.equal(response.status,200,await response.clone().text());
    response=await call(job.path+'/complete','POST',JSON.stringify({uploadId:job.uploadId}),headers);
    assert.ok([200,201].includes(response.status),await response.clone().text());return response.json();
  }
  const sharedBytes=Buffer.from(audio);sharedBytes[99]=7;
  const job=await begin(sharedBytes);
  assert.equal((await call(job.path+'/parts/1','PUT',sharedBytes,{...b,'x-music-upload-id':job.uploadId})).status,403);
  assert.equal((await call(job.path+'/complete','POST',JSON.stringify({uploadId:job.uploadId}),b)).status,403);
  assert.equal((await call(job.path,'DELETE',undefined,{...b,'x-music-upload-id':job.uploadId})).status,403);
  assert.equal((await call(job.path.replace('personal/','')+'/parts/1','PUT',sharedBytes,{...owner,'x-music-upload-id':job.uploadId})).status,403);
  assert.equal((await call(job.path+'/parts/1','PUT',sharedBytes,{...a,Origin:'https://other.invalid','x-music-upload-id':job.uploadId})).status,403);
  const uploaded=await finish(job,sharedBytes);
  const personal=await get('personal/catalog',a);assert.equal(uploaded.etag,personal.etag);assert.deepEqual(personal.tracks.map(track=>track.id),[job.id]);
  assert.deepEqual((await get('catalog')).tracks.map(track=>track.id),[defaultId]);
  assert.equal((await get('library')).tracks.length,2);
  assert.deepEqual((await get('personal/catalog',b)).tracks.map(track=>track.id),[defaultId]);
  const duplicateJob=await begin(sharedBytes,b),duplicate=await finish(duplicateJob,sharedBytes,b);
  assert.equal(duplicate.duplicate,true);assert.equal(duplicate.track.id,job.id);
  assert.equal(await bucket.head('site-music/v1/audio/'+duplicateJob.id),null);
  assert.equal((await get('library')).tracks.length,2);
  assert.deepEqual((await get('personal/catalog',b)).tracks.map(track=>track.id),[defaultId,job.id]);
  assert.equal((await call('personal/tracks/'+job.id,'DELETE',undefined,{...a,'if-match':'stale'})).status,409);
  assert.equal((await call('personal/tracks/'+job.id,'DELETE',undefined,{...a,'if-match':personal.etag})).status,200);
  assert.equal((await get('personal/catalog',a)).tracks.length,0);
  assert.equal((await get('personal/catalog',b)).tracks.length,2);
  assert.ok(await bucket.head('site-music/v1/audio/'+job.id));
  const emptyState=await get('personal/catalog',a),selection={enabled:true,defaultTrack:job.id,tracks:[{id:job.id,src:'https://forged.invalid/audio',title:'forged'}]};
  assert.equal((await put(selection,emptyState.etag,{Cookie:a.Cookie})).status,403,'Missing Origin is denied');
  assert.equal((await put(selection,emptyState.etag,{...a,Origin:'https://other.invalid'})).status,403);
  assert.equal((await put(selection,emptyState.etag,{...a,Cookie:a.Cookie+'tampered'})).status,401);
  assert.equal((await put({...selection,tracks:[{id:randomUUID()}]},emptyState.etag)).status,422);
  assert.equal((await put({...selection,tracks:[{id:job.id},{id:job.id}]},emptyState.etag)).status,422);
  assert.equal((await put(selection,emptyState.etag)).status,200);
  assert.equal((await get('personal/catalog',a)).tracks[0].title,'Community upload');
  assert.equal((await get('personal/catalog',a)).tracks[0].src,'/media/music/'+job.id);
  const defaults=await get('catalog');
  assert.equal((await call('tracks/'+defaultId,'DELETE',undefined,{...owner,'if-match':defaults.etag})).status,200);
  assert.equal((await get('catalog')).tracks.length,0);
  assert.equal((await get('playback')).tracks.length,0);
  assert.equal((await get('personal/catalog',b)).tracks.length,2,'Owner default removal preserves saved account references');
  assert.equal((await mf.dispatchFetch(origin+'/media/music/'+defaultId)).status,200,'Shared media survives owner default removal');
  const third=Buffer.from(audio);third[99]=8;const ownerNew=randomUUID();
  assert.equal((await call('tracks/'+ownerNew,'PUT',third,{...owner,'x-music-details':encodeURIComponent(JSON.stringify({title:'New owner default'}))})).status,201);
  const ownerState=await get('catalog');assert.deepEqual(ownerState.tracks.map(track=>track.id),[ownerNew]);
  assert.equal((await call('catalog','PUT',JSON.stringify({...ownerState,tracks:[{id:ownerNew,title:'Edited owner title',artist:''}]}),{...owner,'if-match':ownerState.etag})).status,200);
  assert.equal((await get('library')).tracks.length,3,'Owner metadata edits retain community library entries');
  assert.equal((await get('personal/catalog',b)).tracks.length,2);
  const parallel=await Promise.allSettled(Array.from({length:32},async(_,index)=>{
    const bytes=Buffer.from(audio);bytes[98]=index+1;
    return finish(await begin(bytes),bytes);
  }));
  assert.equal(parallel.filter(result=>result.status==='rejected').length,0,'All 32 distinct concurrent uploads finish their shared and personal catalog writes');
  assert.equal((await get('personal/catalog',a)).tracks.length,33);
  assert.equal((await get('library')).tracks.length,35);
  const accountState=await get('personal/catalog',a);
  assert.equal((await put({enabled:true,tracks:[],defaultTrack:null},accountState.etag)).status,200);
  // Fill shared storage using valid metadata and real stored audio objects.
  const full=await (await bucket.get('site-music/v1/catalog.json')).json();
  while(full.tracks.length<200){
    const id=randomUUID(),bytes=Buffer.alloc(200+full.tracks.length);bytes.write('RIFF');bytes.write('WAVE',8);
    await bucket.put('site-music/v1/audio/'+id,bytes);
    full.tracks.push({id,title:'Capacity fixture',artist:'',bytes:bytes.length,contentType:'audio/wav',src:'/media/music/'+id,sha256:createHash('sha256').update(bytes).digest('hex')});
  }
  await bucket.put('site-music/v1/catalog.json',JSON.stringify(full));
  const atCapacity=await finish(await begin(sharedBytes),sharedBytes);
  assert.equal(atCapacity.duplicate,true);assert.equal(atCapacity.track.id,job.id);
  assert.deepEqual((await get('personal/catalog',a)).tracks.map(track=>track.id),[job.id],'Empty personal playlist can reuse audio at shared capacity');
  const ownerDuplicateId=randomUUID();
  const ownerDuplicate=await call('tracks/'+ownerDuplicateId,'PUT',sharedBytes,{...owner,'x-music-details':encodeURIComponent(JSON.stringify({title:'Reused owner recording'}))});
  assert.equal(ownerDuplicate.status,200);assert.equal((await ownerDuplicate.json()).duplicate,true);
  assert.equal(await bucket.head('site-music/v1/audio/'+ownerDuplicateId),null);
  const unique=Buffer.from(audio);unique[97]=99;
  const uniqueJob=await begin(unique);
  assert.equal((await call(uniqueJob.path+'/parts/1','PUT',unique,{...a,'x-music-upload-id':uniqueJob.uploadId})).status,200);
  assert.equal((await call(uniqueJob.path+'/complete','POST',JSON.stringify({uploadId:uniqueJob.uploadId}),a)).status,422);
  assert.equal(await bucket.head('site-music/v1/audio/'+uniqueJob.id),null,'Rejected 201st multipart audio is not retained');
  const uniqueOwner=randomUUID();
  assert.equal((await call('tracks/'+uniqueOwner,'PUT',unique,{...owner,'x-music-details':encodeURIComponent(JSON.stringify({title:'New audio over capacity'}))})).status,422);
  assert.equal(await bucket.head('site-music/v1/audio/'+uniqueOwner),null,'Rejected 201st direct upload is not retained');
  assert.equal((await get('library')).tracks.length,200);
  assert.equal((await bucket.list({prefix:'site-music/v1/audio/'})).objects.length,200);
});
