import {credentialFor,remember,forget,managementLink,manageComment} from './comment-ownership.js';
const english=document.documentElement.lang==='en', t=(zh,en)=>english?en:zh;
const $=id=>document.getElementById(id), status=$('manage-status');
const fragment=new URLSearchParams(location.hash.slice(1));
const id=fragment.get('id')||new URLSearchParams(location.search).get('id');
const token=fragment.get('key')||credentialFor(id);
// The capability never remains in the address bar/history after opening.
history.replaceState(null,'',location.pathname+(id?'?'+new URLSearchParams({id}):''));
async function start() {
  if(!id||!token) { status.textContent=t('请使用提交评论后获得的私人删除链接，或在原浏览器中打开这条评论。','Use your private deletion link, or open the comment in the browser you used to submit it.'); return; }
  try {
    const {item}=await manageComment(id,token,'read');
    if(!item) throw Object.assign(Error(),{status:404});
    remember(id,token);
    $('managed-author').textContent=item.author && item.author!=='Anonymous'?item.author:t('匿名','Anonymous');
    $('managed-title').textContent=item.title; $('managed-body').textContent=item.body;
    const date=new Date(item.createdAt);
    $('managed-time').dateTime=date.toISOString();
    $('managed-time').textContent=new Intl.DateTimeFormat(english?'en-GB':'zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(date);
    const routes={Advice:'/repositories/',YinYang:'/repositories/prometheus/',Philosophy:'/philosophy/',Singing:'/singing/'};
    $('back-to-comments').href=(routes[item.kind]||'/repositories/')+(english?'en/':'')+(item.kind==='Advice'?'#advice':'#comments');
    $('managed-comment').hidden=false; $('manage-actions').hidden=false; status.textContent='';
    $('copy-deletion-link').onclick=async()=>{
      const link=managementLink(id,token,english);
      try { await navigator.clipboard.writeText(link); status.textContent=t('私人删除链接已复制，请自己保存，不要公开分享。','Private deletion link copied. Keep it for yourself; do not share it publicly.'); }
      catch { const field=$('deletion-link'); field.value=link; field.hidden=false; field.focus(); field.select(); status.textContent=t('请复制并保存下面的私人链接。','Copy and save the private link below.'); }
    };
    $('delete-comment').onclick=async()=>{
      if(!confirm(t('确定删除这条评论？删除后无法恢复。','Delete this comment? This cannot be undone.'))) return;
      $('delete-comment').disabled=true;
      try { await manageComment(id,token,'delete'); forget(id); $('managed-comment').hidden=true; $('manage-actions').hidden=true; status.textContent=t('评论已删除。','Comment deleted.'); }
      catch(error) { status.textContent=t('暂时无法删除，请稍后重试。','Unable to delete now. Please try again.'); $('delete-comment').disabled=false; }
    };
  } catch(error) {
    status.textContent=error.status===404?t('这条评论已删除或不存在。','This comment has been deleted or does not exist.'):t('无法管理这条评论，请检查私人删除链接是否完整，或稍后重试。','Unable to manage this comment. Check your private link, or try again later.');
  }
}
start();
