import { cp, mkdir, readdir, rm, readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
// dist remains the original static source. Only generated subdirectories are disposable.
await rm('.static-assets', {recursive:true,force:true});
await mkdir('.static-assets', {recursive:true});
for (const entry of await readdir('dist')) {
  if (['client','server','.openai'].includes(entry)) continue;
  await cp(`dist/${entry}`, `.static-assets/${entry}`, {recursive:true});
}
for (const directory of ['dist/client','dist/server']) await rm(directory,{recursive:true,force:true});
const result=spawnSync(process.execPath,['scripts/run-framework.mjs','build'],{stdio:'inherit'});
if (result.status !== 0) process.exit(result.status || 1);
// Restore every original URL after framework prerendering.
await cp('.static-assets','dist/client',{recursive:true});
const configPath='dist/server/wrangler.json';
const config=JSON.parse(await readFile(configPath,'utf8'));
config.assets={...config.assets,binding:'ASSETS',run_worker_first:true};
await writeFile(configPath,JSON.stringify(config,null,2)+'\n');
