#!/usr/bin/env node
import fs from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { startServer } from './server.mjs';
import { launch } from './chrome.mjs';
import { writeReport } from './report.mjs';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const args = process.argv.slice(2), models = [];
let out = 'benchmark-results', three, source, poses;
let loadingMode = 'traverse';
let views = [6, 2.5, 1.2, 0.6], taus = [2], width = 1280, height = 800, chrome = '/usr/bin/chromium', timeoutMs = 120000;
for (let i = 0; i < args.length; ++i) {
  const key = args[i], value = args[++i];
  if (!value) throw new Error(`Missing value for ${key}`);
  if (key === '--model') {
    const equal = value.indexOf('=');
    if (equal < 1) throw new Error('--model expects label=/path/to/model.nxs');
    const label = value.slice(0, equal);
    if (label === 'source' || !/^[a-zA-Z0-9_-]+$/.test(label) || models.some(m => m.label === label)) throw new Error('Model labels must be unique safe filenames; source is reserved');
    models.push({ label, path: path.resolve(value.slice(equal + 1)) });
  } else if (key === '--out') out = value;
  else if (key === '--three') three = path.resolve(value);
  else if (key === '--source') source = path.resolve(value);
  else if (key === '--poses') poses = JSON.parse(await fs.readFile(value, 'utf8'));
  else if (key === '--views') views = value.split(',').map(Number);
  else if (key === '--taus') taus = value.split(',').map(Number);
  else if (key === '--width') width = Number(value);
  else if (key === '--height') height = Number(value);
  else if (key === '--chrome') chrome = value;
  else if (key === '--timeout-ms') timeoutMs = Number(value);
  else if (key === '--loading-mode') loadingMode = value;
  else throw new Error(`Unknown option ${key}`);
}
if (!models.length) throw new Error('Supply at least one --model label=file.nxs (the first is the comparison baseline)');
if (!['render', 'traverse'].includes(loadingMode)) throw new Error('--loading-mode must be render or traverse');
if (![...views, ...taus, width, height, timeoutMs].every(n => Number.isFinite(n) && n > 0)) throw new Error('Dimensions, views, taus, and timeout must be positive');
if (!three) for (const candidate of [path.join(repo, 'node_modules/three'), path.join(repo, 'nexus3d/node_modules/three'), path.resolve(repo, '../not-voyager/experiments/LOD/node_modules/three')]) {
  try { await fs.access(path.join(candidate, 'build/three.module.js')); three = candidate; break; } catch {}
}
if (!three) throw new Error('Supply --three /path/to/node_modules/three');
const readHeader = async filename => {
  const file = await fs.open(filename, 'r'), bytes = Buffer.alloc(88);
  try { if ((await file.read(bytes, 0, 88, 0)).bytesRead !== 88 || bytes.readUInt32LE(0) !== 0x4e787320) throw new Error('Invalid Nexus header'); }
  finally { await file.close(); }
  return { center: [72, 76, 80].map(offset => bytes.readFloatLE(offset)), radius: bytes.readFloatLE(84) };
};
const sphere = await readHeader(models[0].path);
if (!Number.isFinite(sphere.radius) || sphere.radius <= 0) throw new Error('Invalid baseline sphere');
const direction = [0.35, 0.25, 1], length = Math.hypot(...direction);
poses ??= views.map(distance => ({ distanceRadii: distance,
  position: sphere.center.map((c, i) => c + direction[i] / length * distance * sphere.radius), target: sphere.center,
  near: sphere.radius / 1000, far: sphere.radius * 100 }));
if (!Array.isArray(poses) || !poses.length || poses.some(p =>
  ![p.position, p.target, p.up ?? [0, 1, 0]].every(a => Array.isArray(a) && a.length === 3 && a.every(Number.isFinite))
  || !Number.isFinite(p.near) || !Number.isFinite(p.far) || p.near <= 0 || p.far <= p.near))
  throw new Error('Poses require finite position/target/up vectors and valid near/far planes');
out = path.resolve(out); await fs.mkdir(out, { recursive: true });
const report = { created: new Date().toISOString(), viewport: { width, height }, poses, taus,
  accounting: 'Logical live Nexus WebGL buffers and RGBA8 textures including every generated mip; excludes driver overhead, CPU heap, and renderer shell allocations.',
  models: [], runs: [], comparisons: [] };
