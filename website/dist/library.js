// Formula source is preserved in HTML; local KaTeX improves its presentation.
document.querySelectorAll('.math-source').forEach(node => {
  if (!window.katex) return;
  try {
    katex.render(node.dataset.tex, node, {
      displayMode: node.dataset.display === 'true',
      throwOnError: false,
      strict: 'ignore',
      trust: false,
      output: 'htmlAndMathml'
    });
  } catch (_) {
    // Keep the original TeX readable if a formula is outside KaTeX's grammar.
  }
});

// Keep ordinary inline math in the prose. Only a formula wider than its reader
// needs a separate horizontal scroll area; recheck after fonts load and resize.
document.querySelectorAll('.document').forEach(reader => {
  const formulas = [...reader.querySelectorAll('.math-source[data-display="false"]')];
  const fitMath = () => formulas.forEach(node => {
    const visual = node.querySelector('.katex-html');
    const available = Math.min(reader.clientWidth, node.parentElement.clientWidth || reader.clientWidth);
    node.classList.toggle('math-wide', Boolean(visual && visual.getBoundingClientRect().width > available));
  });
  fitMath();
  document.fonts.ready.then(fitMath);
  new ResizeObserver(fitMath).observe(reader);
});
// Book navigation crosses pages; this separate navigation follows the page itself.
// Reference readers retain their existing rail and mobile placement.
const contents = document.querySelector('.commentary .reader-toc');
if (contents) {
  const book = document.querySelector('.philosophy-book');
  const desktop = matchMedia(book ? '(min-width:1280px)' : '(min-width:768px)');
  const rail = contents.parentElement;
  const syncContents = () => {
    if (desktop.matches) rail.prepend(contents);
    else {
      const heading = document.querySelector('.commentary .document h1');
      (heading.closest('.article-heading') || heading).after(contents);
    }
    if (book) contents.open = desktop.matches;
  };
  syncContents();
  desktop.addEventListener('change', syncContents);
  const links = [...contents.querySelectorAll('a[href^="#"]')];
  const headings = links.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1)))).filter(Boolean);
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting);
    if (!visible.length) return;
    const active = visible.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0].target.id;
    links.forEach(link => {
      if (decodeURIComponent(link.hash.slice(1)) === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, {rootMargin: '-5% 0px -70% 0px'});
  headings.forEach(heading => observer.observe(heading));
}
