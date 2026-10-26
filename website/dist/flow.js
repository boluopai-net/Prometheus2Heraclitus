window.sitePage('flow', ({signal,onCleanup}) => {
  const canvas = document.querySelector('#flow');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const button = document.querySelector('#motion');
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = media.matches, frame = 0, time = 0, last = 0, visible = true;
  let width = 0, height = 0;
  function size() {
    if (signal.aborted) return;
    const box = canvas.getBoundingClientRect(), dpr = Math.min(devicePixelRatio || 1, 2);
    width = box.width; height = box.height;
    canvas.width = width * dpr; canvas.height = height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); paint();
  }
  function paint() {
    const w = width, h = height, split = h * .52;
    ctx.fillStyle = '#eee4d4'; ctx.fillRect(0, 0, w, split);
    // Thin nested ribbons rise and curl like an engraved field of flames.
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, w, split); ctx.clip();
    for (let group = 0; group < 7; group++) {
      const center = w * (.20 + group * .13);
      for (let i = 0; i < 18; i++) {
        ctx.beginPath();
        for (let step = 0; step <= 70; step++) {
          const p = step / 70, y = split + 45 - p * (split + 55);
          const envelope = Math.sin(p * Math.PI) * (24 + group * 4);
          const wave = Math.sin(p * 5.1 + group * 1.7 + time * .24) * envelope;
          const x = center + wave + (i - 8.5) * (2 + 5 * (1-p)) * Math.sin(p * 2.6 + .35);
          if (!step) ctx.moveTo(x,y); else ctx.lineTo(x,y);
        }
        ctx.strokeStyle = `rgba(${i % 3 ? '170,67,35' : '205,127,59'},${.24 + i/90})`;
        ctx.lineWidth = i % 5 === 0 ? 1.6 : .8; ctx.stroke();
      }
    }
    ctx.restore();
    ctx.fillStyle = '#d9e2d8'; ctx.fillRect(0, split, w, h-split);
    ctx.save(); ctx.beginPath(); ctx.rect(0, split, w, h-split); ctx.clip();
    for (let row = 0; row < 52; row++) {
      ctx.beginPath();
      for (let step = 0; step <= 100; step++) {
        const p = step/100, x = p*w;
        const bend = Math.sin(p*8.4 + row*.038 + time*.20)*18 + Math.sin(p*17-row*.04-time*.13)*6;
        const y = split + row*6 + bend;
        if (!step) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      }
      ctx.strokeStyle = row % 4 === 0 ? 'rgba(52,88,84,.48)' : 'rgba(67,102,94,.23)';
      ctx.lineWidth = row % 4 === 0 ? 1 : .7; ctx.stroke();
    }
    ctx.restore();
  }
  function tick(stamp) {
    frame = 0;
    if (signal.aborted || paused || document.hidden || !visible) return;
    time += Math.min((stamp-last)/1000 || 0,.05); last = stamp; paint();
    frame = requestAnimationFrame(tick);
  }
  function sync() {
    if (signal.aborted) return;
    cancelAnimationFrame(frame); frame = 0; last = performance.now();
    button.setAttribute('aria-pressed',String(paused));
    const english = document.documentElement.lang === 'en';
    button.textContent = paused ? (english ? 'Play animation ▷' : '播放动效 ▷') : (english ? 'Pause animation Ⅱ' : '暂停动效 Ⅱ');
    if (!paused && visible && !document.hidden) frame=requestAnimationFrame(tick);
  }
  button.addEventListener('click',()=>{paused=!paused;sync()});
  media.addEventListener('change',()=>{paused=media.matches;sync()},{signal});
  document.addEventListener('visibilitychange',sync,{signal});
  const visibility = new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync()});
  const resize = new ResizeObserver(size);
  visibility.observe(canvas); resize.observe(canvas);
  onCleanup(() => {cancelAnimationFrame(frame);visibility.disconnect();resize.disconnect();});
  size(); sync();
});
