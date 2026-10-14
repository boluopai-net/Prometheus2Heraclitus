// Per-comment capabilities stay in the author's browser, never in public reads.
const key = 'boluopai-comment-deletion-v1:';
const validId = value => typeof value === 'string' && /^[0-9a-f-]{36}$/i.test(value);
const validToken = value => typeof value === 'string' && /^[0-9a-f]{64}$/.test(value);
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
export async function manageComment(id,token,action) {
  const response=await fetch('/api/suggestions/manage',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,deletionToken:token,action})});
  const data=await response.json();
  if(!response.ok) throw Object.assign(Error(data.error||'Unable to manage comment'),{status:response.status});
  return data;
}
