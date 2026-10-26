import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {createHash,createHmac} from 'node:crypto';
const require = createRequire(process.env.MUSIC_TEST_PACKAGE || new URL('../package.json',import.meta.url));
const {build} = require('esbuild');
const {Miniflare,createFetchMock} = require('miniflare');
const origin = 'https://music.invalid';
const secret = 'test-only-session-secret-at-least-32-bytes';
const sessionName = '__Host-music-session';
const flowName = '__Host-music-oauth';
function encoded(payload,purpose) {
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  return `${body}.${createHmac('sha256',secret).update(`${purpose}.${body}`).digest('base64url')}`;
}
const payload = value => JSON.parse(Buffer.from(value.split('.')[0],'base64url'));
function cookieValue(result,name) {
  const values = result.headers.getSetCookie();
  const value = values.find(value => value.startsWith(name+'='));
  return value?.split(';')[0].slice(name.length+1);
}

test('GitHub music identity: PKCE, signed sessions, CSRF and redirect boundaries',async t => {
  const built = await build({stdin:{contents:"import {musicAuthResponse,musicIdentity} from './lib/music-identity.js';export default {async fetch(request,env){return await musicAuthResponse(request,env)||Response.json(await musicIdentity(request,env));}};",resolveDir:process.cwd()},bundle:true,write:false,format:'esm',platform:'browser'});
  const mock = createFetchMock(); mock.disableNetConnect();
  const mf = new Miniflare({modules:true,script:built.outputFiles[0].text,compatibilityDate:'2026-05-15',fetchMock:mock,bindings:{GITHUB_CLIENT_ID:'test-client',GITHUB_CLIENT_SECRET:'test-client-secret',MUSIC_SESSION_SECRET:secret}});
  t.after(() => mf.dispose());
  const call = (path,options={}) => mf.dispatchFetch(origin+path,{redirect:'manual',...options});
  const start = async (returnTo='/music?tab=personal') => {
    const result = await call('/auth/github?returnTo='+encodeURIComponent(returnTo));
    assert.equal(result.status,303);
    const location = new URL(result.headers.get('location'));
    assert.equal(location.origin,'https://github.com');
    assert.equal(location.pathname,'/login/oauth/authorize');
    assert.equal(location.searchParams.get('scope'),'');
    assert.equal(location.searchParams.get('redirect_uri'),origin+'/auth/github/callback');
    assert.equal(location.searchParams.get('code_challenge_method'),'S256');
    const value = cookieValue(result,flowName), flow = payload(value);
    assert.equal(location.searchParams.get('code_challenge'),createHash('sha256').update(flow.verifier).digest('base64url'));
    assert.match(result.headers.get('set-cookie'),/Secure; HttpOnly; SameSite=Lax/);
    return {value,flow,state:location.searchParams.get('state')};
  };
  const callback = (flow,extra='',cookie=flow.value) => call('/auth/github/callback?code=test-code&state='+flow.state+extra,{headers:{Cookie:flowName+'='+cookie}});
  assert.equal(await (await call('/whoami')).json(),null);
  const flow = await start();
  assert.equal(flow.flow.exp-flow.flow.iat,600);
  assert.equal((await callback(flow,'&state=other')).status,400);
  assert.equal((await callback({...flow,state:'wrong'})).status,400);
  assert.equal((await callback(flow,'','')).status,400);
  assert.equal((await callback(flow,'',flow.value+'x')).status,400);
  const expiredFlow = {...flow.flow,iat:1,exp:601};
  assert.equal((await callback(flow,'',encoded(expiredFlow,'oauth'))).status,400);
  assert.equal((await callback(flow,'&error=access_denied')).status,400);
  assert.equal((await callback(flow,'&code=second-code')).status,400);
  for (const unsafe of ['https://evil.invalid','//evil.invalid','/\\evil.invalid','/%5cevil.invalid','/path%0d%0aLocation:evil','/auth/github','javascript:alert(1)']) {
    assert.equal((await start(unsafe)).flow.returnTo,'/');
  }
  // Only the exact provider token and public-profile URLs are intercepted;
  // all other outbound traffic is disabled by the mock agent.
  let tokenBody;
  mock.get('https://github.com').intercept({path:'/login/oauth/access_token',method:'POST'}).reply(options => {
    tokenBody = new Response(options.body).text();
    return {statusCode:200,data:JSON.stringify({access_token:'test_github_token',token_type:'bearer',scope:''})};
  });
  mock.get('https://api.github.com').intercept({path:'/user',method:'GET',headers:{authorization:'Bearer test_github_token'}}).reply(200,{id:12345,login:'example-user',email:'must-not-be-saved@example.invalid',name:'Ignored'});
  const result = await callback(flow);
  assert.equal(result.status,303,await result.clone().text());
  const params = new URLSearchParams(await tokenBody);
  assert.equal(params.get('client_id'),'test-client');
  assert.equal(params.get('client_secret'),'test-client-secret');
  assert.equal(params.get('code_verifier'),flow.flow.verifier);
  assert.equal(params.get('redirect_uri'),origin+'/auth/github/callback');
  assert.equal(result.headers.get('location'),'/music?tab=personal');
  assert.equal(cookieValue(result,flowName),'');
  const session = cookieValue(result,sessionName), data = payload(session);
  assert.deepEqual(Object.keys(data).sort(),['exp','iat','id','login','origin']);
  assert.equal(data.exp-data.iat,604800);
  assert.equal(data.id,'12345');
  assert.ok(!JSON.stringify(data).includes('token'));
  const identity = async (value=session,url=origin) => (await mf.dispatchFetch(url+'/whoami',{headers:{Cookie:sessionName+'='+value}})).json();
  assert.deepEqual(await identity(),{id:'12345',login:'example-user'});
  assert.equal(await identity(session+'x'),null);
  assert.equal(await identity(session,'https://other.invalid'),null);
  assert.equal(await identity(encoded({...data,id:'999'},'oauth')),null,'Purpose binding');
  assert.equal(await identity(encoded({...data,iat:1,exp:604801},'session')),null,'Expiry');
  const future = Math.floor(Date.now()/1000)+3600;
  assert.equal(await identity(encoded({...data,iat:future,exp:future+604800},'session')),null,'Future issue time');
  assert.equal(await identity(encoded({...data,exp:data.exp+1},'session')),null,'Lifetime limit');
  assert.equal(await identity(encoded({...data,id:'../owner'},'session')),null,'Stable ID shape');
  assert.equal(await (await call('/whoami',{headers:{Cookie:`${sessionName}=${session}; ${sessionName}=${session}`}})).json(),null,'Duplicate cookies');
  assert.equal((await call('/auth/github/logout')).status,405);
  assert.equal((await call('/auth/github/logout',{method:'POST'})).status,403);
  assert.equal((await call('/auth/github/logout',{method:'POST',headers:{Origin:'https://evil.invalid'}})).status,403);
  const logout = await call('/auth/github/logout?returnTo=%2F%2Fevil.invalid',{method:'POST',headers:{Origin:origin}});
  assert.equal(logout.status,303); assert.equal(logout.headers.get('location'),'/');
  assert.equal(cookieValue(logout,sessionName),'');
  assert.match(logout.headers.getSetCookie().find(value=>value.startsWith(sessionName)),/Max-Age=0/);
  const failed = await start();
  mock.get('https://github.com').intercept({path:'/login/oauth/access_token',method:'POST'}).reply(302,'',{headers:{location:'https://evil.invalid/steal'}});
  assert.equal((await callback(failed)).status,502,'Upstream redirects fail closed');
  mock.assertNoPendingInterceptors();
});
