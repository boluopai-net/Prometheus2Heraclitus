// Native anchors own navigation and history; this only follows reading progress.
const guide = document.querySelector('.practical-guide');
const nav = guide?.querySelector('.guide-sidebar nav');
if (nav) {
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const headings = links.map(link => document.getElementById(link.hash.slice(1)));
  const ids = new Set(headings.map(heading => heading.id));
  const openDestination = hash => {
    const target = headings.find(heading => '#' + heading.id === hash);
    if (target?.matches('details')) target.open = true;
  };
  nav.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link) openDestination(link.hash);
  });
  openDestination(location.hash);
  const narrow = matchMedia('(max-width:1000px)');
  let scheduled = false;
  let current;
  const reveal = link => {
    // The narrow contents stay in normal flow; progress must never pull the page back.
    if (narrow.matches) return;
    const box = link.getBoundingClientRect();
    const rail = nav.getBoundingClientRect();
    if (box.top < rail.top || box.bottom > rail.bottom) {
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
  window.addEventListener('hashchange', () => { openDestination(location.hash); syncLanguage(); schedule(); });
  nav.addEventListener('focusin', event => {
    if (event.target.matches('a')) reveal(event.target);
  });
  syncLanguage();
  schedule();
  document.fonts.ready.then(schedule);
}
