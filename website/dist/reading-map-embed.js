/* Each owned frame reports its natural height; links leave the frame normally. */
window.sitePage('reading-map-embed', ({signal,onCleanup}) => {
  const frames = [...document.querySelectorAll('iframe[data-reading-map]')];
  if (!frames.length) return;
  const theme = () => document.documentElement.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const sendTheme = frame => frame.contentWindow?.postMessage(
    {type: 'reading-map-theme', theme: theme()}, location.origin);
  addEventListener('message', event => {
    if (event.origin !== location.origin || event.data?.type !== 'reading-map-size') return;
    const frame = frames.find(frame => frame.contentWindow === event.source);
    if (!frame || !Number.isFinite(event.data.height) || event.data.height < 100 || event.data.height > 20000) return;
    frame.style.height = `${event.data.height + 2}px`;
    sendTheme(frame);
  },{signal});
  const connect=frame=>{
    sendTheme(frame);
    try{frame.contentDocument?.addEventListener('click',event=>{
      const link=event.target.closest?.('a[href]');
      if(!link||!['_top','_parent'].includes(link.target)||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||!window.siteNavigate)return;
      const target=new URL(link.href,location.href);if(target.origin!==location.origin)return;
      event.preventDefault();window.siteNavigate(target.href);
    },{signal});}catch{/* Cross-origin frames retain their native navigation. */}
  };
  frames.forEach(frame => {frame.addEventListener('load',()=>connect(frame),{signal});connect(frame);});
  const observer = new MutationObserver(() => frames.forEach(sendTheme));
  observer.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
  onCleanup(() => observer.disconnect());
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => frames.forEach(sendTheme),{signal});
});
