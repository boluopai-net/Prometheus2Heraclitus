import { owner, privateHeaders } from './public-api.js';

function html(body, status = 200) {
  const nonce = crypto.randomUUID().replaceAll('-', '');
  return new Response(`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>建议管理 · boluopai</title><style>body{font:16px/1.7 system-ui;max-width:900px;margin:40px auto;padding:20px;background:#fff;color:#252b30}article{border-top:1px solid #ddd;padding:20px 0;margin:20px 0}button{font:inherit;padding:8px 14px;cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}nav{display:flex;gap:20px}a{color:#176b73}button:disabled{cursor:wait;opacity:.6}</style></head><body>${body.replace('nonce="admin"', `nonce="${nonce}"`)}</body></html>`, {
    status,
    headers: {
      ...privateHeaders,
      'Content-Type': 'text/html; charset=utf-8',
      'Content-Security-Policy': `default-src 'none'; script-src 'nonce-${nonce}'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'`,
    },
  });
}

export function adminPage(request, env) {
  if (!request.headers.get('oai-authenticated-user-id')) {
    return html('<h1>建议管理</h1><p>仅网站所有者可管理公开反馈。</p><a href="/signin-with-chatgpt?return_to=%2Fadmin%2Fsuggestions" target="_top">使用 ChatGPT 登录</a>');
  }
  try { owner(request, env); }
  catch {
    return html('<h1>无访问权限</h1><p>请使用网站所有者的 ChatGPT 账户登录。</p><a href="/signout-with-chatgpt?return_to=%2Fadmin%2Fsuggestions" target="_top">退出当前账户</a>', 403);
  }
  return html(String.raw`<nav><a href="/repositories/">返回公开建议区</a><a href="/signout-with-chatgpt?return_to=%2F" target="_top">退出</a></nav>
<h1>评论与建议管理</h1>
<section><h2>评论与建议</h2><p>评论与建议提交后直接公开。按栏目查看并管理内容；公开协作通过 GitHub Issue 与 PR 进行。</p>
<label>栏目 <select id="feedback-kind"><option value="Advice">资料与建议 · Advice</option><option value="YinYang">Yinyang 方法与阅读 · 评论</option><option value="Philosophy">哲学评论 · 评论</option><option value="Singing">唱歌 · 评论</option></select></label>
<p id="status" role="status"></p><div id="suggestions"></div><button id="more" hidden>更多反馈</button></section>
<script nonce="admin">
const list = document.getElementById('suggestions');
const status = document.getElementById('status');
const more = document.getElementById('more');
const kindSelect = document.getElementById('feedback-kind');
let cursor = null;
function node(tag, text) {
  const element = document.createElement(tag);
  element.textContent = text;
  return element;
}
async function api(path, method = 'GET', body) {
  const response = await fetch(path, {method, headers: body ? {'Content-Type': 'application/json'} : {}, body: body ? JSON.stringify(body) : undefined});
  const value = await response.json();
  if (!response.ok) throw Error(value.error || '请求失败');
  return value;
}
async function load(append = false) {
  more.disabled = true;
  status.textContent = '正在读取…';
  try {
    const selectedKind = kindSelect.value;
    const params = new URLSearchParams({kind: selectedKind});
    if (append && cursor) params.set('cursor', cursor);
    const page = await api('/api/suggestions?' + params);
    if (kindSelect.value !== selectedKind) return;
    if (!append) list.replaceChildren();
    for (const item of page.items) {
      const article = node('article', '');
      const column = kindSelect.selectedOptions[0].textContent;
      const attribution = node('p', column + ' · ' + item.author + ' · ' + new Date(item.createdAt).toLocaleString());
      article.append(node('h2', item.title), attribution, node('pre', item.body));
      const rename = node('button', '修改署名');
      rename.onclick = async () => {
        const author = prompt('这条留言的署名', item.author);
        if (author === null || !author.trim() || author.trim() === item.author) return;
        rename.disabled = true;
        try {
          const updated = await api('/api/admin/suggestions/' + encodeURIComponent(item.id), 'PATCH', {author: author.trim(), expectedAuthor: item.author});
          item.author = updated.item.author;
          attribution.textContent = column + ' · ' + item.author + ' · ' + new Date(item.createdAt).toLocaleString();
          status.textContent = '署名已更新';
        } catch (error) {
          status.textContent = error.message;
        } finally { rename.disabled = false; }
      };
      const remove = node('button', '删除这条反馈');
      remove.onclick = async () => {
        if (!confirm('删除这条公开反馈？')) return;
        remove.disabled = true;
        try {
          await api('/api/admin/suggestions/' + encodeURIComponent(item.id), 'DELETE');
          article.remove();
          status.textContent = '已删除';
        } catch (error) {
          status.textContent = error.message;
          remove.disabled = false;
        }
      };
      article.append(rename, remove);
      list.append(article);
    }
    cursor = page.nextCursor;
    more.hidden = !cursor;
    status.textContent = list.children.length ? '' : '还没有建议。';
  } catch (error) { status.textContent = error.message; }
  finally { more.disabled = false; }
}
more.onclick = () => load(true);
kindSelect.onchange = () => { cursor = null; load(); };
load();
</script>`);
}
