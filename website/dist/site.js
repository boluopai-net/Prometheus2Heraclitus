/* Resolve the theme before the body paints; storage is optional. */
(() => {
  const root = document.documentElement;
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let choice;
  try { choice = localStorage.getItem('boluopai-theme'); } catch (_) {}
  if (choice !== 'light' && choice !== 'dark') choice = null;
  const apply = () => {
    const dark = choice ? choice === 'dark' : system.matches;
    root.dataset.theme = dark ? 'dark' : 'light';
    root.style.colorScheme = root.dataset.theme;
    document.querySelectorAll('[data-theme-control]').forEach(button => {
      button.setAttribute('aria-pressed', String(dark));
    });
  };
  apply();
  system.addEventListener('change', apply);
  window.addEventListener('storage', event => {
    if (event.key === 'boluopai-theme') {
      choice = ['light', 'dark'].includes(event.newValue) ? event.newValue : null;
      apply();
    }
  });
  document.addEventListener('DOMContentLoaded', () => {
    apply();
    document.querySelectorAll('[data-theme-control]').forEach(button => {
      button.addEventListener('click', () => {
        choice = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem('boluopai-theme', choice); } catch (_) {}
        apply();
      });
    });
  });
})();
