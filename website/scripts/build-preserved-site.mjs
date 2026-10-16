import { rm, readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
// Keep tracked dist/ as the content publisher's source projection. Runtime
// artifacts have no client assets: hosted asset matching can bypass the Worker.
await rm('.static-assets', {recursive:true,force:true});
for (const directory of ['dist/client','dist/server']) await rm(directory,{recursive:true,force:true});
const result=spawnSync(process.execPath,['scripts/run-framework.mjs','build'],{stdio:'inherit'});
if (result.status !== 0) process.exit(result.status || 1);
// Vinext still emits unused framework client files. Do not deploy a parallel
// asset reader alongside the complete R2 snapshot selected by the Worker.
await rm('dist/client',{recursive:true,force:true});
const configPath='dist/server/wrangler.json';
const config=JSON.parse(await readFile(configPath,'utf8'));
delete config.assets;
await writeFile(configPath,JSON.stringify(config,null,2)+'\n');
