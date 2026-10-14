const kinds = new Set(['Advice', 'YinYang', 'Philosophy', 'Singing']);
const headers = { 'Cache-Control': 'private, no-store', 'X-Robots-Tag': 'noindex, nofollow, noarchive', 'X-Content-Type-Options': 'nosniff' };
const json = (value, status = 200) => new Response(JSON.stringify(value), { status, headers: { ...headers, 'Content-Type': 'application/json; charset=utf-8' } });
const fail = (message, status = 400) => { throw Object.assign(new Error(message), { status }); };
const sha = async (value) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value))), b => b.toString(16).padStart(2, '0')).join('');
function text(value, max, required = true) {
  if (typeof value !== 'string' || value.length > max) fail('Invalid text length');
  const result = value.trim();
  if (required && !result) fail('Required field missing');
  if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/u.test(result)) fail('Use plain text without control characters');
  return result;
}
function owner(request, env) {
  const id = request.headers.get('oai-authenticated-user-id');
  const email = request.headers.get('oai-authenticated-user-email');
  if (!id || !(env.OWNER_USER_ID ? id === env.OWNER_USER_ID : env.OWNER_EMAIL && email?.toLowerCase() === env.OWNER_EMAIL.toLowerCase())) fail('Owner sign-in required', 403);
}
async function body(request) {
  if (!request.headers.get('content-type')?.toLowerCase().startsWith('application/json')) fail('JSON required', 415);
  const reader = request.body?.getReader();
  if (!reader) fail('Request body required');
  let size = 0; const parts = [];
  while (true) { const {done, value} = await reader.read(); if (done) break; size += value.byteLength; if (size > 48_000) { await reader.cancel(); fail('Request too large', 413); } parts.push(value); }
  const bytes = new Uint8Array(size); let offset = 0; for (const part of parts) { bytes.set(part, offset); offset += part.length; }
  try { const value = JSON.parse(new TextDecoder().decode(bytes)); if (!value || typeof value !== 'object' || Array.isArray(value)) fail('Invalid JSON'); return value; } catch { fail('Invalid JSON'); }
}
function sameOrigin(request) {
  const origin = request.headers.get('origin');
  if (!origin || origin !== new URL(request.url).origin || request.headers.get('sec-fetch-site') === 'cross-site') fail('Same-origin request required', 403);
}
async function limit(request, db, bucket, max, seconds) {
  const address = request.headers.get('cf-connecting-ip') || 'local';
  const window = Math.floor(Date.now() / (seconds * 1000));
  const key = `${bucket}:${window}:${await sha(address)}`;
  const now = Date.now();
  const result = await db.prepare('INSERT INTO rate_limits (key, count, expires_at) VALUES (?, 1, ?) ON CONFLICT(key) DO UPDATE SET count=count+1 RETURNING count').bind(key, now + seconds * 1000).first();
  if (result.count > max) fail('Too many requests. Please try later.', 429);
  await db.prepare('DELETE FROM rate_limits WHERE expires_at < ?').bind(now).run();
}
const itemSql = 'SELECT id, kind, title, body, author, created_at AS createdAt FROM suggestions';
function deletionCredential(input) {
  if (typeof input.id !== 'string' || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(input.id) ||
      typeof input.deletionToken !== 'string' || !/^[0-9a-f]{64}$/.test(input.deletionToken)) fail('Invalid deletion credential');
  return {id: input.id, token: input.deletionToken};
}
export async function publicApi(request, env) {
  const url = new URL(request.url); const path = url.pathname;
  if (!path.startsWith('/api/')) return null;
  if (/^\/api\/(?:applications(?:\/|$)|admin\/(?:applications|download-tokens)(?:\/|$)|hermes\/applications(?:\/|$)|releases(?:\/|$)|download(?:\/|$)|download-requests(?:\/|$))/.test(path)) return json({error:'This service has retired. Source and downloads are available on GitHub.', retired:true, url:'https://github.com/boluopai-net/Prometheus2Heraclitus'},410);
  if (path !== '/api/suggestions' && path !== '/api/suggestions/manage' && !path.startsWith('/api/admin/suggestions/')) return json({error:'Not found'},404);
  try {
    if (!env.DB) fail('Storage unavailable', 503);
    const db = env.DB;
    if (request.method === 'POST' || request.method === 'PATCH' || request.method === 'DELETE') sameOrigin(request);
    if (path.startsWith('/api/admin/')) owner(request, env);
    if (path === '/api/suggestions' && request.method === 'GET') {
      await limit(request, db, 'read', 120, 60);
      const kind = url.searchParams.get('kind') || 'Advice'; if (!kinds.has(kind)) fail('Invalid kind');
      const cursor = url.searchParams.get('cursor'); let before = null;
      if (cursor) { try { before = JSON.parse(atob(cursor)); } catch { fail('Invalid cursor'); } if (!Array.isArray(before) || before.length !== 2 || !before.every(x => typeof x === 'string' && x.length <= 100)) fail('Invalid cursor'); }
      const clauses = [], args = []; if (kind) { clauses.push('kind = ?'); args.push(kind); }
      if (before) { clauses.push('(created_at < ? OR (created_at = ? AND id < ?))'); args.push(before[0], before[0], before[1]); }
      const {results} = await db.prepare(itemSql + (clauses.length ? ' WHERE ' + clauses.join(' AND ') : '') + ' ORDER BY created_at DESC, id DESC LIMIT 31').bind(...args).all();
      const items = results.slice(0, 30), last = items.at(-1);
      return json({items, nextCursor: results.length > 30 ? btoa(JSON.stringify([last.createdAt, last.id])) : null});
    }
    if (path === '/api/suggestions' && request.method === 'POST') {
      const input = await body(request);
      if (input.website !== '') fail('Invalid submission'); if (!kinds.has(input.kind)) fail('Invalid kind');
      const credential = input.id !== undefined || input.deletionToken !== undefined ? deletionCredential(input) : null;
      const tokenHash = credential ? await sha(credential.token) : null;
      const item = {id: credential?.id || crypto.randomUUID(), kind: input.kind, title: text(input.title, 200), body: text(input.body, 10000), author: text(input.author, 100, false) || 'Anonymous', createdAt: new Date().toISOString()};
      const existing = await db.prepare(itemSql + ' WHERE id = ?').bind(item.id).first();
      if (!existing) {
        await limit(request, db, 'suggest', 5, 3600);
        await db.prepare('INSERT INTO suggestions (id, kind, title, body, author, created_at, delete_token_hash) VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO NOTHING').bind(item.id,item.kind,item.title,item.body,item.author,item.createdAt,tokenHash).run();
      }
      const stored = await db.prepare(itemSql + ' WHERE id = ?').bind(item.id).first();
      const proof = await db.prepare('SELECT delete_token_hash AS tokenHash FROM suggestions WHERE id = ?').bind(item.id).first();
      if (!stored || !proof || proof.tokenHash !== tokenHash || (existing && !credential) || ['kind','title','body','author'].some(key => stored[key] !== item[key])) fail('Submission conflicts with an existing comment',409);
      return json({item:stored}, existing ? 200 : 201);
    }
    if (path === '/api/suggestions/manage' && request.method === 'POST') {
      await limit(request, db, 'manage-comment', 30, 60);
      const input = await body(request), credential = deletionCredential(input);
      if (input.action !== 'read' && input.action !== 'delete') fail('Invalid action');
      const proof = await db.prepare('SELECT delete_token_hash AS tokenHash FROM suggestions WHERE id = ?').bind(credential.id).first();
      if (!proof) return input.action === 'delete' ? json({ok:true}) : json({error:'Comment no longer exists'},404);
      const tokenHash = await sha(credential.token);
      if (!proof.tokenHash || proof.tokenHash !== tokenHash) fail('Deletion credential does not match this comment',403);
      if (input.action === 'read') return json({item:await db.prepare(itemSql + ' WHERE id = ?').bind(credential.id).first()});
      await db.prepare('DELETE FROM suggestions WHERE id = ? AND delete_token_hash = ?').bind(credential.id,tokenHash).run();
      return json({ok:true});
    }
    if (path.startsWith('/api/admin/suggestions/') && request.method === 'PATCH') {
      const id = text(decodeURIComponent(path.split('/').at(-1)), 100);
      const input = await body(request);
      const author = text(input.author, 100);
      const expectedAuthor = text(input.expectedAuthor, 100);
      const changed = await db.prepare('UPDATE suggestions SET author = ? WHERE id = ? AND author = ? RETURNING id').bind(author, id, expectedAuthor).first();
      if (!changed) {
        const existing = await db.prepare(itemSql + ' WHERE id = ?').bind(id).first();
        if (!existing) fail('Comment no longer exists', 404);
        if (existing.author !== author) fail('Author changed; reload before editing', 409);
        return json({item: existing});
      }
      return json({item: await db.prepare(itemSql + ' WHERE id = ?').bind(id).first()});
    }
    if (path.startsWith('/api/admin/suggestions/') && request.method === 'DELETE') {
      const id=text(decodeURIComponent(path.split('/').at(-1)),100); await db.prepare('DELETE FROM suggestions WHERE id = ?').bind(id).run(); return json({ok:true});
    }
    return json({error:'Not found'},404);
  } catch (error) {
    if (!error.status) console.error('Feedback storage failure', error.name);
    return json({error:error.status ? error.message : 'Service temporarily unavailable'}, error.status || 503);
  }
}
export { owner, headers as privateHeaders, json, fail, sha, text, body, sameOrigin, limit };

