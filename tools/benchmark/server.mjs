import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const benchmark = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(benchmark, '../..');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.gltf': 'model/gltf+json', '.jpg': 'image/jpeg', '.png': 'image/png' };

export async function startServer({ models, three, source }) {
  const roots = { '/benchmark/': benchmark, '/runtime/': path.join(repo, 'nexus3d/src'),
    '/codecs/': path.join(repo, 'nexus3d/dist'), '/three/': three,
    ...(source ? { '/source/': path.dirname(source) } : {}) };
  const server = http.createServer(async (req, res) => {
    try {
      const url = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      let filename;
      const id = /^\/models\/(\d+)\.nxs$/.exec(url);
      if (id) filename = models[Number(id[1])]?.path;
      else for (const [prefix, root] of Object.entries(roots)) {
        if (!url.startsWith(prefix)) continue;
        const candidate = await fs.promises.realpath(path.resolve(root, url.slice(prefix.length)));
        const realRoot = await fs.promises.realpath(root);
        if (candidate.startsWith(realRoot + path.sep)) filename = candidate;
        break;
      }
      if (!filename) { res.writeHead(404); res.end(); return; }
      const stat = await fs.promises.stat(filename);
      if (!stat.isFile()) { res.writeHead(404); res.end(); return; }
      let start = 0, end = stat.size - 1, status = 200;
      if (req.headers.range) {
        const range = /^bytes=(\d+)-(\d*)$/.exec(req.headers.range);
        if (!range) { res.writeHead(416); res.end(); return; }
        start = Number(range[1]); end = range[2] ? Number(range[2]) : end;
        if (start > end || end >= stat.size) { res.writeHead(416); res.end(); return; }
        status = 206;
      }
      res.writeHead(status, { 'Content-Type': types[path.extname(filename)] ?? 'application/octet-stream',
        'Content-Length': end - start + 1, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store',
        ...(status === 206 ? { 'Content-Range': `bytes ${start}-${end}/${stat.size}` } : {}) });
      const stream = fs.createReadStream(filename, { start, end });
      stream.on('error', () => res.destroy()); res.on('close', () => stream.destroy()); stream.pipe(res);
    } catch { res.writeHead(404); res.end(); }
  });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  return { url: `http://127.0.0.1:${server.address().port}`,
    close: () => new Promise(resolve => server.close(resolve)) };
}
