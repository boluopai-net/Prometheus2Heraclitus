import { publicApi, privateHeaders } from '../lib/public-api.js';
import { visitorApi } from '../lib/visitor-api.js';
import { contentReleaseApi, contentResponse } from '../lib/content-release.js';
import { siteMusic, musicOwner } from '../lib/site-music.js';

export default {
  async fetch(request: Request, env: Cloudflare.Env) {
    const url = new URL(request.url);
    const musicManager = /^\/music\/manage(?:\/|$)/.test(url.pathname);
    if (musicManager && !musicOwner(request, env)) {
      if (request.headers.get('oai-authenticated-user-id')) return new Response('Not found', {status:404,headers:privateHeaders});
      return new Response(null, {status:302,headers:{...privateHeaders,Location:'/signin-with-chatgpt?return_to=%2Fmusic%2Fmanage%2F'}});
    }
    const music = await siteMusic(request, env);
    if (music) return music;
    const release = await contentReleaseApi(request, env);
    if (release) return release;
    const visit = await visitorApi(request, env);
    if (visit) return visit;
    const api = await publicApi(request, env);
    if (api) return api;
    if (/^\/(?:talk|contact)(?:\/en)?\/?$/.test(url.pathname)) return Response.redirect('https://github.com/boluopai-net/Prometheus2Heraclitus', 302);
    if (/^\/(?:applications?|downloads?|releases?)(?:\/|$)/.test(url.pathname) || /^\/admin\/(?:applications|download-tokens)(?:\/|$)/.test(url.pathname)) return Response.redirect('https://github.com/boluopai-net/Prometheus2Heraclitus', 302);
    if (url.pathname === '/applications.js') return new Response('Retired', {status:410,headers:privateHeaders});
    if (/^\/(?:admin\/suggestions|comment\/manage)(?:\/|$)/.test(url.pathname) || ['/manage-comment.js', '/comment-ownership.js'].includes(url.pathname)) return new Response('Comments now use GitHub Discussions.', {status:410,headers:privateHeaders});
    if (url.pathname === '/robots.txt') return new Response('User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /admin/\n\nSitemap: https://boluopai.net/sitemap.xml\n', {headers:{'Content-Type':'text/plain','Cache-Control':'public, max-age=300','X-Content-Type-Options':'nosniff'}});
    const content = await contentResponse(request, env);
    if (content) {
      if (musicManager) {
        const headers = new Headers(content.headers);
        headers.set('Cache-Control', 'private, no-store');
        headers.set('X-Robots-Tag', 'noindex, nofollow');
        return new Response(content.body, {status:content.status,headers});
      }
      return content;
    }
    return new Response('Service temporarily unavailable', {status:503,headers:privateHeaders});
  },
};
