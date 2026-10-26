/* Replay only the finite temporal study; native buttons retain keyboard access. */
window.sitePage('article-art', ({onCleanup}) => {
document.querySelectorAll('.time-inset').forEach((inset) => {
  const replay = inset.querySelector('.time-replay');
  const start = () => inset.classList.add('time-active');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        start();
        observer.disconnect();
      }
    }, { threshold: 0.25 });
    observer.observe(inset);
    onCleanup(() => observer.disconnect());
  } else {
    start();
  }
  replay.addEventListener('click', () => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    start();
    inset.querySelector('svg').getAnimations({ subtree: true }).forEach((animation) => {
      animation.currentTime = 0;
      animation.play();
    });
  });
});
});
