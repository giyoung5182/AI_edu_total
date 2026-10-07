// New geometric fixtures only. No source photos or submitted videos are read.
// Run with Node.js and Playwright installed; set CHROME_PATH if needed.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const output = __dirname;
const colors = ['#2463eb','#14836e','#ae4be5','#de6927','#267a91'];
const titles = ['REFERENCE LIBRARY','REVIEW ROOM','EXPERIENCE OPS','PROPOSAL STUDIO','ESTIMATE DESK'];

function svg(index, title = 'SYNTHETIC PRODUCT') {
  const color = colors[index % colors.length];
  return `<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480" viewBox="0 0 640 480"><rect width="640" height="480" fill="#f1f5fb"/><rect x="24" y="24" width="592" height="432" rx="22" fill="white" stroke="#d5deeb"/><text x="48" y="68" font-family="Arial" font-size="22" font-weight="bold" fill="#24354d">${title}</text><text x="48" y="97" font-family="Arial" font-size="14" fill="#586d85">NEW GEOMETRIC TEST FIXTURE ${String(index).padStart(2,'0')}</text><rect x="${100 + index % 4 * 24}" y="142" width="190" height="228" rx="${index % 3 * 16 + 8}" fill="${color}"/><circle cx="413" cy="235" r="${54 + index % 5 * 5}" fill="${color}" opacity="0.35"/><path d="M360 345 L470 345 L415 285 Z" fill="${color}"/><text x="48" y="417" font-family="Arial" font-size="17" fill="#24354d">FICTIONAL SHAPES / NO REAL PRODUCT</text></svg>`;
}

(async () => {
  const options = {headless:true};
  if (process.env.CHROME_PATH) options.executablePath = process.env.CHROME_PATH;
  const browser = await chromium.launch(options);
  const page = await browser.newPage({viewport:{width:640,height:480},deviceScaleFactor:1});
  for (let i=1;i<=17;i++) {
    const source=svg(i);
    fs.writeFileSync(path.join(output,`product_${String(i).padStart(2,'0')}.svg`),source);
    await page.setContent(source);
    await page.screenshot({path:path.join(output,`product_${String(i).padStart(2,'0')}.png`)});
  }
  for (let i=0;i<5;i++) {
    const source=svg(i+31,titles[i]);
    fs.writeFileSync(path.join(output,`preview_${i}.svg`),source);
    await page.setContent(source);
    await page.screenshot({path:path.join(output,`preview_${i}.png`)});
  }
  const plan='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720"><rect width="1200" height="720" fill="#edf2fa"/><text x="40" y="52" font-size="28" font-family="Arial" fill="#24354d">FICTIONAL FLOOR PLAN / SCHEMATIC ONLY</text>'+Array.from({length:6},(_,i)=>`<rect x="${40+i%3*385}" y="${95+Math.floor(i/3)*300}" width="350" height="255" rx="18" fill="white" stroke="${colors[i%5]}" stroke-width="4"/><text x="${64+i%3*385}" y="${145+Math.floor(i/3)*300}" font-family="Arial" font-size="24" fill="#24354d">ZONE ${i+1}</text><rect x="${80+i%3*385}" y="${195+Math.floor(i/3)*300}" width="110" height="80" rx="12" fill="${colors[i%5]}" opacity="0.3"/>`).join('')+'</svg>';
  fs.writeFileSync(path.join(output,'floor-plan.svg'),plan);
  await page.setViewportSize({width:1200,height:720});
  await page.setContent(plan);
  await page.screenshot({path:path.join(output,'floor-plan.png')});
  await page.close();
  const durations=[16,18,12,14];
  const clips=await Promise.all(durations.map(async(duration,index)=>{
    const p=await browser.newPage();
    const data=await p.evaluate(async({duration,index,colors})=>{
      const canvas=document.createElement('canvas');canvas.width=640;canvas.height=360;document.body.append(canvas);
      const ctx=canvas.getContext('2d');
      const stream=canvas.captureStream(15);
      const mimeType='video/webm;codecs=vp8';
      if (!MediaRecorder.isTypeSupported(mimeType)) throw Error('VP8 MediaRecorder unsupported');
      const recorder=new MediaRecorder(stream,{mimeType,videoBitsPerSecond:240000});
      const chunks=[];recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
      const done=new Promise(resolve=>recorder.onstop=resolve);
      let start=performance.now();
      function draw(){
        const t=(performance.now()-start)/1000;
        ctx.fillStyle='#f1f5fb';ctx.fillRect(0,0,640,360);
        ctx.fillStyle='#24354d';ctx.font='bold 23px Arial';ctx.fillText(`SYNTHETIC CLIP ${index+1}`,28,44);
        ctx.font='15px Arial';ctx.fillText('NEW GEOMETRIC VIDEO / NO REAL FOOTAGE',28,73);
        ctx.fillStyle=colors[index];ctx.fillRect(35+(t*19)%350,115,125,150);
        ctx.beginPath();ctx.arc(480,190,48+18*Math.sin(t),0,Math.PI*2);ctx.fill();
        ctx.fillStyle='#24354d';ctx.font='18px Arial';ctx.fillText(`${t.toFixed(1)} s / ${duration} s`,28,330);
        if(recorder.state!=='inactive')requestAnimationFrame(draw);
      }
      recorder.start();draw();
      await new Promise(resolve=>setTimeout(resolve,duration*1000));recorder.stop();await done;
      stream.getTracks().forEach(track=>track.stop());
      const blob=new Blob(chunks,{type:'video/webm'});
      return await new Promise(resolve=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.readAsDataURL(blob);});
    },{duration,index,colors});
    fs.writeFileSync(path.join(output,`clip_${index}.webm`),Buffer.from(data.split(',')[1],'base64'));
    await p.close();
    return {file:`clip_${index}.webm`,requestedSeconds:duration,bytes:fs.statSync(path.join(output,`clip_${index}.webm`)).size};
  }));
  fs.writeFileSync(path.join(output,'generation.json'),JSON.stringify({generated:'2026-10-08',method:'new SVG screenshot and canvas MediaRecorder VP8',sourceAssetsRead:false,clips},null,2));
  await browser.close();
  console.log(JSON.stringify({png:23,svg:23,clips}));
})().catch(e=>{console.error(e);process.exitCode=1;});
