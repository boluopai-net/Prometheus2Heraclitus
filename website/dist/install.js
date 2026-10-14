const english = document.documentElement.lang === 'en';
const t = (zh, en) => english ? en : zh;
const chooser = document.querySelector('#install-skill');
const request = document.querySelector('#install-request');
const status = document.querySelector('#copy-status');
const button = document.querySelector('#copy-install');
function update() {
  const name = chooser.value;
  const companions = name === 'local-teacher' ? ['local-teacher', 'web-teacher'] : [name];
  const commands = ['codex plugin marketplace add boluopai-net/Prometheus2Heraclitus',
    ...companions.map(skill => 'codex plugin add ' + skill + '@boluopai')].join('\n');
  request.value = t(
    '请从 boluopai 的公开 GitHub 插件市场安装 ' + companions.join('、') + '。使用 Codex 原生插件机制执行：\n\n',
    'Install ' + companions.join(' and ') + ' from the public boluopai GitHub marketplace using Codex native plugins:\n\n'
  ) + commands + t(
    '\n\n请核对安装后的完整资源和 Skill 发现结果。如果已经有同名的私人或手工安装版本，先保留并核对，避免重复启用或覆盖。不要把个人材料写进插件缓存；阴阳个性化时请使用独立私人源目录。完成后告诉我如何在新对话中使用。',
    '\n\nVerify the complete installed resources and Skill discovery. Preserve and inspect any existing private or manually installed version before enabling duplicates or replacing it. Keep personal material outside plugin caches; use a separate private source for a situated YinYang. Explain how to use the result in a new chat.'
  );
  document.querySelector('#install-commands').textContent = commands;
  document.querySelector('#install-source').href = 'https://github.com/boluopai-net/Prometheus2Heraclitus/tree/main/skills/' + name;
  document.querySelector('#yinyang-install-note').hidden = name !== 'yinyang';
  document.querySelector('#install-description').textContent = name === 'local-teacher'
    ? t('本地老师会同时安装其配套的云端老师方法。', 'Local teacher also installs its Web teacher companion.')
    : t('安装完整插件，包括入口、参考文档与包内资源。', 'Install the complete plugin, including its entrypoint, references, and resources.');
  status.textContent = '';
  const url = new URL(location.href);
  url.searchParams.set('skill', name);
  history.replaceState(null, '', url);
}
const selected = new URLSearchParams(location.search).get('skill');
if ([...chooser.options].some(option => option.value === selected)) chooser.value = selected;
chooser.addEventListener('change', update);
button.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(request.value);
    status.textContent = t('已复制。粘贴到 Codex 对话并发送即可。', 'Copied. Paste and send in a Codex chat.');
  } catch {
    request.focus();
    request.select();
    status.textContent = t('请复制已选中的指令，再粘贴到 Codex。', 'Copy the selected request and paste it into Codex.');
  }
});
update();
