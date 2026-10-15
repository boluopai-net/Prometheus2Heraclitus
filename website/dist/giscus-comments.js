// The bilingual pages share one GitHub discussion per existing comment stream.
const terms = {Philosophy:'boluopai:philosophy', Singing:'boluopai:singing', Advice:'boluopai:resources'};
const container = document.querySelector('[data-giscus-kind]');
if (container && terms[container.dataset.giscusKind]) {
  const script = document.createElement('script');
  script.src = 'https://giscus.app/client.js';
  script.async = true;
  script.crossOrigin = 'anonymous';
  const config = {
    repo:'boluopai-net/Prometheus2Heraclitus', repoId:'R_kgDOVI4OdQ',
    category:'Announcements', categoryId:'DIC_kwDOVI4Odc4DIbDU',
    mapping:'specific', term:terms[container.dataset.giscusKind], strict:'1',
    reactionsEnabled:'1', emitMetadata:'0', inputPosition:'top',
    theme:document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light',
    lang:container.dataset.giscusLanguage || 'zh-CN', loading:'eager'
  };
  for (const [key,value] of Object.entries(config)) script.dataset[key] = value;
  container.append(script);
  new MutationObserver(() => {
    container.querySelector('iframe.giscus-frame')?.contentWindow.postMessage(
      {giscus:{setConfig:{theme:document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'}}},
      'https://giscus.app');
  }).observe(document.documentElement, {attributes:true,attributeFilter:['data-theme']});
}
