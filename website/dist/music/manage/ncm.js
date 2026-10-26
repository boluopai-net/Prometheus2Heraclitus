import {ecb} from './vendor/aes.js';

// NCM container compatibility follows taurusxin/ncmdump (MIT).
// These public format constants are not account credentials.
const coreKey=new Uint8Array([0x68,0x7a,0x48,0x52,0x41,0x6d,0x73,0x6f,0x35,0x6b,0x49,0x6e,0x62,0x61,0x78,0x57]);
const metadataKey=new Uint8Array([0x23,0x31,0x34,0x6c,0x6a,0x6b,0x5f,0x21,0x5c,0x5d,0x26,0x30,0x55,0x3c,0x27,0x28]);
const utf8=new TextDecoder();
const invalid=()=>{throw Error('这个 NCM 文件无法读取，请重新下载后再试。');};

export async function prepareAudio(file) {
  const name=file.name.replace(/\.[^.]+$/,'');
  const magic=new Uint8Array(await file.slice(0,8).arrayBuffer());
  if(utf8.decode(magic)!=='CTENFDAM') {
    if(/\.ncm$/i.test(file.name))invalid();
    return {size:file.size,title:name,artist:'',slice:async(start,end)=>file.slice(start,end)};
  }
  let offset=10;
  async function read(length) {
    if(!Number.isSafeInteger(length)||length<0||offset+length>file.size)invalid();
    const bytes=new Uint8Array(await file.slice(offset,offset+length).arrayBuffer());offset+=length;return bytes;
  }
  async function length(){const bytes=await read(4);return new DataView(bytes.buffer).getUint32(0,true);}
  const keyLength=await length();if(!keyLength||keyLength>4096)invalid();
  const encryptedKey=await read(keyLength);for(let i=0;i<encryptedKey.length;i++)encryptedKey[i]^=0x64;
  let decodedKey;try{decodedKey=ecb(coreKey).decrypt(encryptedKey);}catch{invalid();}
  if(utf8.decode(decodedKey.subarray(0,17))!=='neteasecloudmusic')invalid();
  const key=decodedKey.subarray(17);if(!key.length)invalid();
  const box=Uint8Array.from({length:256},(_,i)=>i);let last=0,keyOffset=0;
  for(let i=0;i<256;i++){const value=box[i],next=(value+last+key[keyOffset])&255;keyOffset=(keyOffset+1)%key.length;box[i]=box[next];box[next]=value;last=next;}
  const stream=Uint8Array.from({length:256},(_,i)=>{const j=(i+1)&255;return box[(box[j]+box[(box[j]+j)&255])&255];});
  const metadataLength=await length();if(metadataLength>1024*1024)invalid();
  const encryptedMetadata=await read(metadataLength);let metadata={};
  if(metadataLength){
    try{
      for(let i=0;i<encryptedMetadata.length;i++)encryptedMetadata[i]^=0x63;
      const encoded=utf8.decode(encryptedMetadata).slice(22);
      const bytes=Uint8Array.from(atob(encoded),c=>c.charCodeAt(0));
      metadata=JSON.parse(utf8.decode(ecb(metadataKey).decrypt(bytes)).slice(6));
    }catch{/* Audio remains usable when optional title metadata is missing. */}
  }
  await read(5);
  const coverFrameLength=await length(),coverLength=await length();
  if(coverLength>coverFrameLength||offset+coverFrameLength>=file.size)invalid();
  offset+=coverFrameLength;
  const audioStart=offset,size=file.size-audioStart;
  async function slice(start,end){
    const bytes=new Uint8Array(await file.slice(audioStart+start,audioStart+Math.min(end,size)).arrayBuffer());
    for(let i=0;i<bytes.length;i++)bytes[i]^=stream[(start+i)&255];
    return new Blob([bytes]);
  }
  const head=new Uint8Array(await (await slice(0,12)).arrayBuffer());
  const signature=utf8.decode(head);
  if(!signature.startsWith('fLaC')&&!signature.startsWith('ID3')&&!(head[0]===255&&(head[1]&224)===224))invalid();
  const title=typeof metadata.musicName==='string'?metadata.musicName:name;
  const artist=Array.isArray(metadata.artist)?metadata.artist.map(a=>Array.isArray(a)?a[0]:'').filter(a=>typeof a==='string').join(' / '):'';
  return {size,title,artist,slice,converted:true};
}
