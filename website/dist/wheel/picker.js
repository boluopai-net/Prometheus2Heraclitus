(async () => {
  const en = document.documentElement.lang === 'en', t = (zh, english) => en ? english : zh, $ = id => document.getElementById(id), frame = $('wheel');
  const defaults = en ? ['Information Theory','Fundamental Physics','Cybernetics','Numerical Analysis','Data Analysis','Mathematical Logic','Machine Learning','Philosophy of Science','Algorithms and Data Structures','Programming Language Theory','Computational Complexity','Introduction to Computer Science','Computer Networks','Probability','Linear Algebra','Economics','Advanced Mathematics and Mathematical Analysis'] : ['信息论','基础物理','控制论','数值分析','数据分析','数理逻辑','机器学习','科学哲学','算法与数据结构','编程语言理论','计算复杂性','计算机科学概论','计算机网络','概率论','线性代数','经济学','高数与数学分析'];
  const key = 'boluopai-wheel-v2-' + document.documentElement.lang;
  let catalog = [], selected = new Set(), freeSelected = new Set(), known = new Set(), mode = 'catalog', template, runId, running = false, speed = 3;
  function parse() {return [...new Set($('options').value.split(/\r?\n/).map(x => x.trim()).filter(Boolean))];}
  try {
    const p = JSON.parse(localStorage.getItem(key));
    if (Array.isArray(p?.catalog) && p.catalog.length <= 100 && p.catalog.every(x => typeof x === 'string' && x.length <= 200)) catalog = p.catalog;
    if (Array.isArray(p?.selected)) selected = new Set(p.selected);
    if (typeof p?.draft === 'string') $('options').value = p.draft;
    if (Array.isArray(p?.freeSelected)) {freeSelected = new Set(p.freeSelected); known = new Set(parse());}
    if (p?.mode === 'free') mode = 'free';
    if (Number.isFinite(p?.speed)) speed = Math.max(.25, Math.min(3, p.speed));
    // Retire only the untouched starter list; keep visitor-authored state.
    if (!p?.emptyStart && mode === 'catalog' && !$('options').value && speed === 3 &&
        JSON.stringify(catalog) === JSON.stringify(defaults) &&
        selected.size === defaults.length && defaults.every(x => selected.has(x))) {
      catalog = []; selected.clear();
    }
  } catch {}
  function persist() {try {localStorage.setItem(key, JSON.stringify({emptyStart:true,catalog,selected:[...selected],freeSelected:[...freeSelected],draft:$('options').value,mode,speed}));} catch {}}
  function current() {return mode === 'catalog' ? catalog : parse();}
  function selection() {return mode === 'catalog' ? selected : freeSelected;}
  function busy() {document.querySelectorAll('.selection-panel button,.selection-panel input,.selection-panel textarea').forEach(x => x.disabled = running);}
  function draw() {
    if (running) return;
    const values = current(), invalid = values.length > 100 || values.some(x => Array.from(x).length > 200);
    const options = invalid ? [] : values.filter(x => selection().has(x));
    $('message').textContent = invalid ? t('最多 100 个选项，每项最多 200 字。','Use up to 100 options, 200 characters each.') : t(`已选 ${options.length} / ${values.length} 项`,`Selected ${options.length} / ${values.length}`);
    frame.hidden = !options.length; $('empty').hidden = !!options.length;
    if (!options.length) {frame.removeAttribute('srcdoc'); return;}
    if (!template) return;
    runId = crypto.randomUUID();
    const config = {options,speed,runId,drawIndex:0,autoStart:false,locale:en?'en':'zh-CN'};
    frame.srcdoc = template.replace('__WHEEL_CONFIG__', JSON.stringify(config).replaceAll('<','\\u003c'));
  }
  function render() {
    $('catalog-mode').setAttribute('aria-pressed', String(mode === 'catalog')); $('free-mode').setAttribute('aria-pressed', String(mode === 'free'));
    $('free-input').hidden = mode !== 'free'; $('add-option').hidden = mode !== 'catalog'; $('choices').replaceChildren();
    for (const name of current()) {
      const label = document.createElement('label'), input = document.createElement('input'), span = document.createElement('span');
      label.className = 'choice'; input.type = 'checkbox'; input.checked = selection().has(name); span.textContent = name;
      input.addEventListener('change', () => {input.checked ? selection().add(name) : selection().delete(name); persist(); draw();});
      label.append(input, span); $('choices').append(label);
    }
    busy(); draw();
  }
  function updateFree() {
    const values = parse(); for (const name of values) if (!known.has(name)) freeSelected.add(name);
    freeSelected = new Set([...freeSelected].filter(x => values.includes(x))); known = new Set(values); persist(); render();
  }
  $('catalog-mode').onclick = () => {mode = 'catalog'; persist(); render();};
  $('free-mode').onclick = () => {mode = 'free'; persist(); render();};
  $('all').onclick = () => {for (const name of current()) selection().add(name); persist(); render();};
  $('none').onclick = () => {selection().clear(); persist(); render();};
  $('options').addEventListener('input', updateFree);
  $('add-option').addEventListener('submit', event => {
    event.preventDefault(); const name = $('new-option').value.trim();
    if (!name || Array.from(name).length > 200 || (!catalog.includes(name) && catalog.length >= 100)) return;
    if (!catalog.includes(name)) catalog.push(name); selected.add(name); $('new-option').value = ''; persist(); render();
  });
  window.addEventListener('message', event => {
    if (event.source !== frame.contentWindow || event.data?.type !== 'boluopai-wheel:state' || event.data.state?.runId !== runId) return;
    running = event.data.state.running === true;
    if (Number.isFinite(event.data.state.speed)) speed = Math.max(.25,Math.min(3,event.data.state.speed));
    busy(); persist();
  });
  updateFree();
  try {
    const response = await fetch('/wheel/engine.html'); if (!response.ok) throw Error();
    template = (await response.text()).replace('</body>', '<script>window.addEventListener("random-wheel:state",e=>parent.postMessage({type:"boluopai-wheel:state",state:e.detail},"*"));<\/script></body>');
    template = template.replace('</head>', '<style>h3,.wheel-options{display:none!important}body{padding:0}.wheel-area{max-width:320px!important}</style></head>');
    draw();
  } catch {$('message').textContent = t('转盘加载失败，请刷新重试。','Could not load the wheel. Please refresh.');}
})();
