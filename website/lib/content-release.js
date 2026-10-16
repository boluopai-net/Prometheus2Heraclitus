// Public content is a complete immutable projection, independent of Worker deploys.
// This namespace must never read/list the historical private objects in BUCKET.
export const PREFIX = 'public-content/v1/';
export const API = '/api/content-release';
export const SNAPSHOT = '/_content/';
export const PART_SIZE = 32;
export const MAX_OBJECT = 16 * 1024 * 1024;
export const MAX_MANIFEST = 2 * 1024 * 1024;
const HASH = /^[a-f0-9]{64}$/;
const TYPES = new Set(['text/html; charset=utf-8', 'text/css; charset=utf-8', 'text/javascript; charset=utf-8', 'application/json; charset=utf-8', 'text/plain; charset=utf-8', 'image/png', 'image/jpeg', 'image/svg+xml', 'image/webp', 'image/gif', 'image/x-icon', 'font/ttf', 'font/woff', 'font/woff2', 'application/pdf', 'application/octet-stream']);
const baseHeaders = {'Cache-Control':'no-store', 'X-Robots-Tag':'noindex, nofollow, noarchive', 'X-Content-Type-Options':'nosniff'};
const json = (value, status = 200) => new Response(JSON.stringify(value), {status, headers:{...baseHeaders, 'Content-Type':'application/json; charset=utf-8'}});
export const sha256 = async bytes => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x => x.toString(16).padStart(2,'0')).join('');
const error = (status, message) => { throw Object.assign(new Error(message), {status}); };
export function publicPath(path) {
  return typeof path === 'string' && path.length <= 1024 && /^\/[A-Za-z0-9_./-]+$/.test(path) &&
    !path.includes('//') && !path.split('/').some(x => x === '.' || x === '..' || x.startsWith('.')) &&
    !/^\/(?:api|admin|_content|signin-with-chatgpt|signout-with-chatgpt|callback)(?:\/|$)/.test(path) && path !== '/';
}
export function parseManifest(bytes) {
  let manifest;
  try { manifest = JSON.parse(new TextDecoder('utf-8', {fatal:true}).decode(bytes)); } catch { error(422, 'Invalid manifest'); }
  if (!manifest || Object.keys(manifest).sort().join() !== 'files,schema,source' || manifest.schema !== 1 ||
      !manifest.source || Object.keys(manifest.source).join() !== 'commit' || !/^[a-f0-9]{40}$/.test(manifest.source.commit) ||
      !Array.isArray(manifest.files) || !manifest.files.length || manifest.files.length > 1024) error(422, 'Invalid manifest');
  let previous = '';
  for (const file of manifest.files) {
    if (!file || Object.keys(file).sort().join() !== 'contentType,path,sha256,size' || !publicPath(file.path) ||
        file.path.endsWith('/') || file.path <= previous || !HASH.test(file.sha256) ||
        !Number.isSafeInteger(file.size) || file.size < 0 || file.size > MAX_OBJECT || !TYPES.has(file.contentType)) error(422, 'Invalid manifest entry');
    previous = file.path;
  }
  if (!manifest.files.some(f => f.path === '/index.html')) error(422, 'Missing homepage');
  return manifest;
}
async function bodyBytes(request, max) {
  if (Number(request.headers.get('content-length')) > max) error(413, 'Payload too large');
  const reader = request.body?.getReader();
  if (!reader) return new Uint8Array();
  const chunks = []; let size = 0;
  while (true) {
    const {value, done} = await reader.read(); if (done) break;
    size += value.byteLength;
    if (size > max) { await reader.cancel(); error(413, 'Payload too large'); }
    chunks.push(value);
  }
  const bytes = new Uint8Array(size); let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  return bytes;
}
async function authenticated(request, env) {
  if (typeof env.CONTENT_PUBLISH_KEY !== 'string' || env.CONTENT_PUBLISH_KEY.length < 32) return false;
  const supplied = request.headers.get('authorization') || '';
  const a = new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(supplied)));
  const b = new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(`Bearer ${env.CONTENT_PUBLISH_KEY}`)));
  return a.reduce((difference, value, i) => difference | (value ^ b[i]), 0) === 0;
}
const objectKey = hash => `${PREFIX}objects/${hash}`;
const manifestKey = hash => `${PREFIX}manifests/${hash}`;
const receiptKey = (hash, part) => `${PREFIX}receipts/${hash}/${part}`;
const activeKey = `${PREFIX}active.json`;
const retiredKey = `${PREFIX}bootstrap-retired`;
async function loadManifest(bucket, hash) {
  if (!HASH.test(hash)) error(404, 'Not found');
  const stored = await bucket.get(manifestKey(hash));
  if (!stored) error(404, 'Manifest not found');
  const bytes = await stored.arrayBuffer();
  if (await sha256(bytes) !== hash) error(503, 'Manifest integrity failure');
  return parseManifest(bytes);
}
async function activeState(bucket) {
  const stored = await bucket.get(activeKey);
  if (!stored) return {active:null, etag:null};
  const active = await stored.json();
  if (!HASH.test(active.manifest) || !/^[a-f0-9]{40}$/.test(active.source)) error(503, 'Content pointer unavailable');
  return {active, etag:stored.etag};
}
async function retireBootstrap(bucket) {
  await bucket.put(retiredKey, 'retired', {onlyIf:{etagDoesNotMatch:'*'}});
}
export async function contentReleaseApi(request, env) {
  const path = new URL(request.url).pathname;
  if (path !== API && !path.startsWith(`${API}/`)) return null;
  if (!await authenticated(request, env)) return json({error:'Unauthorized'},401);
  if (!env.BUCKET) return json({error:'Content storage unavailable'},503);
  const bucket = env.BUCKET;
  try {
    if (path === `${API}/status` && request.method === 'GET') {
      return json({...await activeState(bucket), bootstrapRetired:!!await bucket.head(retiredKey)});
    }
    const object = path.match(new RegExp(`^${API}/objects/([a-f0-9]{64})$`));
    if (object && ['HEAD','PUT'].includes(request.method)) {
      const key = objectKey(object[1]);
      if (request.method === 'HEAD') {
        const stored = await bucket.head(key);
        return new Response(null, {status:stored ? 200 : 404, headers:{...baseHeaders, ...(stored ? {'Content-Length':String(stored.size)} : {})}});
      }
      const bytes = await bodyBytes(request, MAX_OBJECT);
      if (await sha256(bytes) !== object[1]) error(422, 'Digest mismatch');
      const stored = await bucket.put(key, bytes, {sha256:object[1], onlyIf:{etagDoesNotMatch:'*'}});
      if (!stored) {
        const existing = await bucket.head(key);
        if (!existing || existing.size !== bytes.byteLength) error(409, 'Object conflict');
      }
      return json({sha256:object[1], size:bytes.byteLength});
    }
    const staged = path.match(new RegExp(`^${API}/manifests/([a-f0-9]{64})$`));
    if (staged && ['GET','PUT'].includes(request.method)) {
      if (request.method === 'GET') return json(await loadManifest(bucket, staged[1]));
      const bytes = await bodyBytes(request, MAX_MANIFEST);
      if (await sha256(bytes) !== staged[1]) error(422, 'Digest mismatch');
      const manifest = parseManifest(bytes);
      await bucket.put(manifestKey(staged[1]), bytes, {sha256:staged[1], onlyIf:{etagDoesNotMatch:'*'}});
      return json({manifest:staged[1], files:manifest.files.length, parts:Math.ceil(manifest.files.length / PART_SIZE)});
    }
    const validate = path.match(new RegExp(`^${API}/validate/([a-f0-9]{64})/(0|[1-9][0-9]*)$`));
    if (validate && request.method === 'POST') {
      const hash = validate[1], part = Number(validate[2]), manifest = await loadManifest(bucket, hash);
      if (part >= Math.ceil(manifest.files.length / PART_SIZE)) error(422, 'Invalid partition');
      for (const file of manifest.files.slice(part * PART_SIZE, (part + 1) * PART_SIZE)) {
        const stored = await bucket.get(objectKey(file.sha256));
        if (!stored || stored.size !== file.size) error(422, 'Snapshot object missing or size mismatch');
        const checksum = stored.checksums?.sha256;
        if (checksum && [...new Uint8Array(checksum)].map(x => x.toString(16).padStart(2,'0')).join('') !== file.sha256) error(422, 'Snapshot object digest mismatch');
        // R2 verified sha256 during immutable PUT. Binary bytes need not travel
        // through every later prose release; textual resources still need closure.
        if (!checksum || /^text\/(?:html|css|javascript)/.test(file.contentType)) {
          const bytes = await stored.arrayBuffer();
          if (!checksum && await sha256(bytes) !== file.sha256) error(422, 'Snapshot object digest mismatch');
          try { validateDependencies(bytes, file, manifest); } catch { error(422, 'Snapshot dependency missing'); }
        } else await stored.body?.cancel();
      }
      const receipt = {manifest:hash, part, files:Math.min(PART_SIZE, manifest.files.length - part * PART_SIZE)};
      await bucket.put(receiptKey(hash, part), JSON.stringify(receipt), {onlyIf:{etagDoesNotMatch:'*'}});
      return json(receipt);
    }
    if (path === `${API}/promote` && request.method === 'POST') {
      let input; try { input = JSON.parse(new TextDecoder().decode(await bodyBytes(request, 1024))); } catch { error(422, 'Invalid promotion'); }
      if (!input || Object.keys(input).sort().join() !== 'expected,manifest' || !HASH.test(input.manifest) ||
          !(input.expected === null || typeof input.expected === 'string' && /^[a-f0-9]{32}$/.test(input.expected))) error(422, 'Invalid promotion');
      const manifest = await loadManifest(bucket, input.manifest);
      for (let part = 0; part < Math.ceil(manifest.files.length / PART_SIZE); part++) {
        const stored = await bucket.get(receiptKey(input.manifest, part));
        if (!stored) error(409, 'Validation incomplete');
        const receipt = await stored.json();
        if (receipt.manifest !== input.manifest || receipt.part !== part || receipt.files !== Math.min(PART_SIZE, manifest.files.length - part * PART_SIZE)) error(409, 'Validation incomplete');
      }
      const current = await activeState(bucket);
      if (current.active?.manifest === input.manifest) { await retireBootstrap(bucket); return json({...current, bootstrapRetired:true}); }
      if (current.etag !== input.expected) error(409, 'Active snapshot changed');
      const active = {manifest:input.manifest, source:manifest.source.commit};
      const result = await bucket.put(activeKey, JSON.stringify(active), {onlyIf: input.expected === null ? {etagDoesNotMatch:'*'} : {etagMatches:input.expected}});
      if (!result) error(409, 'Active snapshot changed');
      // Pointer first preserves zero downtime. An uncertain marker write is reconciled
      // by status + retire-bootstrap (or an identical promotion), never by rollback.
      await retireBootstrap(bucket);
      return json({active, etag:result.etag, bootstrapRetired:true});
    }
    if (path === `${API}/retire-bootstrap` && request.method === 'POST') {
      const current = await activeState(bucket);
      if (!current.active) error(409, 'No active snapshot');
      await retireBootstrap(bucket); return json({...current, bootstrapRetired:true});
    }
    return json({error:'Not found'},404);
  } catch (failure) { return json({error:failure.status ? failure.message : 'Content release unavailable'}, failure.status || 503); }
}

