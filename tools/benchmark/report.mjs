import fs from 'node:fs/promises';
import path from 'node:path';

export async function writeReport(report, out) {
const rows = report.runs.filter(r => !r.source).map(r =>
  `| ${r.label} | ${r.view} | ${r.tau} | ${r.residentNodes} | ${(r.geometryBytes / 1048576).toFixed(3)} | ${(r.textureBytes / 1048576).toFixed(3)} | ${(r.gpuBytes / 1048576).toFixed(3)} | ${(r.legacyEstimatedCacheBytes / 1048576).toFixed(3)} |`);
const comparisons = report.comparisons.map(c =>
  `| ${c.label} / ${c.reference} | ${c.view} | ${c.tau} | ${c.mode} | ${c.identical ? 'identical' : c.psnrDb?.toFixed(2)} | ${(100 * c.changedPixelsOver8Fraction).toFixed(3)}% | ${c.silhouetteIoU.toFixed(5)} |`);
await fs.writeFile(path.join(out, 'summary.md'), `# Nexus cache and image comparison\n\nGPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.\n\n| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |\n|---|---:|---:|---:|---:|---:|---:|---:|\n${rows.join('\n')}\n\nPixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.\n\n| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |\n|---|---:|---:|---|---:|---:|---:|\n${comparisons.join('\n')}\n\n[Image gallery](gallery.html) · [Full measurements](results.json)\n`);
const pictures = report.runs.flatMap(r => ['textured', 'shaded'].map(mode => {
  const stem = `${r.label}-v${r.view}-t${r.tau}-${mode}`;
  return `<figure><a href="${stem}.png"><img loading="lazy" src="${stem}.png"></a><figcaption>${stem}</figcaption></figure>`;
}));
await fs.writeFile(path.join(out, 'gallery.html'), `<!doctype html><meta charset="utf-8"><title>Nexus benchmark images</title><style>body{font:16px sans-serif;background:#202326;color:#eee}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:16px}figure{margin:0}img{width:100%}figcaption{padding:8px}</style><h1>Nexus benchmark images</h1><p><a href="summary.md">Measurements</a> · <a href="results.json">JSON</a>. Difference images amplify absolute channel differences by 4.</p><main>${pictures.join('')}${report.comparisons.map(c => `<figure><a href="${c.diff}"><img loading="lazy" src="${c.diff}"></a><figcaption>${c.diff}</figcaption></figure>`).join('')}</main>`);
}
