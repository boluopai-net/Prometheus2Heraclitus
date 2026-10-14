const headers = { 'Cache-Control': 'private, no-store', 'X-Robots-Tag': 'noindex, nofollow, noarchive', 'X-Content-Type-Options': 'nosniff' };
const json = (value, status = 200) => new Response(JSON.stringify(value), { status, headers: { ...headers, 'Content-Type': 'application/json; charset=utf-8' } });
export async function publicApi(request) {
  const path = new URL(request.url).pathname;
  if (!path.startsWith('/api/')) return null;
  if (/^\/api\/(?:suggestions(?:\/|$)|admin\/suggestions(?:\/|$))/.test(path)) return json({error:'Comments now use GitHub Discussions.', retired:true, url:'https://github.com/boluopai-net/Prometheus2Heraclitus/discussions'},410);
  if (/^\/api\/(?:applications(?:\/|$)|admin\/(?:applications|download-tokens)(?:\/|$)|hermes\/applications(?:\/|$)|releases(?:\/|$)|download(?:\/|$)|download-requests(?:\/|$))/.test(path)) return json({error:'This service has retired. Source and downloads are available on GitHub.', retired:true, url:'https://github.com/boluopai-net/Prometheus2Heraclitus'},410);
  return json({error:'Not found'},404);
}
export { headers as privateHeaders, json };

