import { json } from './public-api.js';

// The owner retired public model access. Keep old clients from queuing work;
// the private owner assistant does not receive website approval requests.
export async function visitorApi(request) {
  const path = new URL(request.url).pathname;
  if (path === '/api/visit/status') return json({online:false, retired:true});
  if (path.startsWith('/api/visit/') || ['/api/hermes/claim', '/api/hermes/complete'].includes(path)) {
    return json({error:'公开聊天已关闭。请通过 GitHub 交流，或在哲学、唱歌、资料页面留言。'},410);
  }
  return null;
}