export function resourceURL(value, path, hash, manifest) {
  if (!value || /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(value)) return value;
  const resolved = new URL(value.replaceAll('&amp;', '&'), `https://snapshot.invalid${path}`);
  const entry = resolveFile(manifest, resolved.pathname);
  if (!entry) throw new Error(`Missing snapshot dependency: ${resolved.pathname}`);
  return `${SNAPSHOT}${hash}${entry.path}${resolved.search}${resolved.hash}`;
}
export function resolveFile(manifest, path) {
  return manifest.files.find(f => f.path === path) || manifest.files.find(f => f.path === `${path.endsWith('/') ? path : path + '/'}index.html`);
}
export function rewriteCSS(text, path, hash, manifest) {
  return text.replace(/url\(\s*(["']?)([^)'"\s]+)\1\s*\)/gi, (_, quote, value) => `url(${quote}${resourceURL(value, path, hash, manifest)}${quote})`);
}
export function rewriteJS(text, path, hash, manifest) {
  // These are the current two data dependencies; all other links remain navigation.
  return text.replace(/(['"])(\/(?:repositories\/prometheus\/files\.json|wheel\/engine\.html))\1/g,
    (_, quote, value) => `${quote}${resourceURL(value, path, hash, manifest)}${quote}`);
}
export function validateDependencies(bytes, file, manifest) {
  const text = new TextDecoder().decode(bytes), hash = '0'.repeat(64);
  if (file.contentType.startsWith('text/css')) rewriteCSS(text,file.path,hash,manifest);
  if (file.contentType.startsWith('text/javascript')) rewriteJS(text,file.path,hash,manifest);
  if (!file.contentType.startsWith('text/html')) return;
  // Only resource attributes participate in closure; anchors and canonical URLs
  // intentionally continue to select the current snapshot on ordinary navigation.
  const markup = text.replace(/(<script\b[^>]*>)[\s\S]*?<\/script\s*>/gi,'$1</script>');
  for (const tag of markup.matchAll(/<(?:img|script|iframe|source|video|audio|input|track|link|object|embed)\b[^>]*>/gi)) {
    const attributes = new Map([...tag[0].matchAll(/\b([\w-]+)\s*=\s*(["'])(.*?)\2/gs)].map(m => [m[1].toLowerCase(),m[3]]));
    for (const name of ['src','poster','data']) if (attributes.has(name)) resourceURL(attributes.get(name),file.path,hash,manifest);
    if (/^<link\b/i.test(tag[0]) && /(?:stylesheet|icon|preload|modulepreload)/.test(attributes.get('rel') || '') && attributes.has('href')) resourceURL(attributes.get('href'),file.path,hash,manifest);
    if (attributes.has('srcset') && !attributes.get('srcset').includes('data:')) {
      for (const item of attributes.get('srcset').split(',')) resourceURL(item.trim().split(/\s+/)[0],file.path,hash,manifest);
    }
  }
  for (const style of markup.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style\s*>|\bstyle\s*=\s*(["'])(.*?)\2/gi)) rewriteCSS(style[1] ?? style[3],file.path,hash,manifest);
}
export function rewriteHTML(text, path, hash, manifest) {
  // Source is trusted generated HTML, but use the platform parser to preserve prose,
  // inline scripts, canonical/alternate links, giscus configuration and navigation.
  const pin = value => resourceURL(value, path, hash, manifest);
  let styleText = '';
  return new HTMLRewriter().on('style', {text(chunk) {
    styleText += chunk.text;
    if (chunk.lastInTextNode) { chunk.replace(rewriteCSS(styleText,path,hash,manifest),{html:true}); styleText = ''; }
    else chunk.remove();
  }}).on('*', {element(element) {
    for (const attribute of ['src','poster']) {
      const value = element.getAttribute(attribute); if (value) element.setAttribute(attribute, pin(value));
    }
    if (['object','embed'].includes(element.tagName)) {
      const attribute = element.tagName === 'object' ? 'data' : 'src', value = element.getAttribute(attribute);
      if (value) element.setAttribute(attribute, pin(value));
    }
    if (element.tagName === 'link' && /(?:stylesheet|icon|preload|modulepreload)/.test(element.getAttribute('rel') || '')) {
      const value = element.getAttribute('href'); if (value) element.setAttribute('href', pin(value));
    }
    const srcset = element.getAttribute('srcset');
    if (srcset && !srcset.includes('data:')) element.setAttribute('srcset', srcset.split(',').map(item => {
      const [value, ...descriptor] = item.trim().split(/\s+/); return [pin(value), ...descriptor].join(' ');
    }).join(', '));
    const style = element.getAttribute('style'); if (style) element.setAttribute('style', rewriteCSS(style, path, hash, manifest));
  }}).transform(new Response(text, {headers:{'Content-Type':'text/html; charset=utf-8'}}));
}
export async function contentResponse(request, env) {
  const url = new URL(request.url);
  try {
    if (!env.BUCKET) error(503, 'Content storage unavailable');
    let hash, path = url.pathname;
    const pinned = path.match(/^\/_content\/([a-f0-9]{64})(\/.*)$/);
    if (path.startsWith(SNAPSHOT) && !pinned) return new Response('Not found', {status:404, headers:baseHeaders});
    if (!['GET','HEAD'].includes(request.method)) return new Response('Method not allowed', {status:405, headers:baseHeaders});
    if (pinned) { hash = pinned[1]; path = pinned[2]; }
    else {
      const current = await activeState(env.BUCKET);
      if (!current.active) {
        if (await env.BUCKET.head(retiredKey)) error(503, 'Content pointer unavailable');
        return null;
      }
      hash = current.active.manifest;
    }
    if (path !== '/' && !publicPath(path)) return new Response('Not found', {status:404, headers:baseHeaders});
    const manifest = await loadManifest(env.BUCKET, hash), file = resolveFile(manifest, path);
    if (!file) return new Response('Not found', {status:404, headers:baseHeaders});
    if (!pinned && !path.endsWith('/') && file.path === `${path}/index.html`) {
      return Response.redirect(`${url.origin}${path}/${url.search}`,301);
    }
    const object = await env.BUCKET.get(objectKey(file.sha256));
    if (!object || object.size !== file.size) error(503, 'Selected content unavailable');
    const headers = {...baseHeaders, 'Content-Type':file.contentType, 'X-Content-Manifest':hash, 'X-Content-Source':manifest.source.commit,
      'Cache-Control':pinned ? 'public, max-age=31536000, immutable' : 'no-cache'};
    if (request.method === 'HEAD') return new Response(null, {headers});
    if (file.contentType.startsWith('text/html')) {
      const rewritten = rewriteHTML(await object.text(), file.path, hash, manifest);
      return new Response(rewritten.body, {headers});
    }
    if (file.contentType.startsWith('text/css')) return new Response(rewriteCSS(await object.text(),file.path,hash,manifest), {headers});
    if (file.contentType.startsWith('text/javascript')) return new Response(rewriteJS(await object.text(),file.path,hash,manifest), {headers});
    return new Response(object.body, {headers});
  } catch { return new Response('Selected content unavailable', {status:503, headers:baseHeaders}); }
}
