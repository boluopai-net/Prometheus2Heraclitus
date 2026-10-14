// Per-comment capabilities stay in the author's browser, never in public reads.
const key = 'boluopai-comment-deletion-v1:';
const draftKey = 'boluopai-comment-drafts-v1';
const validId = value => typeof value === 'string' && /^[0-9a-f-]{36}$/i.test(value);
const validToken = value => typeof value === 'string' && /^[0-9a-f]{64}$/.test(value);
const read = name => { try { const value=JSON.parse(sessionStorage.getItem(name)); return value && typeof value==='object' && !Array.isArray(value) ? value : {}; } catch { return {}; } };
const save = (name,value) => { try { sessionStorage.setItem(name,JSON.stringify(value)); return true; } catch { return false; } };
const owned = new Map();
export function credentialFor(id) { let token=owned.get(id); try { token=token||localStorage.getItem(key+id); } catch {} return validToken(token)?token:undefined; }
export function remember(id,token) {
  if(!validId(id)||!validToken(token)) throw Error('Invalid credential');
  owned.set(id,token);
  try { localStorage.setItem(key+id,token); return true; } catch { return false; }
}
export function forget(id) { owned.delete(id); try { localStorage.removeItem(key+id); } catch {} }
export function managementLink(id,token,english=false) {
  return new URL('/comment/manage/'+(english?'en/':''),location.origin).href+'#'+new URLSearchParams({id,key:token});
}
export function prepareSubmission(kind,fields) {
  const drafts=read(draftKey), fingerprint=JSON.stringify(fields);
  let draft=drafts[kind];
  if(!draft || draft.fingerprint!==fingerprint || !validId(draft.id) || !validToken(draft.token)) {
    draft={id:crypto.randomUUID(),token:Array.from(crypto.getRandomValues(new Uint8Array(32)),x=>x.toString(16).padStart(2,'0')).join(''),fingerprint};
    drafts[kind]=draft; save(draftKey,drafts);
  }
  const remembered=remember(draft.id,draft.token);
  return {id:draft.id,deletionToken:draft.token,remembered};
}
export function finishSubmission(kind) { const drafts=read(draftKey); delete drafts[kind]; save(draftKey,drafts); }
export async function manageComment(id,token,action) {
  const response=await fetch('/api/suggestions/manage',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,deletionToken:token,action})});
  const data=await response.json();
  if(!response.ok) throw Object.assign(Error(data.error||'Unable to manage comment'),{status:response.status});
  return data;
}
