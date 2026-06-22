#!/usr/bin/env node
// Minimal static file server with HTTP Range support (nexus streams via byte ranges).
import { createServer } from 'node:http';
import { stat, open } from 'node:fs/promises';
import { join, extname, normalize } from 'node:path';

const root = process.argv[2] || '.';
const port = Number(process.argv[3] || 8080);
const types = {
	'.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
	'.json': 'application/json', '.wasm': 'application/wasm',
	'.nxs': 'application/octet-stream', '.nxz': 'application/octet-stream',
	'.jpg': 'image/jpeg', '.ktx2': 'image/ktx2',
};

createServer(async (req, res) => {
	try {
		const url = decodeURIComponent(req.url.split('?')[0]);
		const path = join(root, normalize(url).replace(/^(\.\.[/\\])+/, ''));
		const st = await stat(path);
		const file = path + (st.isDirectory() ? '/index.html' : '');
		const size = (await stat(file)).size;
		const type = types[extname(file)] || 'application/octet-stream';
		const fd = await open(file, 'r');
		res.setHeader('Accept-Ranges', 'bytes');
		res.setHeader('Content-Type', type);
		const range = req.headers.range;
		if (range) {
			const m = /bytes=(\d+)-(\d*)/.exec(range);
			const start = Number(m[1]);
			const end = m[2] ? Number(m[2]) : size - 1;
			res.writeHead(206, {
				'Content-Range': `bytes ${start}-${end}/${size}`,
				'Content-Length': end - start + 1,
			});
			fd.createReadStream({ start, end }).pipe(res).on('close', () => fd.close());
		} else {
			res.writeHead(200, { 'Content-Length': size });
			fd.createReadStream().pipe(res).on('close', () => fd.close());
		}
	} catch (e) {
		res.writeHead(404).end(String(e));
	}
}).listen(port, () => console.error(`serving ${root} at http://localhost:${port}`));
