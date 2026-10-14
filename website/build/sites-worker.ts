import { publicApi, privateHeaders } from '../lib/public-api.js';
import { adminPage } from '../lib/suggestion-admin.js';
import { visitorApi } from '../lib/visitor-api.js';

export default {
  async fetch(request: Request, env: Cloudflare.Env) {
    const visit = await visitorApi(request, env);
    if (visit) return visit;
    const api = await publicApi(request, env);
    if (api) return api;
    const url = new URL(request.url);
    if (/^\/(?:talk|contact)(?:\/en)?\/?$/.test(url.pathname)) return Response.redirect('https://github.com/boluopai-net/Prometheus2Heraclitus', 302);
    if (/^\/(?:applications?|downloads?|releases?)(?:\/|$)/.test(url.pathname) || /^\/admin\/(?:applications|download-tokens)(?:\/|$)/.test(url.pathname)) return Response.redirect('https://github.com/boluopai-net/Prometheus2Heraclitus', 302);
    if (url.pathname === '/applications.js') return new Response('Retired', {status:410,headers:privateHeaders});
    if (url.pathname === '/admin/suggestions') return adminPage(request, env);
    if (url.pathname === '/robots.txt') return new Response('User-agent: Googlebot\nDisallow: /api/\nDisallow: /admin/\n\nUser-agent: Bingbot\nDisallow: /api/\nDisallow: /admin/\n\nUser-agent: *\nDisallow: /\n', {headers:{...privateHeaders,'Content-Type':'text/plain'}});
    if (env.ASSETS) {
      const response = await env.ASSETS.fetch(request);
      const result = new Response(response.body, response);
      result.headers.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
      result.headers.set('X-Content-Type-Options', 'nosniff');
      return result;
    }
    return new Response('Service temporarily unavailable', {status:503,headers:privateHeaders});
  },
};
