// Run against a dist server; emulate the immutable asset URLs used by content releases.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base=process.env.SITE_URL || 'http://127.0.0.1:8768';
const prefix=`/_content/${'a'.repeat(64)}`;
const wav=Buffer.alloc(44+8000*30*2);
wav.write('RIFF');wav.writeUInt32LE(wav.length-8,4);wav.write('WAVEfmt ',8);
wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(1,22);
wav.writeUInt32LE(8000,24);wav.writeUInt32LE(16000,28);wav.writeUInt16LE(2,32);wav.writeUInt16LE(16,34);
wav.write('data',36);wav.writeUInt32LE(wav.length-44,40);
const browser=await chromium.launch({headless:true,args:['--autoplay-policy=no-user-gesture-required'],...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
try {
  const page=await browser.newPage({viewport:{width:1440,height:1100}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.addInitScript(()=>{
    window.navigationAudio=[];
    const Original=window.Audio;
    window.Audio=function(...args){const audio=new Original(...args);window.navigationAudio.push(audio);return audio;};
  });
  await page.route('**/*',async route=>{
    const url=new URL(route.request().url());
    if(url.origin!==new URL(base).origin)return route.fulfill({status:204});
    if(url.pathname==='/api/music/catalog')return route.fulfill({json:{active:true,tracks:[{id:'probe',title:'Navigation probe',src:'/probe.wav'}]}});
    if(url.pathname==='/probe.wav')return route.fulfill({contentType:'audio/wav',body:wav});
    if(url.pathname.startsWith(prefix+'/')){
      url.pathname=url.pathname.slice(prefix.length);
      return route.fulfill({response:await route.fetch({url:url.href})});
    }
    const response=await route.fetch();
    if((response.headers()['content-type']||'').includes('text/html')){
      const body=(await response.text()).replace(/(src|href)="(\/[^"#?]*\.(?:js|css|svg|jpg|png)(?:\?[^"#]*)?)"/g,`$1="${prefix}$2"`);
      return route.fulfill({response,body});
    }
    return route.fulfill({response});
  });
  await page.goto(base+'/repositories/');
  await page.waitForFunction(()=>window.siteNavigation&&window.navigationAudio.length===1);
  await page.evaluate(()=>{window.originalNavigationAudio=window.navigationAudio[0];});
  await page.waitForFunction(()=>!window.originalNavigationAudio.paused&&window.originalNavigationAudio.currentTime>0);
  const initialTime=await page.evaluate(()=>window.originalNavigationAudio.currentTime);
  async function checkHome(label){
    await page.waitForSelector('#flow');
    await page.waitForTimeout(150);
    const state=await page.locator('#flow').evaluate(canvas=>{
      const box=canvas.getBoundingClientRect();
      const data=canvas.getContext('2d').getImageData(0,0,canvas.width,canvas.height).data;
      let opaque=0;for(let i=3;i<data.length;i+=4)if(data[i])opaque++;
      return {width:canvas.width,height:canvas.height,boxWidth:box.width,boxHeight:box.height,opaque};
    });
    assert.ok(state.opaque>state.width*state.height*.95,`${label}: blank canvas ${JSON.stringify(state)}`);
    assert.equal(state.width,state.boxWidth,`${label}: wrong canvas width`);
    assert.equal(state.height,state.boxHeight,`${label}: wrong canvas height`);
    assert.ok(await page.evaluate(()=>window.navigationAudio.length===1&&window.navigationAudio[0]===window.originalNavigationAudio),`${label}: audio replaced`);
    assert.ok(await page.evaluate(()=>!window.originalNavigationAudio.paused),`${label}: audio paused`);
    console.log(label,state);
  }
  for(let i=0;i<3;i++){
    await page.locator('header a[href="/"]').first().click();
    await checkHome(`home ${i+1}`);
    await page.locator('header a[href="/repositories/"]').click();
    await page.waitForSelector('#flow',{state:'detached'});
    await page.goBack();await checkHome(`back ${i+1}`);
    await page.goForward();await page.waitForSelector('#flow',{state:'detached'});
  }
  await page.locator('header a[href="/"]').first().click();await checkHome('final');
  await page.screenshot({path:process.env.NAV_SCREENSHOT || '/tmp/site-navigation-after.png'});
  assert.ok(await page.evaluate(()=>window.originalNavigationAudio.currentTime)>initialTime,'Audio playback did not advance');
  assert.deepEqual(errors,[]);
  console.log('PASS: pinned page scripts remount and one Audio instance survives navigation/history.');
} finally {await browser.close();}
