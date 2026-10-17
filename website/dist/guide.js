// Native anchors own navigation and history; this only follows reading progress.
const guide = document.querySelector('.practical-guide');
const nav = guide?.querySelector('.guide-sidebar nav');
if (nav) {
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const headings = links.map(link => document.getElementById(link.hash.slice(1)));
  const ids = new Set(headings.map(heading => heading.id));
  const narrow = matchMedia('(max-width:1000px)');
  let scheduled = false;
  let current;
  const reveal = link => {
    const box = link.getBoundingClientRect();
    const rail = nav.getBoundingClientRect();
    if (narrow.matches) {
      if (box.left < rail.left || box.right > rail.right)
        nav.scrollLeft += box.left - rail.left - (nav.clientWidth - box.width) / 2;
    } else if (box.top < rail.top || box.bottom > rail.bottom) {
      nav.scrollTop += box.top - rail.top - (nav.clientHeight - box.height) / 2;
    }
  };
  const update = () => {
    scheduled = false;
    // Read the native landing offset; changing it after load would desynchronize deep links.
    const margin = parseFloat(getComputedStyle(headings[0]).scrollMarginTop) || 0;
    const threshold = margin + (parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0);
    let index = 0;
    headings.forEach((heading, i) => {
      if (heading.getBoundingClientRect().top <= threshold + 1) index = i;
    });
    if (current !== links[index]) {
      current = links[index];
      links.forEach(link => {
        if (link === current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
      reveal(current);
    }
  };
  const schedule = () => {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(update);
    }
  };
  const language = document.querySelector('.header .language-control[href]');
  const syncLanguage = () => {
    if (!language) return;
    const target = new URL(language.href, location.href);
    let fragment;
    try { fragment = decodeURIComponent(location.hash.slice(1)); } catch { fragment = ''; }
    target.hash = ids.has(fragment) ? location.hash : '';
    language.href = target.pathname + target.hash;
  };
  window.addEventListener('scroll', schedule, {passive: true});
  window.addEventListener('resize', () => { current = null; schedule(); });
  window.addEventListener('hashchange', () => { syncLanguage(); schedule(); });
  nav.addEventListener('focusin', event => {
    if (event.target.matches('a')) reveal(event.target);
  });
  syncLanguage();
  schedule();
  document.fonts.ready.then(schedule);
}
