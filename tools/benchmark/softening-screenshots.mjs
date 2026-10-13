// Present existing benchmark captures as HTML, then screenshot the comparison.
// Zooms use the same source pixels and nearest-neighbor magnification; no rerender.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { launch } from './chrome.mjs';
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const out = path.join(repo, 'doc/measurements/softening-comparisons');
await fs.mkdir(out, { recursive: true });
const cases = [
  { id:'lion-error-metric', title:'Lion sculpture — revised error metric, 0.5 px',
    root:'isti-reconstruction-10/screenshots/RWT139', left:'round1', right:'reconstruction', tau:'0.5',
    leftLabel:'Round 1: footprint error', rightLabel:'Round 4: reconstruction error', x:520,y:255,
    note:'Same texture payloads; revised error selects fewer nodes. Inspect the mane and face.' },
  { id:'rock-finer-sizing', title:'Mossy rock — finer texture sizing, 0.1 px',
    root:'isti-fine-10/screenshots/RWT76', left:'round2', right:'fine', tau:'0.1',
    leftLabel:'Round 2: halving', rightLabel:'Round 3: multiples of four', x:520,y:300,
    note:'Same geometry selection; only texture dimensions change. Inspect surface grain and moss.' },
  { id:'cake-finer-sizing', title:'Cake — finer texture sizing, 2 px',
    root:'isti-fine-10/screenshots/RWT319', left:'round2', right:'fine', tau:'2',
    leftLabel:'Round 2: halving', rightLabel:'Round 3: multiples of four', x:555,y:350,
    note:'Same geometry selection; only texture dimensions change. Inspect crumb and chocolate edges.' },
];
const browser = await launch({width:1280,height:1100});
try {
  for(const c of cases) {
    const filenames = [c.left,c.right].map(label=>`${label}-v0-t${c.tau}-textured.png`);
    const urls = filenames.map(file=>`../${c.root}/${file}`);
    const panels = c.leftLabel ? [c.leftLabel,c.rightLabel].map((label,i)=>`<section><h2>${label}</h2><a href="${urls[i]}"><img class="whole" src="${urls[i]}"></a><h3>Identical 160 × 120 px crop, magnified 4×</h3><div class="crop"><img src="${urls[i]}" style="left:${-c.x*4}px;top:${-c.y*4}px"></div></section>`).join('') : '';
    const html = `<!doctype html><meta charset="utf-8"><title>${c.title}</title><style>*{box-sizing:border-box}body{margin:0;width:1280px;background:#202326;color:#f0f0f0;font-family:Arial,sans-serif}header{padding:16px 20px;height:88px}h1{font-size:24px;margin:0 0 8px}p{margin:0;font-size:17px}main{display:grid;grid-template-columns:640px 640px}section{margin:0}h2{height:38px;margin:0;padding:9px 12px;font-size:18px;background:#30353a}h3{height:36px;margin:0;padding:9px 12px;font-size:16px;background:#30353a}.whole{display:block;width:640px;height:400px}.crop{position:relative;width:640px;height:480px;overflow:hidden}.crop img{position:absolute;width:5120px;height:3200px;max-width:none;image-rendering:pixelated}footer{height:40px;padding:12px;font-size:14px}a{color:#b6d9ff}</style><header><h1>${c.title}</h1><p>${c.note}</p></header><main>${panels}</main><footer>Top: complete fixed-view capture at 50% scale. Bottom: original pixels at 4×; no new render or sharpening. Left = baseline; right = experiment.</footer>`;
    await fs.writeFile(path.join(out, `${c.id}.html`),html);
    let embedded = html;
    for(let i=0;i<urls.length;i++) {
      const bytes=await fs.readFile(path.join(repo,'doc/measurements',c.root,filenames[i]));
      embedded=embedded.replaceAll(`src="${urls[i]}"`,`src="data:image/png;base64,${bytes.toString('base64')}"`);
    }
    const frame = (await browser.send('Page.getFrameTree')).frameTree.frame.id;
    await browser.send('Page.setDocumentContent',{frameId:frame,html:embedded});
    await browser.evaluate('Promise.all([...document.images].map(image=>image.decode()))');
    const height=await browser.evaluate('document.body.scrollHeight');
    await browser.send('Emulation.setDeviceMetricsOverride',{width:1280,height,deviceScaleFactor:1,mobile:false});
    const capture=await browser.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});
    await fs.writeFile(path.join(out,`${c.id}.png`),Buffer.from(capture.data,'base64'));
    console.log(c.id);
  }
} finally { await browser.close(); }
await fs.writeFile(path.join(out,'index.html'),`<!doctype html><meta charset="utf-8"><title>Texture softening comparisons</title><style>body{font:18px sans-serif;background:#202326;color:#eee}a{color:#b6d9ff}img{display:block;width:100%;max-width:1280px;margin:16px 0}</style><h1>Texture softening comparisons</h1><p>Each sheet shows the complete original view, followed by matching 4× magnified crops. Left: baseline. Right: experiment.</p>${cases.map(c=>`<h2>${c.title}</h2><p><a href="${c.id}.html">Interactive page and original captures</a> · <a href="${c.id}.png">Full-size comparison sheet</a></p><img src="${c.id}.png">`).join('')}`);
