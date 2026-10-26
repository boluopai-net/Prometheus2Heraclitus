import {Swup,HeadPlugin,ScrollPlugin} from './vendor/navigation/swup.js';

const pageScripts=new Set(['/flow.js','/guide.js','/library.js','/wheel/picker.js','/giscus-comments.js','/reading-map-embed.js','/article-art.js','/repositories/prometheus/vendor/katex/katex.min.js']);
// Content releases pin assets to a snapshot; page behavior identity stays stable.
const scriptPath=src=>new URL(src,location.href).pathname.replace(/^\/_content\/[a-f0-9]{64}(?=\/)/,'');
const ordinaryPage=doc=>!!doc.querySelector('header.header')&&!!doc.querySelector('main');
function destination(url){
  const target=new URL(url,location.href);
  if(target.origin===location.origin&&target.hash==='#package-contract'&&/\/creation-method(?:\.zh-CN)?\.html$/.test(target.pathname)){
    target.pathname=target.pathname.replace('/creation-method','/skill-package');target.hash='';
  }
  return target;
}
function wrapPage(doc){
  for(const link of doc.querySelectorAll('a[href]')){
    const raw=new URL(link.getAttribute('href'),location.href),target=destination(raw);
    if(raw.href!==target.href)link.href=target.href;
  }
  if(doc.querySelector('#site-page'))return;
  const content=doc.createElement('div');content.id='site-page';content.style.display='contents';
  const children=[...doc.body.childNodes].filter(node=>!node.matches?.('.theme-music'));
  doc.body.prepend(content);content.append(...children);
}
export function startNavigation(){
  if(window.siteNavigation||window.top!==window||!ordinaryPage(document))return;
  wrapPage(document);
  const loaded=new Map([...document.querySelectorAll('script[src]')].map(script=>[scriptPath(script.src),Promise.resolve()]));
  function loadScript(info){
    const path=scriptPath(info.src);
    if(!pageScripts.has(path)||loaded.has(path))return loaded.get(path);
    const task=new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=info.src;if(info.type)script.type=info.type;script.onload=resolve;script.onerror=()=>reject(Error('Could not load '+path));document.head.append(script);});
    loaded.set(path,task);return task;
  }
  const ignoreVisit=url=>{
    const target=new URL(url,location.href);
    return target.origin!==location.origin||(target.pathname===location.pathname&&target.search===location.search&&!!target.hash)||/^\/(?:api|media|music|auth|signin-with-chatgpt)(?:\/|$)/.test(target.pathname)||/\.(?:pdf|png|jpe?g|svg|webp|zip|mp3|flac|wav)$/i.test(target.pathname);
  };
  const swup=new Swup({
    // Keep the rendered old view until head assets, scoped initializers and
    // scroll restoration finish; replacing styles must never expose old markup.
    containers:['#site-page'],native:true,animationSelector:false,animateHistoryBrowsing:true,cache:true,ignoreVisit,skipPopStateHandling:()=>false,
    plugins:[new HeadPlugin({awaitAssets:true,persistTags:'script[src],link[data-site-persistent]'}),new ScrollPlugin({animateScroll:false,offset:target=>(parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0)+(target?parseFloat(getComputedStyle(target).scrollMarginTop)||0:0)})]
  });
  window.siteNavigation=swup;
  const rememberScroll=()=>history.replaceState({...history.state,siteScroll:[scrollX,scrollY]},'');
  document.addEventListener('click',event=>{
    const link=event.target.closest?.('a[href]');
    if(!link||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const target=new URL(link.getAttribute('href'),location.href);
    if(target.origin===location.origin&&target.pathname===location.pathname&&target.search===location.search&&target.hash)rememberScroll();
  },true);
  swup.hooks.before('visit:start',visit=>{
    if(!visit.history.popstate)rememberScroll();
    // Fetch readiness belongs before the native snapshot, whose update callback
    // must stay short even on a slow connection.
    visit.animation.wait=true;
  });
  window.addEventListener('popstate',event=>{
    const current=new URL(swup.location.url,location.href);
    if(current.pathname!==location.pathname||current.search!==location.search)return;
    requestAnimationFrame(()=>{
      if(event.state?.siteScroll)window.scrollTo({left:event.state.siteScroll[0],top:event.state.siteScroll[1],behavior:'instant'});
      else if(location.hash)swup.getAnchorElement(location.hash)?.scrollIntoView({behavior:'instant'});
    });
  });
  window.siteNavigate=url=>{const target=destination(url);return ignoreVisit(target.href)?location.assign(target.href):swup.navigate(target.href);};
  const clearPreloads=visit=>{
    for(const link of visit.meta.assetPreloads||[]){
      // A removed pending link need not emit load/error. Release its waiter too.
      link.onload?.();link.onload=link.onerror=null;link.remove();
    }
    visit.meta.assetPreloads=[];
  };
  swup.hooks.on('visit:abort',clearPreloads);
  swup.hooks.on('visit:fail',clearPreloads);
  swup.hooks.on('page:load',async(visit,{page})=>{
    const incoming=new DOMParser().parseFromString(page.html,'text/html');
    if(!ordinaryPage(incoming)){visit.ignore();location.assign(visit.to.url+visit.to.hash);return;}
    // Warm new styles/scripts without applying CSS to the still-visible page.
    // The head plugin can then preserve its original cascade order at commit.
    const assets=[...incoming.querySelectorAll('link[rel="stylesheet"][href],script[src]')].filter(node=>{
      if(node.tagName==='SCRIPT')return pageScripts.has(scriptPath(node.src))&&!loaded.has(scriptPath(node.src));
      return ![...document.querySelectorAll('link[rel="stylesheet"][href]')].some(link=>link.href===node.href);
    });
    visit.meta.assetPreloads=[];
    try{
      await Promise.all(assets.map(asset=>new Promise((resolve,reject)=>{
        const link=document.createElement('link');
        link.rel=asset.type==='module'?'modulepreload':'preload';link.as=asset.tagName==='SCRIPT'?'script':'style';link.href=asset.src||asset.href;
        if(asset.hasAttribute('crossorigin'))link.crossOrigin=asset.crossOrigin;
        link.onload=resolve;link.onerror=()=>reject(Error('Could not preload '+link.href));
        visit.meta.assetPreloads.push(link);document.head.append(link);
      })));
    }catch(error){
      clearPreloads(visit);
      if(!visit.done){visit.ignore();location.assign(visit.to.url+visit.to.hash);}
    }
    if(visit.done)clearPreloads(visit);
  });
  swup.hooks.before('content:replace',visit=>{
    const incoming=visit.to.document;
    visit.meta.scripts=[...incoming.querySelectorAll('script[src]')].map(script=>({src:script.getAttribute('src'),type:script.type}));
    // Page scripts are loaded once and register scoped initializers, not re-evaluated.
    incoming.querySelectorAll('script[src]').forEach(script=>script.remove());
    wrapPage(incoming);window.sitePages.unmount();
    for(const attr of [...document.body.attributes])document.body.removeAttribute(attr.name);
    for(const attr of incoming.body.attributes)document.body.setAttribute(attr.name,attr.value);
  },{priority:-100});
  swup.hooks.on('content:replace',async visit=>{
    try{
      for(const script of visit.meta.scripts)await loadScript(script);
      window.sitePages.mount();
      document.dispatchEvent(new Event('site:language'));
      const main=document.querySelector('main');main?.setAttribute('tabindex','-1');main?.focus({preventScroll:true});
    }catch(error){visit.ignore();location.assign(visit.to.url+visit.to.hash);}finally{clearPreloads(visit);}
  });
  // Expand a native disclosure before the scroll plugin resolves its anchor.
  swup.hooks.before('scroll:anchor',(_visit,{hash})=>{
    let id;try{id=decodeURIComponent(hash.slice(1));}catch{return;}
    const target=document.getElementById(id);for(let node=target;node;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;
  });
}
