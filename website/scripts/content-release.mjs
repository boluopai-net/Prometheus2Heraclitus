#!/usr/bin/env node
// Secret input: one JSON line on stdin, never flags, environment, or disk.
import {execFileSync} from 'node:child_process';
import {readFile, writeFile, mkdir, stat} from 'node:fs/promises';
import {resolve, dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {API, PART_SIZE, MAX_MANIFEST, parseManifest, validateDependencies} from '../lib/content-release.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const git = (...args) => execFileSync('git', args, {cwd:root,maxBuffer:32*1024*1024});
const types = {html:'text/html; charset=utf-8',xml:'application/xml; charset=utf-8',css:'text/css; charset=utf-8',js:'text/javascript; charset=utf-8',json:'application/json; charset=utf-8',txt:'text/plain; charset=utf-8',py:'text/plain; charset=utf-8',png:'image/png',jpg:'image/jpeg',jpeg:'image/jpeg',svg:'image/svg+xml',webp:'image/webp',gif:'image/gif',ico:'image/x-icon',ttf:'font/ttf',woff:'font/woff',woff2:'font/woff2',pdf:'application/pdf'};
function argsOf(values) {
  const args = {};
  while (values.length) {
    const key = values.shift();
    if (!/^--(?:out|commit|candidate|site|expected)$/.test(key) || !values.length || args[key.slice(2)] !== undefined) throw Error('Invalid arguments');
    args[key.slice(2)] = values.shift();
  }
  return args;
}
async function prepare(args) {
  if (!args.out) throw Error('prepare requires --out DIRECTORY');
  const commit = git('rev-parse', '--verify', `${args.commit || 'HEAD'}^{commit}`).toString().trim();
  const out = resolve(args.out);
  // Do not overwrite another candidate, including one bound to an older revision.
  await mkdir(out);
  await mkdir(join(out, 'objects'));
  const paths = git('ls-tree','-r','--name-only',commit,'--','dist').toString().trim().split('\n').filter(Boolean).sort();
  const files = [], objects = new Map();
  for (const path of paths) {
    if (/^dist\/(?:client|server|\.openai)(?:\/|$)/.test(path)) continue;
    const bytes = git('show',`${commit}:${path}`), hash = digest(bytes);
    const extension = path.includes('.') ? path.split('.').pop().toLowerCase() : '';
    const file = {path:path.slice(4), sha256:hash, size:bytes.byteLength, contentType:types[extension] || 'text/plain; charset=utf-8'};
    files.push(file); objects.set(hash, bytes);
  }
  const manifest = {schema:1,source:{commit},files}, bytes = Buffer.from(JSON.stringify(manifest));
  if (bytes.byteLength > MAX_MANIFEST) throw Error('Manifest too large');
  parseManifest(bytes);
  for (const file of files) validateDependencies(objects.get(file.sha256),file,manifest);
  for (const [hash, object] of objects) await writeFile(join(out,'objects',hash),object,{flag:'wx'});
  await writeFile(join(out,'manifest.json'),bytes,{flag:'wx'});
  return {candidate:out,manifest:digest(bytes),source:commit,files:files.length,objects:objects.size,bytes:files.reduce((sum,f) => sum+f.size,0),parts:Math.ceil(files.length/PART_SIZE)};
}
async function credentials() {
  if (process.stdin.isTTY) throw Error('Provide {"key":"…"} through a runtime pipe on stdin');
  let data = '';
  for await (const chunk of process.stdin) { data += chunk; if (data.length > 8192) throw Error('Invalid credential input'); }
  let input; try { input = JSON.parse(data); } catch { throw Error('Invalid credential input'); }
  if (typeof input.key !== 'string' || input.key.length < 32 || /[\r\n]/.test(input.key)) throw Error('Invalid credential input');
  return input.key;
}
function siteURL(value) {
  const url = new URL(value);
  if (url.protocol !== 'https:' || url.username || url.password || url.pathname !== '/' || url.search || url.hash) throw Error('Use the exact HTTPS Site origin');
  return url.origin;
}
async function candidate(directory) {
  if (!directory) throw Error('--candidate DIRECTORY required');
  const base = resolve(directory), bytes = await readFile(join(base,'manifest.json'));
  const manifest = parseManifest(bytes);
  for (const file of manifest.files) {
    const path = join(base,'objects',file.sha256), info = await stat(path);
    if (!info.isFile() || info.size !== file.size) throw Error('Candidate object missing or changed');
    const object = await readFile(path);
    if (digest(object) !== file.sha256) throw Error('Candidate object digest mismatch');
    validateDependencies(object,file,manifest);
  }
  return {base,bytes,manifest,hash:digest(bytes)};
}
async function remote(command,args) {
  if (!args.site) throw Error('--site ORIGIN required');
  const origin = siteURL(args.site), key = await credentials();
  const call = async (path,method='GET',body) => {
    let response;
    for (let attempt=0; ; attempt++) {
      const started=Date.now();
      try {
        response = await fetch(`${origin}${API}${path}`, {method,body,headers:{Authorization:`Bearer ${key}`},signal:AbortSignal.timeout(60000),redirect:'error'});
        break;
      } catch (failure) {
        const retry=['GET','HEAD'].includes(method) && failure.cause?.code === 'ECONNRESET' && attempt<2;
        console.error(JSON.stringify({method,path:API+path,transportError:failure.name,causeCode:failure.cause?.code || null,elapsedMs:Date.now()-started,retry}));
        if (!retry) throw Error('Release request outcome unknown; use status/reconcile before retrying.');
        await new Promise(resolve => setTimeout(resolve,250*(attempt+1)));
      }
    }
    if (method === 'HEAD') return response;
    const result = await response.json().catch(() => ({}));
    if (!response.ok) throw Error(`Release request failed (${response.status}): ${result.error || 'unavailable'}`);
    return result;
  };
  if (command === 'status') return call('/status');
  if (command === 'retire-bootstrap') return call('/retire-bootstrap','POST');
  const local = await candidate(args.candidate);
  let status = await call('/status');
  if (command === 'reconcile') return {manifest:local.hash,matches:status.active?.manifest === local.hash,...status};
  if (!['upload','stage','validate','promote','publish'].includes(command)) throw Error('Unknown command');
  // Persisted candidate bytes are the retry identity. Fetch state before every run;
  // network timeouts never trigger an automatic blind mutation retry.
  let uploaded = 0, reused = 0;
  if (['upload','publish'].includes(command)) {
    const known = new Set(command === 'publish' && status.active ? (await call(`/manifests/${status.active.manifest}`)).files.map(file => file.sha256) : []);
    const objects=[...new Set(local.manifest.files.map(file => file.sha256))];
    const pending=objects.filter(hash => { if (known.has(hash)) { reused++; return false; } return true; });
    let cursor=0;
    const failedObjects=[];
    const outcomes=await Promise.allSettled(Array.from({length:Math.min(4,pending.length)},async () => {
      while (cursor<pending.length) {
        const hash=pending[cursor++];
        try {
          const head=await call(`/objects/${hash}`,'HEAD');
          if (head.ok) { reused++; continue; }
          if (head.status !== 404) throw Error(`Object readback failed (${head.status})`);
          await call(`/objects/${hash}`,'PUT',await readFile(join(local.base,'objects',hash))); uploaded++;
        } catch (failure) { failedObjects.push(hash); throw failure; }
      }
    }));
    const failed=outcomes.find(outcome => outcome.status === 'rejected');
    if (failed) {
      console.error(JSON.stringify({phase:'upload',confirmed:uploaded+reused,total:objects.length,uploaded,reused,failedObjects,unattempted:pending.length-cursor}));
      throw failed.reason;
    }
    if (command === 'upload') return {manifest:local.hash,uploaded,reused};
  }
  if (['stage','publish'].includes(command)) {
    const result = await call(`/manifests/${local.hash}`,'PUT',local.bytes);
    if (command === 'stage') return result;
  }
  if (['validate','publish'].includes(command)) {
    const parts=Math.ceil(local.manifest.files.length/PART_SIZE);
    let cursor=0;
    const outcomes=await Promise.allSettled(Array.from({length:Math.min(4,parts)},async () => {
      while (cursor<parts) {
        const part=cursor++;
        await call(`/validate/${local.hash}/${part}`,'POST');
      }
    }));
    const failed=outcomes.find(outcome => outcome.status === 'rejected');
    if (failed) throw failed.reason;
    if (command === 'validate') return {manifest:local.hash,parts:Math.ceil(local.manifest.files.length/PART_SIZE),validated:true};
  }
  // publish binds its CAS to the state seen before uploading, so a slow old release
  // cannot overwrite a newer release completed in the meantime.
  const expected = command === 'promote' ? args.expected : status.etag;
  if (command === 'promote' && expected === undefined) throw Error('promote requires --expected ETAG (or null for first seed)');
  const result = await call('/promote','POST',JSON.stringify({manifest:local.hash,expected:expected === 'null' ? null : expected}));
  status = await call('/status');
  if (status.active?.manifest !== local.hash || !status.bootstrapRetired) throw Error('Promotion readback differs; reconcile before retrying');
  const homepage = await fetch(`${origin}/`,{redirect:'error',signal:AbortSignal.timeout(60000)});
  if (!homepage.ok || homepage.headers.get('x-content-manifest') !== local.hash || homepage.headers.get('x-content-source') !== local.manifest.source.commit) throw Error('Consumer readback differs; reconcile before retrying');
  await homepage.body?.cancel();
  return {...result,uploaded,reused,consumerVerified:true};
}
try {
  const [command,...values] = process.argv.slice(2), args = argsOf(values);
  if (!command) throw Error('Usage: content-release.mjs prepare|upload|stage|validate|promote|publish|status|reconcile|retire-bootstrap');
  console.log(JSON.stringify(command === 'prepare' ? await prepare(args) : await remote(command,args)));
} catch (failure) { console.error(failure.message); process.exitCode = 1; }
