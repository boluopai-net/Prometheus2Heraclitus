import {prepareAudio} from './ncm.js';

const $=selector=>document.querySelector(selector);
const personal=document.body.dataset.musicProfile==='personal';
const apiRoot='/api/music/'+(personal?'personal/':'');
let state, busy=false;
let draggedRow=null;
let completion=Promise.resolve();
const queue=document.createElement('ol');queue.id='upload-queue';$('#upload-progress').replaceWith(queue);
const message=text=>{$('#message').textContent=text;$('#message').hidden=!text;};
let saveTimer,dirty=false,saveChain=Promise.resolve(true);
function scheduleSave(delay=350){dirty=true;clearTimeout(saveTimer);saveTimer=setTimeout(saveChanges,delay);}
function saveChanges(){
  clearTimeout(saveTimer);if(!dirty)return saveChain;dirty=false;const draft=collect();
  saveChain=saveChain.then(async()=>{try{const result=await api('catalog',{method:'PUT',keepalive:true,headers:{'Content-Type':'application/json','If-Match':state.etag||'empty'},body:JSON.stringify(draft)});state.etag=result.etag;message('');return true;}catch(e){dirty=true;message('未能自动保存：'+e.message);return false;}});
  return saveChain;
}
function setBusy(value){busy=value;document.querySelectorAll('#manager button,#manager input,#manager select').forEach(el=>el.disabled=value);$('#upload').disabled=value||!$('#files').files.length;updateSelection();}
async function api(path,options={}){
  const response=await fetch(apiRoot+path,options);const data=await response.json();
  if(!response.ok)throw Error(response.status===409?'歌单已在其他页面修改，请刷新此页面后再试。':data.error||'操作失败，请刷新页面确认结果。');return data;
}
function collect(){
  return {enabled:$('#enabled').checked,defaultTrack:$('#default-track').value||null,tracks:[...document.querySelectorAll('#tracks .track-row')].map(row=>({id:row.dataset.id,title:row.querySelector('[data-title]').textContent,artist:state.tracks.find(t=>t.id===row.dataset.id)?.artist||''}))};
}
function updateSelection(){
  const count=document.querySelectorAll('[data-select]:checked').length;
  $('#selection-count').textContent=count?'已选 '+count+' 首':'';
  $('#delete-selected').disabled=busy||!count;
  $('#select-all').disabled=$('#invert-selection').disabled=busy||!state?.tracks.length;
}
async function deleteTracks(ids){
  if(busy||!ids.length||!confirm('从'+(personal?'我的歌单':'网站歌单')+'移除所选的 '+ids.length+' 首歌曲？共享曲库中的音频会保留。'))return;
  setBusy(true);let deleted=0;
  try{
    if(!await saveChanges())return;
    for(const id of ids){const result=await api('tracks/'+id,{method:'DELETE',headers:{'If-Match':state.etag||'empty'}});state.etag=result.etag;deleted++;}
    await refresh();message('');
  }catch(e){
    message('已移除 '+deleted+' 首；'+e.message);
    try{await refresh();}catch{}
  }finally{setBusy(false);}
}
function render(){
  $('#enabled').checked=state.enabled;$('#tracks').replaceChildren();$('#empty').hidden=state.tracks.length>0;
  $('#track-count').textContent=state.tracks.length+' 首';
  $('#default-track').replaceChildren(...state.tracks.map(track=>new Option(track.title,track.id)));
  $('#default-track').value=state.defaultTrack||'';
  for(const track of state.tracks){
    const row=document.createElement('li');row.className='track-row';row.dataset.id=track.id;row.draggable=true;row.tabIndex=0;
    row.setAttribute('aria-label','歌曲 '+track.title+'，可拖拽或用上下方向键排序');
    row.innerHTML='<input data-select type="checkbox"><span class="drag-mark" aria-hidden="true">⠿</span><span data-title></span>';
    const checkbox=row.querySelector('[data-select]');checkbox.setAttribute('aria-label','选择 '+track.title);checkbox.onchange=updateSelection;
    const title=row.querySelector('[data-title]');title.textContent=track.title;title.title=track.title;
    row.ondragstart=e=>{if(busy||e.target.closest('input,button')){e.preventDefault();return;}draggedRow=row;row.classList.add('dragging');e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',track.id);};
    row.ondragend=()=>{row.classList.remove('dragging');draggedRow=null;scheduleSave(0);};
    row.ondragover=e=>{if(!draggedRow||draggedRow===row)return;e.preventDefault();e.dataTransfer.dropEffect='move';const box=row.getBoundingClientRect();row.parentElement.insertBefore(draggedRow,e.clientY<box.top+box.height/2?row:row.nextSibling);};
    row.ondrop=e=>{if(draggedRow)e.preventDefault();};
    row.onkeydown=e=>{if(busy||e.target!==row)return;if(e.key==='ArrowUp'&&row.previousElementSibling){e.preventDefault();row.parentElement.insertBefore(row,row.previousElementSibling);}else if(e.key==='ArrowDown'&&row.nextElementSibling){e.preventDefault();row.parentElement.insertBefore(row.nextElementSibling,row);}else return;row.focus();scheduleSave(0);};
    $('#tracks').append(row);
  }
  updateSelection();
}
async function refresh(){state=await api('catalog');render();}
function acceptUpload(result){
  const draft=collect();
  state={...state,...draft,etag:result.etag,tracks:draft.tracks.map(track=>({...state.tracks.find(t=>t.id===track.id),...track}))};
  if(result.track&&!state.tracks.some(track=>track.id===result.track.id))state.tracks.push(result.track);
  if(!state.defaultTrack)state.defaultTrack=result.track?.id||null;
  render();setBusy(busy);
}
$('#files').onchange=()=>$('#upload').disabled=busy||!$('#files').files.length;
function uploadPart(path,uploadId,blob,offset,total,progress){return new Promise((resolve,reject)=>{
  const xhr=new XMLHttpRequest();xhr.open('PUT',apiRoot+path);xhr.setRequestHeader('X-Music-Upload-Id',uploadId);xhr.setRequestHeader('Content-Type','application/octet-stream');
  xhr.upload.onprogress=e=>{if(e.lengthComputable)progress((offset+e.loaded)/total*100);};
  xhr.onload=()=>{let d;try{d=JSON.parse(xhr.responseText);}catch{reject(Error('服务器响应异常，请重新读取歌单确认。'));return;}if(xhr.status>=200&&xhr.status<300)resolve(d);else reject(Error(d.error||'上传失败，请重新读取确认。'));};
  xhr.onerror=()=>reject(Error('网络中断，请重新上传这个文件。'));xhr.ontimeout=xhr.onerror;xhr.timeout=180000;xhr.send(blob);
});}
async function upload(track,audio,progress,finalizing){
  const base='tracks/'+track.id+'/upload';let uploadId;
  try{
    const session=await api(base,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:track.title,artist:track.artist,bytes:audio.size})});uploadId=session.uploadId;
    for(let start=0,part=1;start<audio.size;start+=session.partBytes,part++){
      const blob=await audio.slice(start,Math.min(start+session.partBytes,audio.size));
      await uploadPart(base+'/parts/'+part,uploadId,blob,start,audio.size,progress);
    }
    finalizing();
    // Audio transfers overlap; serialize only the shared playlist publication.
    const finish=completion.then(()=>api(base+'/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uploadId})}));
    completion=finish.catch(()=>{});return await finish;
  }catch(error){
    try{const catalog=await api('catalog'),existing=catalog.tracks.find(t=>t.id===track.id);if(existing)return {track:existing,etag:catalog.etag};}catch{}
    if(uploadId)try{await api(base,{method:'DELETE',headers:{'X-Music-Upload-Id':uploadId}});}catch{}
    throw error;
  }
}
$('#upload').onclick=async()=>{
  const files=[...$('#files').files];if(busy||!files.length)return;
  setBusy(true);if(!await saveChanges()){setBusy(false);return;}queue.replaceChildren();message('');
  const jobs=files.map(file=>{const row=document.createElement('li'),name=document.createElement('span'),status=document.createElement('span'),bar=document.createElement('progress'),retry=document.createElement('button');name.textContent=file.name;status.textContent='等待中';bar.max=100;bar.value=0;retry.type='button';retry.textContent='重试';retry.hidden=true;row.append(name,status,bar,retry);queue.append(row);return{file,status,bar,retry,done:false};});
  async function run(job){
    job.retry.hidden=true;job.bar.value=0;
    try{
      if(job.file.size>512*1024*1024)throw Error('文件超过 512 MB');
      job.status.textContent='正在读取与转换';const audio=await prepareAudio(job.file);
      job.status.textContent='正在上传';const result=await upload({id:crypto.randomUUID(),title:audio.title.slice(0,200),artist:audio.artist.slice(0,200)},audio,value=>{job.bar.value=value;job.status.textContent='上传 '+Math.round(value)+'%';},()=>{job.bar.value=100;job.status.textContent='正在加入歌单';});
      acceptUpload(result);job.done=true;
      if(result.duplicate){job.status.textContent='曲库中已有，已加入歌单';job.bar.remove();}else job.status.parentElement.remove();
    }catch(e){job.status.textContent=e.message;job.retry.hidden=false;}
  }
  setBusy(true);let cursor=0;
  try{await Promise.all(Array.from({length:Math.min(32,jobs.length)},async()=>{while(cursor<jobs.length)await run(jobs[cursor++]);}));$('#files').value='';await refresh();}
  catch(e){message(e.message);}
  finally{setBusy(false);}
  for(const job of jobs)job.retry.onclick=async()=>{setBusy(true);try{if(!await saveChanges())return;await run(job);await refresh();}catch(e){message(e.message);}finally{setBusy(false);}};
};
$('#enabled').onchange=()=>scheduleSave(0);
$('#default-track').onchange=()=>scheduleSave(0);
$('#select-all').onclick=()=>{document.querySelectorAll('[data-select]').forEach(input=>input.checked=true);updateSelection();};
$('#invert-selection').onclick=()=>{document.querySelectorAll('[data-select]').forEach(input=>input.checked=!input.checked);updateSelection();};
$('#delete-selected').onclick=()=>deleteTracks([...document.querySelectorAll('[data-select]:checked')].map(input=>input.closest('.track-row').dataset.id));
window.addEventListener('pagehide',()=>saveChanges());
if(personal){
  const dialog=$('#library-dialog'),list=$('#library-tracks');let library=[],librarySelection=new Set();
  function renderLibrary(){
    const query=$('#library-search').value.trim().toLocaleLowerCase();list.replaceChildren();
    for(const track of library.filter(track=>(track.title+' '+(track.artist||'')).toLocaleLowerCase().includes(query))){
      const label=document.createElement('label'),input=document.createElement('input'),title=document.createElement('span');
      input.type='checkbox';input.value=track.id;input.checked=librarySelection.has(track.id);input.disabled=state.tracks.some(item=>item.id===track.id);
      input.onchange=()=>{if(input.checked)librarySelection.add(track.id);else librarySelection.delete(track.id);};
      title.textContent=track.title+(track.artist?' · '+track.artist:'');label.append(input,title);list.append(label);
    }
    $('#library-empty').hidden=list.children.length>0;
  }
  $('#open-library').onclick=async()=>{if(busy)return;try{const response=await fetch('/api/music/library');const data=await response.json();if(!response.ok)throw Error(data.error||'暂时无法读取曲库');library=data.tracks;librarySelection=new Set();$('#library-message').textContent='';$('#library-search').value='';renderLibrary();dialog.showModal();$('#library-search').focus();}catch(e){message(e.message);}};
  $('#library-search').oninput=renderLibrary;
  $('#close-library').onclick=()=>dialog.close();
  $('#add-library').onclick=async()=>{
    const ids=librarySelection;
    const additions=library.filter(track=>ids.has(track.id)&&!state.tracks.some(item=>item.id===track.id));
    if(!additions.length){dialog.close();return;}
    if(state.tracks.length+additions.length>200){$('#library-message').textContent='歌单最多 200 首，请减少所选歌曲。';return;}
    dialog.close();setBusy(true);
    try{if(!await saveChanges())return;const draft=collect();state={...state,...draft,tracks:[...draft.tracks,...additions]};state.defaultTrack||=additions[0].id;render();scheduleSave(0);await saveChanges();}catch(e){message(e.message);}finally{setBusy(false);}
  };
}
try{const session=await api('session');if(session.canManage){$('#manager').hidden=false;if(personal){$('#account').hidden=false;$('#account-name').textContent=session.user.login;}await refresh();}else{$('#login').hidden=false;if(personal&&session.signIn)$('#sign-in').href=session.signIn;}}catch(e){message(e.message);}
