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
    reactionsEnabled:'1', emitMetadata:'1', inputPosition:'top',
    theme:document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light',
    lang:container.dataset.giscusLanguage || 'zh-CN', loading:'lazy'
  };
  for (const [key,value] of Object.entries(config)) script.dataset[key] = value;
  const link = document.querySelector('[data-github-discussion]');
  if (link) link.href = 'https://github.com/boluopai-net/Prometheus2Heraclitus/discussions?discussions_q=' + encodeURIComponent(config.term);
  window.addEventListener('message', event => {
    const frame = container.querySelector('iframe.giscus-frame');
    if (event.origin !== 'https://giscus.app' || event.source !== frame?.contentWindow) return;
    const url = event.data?.giscus?.discussion?.url;
    if (link && typeof url === 'string' && /^https:\/\/github\.com\/boluopai-net\/Prometheus2Heraclitus\/discussions\/\d+$/.test(url)) link.href = url;
  });
  container.append(script);
  new MutationObserver(() => {
    container.querySelector('iframe.giscus-frame')?.contentWindow.postMessage(
      {giscus:{setConfig:{theme:document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'}}},
      'https://giscus.app');
  }).observe(document.documentElement, {attributes:true,attributeFilter:['data-theme']});
}
