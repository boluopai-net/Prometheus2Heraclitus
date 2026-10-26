/* Native audio. The owner manages the live playlist independently of source. */
export function mountThemeMusic(config) {
  if (!config.active || window.top !== window || document.querySelector('.theme-music')) return;
  const tracks = config.tracks.filter(track => typeof track.src === 'string' && track.src);
  if (!tracks.length) return;
  const t = (zh, english) => document.documentElement.lang === 'en' ? english : zh;
  const key = 'boluopai-theme-music';
  let saved = {}, progress = {};
  try { saved = JSON.parse(localStorage.getItem(key)) || {}; } catch (_) {}
  try { progress = JSON.parse(sessionStorage.getItem(key)) || {}; } catch (_) {}
  let selected = tracks.find(track => track.id === saved.track) || tracks.find(track => track.id === config.defaultTrack) || tracks[0];
  let enabled = saved.enabled !== false;
  let volume = Number.isFinite(saved.volume) ? Math.max(0, Math.min(1, saved.volume)) : 0.25;
  const modes = {sequence:['顺序播放','In order'],list:['列表循环','Repeat playlist'],single:['单曲循环','Repeat track'],shuffle:['随机播放','Shuffle']};
  const modeIcons = {
    sequence:'<path d="M4 5h12M4 10h12M4 15h5M4 20h5M13 17h7m-3-3 3 3-3 3"/>',
    list:'<path d="m17 2 4 4-4 4M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4m14-1v2a3 3 0 0 1-3 3H3"/>',
    single:'<path d="m17 2 4 4-4 4M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4m14-1v2a3 3 0 0 1-3 3H3m7-7 2-1v5"/>',
    shuffle:'<path d="m18 3 3 3-3 3m0 6 3 3-3 3M3 6h2c5 0 9 12 14 12h2M3 18h2c2 0 4-2 6-5m2-2c2-3 4-5 6-5h2"/>'
  };
  const modeIcon = value => `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${modeIcons[value]}</svg>`;
  let mode = Object.hasOwn(modes,saved.mode) ? saved.mode : 'list';
  let request = 0;
  const audio = new Audio();
  audio.preload = 'metadata';
  audio.loop = mode === 'single';
  audio.volume = volume;
  const style = document.createElement('link');
  style.rel = 'stylesheet';
  style.dataset.sitePersistent = '';
  style.href = new URL('./theme-music.css', import.meta.url).href;
  document.head.append(style);
  const root = document.createElement('aside');
  root.className = 'theme-music';
  root.setAttribute('aria-label', t('网站音乐', 'Site music'));
  root.innerHTML = `
    <section class="music-panel" id="theme-music-panel" aria-label="${t('主题曲选择', 'Theme music selection')}" hidden>
      <div class="music-heading"><h2>${t('火与河流', 'Fire and Flow')}</h2><button type="button" data-collapse aria-label="${t('收起面板，保留播放', 'Collapse panel, keep playing')}">−</button></div>
      <div class="music-tracks" role="group" aria-label="${t('选择歌曲', 'Choose a track')}"></div>
      <div class="music-mode"><button type="button" class="music-mode-toggle" aria-expanded="false" aria-controls="theme-music-mode-wheel"></button><div class="music-mode-wheel" id="theme-music-mode-wheel" role="group" hidden></div></div>
      <div class="music-progress"><label class="music-sr" for="theme-music-seek">${t('播放进度', 'Playback position')}</label><input id="theme-music-seek" type="range" min="0" max="0" value="0" step="1" disabled><div><span data-elapsed>0:00</span><span data-duration>0:00</span></div></div>
      <p class="music-status" role="status" aria-live="polite"></p>
      <div class="music-volume"><label for="theme-music-volume">${t('音量', 'Volume')}</label><input id="theme-music-volume" type="range" min="0" max="100" step="1"><output for="theme-music-volume"></output></div>
    </section>
    <div class="music-dock"><button type="button" class="music-play" data-play></button><button type="button" class="music-open" aria-controls="theme-music-panel" aria-expanded="false"><span data-track-name></span></button></div>`;
  document.body.append(root);
  const panel = root.querySelector('.music-panel');
  const play = root.querySelector('[data-play]');
  const open = root.querySelector('.music-open');
  const status = root.querySelector('.music-status');
  const seek = root.querySelector('#theme-music-seek');
  const volumeInput = root.querySelector('#theme-music-volume');
  const modeToggle = root.querySelector('.music-mode-toggle');
  const modeWheel = root.querySelector('.music-mode-wheel');
  for (const value of Object.keys(modes)) {
    const button=document.createElement('button');button.type='button';button.dataset.mode=value;button.innerHTML=modeIcon(value);modeWheel.append(button);
    button.addEventListener('click',()=>{mode=value;audio.loop=mode==='single';save();paint();showModes(false);modeToggle.focus();});
  }
  const showModes = value => {modeWheel.hidden=!value;modeToggle.setAttribute('aria-expanded',String(value));};
  const name = root.querySelector('[data-track-name]');
  const format = value => `${Math.floor((value || 0) / 60)}:${String(Math.floor((value || 0) % 60)).padStart(2, '0')}`;
  const save = () => {
    try { localStorage.setItem(key, JSON.stringify({track: selected.id, enabled, volume, mode})); } catch (_) {}
  };
  const rememberPosition = () => {
    progress = {track: selected.id, time: audio.currentTime};
    try { sessionStorage.setItem(key, JSON.stringify(progress)); } catch (_) {}
  };
  const showPanel = value => {
    panel.hidden = !value;
    open.setAttribute('aria-expanded', String(value));
    if(!value)showModes(false);
  };
  const paint = () => {
    const playing = !audio.paused && !audio.ended;
    root.dataset.playing = String(playing);
    play.textContent = playing ? 'Ⅱ' : '▶';
    play.setAttribute('aria-label', playing ? t('暂停音乐', 'Pause music') : t('播放 ', 'Play ') + selected.title);
    name.textContent = selected.title;
    root.setAttribute('aria-label',t('网站音乐','Site music'));
    panel.setAttribute('aria-label',t('主题曲选择','Theme music selection'));
    root.querySelector('.music-tracks').setAttribute('aria-label',t('选择歌曲','Choose a track'));
    root.querySelector('.music-heading h2').textContent=t('火与河流','Fire and Flow');
    root.querySelector('[data-collapse]').setAttribute('aria-label',t('收起面板，保留播放','Collapse panel, keep playing'));
    root.querySelector('label[for="theme-music-volume"]').textContent=t('音量','Volume');
    root.querySelector('label[for="theme-music-seek"]').textContent=t('播放进度','Playback position');
    modeToggle.innerHTML=modeIcon(mode);
    modeToggle.title=t(...modes[mode]);
    modeToggle.setAttribute('aria-label',t('播放方式：','Playback mode: ')+t(...modes[mode]));
    modeWheel.setAttribute('aria-label',t('选择播放方式','Choose playback mode'));
    for(const button of modeWheel.querySelectorAll('[data-mode]')){button.title=t(...modes[button.dataset.mode]);button.setAttribute('aria-label',button.title);button.setAttribute('aria-pressed',String(button.dataset.mode===mode));}
    root.querySelectorAll('[data-track]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.track === selected.id)));
    volumeInput.value = String(Math.round(volume * 100));
    root.querySelector('output').textContent = `${Math.round(volume * 100)}%`;
  };
  const start = async () => {
    const current = ++request;
    status.textContent = t('正在加载…', 'Loading…');
    try {
      await audio.play();
      if (current !== request) return;
      status.textContent = '';
    } catch (error) {
      if (current !== request) return;
      status.textContent = error.name === 'NotAllowedError'
        ? ''
        : t('暂时无法播放，请稍后重试。', 'Playback is unavailable. Please try again.');
    }
    paint();
  };
  const pause = () => {
    ++request;
    audio.pause();
    enabled = false;
    rememberPosition();
    save();
    status.textContent = t('已暂停', 'Paused');
    paint();
  };
  const loadTrack = track => {
    ++request;
    audio.pause();
    selected = track;
    audio.src = new URL(track.src, import.meta.url).href;
    audio.load();
    seek.disabled = true;
    seek.value = '0';
    root.querySelector('[data-elapsed]').textContent = '0:00';
    root.querySelector('[data-duration]').textContent = '0:00';
    paint();
  };
  for (const track of tracks) {
    const button = document.createElement('button');
    button.type = 'button';
    button.dataset.track = track.id;
    const title = document.createElement('strong');
    title.textContent = track.title;
    const artist = document.createElement('span');
    artist.textContent = track.artist;
    button.append(title, artist);
    button.addEventListener('click', () => {
      if (selected.id !== track.id) { progress = {}; loadTrack(track); }
      enabled = true;
      save();
      start();
    });
    root.querySelector('.music-tracks').append(button);
  }
  play.addEventListener('click', () => {
    if (!audio.paused) { pause(); return; }
    enabled = true;
    save();
    start();
  });
  open.addEventListener('click', () => showPanel(panel.hidden));
  root.querySelector('[data-collapse]').addEventListener('click', () => { showPanel(false); open.focus(); });
  root.addEventListener('keydown', event => {
    if(event.key==='Escape'&&!modeWheel.hidden){showModes(false);modeToggle.focus();event.stopPropagation();return;}
    if (event.key === 'Escape' && !panel.hidden) { showPanel(false); open.focus(); }
  });
  modeToggle.addEventListener('click',()=>{showModes(modeWheel.hidden);if(!modeWheel.hidden)modeWheel.querySelector('[aria-pressed="true"]').focus();});
  document.addEventListener('pointerdown',event=>{if(!event.target.closest('.music-mode'))showModes(false);});
  volumeInput.addEventListener('input', () => { volume = Number(volumeInput.value) / 100; audio.volume = volume; save(); paint(); });
  audio.addEventListener('ended', () => {
    const index=tracks.findIndex(track=>track.id===selected.id);
    if(mode==='sequence'&&index===tracks.length-1){pause();return;}
    let next=(index+1)%tracks.length;
    if(mode==='single')next=index;
    if(mode==='shuffle'&&tracks.length>1)next=(index+1+Math.floor(Math.random()*(tracks.length-1)))%tracks.length;
    progress={};loadTrack(tracks[next]);rememberPosition();save();start();
  });
  seek.addEventListener('input', () => { if (Number.isFinite(audio.duration)) { audio.currentTime = Number(seek.value); rememberPosition(); } });
  audio.addEventListener('loadedmetadata', () => {
    if (!Number.isFinite(audio.duration)) return;
    if (progress.track === selected.id && Number.isFinite(progress.time) && progress.time < audio.duration) audio.currentTime = Math.max(0, progress.time);
    seek.max = String(Math.floor(audio.duration));
    seek.disabled = false;
    root.querySelector('[data-duration]').textContent = format(audio.duration);
  });
  audio.addEventListener('timeupdate', () => {
    seek.value = String(Math.floor(audio.currentTime));
    root.querySelector('[data-elapsed]').textContent = format(audio.currentTime);
  });
  audio.addEventListener('playing', () => { status.textContent = ''; paint(); });
  audio.addEventListener('pause', paint);
  document.addEventListener('site:language',()=>{paint();status.textContent=audio.error?t('暂时无法播放，请稍后重试。','Playback is unavailable. Please try again.') : '';});
  audio.addEventListener('error', () => { status.textContent = t('暂时无法播放，请稍后重试。', 'Playback is unavailable. Please try again.'); paint(); });
  document.addEventListener('play', event => {
    if (event.target !== audio && event.target instanceof HTMLMediaElement) pause();
  }, true);
  window.addEventListener('pagehide', () => { rememberPosition(); ++request; audio.pause(); });
  window.addEventListener('pageshow', event => { if (event.persisted && enabled) start(); });
  loadTrack(selected);
  status.textContent = '';
  if (enabled) start();
  return {audio, root};
}

export async function startSiteMusic() {
  if (!document.querySelector('header.header') || document.querySelector('.theme-music')) return;
  const response = await fetch('/api/music/catalog');
  if (!response.ok) return;
  mountThemeMusic(await response.json());
}
