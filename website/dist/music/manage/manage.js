import {prepareAudio} from './ncm.js';

const $=selector=>document.querySelector(selector);
let state, busy=false;
let draggedRow=null;
let completion=Promise.resolve();
const queue=document.createElement('ol');queue.id='upload-queue';$('#upload-progress').replaceWith(queue);
const message=text=>{$('#message').textContent=text;$('#message').hidden=!text;};
let saveTimer,dirty=false,saveChain=Promise.resolve(true);
function scheduleSave(delay=350){dirty=true;clearTimeout(saveTimer);saveTimer=setTimeout(saveChanges,delay);}
function saveChanges(){
  clearTimeout(saveTimer);if(!dirty)return saveChain;dirty=false;const draft=collect();
  saveChain=saveChain.then(async()=>{try{const result=await api('catalog',{method:'PUT',keepalive:true,headers:{'Content-Type':'application/json','If-Match':state.etag||'empty'},body:JSON.stringify(draft)});state.etag=result.etag;message('');return true;}catch(e){message('未能自动保存：'+e.message);return false;}});
  return saveChain;
}
function setBusy(value){busy=value;document.querySelectorAll('#manager button,#manager input').forEach(el=>el.disabled=value);$('#upload').disabled=value||!$('#files').files.length;}
async function api(path,options={}){
  const response=await fetch('/api/music/'+path,options);const data=await response.json();
  if(!response.ok)throw Error(response.status===409?'歌单已在其他页面修改，请刷新此页面后再试。':data.error||'操作失败，请刷新页面确认结果。');return data;
}
function collect(){
  return {enabled:$('#enabled').checked,defaultTrack:$('#tracks input[name=default]:checked')?.value||null,tracks:[...document.querySelectorAll('#tracks .track-row')].map(row=>({id:row.dataset.id,title:row.querySelector('[data-title]').value.trim(),artist:state.tracks.find(t=>t.id===row.dataset.id)?.artist||''}))};
}
function render(){
  $('#enabled').checked=state.enabled;$('#tracks').replaceChildren();$('#empty').hidden=state.tracks.length>0;
  for(const track of state.tracks){
    const row=document.createElement('li');row.className='track-row';row.dataset.id=track.id;
    row.innerHTML='<div class="track-fields"><label>曲名<input data-title type="text" maxlength="200"></label></div><div class="track-actions"><label><input type="radio" name="default"> 默认曲目</label><button data-reorder type="button" draggable="true">拖动排序</button><button data-delete type="button">删除</button></div>';
    const title=row.querySelector('[data-title]');title.value=track.title;title.oninput=()=>scheduleSave();title.onblur=()=>saveChanges();
    const radio=row.querySelector('[name=default]');radio.value=track.id;radio.checked=track.id===state.defaultTrack;
    radio.onchange=()=>scheduleSave(0);
    const audio=document.createElement('audio');audio.controls=true;audio.preload='none';audio.src=track.src;audio.setAttribute('aria-label',track.title);row.append(audio);
    const handle=row.querySelector('[data-reorder]');
    handle.setAttribute('aria-label','拖动调整「'+track.title+'」的顺序，也可使用上下方向键');
    handle.ondragstart=e=>{if(busy){e.preventDefault();return;}draggedRow=row;row.classList.add('dragging');e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',track.id);};
    handle.ondragend=()=>{row.classList.remove('dragging');draggedRow=null;scheduleSave(0);};
    row.ondragover=e=>{if(!draggedRow||draggedRow===row)return;e.preventDefault();e.dataTransfer.dropEffect='move';const box=row.getBoundingClientRect();row.parentElement.insertBefore(draggedRow,e.clientY<box.top+box.height/2?row:row.nextSibling);};
    row.ondrop=e=>{if(draggedRow)e.preventDefault();};
    handle.onkeydown=e=>{if(e.key==='ArrowUp'&&row.previousElementSibling){e.preventDefault();row.parentElement.insertBefore(row,row.previousElementSibling);}else if(e.key==='ArrowDown'&&row.nextElementSibling){e.preventDefault();row.parentElement.insertBefore(row.nextElementSibling,row);}else return;handle.focus();scheduleSave(0);};
    row.querySelector('[data-delete]').onclick=async()=>{
      if(!confirm('从网站删除「'+track.title+'」？本机原文件不受影响。'))return;
      setBusy(true);try{if(!await saveChanges())return;await api('tracks/'+track.id,{method:'DELETE',headers:{'If-Match':state.etag}});await refresh();message('');}catch(e){message(e.message);}finally{setBusy(false);}
    };
    $('#tracks').append(row);
  }
}
async function refresh(){state=await api('catalog');render();}
$('#files').onchange=()=>$('#upload').disabled=busy||!$('#files').files.length;
function uploadPart(path,uploadId,blob,offset,total,progress){return new Promise((resolve,reject)=>{
  const xhr=new XMLHttpRequest();xhr.open('PUT','/api/music/'+path);xhr.setRequestHeader('X-Music-Upload-Id',uploadId);xhr.setRequestHeader('Content-Type','application/octet-stream');
  xhr.upload.onprogress=e=>{if(e.lengthComputable)progress((offset+e.loaded)/total*100);};
  xhr.onload=()=>{let d;try{d=JSON.parse(xhr.responseText);}catch{reject(Error('服务器响应异常，请重新读取歌单确认。'));return;}if(xhr.status>=200&&xhr.status<300)resolve(d);else reject(Error(d.error||'上传失败，请重新读取确认。'));};
  xhr.onerror=()=>reject(Error('网络中断，请重新上传这个文件。'));xhr.ontimeout=xhr.onerror;xhr.timeout=180000;xhr.send(blob);
});}
async function upload(track,audio,progress){
  const base='tracks/'+track.id+'/upload';let uploadId;
  try{
    const session=await api(base,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:track.title,artist:track.artist,bytes:audio.size})});uploadId=session.uploadId;
    for(let start=0,part=1;start<audio.size;start+=session.partBytes,part++){
      const blob=await audio.slice(start,Math.min(start+session.partBytes,audio.size));
      await uploadPart(base+'/parts/'+part,uploadId,blob,start,audio.size,progress);
    }
    // Audio transfers overlap; serialize only the shared playlist publication.
    const finish=completion.then(()=>api(base+'/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uploadId})}));
    completion=finish.catch(()=>{});return await finish;
  }catch(error){
    try{const catalog=await api('catalog');if(catalog.tracks.some(t=>t.id===track.id))return;}catch{}
    if(uploadId)try{await api(base,{method:'DELETE',headers:{'X-Music-Upload-Id':uploadId}});}catch{}
    throw error;
  }
}
$('#upload').onclick=async()=>{
  const files=[...$('#files').files];if(!files.length)return;
  if(!await saveChanges())return;queue.replaceChildren();message('');
  const jobs=files.map(file=>{const row=document.createElement('li'),name=document.createElement('span'),status=document.createElement('span'),bar=document.createElement('progress'),retry=document.createElement('button');name.textContent=file.name;status.textContent='等待中';bar.max=100;bar.value=0;retry.type='button';retry.textContent='重试';retry.hidden=true;row.append(name,status,bar,retry);queue.append(row);return{file,status,bar,retry,done:false};});
  async function run(job){
    job.retry.hidden=true;job.bar.value=0;
    try{
      if(job.file.size>512*1024*1024)throw Error('文件超过 512 MB');
      job.status.textContent='正在读取与转换';const audio=await prepareAudio(job.file);
      job.status.textContent='正在上传';await upload({id:crypto.randomUUID(),title:audio.title.slice(0,200),artist:audio.artist.slice(0,200)},audio,value=>{job.bar.value=value;job.status.textContent='上传 '+Math.round(value)+'%';});
      job.done=true;job.status.parentElement.remove();
    }catch(e){job.status.textContent=e.message;job.retry.hidden=false;}
  }
  setBusy(true);let cursor=0;
  try{await Promise.all(Array.from({length:Math.min(10,jobs.length)},async()=>{while(cursor<jobs.length)await run(jobs[cursor++]);}));$('#files').value='';await refresh();}
  catch(e){message(e.message);}
  finally{setBusy(false);}
  for(const job of jobs)job.retry.onclick=async()=>{setBusy(true);try{if(!await saveChanges())return;await run(job);await refresh();}catch(e){message(e.message);}finally{setBusy(false);}};
};
$('#enabled').onchange=()=>scheduleSave(0);
window.addEventListener('pagehide',()=>saveChanges());
document.addEventListener('play',e=>{document.querySelectorAll('audio').forEach(a=>{if(a!==e.target)a.pause();});},true);
try{const session=await api('session');if(session.canManage){$('#manager').hidden=false;await refresh();}else{$('#login').hidden=false;}}catch(e){message(e.message);}
