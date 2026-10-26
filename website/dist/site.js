/* Page behaviors mount once per document view; the music shell outlives them. */
(() => {
  if (window.sitePage) return;
  const tasks=new Map();let generation=0,ready=false,controller=new AbortController(),cleanups=[];
  const run=task=>{
    if(!ready||task.generation===generation)return;
    task.generation=generation;
    try{
      const result=task.init({signal:controller.signal,onCleanup:fn=>cleanups.push(fn)});
      if(typeof result==='function')cleanups.push(result);
      else result?.catch?.(error=>{if(error.name!=='AbortError')console.error(error);});
    }catch(error){console.error(error);}
  };
  window.sitePage=(name,init)=>{if(!tasks.has(name))tasks.set(name,{init,generation:-1});run(tasks.get(name));};
  window.sitePages={
    unmount(){ready=false;controller.abort();for(const fn of cleanups.splice(0)){try{fn();}catch(error){console.error(error);}}generation++;},
    mount(){if(controller.signal.aborted)controller=new AbortController();ready=true;for(const task of tasks.values())run(task);}
  };
  document.addEventListener('DOMContentLoaded',()=>{
    window.sitePages.mount();
    if(window.top===window&&document.querySelector('header.header'))import('./site-navigation.js').then(module=>module.startNavigation()).catch(console.error);
  },{once:true});
})();

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
  window.sitePage('theme-controls', () => {
    apply();
    import('./theme-music.js').then(module => module.startSiteMusic()).catch(error => {
      console.warn('Site music is unavailable:', error.message);
    });
    document.querySelectorAll('[data-theme-control]').forEach(button => {
      button.addEventListener('click', () => {
        choice = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem('boluopai-theme', choice); } catch (_) {}
        apply();
      });
    });
  });
})();

/* One secure draw; motion and speed only determine its presentation. */
window.sitePage('skills-wheel', ({signal,onCleanup}) => {
  const slider = document.querySelector('[data-wheel-speed]');
  const wheel = document.querySelector('[data-wheel-disc]');
  if (!slider || !wheel) return;

  const output = document.querySelector('[data-wheel-speed-output]');
  const toggle = document.querySelector('[data-wheel-motion]');
  const button = document.querySelector('[data-wheel-draw]');
  const result = document.querySelector('[data-wheel-result]');
  const options = [...wheel.querySelectorAll('[data-wheel-option]')];
  const english = document.documentElement.lang === 'en';
  let enabled = true, angle = 0, duration = 48, draw = null, last = null;
  let settled = false, navigation = null, frame = 0;
  onCleanup(()=>{cancelAnimationFrame(frame);clearTimeout(navigation);});
  const preferenceKey = 'boluopai-skills-wheel';
  try {
    const saved = JSON.parse(localStorage.getItem(preferenceKey));
    if (saved && typeof saved.motion === 'boolean') enabled = saved.motion;
    if (saved && typeof saved.speed === 'number' && Number.isFinite(saved.speed) && saved.speed >= 0 && saved.speed <= 100) slider.value = saved.speed;
  } catch (_) {}
  const savePreferences = () => {
    try { localStorage.setItem(preferenceKey, JSON.stringify({motion: enabled, speed: Number(slider.value)})); } catch (_) {}
  };
  const paint = () => wheel.setAttribute('transform', `rotate(${angle} 280 280)`);
  const finish = () => {
    if (!draw || settled) return;
    settled = true;
    angle = draw.target;
    paint();
    const option = options[draw.index];
    option.setAttribute('data-selected', '');
    result.textContent = english ? `Selected: ${option.dataset.wheelLabel}. Opening…` : `选中：${option.dataset.wheelLabel}，正在打开…`;
    navigation = setTimeout(() => (window.siteNavigate || (url=>location.assign(url)))(option.getAttribute('href')), enabled ? 1000 : 250);
  };
  const slowDuration = 120;
  const fastDuration = .1;

  const update = () => {
    const position = Number(slider.value) / 100;
    duration = slowDuration * Math.pow(fastDuration / slowDuration, position);
    const seconds = Number(duration.toFixed(duration < 1 ? 2 : 1));
    const speedLabel = duration < 1
      ? (english ? `${Number((1 / duration).toFixed(1))} rotations / sec` : `${Number((1 / duration).toFixed(1))} 圈/秒`)
      : (english ? `${seconds} sec / rotation` : `${seconds} 秒/圈`);
    slider.disabled = !enabled;
    slider.setAttribute('aria-valuetext', english ? `${seconds} seconds per rotation` : `${seconds} 秒/圈`);
    if (output) output.textContent = speedLabel;
    if (toggle) {
      toggle.setAttribute('aria-checked', String(enabled));
      toggle.textContent = english
        ? `Motion: ${enabled ? 'On' : 'Off'}`
        : `动态效果：${enabled ? '开' : '关'}`;
    }

    if (!enabled && draw) finish();
  };
  button.addEventListener('click', () => {
    if (draw) return;
    const sample = new Uint32Array(1);
    const limit = Math.floor(4294967296 / options.length) * options.length;
    try { do { crypto.getRandomValues(sample); } while (sample[0] >= limit); }
    catch { result.textContent = english ? 'Random selection is unavailable. Choose a Skill below.' : '暂时无法随机抽选，请直接选择下方 Skill。'; return; }
    const index = sample[0] % options.length;
    const target = (360 - index * 360 / options.length) % 360;
    draw = {index, target, start: angle, distance: 360 * 5 + (target - angle % 360 + 360) % 360, progress: 0};
    button.disabled = true;
    result.textContent = english ? 'Spinning…' : '正在抽选…';
    if (!enabled) finish();
  });
  function tick(now) {
    if(signal.aborted)return;
    const dt = last === null ? 0 : Math.min(now - last, 100);
    last = now;
    if (enabled && !settled) {
      if (draw) {
        draw.progress = Math.min(1, draw.progress + dt / (4800 * Math.pow(duration / 48, .2)));
        // Smooth acceleration followed by a longer deceleration; zero end velocity.
        const p = draw.progress;
        const ease = 1 - Math.pow(1 - p, 3) * (1 + 3 * p);
        angle = draw.start + draw.distance * ease;
        if (p === 1) finish();
      } else angle = (angle + dt * 360 / (duration * 1000)) % 360;
      paint();
    }
    frame=requestAnimationFrame(tick);
  }
  slider.addEventListener('input', () => { update(); savePreferences(); });
  toggle?.addEventListener('click', () => { enabled = !enabled; update(); savePreferences(); });
  window.addEventListener('pagehide', () => clearTimeout(navigation),{signal});
  window.addEventListener('pageshow', event => {
    if (event.persisted) { draw = null; settled = false; button.disabled = false; last = null; options.forEach(option => option.removeAttribute('data-selected')); result.textContent = english ? 'Spin to discover another Skill.' : '再转一次，发现另一个 Skill。'; }
  },{signal});
  update();
  frame=requestAnimationFrame(tick);
});
