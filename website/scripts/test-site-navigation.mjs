// Run against a dist server; emulate the immutable asset URLs used by content releases.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base=process.env.SITE_URL || 'http://127.0.0.1:8768';
let prefix=`/_content/${'a'.repeat(64)}`;
const wav=Buffer.alloc(44+8000*30*2);
wav.write('RIFF');wav.writeUInt32LE(wav.length-8,4);wav.write('WAVEfmt ',8);
wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(1,22);
wav.writeUInt32LE(8000,24);wav.writeUInt32LE(16000,28);wav.writeUInt16LE(2,32);wav.writeUInt16LE(16,34);
wav.write('data',36);wav.writeUInt32LE(wav.length-44,40);
const browser=await chromium.launch({headless:true,args:['--autoplay-policy=no-user-gesture-required'],...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
try {
  const page=await browser.newPage({viewport:{width:1440,height:1100}});
  let assetDelay=0;
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.addInitScript(()=>{
    window.navigationAudio=[];
    const Original=window.Audio;
    window.Audio=function(...args){const audio=new Original(...args);window.navigationAudio.push(audio);return audio;};
  });
  await page.route('**/*',async route=>{
    const url=new URL(route.request().url());
    if(url.origin!==new URL(base).origin)return route.fulfill({status:204});
    if(['/api/music/catalog','/api/music/playback'].includes(url.pathname))return route.fulfill({json:{active:true,profileKey:'default',tracks:[{id:'probe',title:'Navigation probe',src:'/probe.wav'}]}});
    if(url.pathname==='/probe.wav')return route.fulfill({contentType:'audio/wav',body:wav});
    if(/^\/_content\/[a-f0-9]{64}\//.test(url.pathname)){
      url.pathname=url.pathname.replace(/^\/_content\/[a-f0-9]{64}/,'');
      if(assetDelay&&/\.(?:css|js)$/.test(url.pathname))await new Promise(resolve=>setTimeout(resolve,assetDelay));
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
  const navigate=async path=>{
    await page.evaluate(path=>window.siteNavigation.navigate(path,{cache:false}),path);
    await page.waitForFunction(path=>location.pathname===path&&!window.siteNavigation.navigating,path);
  };
  prefix=`/_content/${'b'.repeat(64)}`;await navigate('/philosophy/');
  // Sample every paint opportunity, not only final geometry. A removed outgoing
  // stylesheet used to turn the visible philosophy/guide grid into stacked blocks.
  await page.evaluate(()=>{
    window.navigationFrames=[];window.sampleNavigation=true;
    function sample(){
      const main=document.querySelector('main'),grid=main?.matches('.philosophy-book')?main:document.querySelector('.guide-layout');
      const canvas=document.querySelector('#flow');
      const blank=canvas&&(!canvas.getContext('2d').getImageData(0,0,1,1).data[3]||canvas.width!==canvas.getBoundingClientRect().width);
      window.navigationFrames.push({page:main?.className,grid:grid?getComputedStyle(grid).display:null,invalid:!!(grid&&getComputedStyle(grid).display!=='grid'||blank)});
      if(window.sampleNavigation)requestAnimationFrame(sample);
    }
    requestAnimationFrame(sample);
  });
  assetDelay=5500; // Exceeds both the head plugin's 3s and native update's 4s timeouts.
  prefix=`/_content/${'c'.repeat(64)}`;
  const slowVisit=navigate('/repositories/');
  await page.waitForTimeout(500);
  assert.equal(await page.locator('main.philosophy-book').evaluate(main=>getComputedStyle(main).display),'grid','Outgoing layout changed while assets were pending');
  await page.screenshot({path:'/tmp/site-navigation-pending-assets.png'});
  await slowVisit;
  assetDelay=350;
  for(const [index,path] of ['/getting-started/','/','/philosophy/','/repositories/'].entries()){
    prefix=`/_content/${(index+1).toString(16).repeat(64)}`;
    await navigate(path);
  }
  const frames=await page.evaluate(()=>{window.sampleNavigation=false;return window.navigationFrames;});
  assert.ok(frames.length>20,'No intermediate paint opportunities sampled');
  assert.deepEqual(frames.filter(frame=>frame.invalid),[],'A paint exposed an unstyled grid or uninitialized canvas');
  assert.equal(await page.locator('link[rel="preload"],link[rel="modulepreload"]').count(),0,'Temporary asset hints leaked');
  console.log(`PASS: ${frames.length} paint opportunities across cold routes; no partial layout or blank canvas.`);
  assetDelay=1000;prefix=`/_content/${'5'.repeat(64)}`;
  await page.evaluate(()=>window.siteNavigation.navigate('/getting-started/',{cache:false}));
  await page.waitForFunction(()=>window.siteNavigation.visit.meta.assetPreloads?.length>0);
  await page.evaluate(()=>{
    window.canceledVisit=window.siteNavigation.visit;
    window.canceledLinks=window.canceledVisit.meta.assetPreloads.slice();window.canceledWaiters=0;
    for(const link of window.canceledLinks){const ready=link.onload;link.onload=()=>{window.canceledWaiters++;ready();};}
  });
  assetDelay=0;prefix=`/_content/${'6'.repeat(64)}`;
  await navigate('/philosophy/');
  assert.ok(await page.evaluate(()=>canceledVisit.done&&canceledVisit.meta.assetPreloads.length===0&&canceledWaiters===canceledLinks.length&&canceledLinks.every(link=>!link.isConnected&&!link.onload&&!link.onerror)),'Aborted visit left pending asset waiters or listeners');
  console.log('PASS: rapid second navigation settles all aborted preload waiters and clears listeners.');
  assert.ok(await page.evaluate(()=>window.originalNavigationAudio.currentTime)>initialTime,'Audio playback did not advance');
  assert.ok(await page.evaluate(()=>window.navigationAudio.length===1&&window.navigationAudio[0]===window.originalNavigationAudio&&!window.originalNavigationAudio.paused),'Cold navigation interrupted audio');
  assert.deepEqual(errors,[]);
  await page.unrouteAll({behavior:'wait'});
  console.log('PASS: pinned page scripts remount and one Audio instance survives navigation/history.');
} finally {await browser.close();}
