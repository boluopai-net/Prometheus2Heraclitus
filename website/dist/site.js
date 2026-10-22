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

/* Keep the Skills illustration speed control local to the large wheel. */
document.addEventListener('DOMContentLoaded', () => {
  const slider = document.querySelector('[data-wheel-speed]');
  const wheel = document.querySelector('.skills-wheel-heading > .motif');
  if (!slider || !wheel) return;

  const output = document.querySelector('[data-wheel-speed-output]');
  const toggle = document.querySelector('[data-wheel-motion]');
  let enabled = true;
  const baseDuration = 48;
  const slowDuration = 120;
  const fastDuration = 6;

  const update = () => {
    const position = Number(slider.value) / 100;
    const duration = slowDuration * Math.pow(fastDuration / slowDuration, position);
    const seconds = Math.round(duration);
    const english = document.documentElement.lang === 'en';
    slider.disabled = !enabled;
    slider.setAttribute('aria-valuetext', english ? `${seconds} seconds per rotation` : `${seconds} 秒/圈`);
    if (output) output.textContent = english
      ? `${seconds} sec / rotation`
      : `${seconds} 秒/圈`;
    if (toggle) {
      toggle.setAttribute('aria-checked', String(enabled));
      toggle.textContent = english
        ? `Motion: ${enabled ? 'On' : 'Off'}`
        : `动态效果：${enabled ? '开' : '关'}`;
    }

    const playbackRate = baseDuration / duration;
    for (const animation of wheel.getAnimations()) {
      if (animation.animationName !== 'skills-wheel-turn') continue;
      if (!enabled) { animation.pause(); continue; }
      if (typeof animation.updatePlaybackRate === 'function') {
        animation.updatePlaybackRate(playbackRate);
      } else {
        const time = animation.currentTime;
        animation.playbackRate = playbackRate;
        animation.currentTime = time;
      }
      animation.play();
    }
  };

  slider.addEventListener('input', update);
  toggle?.addEventListener('click', () => { enabled = !enabled; update(); });
  update();
});
