const $=selector=>document.querySelector(selector);
let state, busy=false;
const message=text=>$('#message').textContent=text;
function setBusy(value){busy=value;document.querySelectorAll('#manager button,#manager input').forEach(el=>el.disabled=value);$('#upload').disabled=value||!$('#files').files.length;}
async function api(path,options={}){
  const response=await fetch('/api/music/'+path,options);const data=await response.json();
  if(!response.ok)throw Error(response.status===409?'歌单刚刚有变化，请重新读取后再操作。':data.error||'操作失败，请重新读取确认结果。');return data;
}
function collect(){
  return {enabled:$('#enabled').checked,defaultTrack:$('#tracks input[name=default]:checked')?.value||null,tracks:[...$('#tracks .track-row')].map(row=>({id:row.dataset.id,title:row.querySelector('[data-title]').value.trim(),artist:row.querySelector('[data-artist]').value.trim()}))};
}
function render(){
  $('#enabled').checked=state.enabled;$('#tracks').replaceChildren();$('#empty').hidden=state.tracks.length>0;
  for(const track of state.tracks){
    const row=document.createElement('li');row.className='track-row';row.dataset.id=track.id;
    row.innerHTML='<div class="track-fields"><label>曲名<input data-title type="text" maxlength="200"></label><label>演唱／演奏者<input data-artist type="text" maxlength="200"></label></div><div class="track-actions"><label><input type="radio" name="default"> 默认曲目</label><button data-up type="button">上移</button><button data-down type="button">下移</button><button data-delete type="button">删除</button></div>';
    row.querySelector('[data-title]').value=track.title;row.querySelector('[data-artist]').value=track.artist;
    const radio=row.querySelector('[name=default]');radio.value=track.id;radio.checked=track.id===state.defaultTrack;
    const audio=document.createElement('audio');audio.controls=true;audio.preload='none';audio.src=track.src;audio.setAttribute('aria-label',track.title);row.append(audio);
    row.querySelector('[data-up]').onclick=()=>{if(row.previousElementSibling)row.parentElement.insertBefore(row,row.previousElementSibling);};
    row.querySelector('[data-down]').onclick=()=>{if(row.nextElementSibling)row.parentElement.insertBefore(row.nextElementSibling,row);};
    row.querySelector('[data-delete]').onclick=async()=>{
      if(!confirm('从网站删除「'+track.title+'」？本机原文件不受影响。'))return;
      setBusy(true);try{await api('tracks/'+track.id,{method:'DELETE',headers:{'If-Match':state.etag}});await refresh();message('已从网站删除。');}catch(e){message(e.message);}finally{setBusy(false);}
    };
    $('#tracks').append(row);
  }
}
async function refresh(){state=await api('catalog');render();}
$('#files').onchange=()=>$('#upload').disabled=busy||!$('#files').files.length;
function upload(track,file){return new Promise((resolve,reject)=>{
  const xhr=new XMLHttpRequest();xhr.open('PUT','/api/music/tracks/'+track.id);xhr.setRequestHeader('X-Music-Details',encodeURIComponent(JSON.stringify({title:track.title,artist:track.artist})));xhr.setRequestHeader('Content-Type','application/octet-stream');
  xhr.upload.onprogress=e=>{if(e.lengthComputable)$('#upload-progress').value=e.loaded/e.total*100;};
  xhr.onload=()=>{let d;try{d=JSON.parse(xhr.responseText);}catch{reject(Error('服务器响应异常，请重新读取歌单确认。'));return;}if(xhr.status>=200&&xhr.status<300)resolve(d);else reject(Error(d.error||'上传失败，请重新读取确认。'));};
  xhr.onerror=()=>reject(Error('网络中断，请重新读取歌单确认是否已上传。'));xhr.ontimeout=xhr.onerror;xhr.timeout=180000;xhr.send(file);
});}
$('#upload').onclick=async()=>{
  const files=[...$('#files').files];if(!files.length)return;
  for(const file of files){if(/\.ncm$/i.test(file.name)){message('NCM 不是浏览器可播放的音频，请先转成 MP3 或 M4A。');return;}if(file.size>32*1024*1024){message('「'+file.name+'」超过 32 MB，请先压缩或转换为 MP3。');return;}}
  setBusy(true);$('#upload-progress').hidden=false;let count=0;
  try{for(const file of files){message('正在上传 '+(count+1)+' / '+files.length+'：'+file.name);$('#upload-progress').value=0;await upload({id:crypto.randomUUID(),title:file.name.replace(/\.[^.]+$/,'').slice(0,200),artist:$('#upload-artist').value.trim()},file);count++;}$('#files').value='';await refresh();message('已上传 '+count+' 首，网站现在可以播放。');}
  catch(e){try{await refresh();}catch{}message(e.message+' 已完成 '+count+' 首。');}
  finally{$('#upload-progress').hidden=true;setBusy(false);}
};
$('#save').onclick=async()=>{setBusy(true);try{await api('catalog',{method:'PUT',headers:{'Content-Type':'application/json','If-Match':state.etag||'empty'},body:JSON.stringify(collect())});await refresh();message('歌单已保存，访客刷新页面即可读取。');}catch(e){message(e.message);}finally{setBusy(false);}};
$('#refresh').onclick=async()=>{setBusy(true);try{await refresh();message('已读取最新歌单。');}catch(e){message(e.message);}finally{setBusy(false);}};
document.addEventListener('play',e=>{document.querySelectorAll('audio').forEach(a=>{if(a!==e.target)a.pause();});},true);
try{const session=await api('session');if(session.canManage){$('#manager').hidden=false;await refresh();message('上传和修改会直接更新网站音乐。');}else{$('#login').hidden=false;message('访客可以听音乐；只有站主能修改歌单。');}}catch(e){message(e.message);}
