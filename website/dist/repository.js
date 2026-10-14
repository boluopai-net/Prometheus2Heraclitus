/* Public reading and consistent comments across each content section. */
import {credentialFor,managementLink,prepareSubmission,finishSubmission,manageComment,forget} from './comment-ownership.js';
(() => {
  const root = document.querySelector('[data-repository-tools]');
  if (!root) return;
  const english = root.dataset.language === 'en';
  const kind = root.dataset.feedbackKind || 'Advice';
  const t = (zh, en) => english ? en : zh;
  const $ = selector => root.querySelector(selector);
  const node = (tag, text, className) => {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  };
  const status = (element, text, error = false) => {
    element.textContent = text;
    element.dataset.error = String(error);
  };
  const request = async (url, body) => {
    const response = await fetch(url, body === undefined ? {} : {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)
    });
    if (!response.ok) {
      const detail = await response.json().catch(() => ({}));
      const fallback = response.status === 429
        ? t('请求过于频繁，请稍后再试。', 'Too many requests. Please try again later.')
        : t('暂时无法完成，请稍后重试。', 'Unable to complete this now. Please try again.');
      throw new Error(typeof detail.error === 'string' ? detail.error : fallback);
    }
    return response;
  };

  if ($('#file-search')) {
  const folderKey = 'boluopai-repository-folder';
  const savedFolder = () => {
    let saved = '';
    try { saved = sessionStorage.getItem(folderKey) || ''; } catch (_) {}
    const path = new URLSearchParams(location.search).get('folder') ?? saved;
    return path && !path.startsWith('/') && !path.split('/').some(part => part === '..' || part === '.') ? path.replace(/\/?$/, '/') : '';
  };
  let files = [], folder = savedFolder();
  history.replaceState({...history.state, repositoryFolder: folder}, '', location.href);
  const enterFolder = path => {
    folder = path;
    try { sessionStorage.setItem(folderKey, folder); } catch (_) {}
    const address = new URL(location.href);
    if (folder) address.searchParams.set('folder', folder); else address.searchParams.delete('folder');
    address.hash = 'files-title'; history.pushState({repositoryFolder: folder}, '', address);
    $('#file-search').value = ''; drawFiles();
    $('[data-file-breadcrumb]').lastElementChild.focus();
  };
  window.addEventListener('popstate', event => {
    folder = typeof event.state?.repositoryFolder === 'string' ? event.state.repositoryFolder : savedFolder();
    try { sessionStorage.setItem(folderKey, folder); } catch (_) {}
    $('#file-search').value = ''; drawFiles();
  });
  const drawFiles = () => {
    const query = $('#file-search').value.trim().toLowerCase();
    const crumbs = $('[data-file-breadcrumb]');
    crumbs.replaceChildren();
    const crumb = (label, path) => {
      const button = node('button', label); button.type = 'button';
      button.addEventListener('click', () => enterFolder(path));
      crumbs.append(button);
    };
    crumb('Prometheus2Heraclitus', '');
    let current = '';
    for (const part of folder.split('/').filter(Boolean)) {
      current += part + '/'; crumbs.append(node('span', '/')); crumb(part, current);
    }
    const list = $('[data-file-list]'); list.replaceChildren();
    if (folder && !query) {
      const li = node('li'); const up = node('button', t('.. / 返回上级', '.. / Parent folder'));
      up.type = 'button'; up.addEventListener('click', () => {
        const parent = folder.slice(0, -1).split('/').slice(0, -1).join('/');
        enterFolder(parent ? parent + '/' : '');
      }); li.append(up); list.append(li);
    }
    const rows = new Map();
    for (const file of files) {
      if (!file.path.startsWith(folder)) continue;
      const relative = file.path.slice(folder.length);
      if (query) {
        if (file.path.toLowerCase().includes(query)) rows.set(file.path, {name: relative, file});
      } else if (relative.includes('/')) {
        const name = relative.split('/')[0]; rows.set(name + '/', {name, directory: true});
      } else rows.set(relative, {name: relative, file});
    }
    for (const row of [...rows.values()].sort((a, b) => Number(!!b.directory) - Number(!!a.directory) || a.name.localeCompare(b.name))) {
      const li = node('li');
      const action = node(row.directory ? 'button' : 'a');
      action.append(node('span', row.directory ? row.name + '/' : row.name), node('span', row.directory ? t('文件夹', 'Folder') : t('文件', 'File'), 'file-type'));
      if (row.directory) {
        action.type = 'button'; action.addEventListener('click', () => enterFolder(folder + row.name + '/'));
      } else action.href = row.file.urls?.[english ? 'en' : 'zh-CN'] || row.file.url;
      li.append(action); list.append(li);
    }
    status($('[data-file-status]'), rows.size ? '' : t('没有找到文件。', 'No files found.'));
  };
  $('#file-search').addEventListener('input', drawFiles);
  status($('[data-file-status]'), t('正在载入文件…', 'Loading files…'));
  request('/repositories/prometheus/files.json').then(r => r.json()).then(data => {
    files = data.files.filter(file => typeof file.path === 'string' && typeof file.url === 'string' && file.url.startsWith('/') && !file.url.startsWith('//'));
    drawFiles();
  }).catch(error => status($('[data-file-status]'), error.message, true));
  }

  let cursor = null;
  const loadAdvice = async (append = false) => {
    const list=$('[data-suggestion-list]'), more=$('[data-more-suggestions]'), message=$('[data-suggestion-list-status]');
    more.disabled=true;
    try {
      const params = new URLSearchParams({kind});
      if (append && cursor) params.set('cursor', cursor);
      const data=await (await request('/api/suggestions?' + params)).json();
      if(!append) list.replaceChildren();
      for(const item of data.items) {
        const entry=node('article',undefined,'suggestion-entry');
        const meta=node('p',undefined,'suggestion-meta');
        const author=item.author && item.author !== 'Anonymous' ? item.author : t('匿名','Anonymous');
        meta.append(node('strong',author,'suggestion-author'));
        const date=new Date(item.createdAt);
        if (!Number.isNaN(date.getTime())) {
          const time=node('time',new Intl.DateTimeFormat(english?'en-GB':'zh-CN',{
            timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',
            hour:'2-digit',minute:'2-digit',hourCycle:'h23'
          }).format(date));
          time.dateTime=date.toISOString();
          meta.append(time);
        }
        entry.append(meta);
        entry.append(node('h3',item.title));
        entry.append(node('p',item.body,'suggestion-body'));
        const token=credentialFor(item.id);
        if(token) {
          const actions=node('div',undefined,'suggestion-actions');
          const remove=node('button',t('删除我的评论','Delete my comment')); remove.type='button';
          const manage=node('a',t('管理与保存删除链接','Manage / save deletion link'));
          manage.href=managementLink(item.id,token,english); manage.rel='nofollow';
          remove.addEventListener('click',async()=>{
            if(!confirm(t('确定删除这条评论？删除后无法恢复。','Delete this comment? This cannot be undone.'))) return;
            remove.disabled=true;
            try { await manageComment(item.id,token,'delete'); forget(item.id); await loadAdvice(); }
            catch(error) { status(message,error.message,true); remove.disabled=false; }
          });
          actions.append(remove,manage); entry.append(actions);
        }
        list.append(entry);
      }
      cursor=data.nextCursor; more.hidden=!cursor;
      status(message,list.children.length?'':t('还没有评论。','No comments yet.'));
    } catch(error) { status(message,error.message,true); }
    finally { more.disabled=false; }
  };
  $('[data-more-suggestions]').addEventListener('click',()=>loadAdvice(true));
  loadAdvice();
  const submitForm = (selector, handler) => {
    const form = $(selector);
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      const message = form.querySelector('[data-form-status]');
      button.disabled = true; status(message, t('正在处理…', 'Working…'));
      try { await handler(Object.fromEntries(new FormData(form)), form, message); }
      catch (error) { status(message, error.message, true); }
      finally { button.disabled = false; }
    });
  };
  submitForm('[data-suggestion-form]', async (body,form,message)=>{
    const {id,deletionToken,remembered}=prepareSubmission(kind,body);
    await request('/api/suggestions',{...body,kind,id,deletionToken});
    finishSubmission(kind); form.reset();
    status(message,remembered?t('已提交。你可以在评论下方管理或删除它。','Submitted. You can manage or delete it below.'):t('已提交，但浏览器无法保存删除凭证。请立即保存这条评论下方的私人删除链接。','Submitted, but this browser could not save your deletion credential. Save the private link below now.'));
    await loadAdvice();
  });
})();
