// GitHub OAuth identity only. Native Sites owner authentication remains separate.
const SESSION = '__Host-music-session';
const FLOW = '__Host-music-oauth';
const SESSION_SECONDS = 7 * 24 * 60 * 60;
const FLOW_SECONDS = 10 * 60;
const encoder = new TextEncoder();
const headers = {'Cache-Control':'no-store', 'Referrer-Policy':'no-referrer', 'X-Content-Type-Options':'nosniff'};
const now = () => Math.floor(Date.now() / 1000);
const base64 = bytes => btoa(String.fromCharCode(...bytes)).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
function unbase64(value) {
  if (!/^[\w-]+$/.test(value)) throw new Error('Invalid encoding');
  return Uint8Array.from(atob(value.replace(/-/g,'+').replace(/_/g,'/')), character => character.charCodeAt(0));
}
const random = () => base64(crypto.getRandomValues(new Uint8Array(32)));
const configured = env => typeof env.MUSIC_SESSION_SECRET === 'string' && env.MUSIC_SESSION_SECRET.length >= 32;
const cookie = (name,value,seconds) => `${name}=${value}; Path=/; Max-Age=${seconds}; Secure; HttpOnly; SameSite=Lax`;
function cookies(request) {
  const values = new Map();
  for (const piece of (request.headers.get('cookie') || '').split(';')) {
    const index = piece.indexOf('=');
    if (index > 0) {
      const name = piece.slice(0,index).trim();
      // Duplicate cookies fail closed rather than depending on parser order.
      values.set(name,values.has(name) ? '' : piece.slice(index+1).trim());
    }
  }
  return values;
}
async function key(env) {
  return crypto.subtle.importKey('raw',encoder.encode(env.MUSIC_SESSION_SECRET),{name:'HMAC',hash:'SHA-256'},false,['sign','verify']);
}
async function signed(payload,purpose,env) {
  const body = base64(encoder.encode(JSON.stringify(payload)));
  const signature = await crypto.subtle.sign('HMAC',await key(env),encoder.encode(`${purpose}.${body}`));
  return `${body}.${base64(new Uint8Array(signature))}`;
}
async function verified(value,purpose,env,lifetime,origin) {
  if (!configured(env) || !value || value.length > 4096) return null;
  try {
    const parts = value.split('.');
    if (parts.length !== 2 || !await crypto.subtle.verify('HMAC',await key(env),unbase64(parts[1]),encoder.encode(`${purpose}.${parts[0]}`))) return null;
    const data = JSON.parse(new TextDecoder().decode(unbase64(parts[0])));
    if (!Number.isInteger(data.iat) || !Number.isInteger(data.exp) || data.iat > now() || data.exp <= now() || data.exp-data.iat !== lifetime || data.origin !== origin) return null;
    return data;
  } catch { return null; }
}
function returnPath(value,origin) {
  if (typeof value !== 'string' || value.length > 1024 || !value.startsWith('/') || value.startsWith('//') || /[\\\u0000-\u0020\u007f]/.test(value) || /%(?:5c|0[0-9a-f]|1[0-9a-f]|7f)/i.test(value)) return '/';
  try {
    const target = new URL(value,origin);
    return target.origin === origin && !target.pathname.startsWith('/auth/') ? target.pathname+target.search+target.hash : '/';
  } catch { return '/'; }
}
function response(message,status=400,setCookies=[]) {
  const result = new Response(message,{status,headers});
  for (const value of setCookies) result.headers.append('Set-Cookie',value);
  return result;
}
function redirect(location,setCookies=[]) {
  const result = response(null,303,setCookies);
  result.headers.set('Location',location);
  return result;
}
async function githubJson(url,options) {
  const controller = new AbortController(), timer = setTimeout(() => controller.abort(),10000);
  try {
    const result = await fetch(url,{...options,redirect:'manual',signal:controller.signal});
    if (!result.ok) throw new Error('GitHub unavailable');
    const reader = result.body.getReader();
    let size = 0; const chunks = [];
    while (true) {
      const {done,value} = await reader.read(); if (done) break;
      size += value.length;
      if (size > 32768) { await reader.cancel(); throw new Error('Invalid GitHub response'); }
      chunks.push(value);
    }
    const bytes = new Uint8Array(size); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk,offset); offset += chunk.length; }
    return JSON.parse(new TextDecoder().decode(bytes));
  } finally { clearTimeout(timer); }
}

