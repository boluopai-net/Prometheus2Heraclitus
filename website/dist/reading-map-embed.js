/* Each owned frame reports its natural height; links leave the frame normally. */
(() => {
  if (window.readingMapsConnected) return;
  window.readingMapsConnected = true;
  const frames = () => [...document.querySelectorAll('iframe[data-reading-map]')];
  const theme = () => document.documentElement.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const sendTheme = frame => frame.contentWindow?.postMessage(
    {type: 'reading-map-theme', theme: theme()}, location.origin);
  addEventListener('message', event => {
    if (event.origin !== location.origin || event.data?.type !== 'reading-map-size') return;
    const frame = frames().find(frame => frame.contentWindow === event.source);
    if (!frame || !Number.isFinite(event.data.height) || event.data.height < 100 || event.data.height > 20000) return;
    frame.style.height = `${event.data.height + 2}px`;
    sendTheme(frame);
  });
  frames().forEach(frame => frame.addEventListener('load', () => sendTheme(frame)));
  new MutationObserver(() => frames().forEach(sendTheme))
    .observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => frames().forEach(sendTheme));
})();
