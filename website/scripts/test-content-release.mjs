import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {build} from 'esbuild';
import {Miniflare} from 'miniflare';
import {PREFIX, API, PART_SIZE} from '../lib/content-release.js';

const key = 'local-test-only-content-authority-0123456789';
const hash = value => createHash('sha256').update(value).digest('hex');
test('public Worker: immutable releases, authority, closure and atomic activation', async t => {
  const built = await build({entryPoints:['build/sites-worker.ts'],bundle:true,write:false,format:'esm',platform:'browser'});
  const mf = new Miniflare({modules:true,script:built.outputFiles[0].text,compatibilityDate:'2026-05-15',
    r2Buckets:['BUCKET'],bindings:{CONTENT_PUBLISH_KEY:key}});
  t.after(() => mf.dispose());
  const bucket = await mf.getR2Bucket('BUCKET');
  const call = (path, method='GET', body, authorized=true) => mf.dispatchFetch(`https://public.invalid${path}`,{method,body,headers:authorized ? {authorization:`Bearer ${key}`} : {}});
  const api = (path, method='GET', body, authorized=true) => call(`${API}${path}`,method,body,authorized);
  const payload = entries => {
    const files = Object.entries(entries).sort(([a],[b]) => a < b ? -1 : 1).map(([path,value]) => ({path,sha256:hash(value),size:Buffer.byteLength(value),contentType:path.endsWith('.html') ? 'text/html; charset=utf-8' : path.endsWith('.css') ? 'text/css; charset=utf-8' : path.endsWith('.js') ? 'text/javascript; charset=utf-8' : 'application/octet-stream'}));
    const manifest = {schema:1,source:{commit:'a'.repeat(40)},files}, bytes=JSON.stringify(manifest);
    return {manifest,bytes,digest:hash(bytes),entries};
  };
  const upload = async release => {
    for (const [path,value] of Object.entries(release.entries)) assert.equal((await api(`/objects/${hash(value)}`,'PUT',value)).status,200,path);
    assert.equal((await api(`/manifests/${release.digest}`,'PUT',release.bytes)).status,200);
  };
  const validate = async release => {
    for (let part=0; part<Math.ceil(release.manifest.files.length/PART_SIZE);part++) assert.equal((await api(`/validate/${release.digest}/${part}`,'POST')).status,200);
  };
  const promote = (release, expected) => api('/promote','POST',JSON.stringify({manifest:release.digest,expected}));
  const status = async () => (await api('/status')).json();

  await t.test('empty storage fails closed without assets; retired APIs win', async () => {
    assert.equal((await call('/')).status,503);
    assert.equal((await call('/api/releases/private-object')).status,410);
    assert.equal((await call('/api/visit/status')).status,200);
    assert.equal((await (await call('/api/visit/status')).json()).retired,true);
    assert.equal((await call('/robots.txt')).headers.get('content-type'),'text/plain');
  });
  await t.test('missing bucket fails closed while retired APIs remain available', async () => {
    const unbound = new Miniflare({modules:true,script:built.outputFiles[0].text,compatibilityDate:'2026-05-15'});
    try {
      assert.equal((await unbound.dispatchFetch('https://public.invalid/')).status,503);
      assert.equal((await unbound.dispatchFetch('https://public.invalid/api/releases/private')).status,410);
    } finally { await unbound.dispose(); }
  });
  await t.test('all publisher operations reject anonymous callers; historical keys have no read route', async () => {
    await bucket.put('historical-private-download','PRIVATE');
    for (const [path,method] of [['/status','GET'],[`/objects/${'b'.repeat(64)}`,'PUT'],[`/manifests/${'b'.repeat(64)}`,'PUT'],[`/validate/${'b'.repeat(64)}/0`,'POST'],['/promote','POST'],['/retire-bootstrap','POST']]) {
      assert.equal((await api(path,method,method === 'GET' ? undefined : '{}',false)).status,401);
    }
    assert.equal((await api('/objects/historical-private-download')).status,404);
    assert.equal((await call(`/_content/${'b'.repeat(64)}/historical-private-download`)).status,503);
    assert.equal((await bucket.list({prefix:PREFIX})).objects.length,0);
  });
  await t.test('invalid digest, traversal, reserved and ambiguous manifest paths fail', async () => {
    assert.equal((await api(`/objects/${'b'.repeat(64)}`,'PUT','wrong')).status,422);
    for (const path of ['/../secret','/%2e%2e/secret','//secret','/api/private','/admin/private','/_content/private','/callback','/.private']) {
      const release = payload({'/index.html':'ok',[path]:'secret'});
      assert.equal((await api(`/manifests/${release.digest}`,'PUT',release.bytes)).status,422,path);
    }
  });
  const first = payload({'/index.html':'<!doctype html><link rel="canonical" href="https://boluopai.net/"><link rel="stylesheet" href="/css/a.css"><a href="/next/">Next</a><img src="/art/a.png" srcset="/art/a.png 1x, /art/b.png 2x"><iframe src="/wheel/engine.html"></iframe><object data="/art/a.png"></object><script src="/repository.js"></script><script src="/wheel/picker.js"></script><script src="https://giscus.app/client.js"></script>',
    '/css/a.css':'@font-face{src:url(../fonts/a.woff2)}', '/fonts/a.woff2':'font','/art/a.png':'image-a','/art/b.png':'image-b',
    '/wheel/engine.html':'<p>engine</p>','/wheel/picker.js':"fetch('/wheel/engine.html')",'/repository.js':"request('/repositories/prometheus/files.json')",'/repositories/prometheus/files.json':'{}'});
  await upload(first);
  await t.test('missing objects, wrong sizes, wrong digests and unclosed resources cannot validate', async () => {
    const bad = payload({'/index.html':'<img src="/missing.png">'}); await upload(bad);
    assert.equal((await api(`/validate/${bad.digest}/0`,'POST')).status,422);
    await bucket.delete(`${PREFIX}objects/${hash('font')}`);
    assert.equal((await api(`/validate/${first.digest}/0`,'POST')).status,422);
    await bucket.put(`${PREFIX}objects/${hash('font')}`,'bad-size');
    assert.equal((await api(`/validate/${first.digest}/0`,'POST')).status,422);
    await bucket.put(`${PREFIX}objects/${hash('font')}`,'fail');
    assert.equal((await api(`/validate/${first.digest}/0`,'POST')).status,422);
    await bucket.delete(`${PREFIX}objects/${hash('font')}`);
    assert.equal((await api(`/objects/${hash('font')}`,'PUT','font')).status,200);
  });
  await t.test('promotion requires every immutable validation receipt', async () => {
    assert.equal((await promote(first,null)).status,409);
    await validate(first);
    assert.equal((await promote(first,null)).status,200);
    const state = await status();
    assert.equal(state.active.manifest,first.digest); assert.equal(state.bootstrapRetired,true);
    assert.ok(state.etag);
  });
  await t.test('all partitions are required and interrupted marker write is reconcilable', async () => {
    const many = payload(Object.fromEntries([['/index.html','<p>partitioned</p>'],...Array.from({length:33},(_,i) => [`/art/p${String(i).padStart(2,'0')}.png`,`binary-${i}`])]));
    await upload(many);
    assert.equal((await api(`/validate/${many.digest}/0`,'POST')).status,200);
    assert.equal((await promote(many,(await status()).etag)).status,409);
    assert.equal((await api(`/validate/${many.digest}/1`,'POST')).status,200);
    await bucket.delete(`${PREFIX}bootstrap-retired`);
    assert.equal((await status()).bootstrapRetired,false);
    assert.equal((await call('/')).headers.get('x-content-manifest'),first.digest);
    assert.equal((await promote(first,null)).status,200,'same active manifest repairs uncertain marker outcome');
    assert.equal((await status()).bootstrapRetired,true);
    assert.equal((await call('/absent-from-manifest.html')).status,404);
  });
  let initialETag;
  await t.test('resource links and dynamic data are pinned; navigation and giscus remain canonical', async () => {
    const response = await call('/'), html = await response.text(), prefix=`/_content/${first.digest}`;
    assert.equal(response.headers.get('x-content-manifest'),first.digest);
    assert.match(html,new RegExp(`${prefix}/css/a.css`));
    assert.match(html,new RegExp(`${prefix}/art/a.png 1x, ${prefix}/art/b.png 2x`));
    assert.ok(html.includes(`data="${prefix}/art/a.png"`));
    assert.ok(html.includes('href="/next/"')); assert.ok(html.includes('https://giscus.app/client.js'));
    assert.ok(html.includes('href="https://boluopai.net/"'));
    assert.ok((await (await call(`${prefix}/css/a.css`)).text()).includes(`${prefix}/fonts/a.woff2`));
    assert.ok((await (await call(`${prefix}/repository.js`)).text()).includes(`${prefix}/repositories/prometheus/files.json`));
    assert.ok((await (await call(`${prefix}/wheel/picker.js`)).text()).includes(`${prefix}/wheel/engine.html`));
    assert.equal((await call(`${prefix}/historical-private-download`)).status,404);
    assert.equal((await call(`${prefix}/%252e%252e/private`)).status,404);
    initialETag=(await status()).etag;
  });
  const second = payload({'/index.html':'<p>second</p>'}), third = payload({'/index.html':'<p>third</p>'});
  await upload(second); await validate(second); await upload(third); await validate(third);
  let winner;
  await t.test('concurrent publishers cannot overwrite a newer pointer with stale CAS', async () => {
    const outcomes = await Promise.all([promote(second,initialETag),promote(third,initialETag)]);
    assert.deepEqual(outcomes.map(r => r.status).sort(),[200,409]);
    winner = outcomes[0].status === 200 ? second : third;
    assert.equal((await status()).active.manifest,winner.digest);
    assert.equal(await (await call(`/_content/${first.digest}/art/a.png`)).text(),'image-a');
    assert.equal((await promote(winner,initialETag)).status,200,'same-manifest retry reconciles outcome');
  });
  await t.test('selected object loss and missing pointer never fall back to bundled stale content', async () => {
    await bucket.delete(`${PREFIX}objects/${winner.manifest.files[0].sha256}`);
    assert.equal((await call('/')).status,503);
    await bucket.delete(`${PREFIX}active.json`);
    assert.equal((await call('/')).status,503);
    assert.equal(await (await bucket.get('historical-private-download')).text(),'PRIVATE');
  });
});