export async function musicIdentity(request,env) {
  const data = await verified(cookies(request).get(SESSION),'session',env,SESSION_SECONDS,new URL(request.url).origin);
  return data && /^[1-9]\d{0,19}$/.test(data.id) && typeof data.login === 'string' && /^[a-z\d](?:[a-z\d-]{0,38})$/i.test(data.login) ? {id:data.id,login:data.login} : null;
}

export async function musicAuthResponse(request,env) {
  const url = new URL(request.url), path = url.pathname;
  if (!['/auth/github','/auth/github/callback','/auth/github/logout'].includes(path)) return null;
  if (path === '/auth/github/logout') {
    if (request.method !== 'POST') return response('Use POST to sign out.',405);
    if (request.headers.get('origin') !== url.origin) return response('Invalid request origin.',403);
    return redirect(returnPath(url.searchParams.get('returnTo'),url.origin),[cookie(SESSION,'',0),cookie(FLOW,'',0)]);
  }
  if (request.method !== 'GET') return response('Method not allowed.',405);
  if (url.protocol !== 'https:' || !configured(env) || !env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) return response('GitHub sign-in is unavailable.',503);
  const callback = url.origin+'/auth/github/callback';
  if (path === '/auth/github') {
    const state = random(), verifier = random(), issued = now();
    const flow = await signed({state,verifier,returnTo:returnPath(url.searchParams.get('returnTo'),url.origin),origin:url.origin,iat:issued,exp:issued+FLOW_SECONDS},'oauth',env);
    const authorize = new URL('https://github.com/login/oauth/authorize');
    authorize.search = new URLSearchParams({client_id:env.GITHUB_CLIENT_ID,redirect_uri:callback,scope:'',state,code_challenge:base64(new Uint8Array(await crypto.subtle.digest('SHA-256',encoder.encode(verifier)))),code_challenge_method:'S256'}).toString();
    return redirect(authorize.href,[cookie(FLOW,flow,FLOW_SECONDS)]);
  }
  const clear = [cookie(FLOW,'',0)];
  const flow = await verified(cookies(request).get(FLOW),'oauth',env,FLOW_SECONDS,url.origin);
  const state = url.searchParams.get('state'), code = url.searchParams.get('code');
  if (!flow || typeof flow.state !== 'string' || !/^[\w-]{43}$/.test(flow.verifier) || state !== flow.state || !code || code.length > 1024 || url.searchParams.getAll('state').length !== 1 || url.searchParams.getAll('code').length !== 1 || url.searchParams.has('error')) return response('Sign-in expired or was cancelled. Try again.',400,clear);
  try {
    const token = await githubJson('https://github.com/login/oauth/access_token',{method:'POST',headers:{Accept:'application/json','Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({client_id:env.GITHUB_CLIENT_ID,client_secret:env.GITHUB_CLIENT_SECRET,code,redirect_uri:callback,code_verifier:flow.verifier}).toString()});
    if (typeof token.access_token !== 'string' || !/^[\w-]{1,512}$/.test(token.access_token) || token.token_type?.toLowerCase() !== 'bearer') throw new Error('Invalid token');
    const user = await githubJson('https://api.github.com/user',{headers:{Accept:'application/vnd.github+json',Authorization:`Bearer ${token.access_token}`,'User-Agent':'boluopai-music','X-GitHub-Api-Version':'2022-11-28'}});
    if (!Number.isSafeInteger(user.id) || user.id <= 0 || typeof user.login !== 'string' || !/^[a-z\d][a-z\d-]{0,38}$/i.test(user.login)) throw new Error('Invalid identity');
    const issued = now();
    const session = await signed({id:String(user.id),login:user.login,origin:url.origin,iat:issued,exp:issued+SESSION_SECONDS},'session',env);
    return redirect(returnPath(flow.returnTo,url.origin),[...clear,cookie(SESSION,session,SESSION_SECONDS)]);
  } catch { return response('GitHub sign-in failed. Try again.',502,clear); }
}