for (const model of models) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(model.path)) hash.update(chunk);
  report.models.push({ ...model, fileBytes: (await fs.stat(model.path)).size, sha256: hash.digest('hex') });
}
const server = await startServer({ models, three, source });
let browser;
const images = new Map(), logs = [];
try {
  browser = await launch({ binary: chrome, width, height });
  report.browser = await browser.send('Browser.getVersion');
  report.threePackageVersion = JSON.parse(await fs.readFile(path.join(three, 'package.json'), 'utf8')).version;
  let fetchedHttpBytes = 0, modelRequests = 0;
  const requests = new Set();
  browser.on(message => {
    if (message.method === 'Network.requestWillBeSent' && message.params.request.url.includes('/models/')) { requests.add(message.params.requestId); modelRequests++; }
    if (message.method === 'Network.loadingFinished' && requests.delete(message.params.requestId)) fetchedHttpBytes += message.params.encodedDataLength;
    if (message.method === 'Runtime.exceptionThrown') logs.push(message.params.exceptionDetails.exception?.description ?? message.params.exceptionDetails.text);
    if (message.method === 'Runtime.consoleAPICalled' && message.params.type === 'error')
      logs.push(message.params.args.map(a => a.value ?? a.description).join(' '));
  });
  const jobs = [];
  for (let view = 0; view < poses.length; ++view) {
    if (source) jobs.push({ label: 'source', view, kind: 'source', url: '/source/' + encodeURIComponent(path.basename(source)), tau: 0 });
    for (const tau of taus) for (let id = 0; id < models.length; ++id)
      jobs.push({ label: models[id].label, id, view, tau, kind: 'nexus', url: `/models/${id}.nxs` });
  }
  for (const job of jobs) {
    // A fresh document/context clears the singleton cache and any leaked GPU state.
    await browser.goto(`${server.url}/benchmark/page.html?job=${report.runs.length}`);
    fetchedHttpBytes = modelRequests = 0; logs.length = 0; requests.clear();
    const options = { url: job.url, kind: job.kind, tau: job.tau, pose: poses[job.view], timeoutMs, loadingMode };
    const result = await browser.evaluate(`bench.run(${JSON.stringify(options)})`);
    const row = { label: job.label, view: job.view, tau: job.tau, ...result, fetchedHttpBytes, modelRequests, logs: [...logs] };
    if (logs.length) throw new Error(`Browser errors: ${logs.join('\n')}`);
    for (const mode of ['textured', 'shaded']) {
      const stem = `${job.label}-v${job.view}-t${job.tau}-${mode}`;
      const png = await browser.evaluate(`bench.capture(${JSON.stringify(mode)})`);
      await fs.writeFile(path.join(out, `${stem}.png`), Buffer.from(png, 'base64'));
      images.set(`${job.label}/${job.view}/${job.tau}/${mode}`, png);
      const references = [];
      if (job.kind !== 'source') {
        for (let id = 0; id < job.id; ++id) references.push({ label: models[id].label, tau: job.tau });
        if (source) references.push({ label: 'source', tau: 0 });
      }
      for (const reference of references) {
        const previous = images.get(`${reference.label}/${job.view}/${reference.tau}/${mode}`);
        const comparison = await browser.evaluate(`bench.compare(${JSON.stringify(previous)},${JSON.stringify(mode)})`);
        const { heatPng, ...metrics } = comparison;
        const diffName = `${stem}-vs-${reference.label}-diff.png`;
        await fs.writeFile(path.join(out, diffName), Buffer.from(heatPng, 'base64'));
        report.comparisons.push({ label: job.label, reference: reference.label, view: job.view, tau: job.tau, mode, ...metrics, diff: diffName });
      }
    }
    report.runs.push(row);
    await fs.writeFile(path.join(out, 'results.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(`${job.label} view ${job.view} tau ${job.tau}: ${result.source ? 'reference captured' : `${result.residentNodes}/${result.totalNodes} nodes, ${(result.gpuBytes / 1048576).toFixed(3)} MiB audited GPU cache`}`);
  }
} finally { await browser?.close(); await server.close(); }
await writeReport(report, out);
console.log(`Results: ${path.join(out, 'results.json')}`);
