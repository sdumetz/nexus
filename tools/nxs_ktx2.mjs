#!/usr/bin/env node
// Rewrite the node textures of a .nxs file as KTX2 supercompressed images.
// Reads every JPEG node texture, transcodes it with the `ktx` CLI, and writes
// a new .nxs with the texture table offsets and data tail updated.
//
// Usage: node nxs_ktx2.mjs <input.nxs> <output.nxs> [--encode basis-lz|uastc] [--quality N]

import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const PADDING = 256;
const HEADER_SIZE = 88;
const NODE_SIZE = 44;
const PATCH_SIZE = 12;
const TEXTURE_SIZE = 68;

function pad(n) { return Math.ceil(n / PADDING) * PADDING; }

function parseArgs(argv) {
	const pos = [];
	const opts = { encode: 'basis-lz', quality: null };
	for (let i = 0; i < argv.length; i++) {
		const a = argv[i];
		if (a === '--encode') opts.encode = argv[++i];
		else if (a === '--quality') opts.quality = argv[++i];
		else pos.push(a);
	}
	if (pos.length < 2) {
		console.error('Usage: node nxs_ktx2.mjs <input.nxs> <output.nxs> [--encode basis-lz|uastc] [--quality N]');
		process.exit(1);
	}
	opts.input = pos[0];
	opts.output = pos[1];
	return opts;
}

function readHeader(buf) {
	if (buf.readUInt32LE(0) !== 0x4e787320) throw new Error('not a .nxs file (bad magic)');
	const flags = buf.readUInt32LE(56);
	return {
		flags,
		nNodes: buf.readUInt32LE(60),
		nPatches: buf.readUInt32LE(64),
		nTextures: buf.readUInt32LE(68),
	};
}

function ktxEncode(jpeg, opts, tmp) {
	const inFile = join(tmp, 'in.jpg');
	const outFile = join(tmp, 'out.ktx2');
	writeFileSync(inFile, jpeg);
	const args = [
		'create',
		'--format', 'R8G8B8A8_SRGB',
		'--encode', opts.encode,
		'--generate-mipmap',
		// store bottom-up so the data matches nexus' UNPACK_FLIP_Y_WEBGL=true jpeg path
		'--convert-texcoord-origin', 'bottom-left',
	];
	if (opts.encode === 'uastc') args.push('--zstd', '18');
	if (opts.quality) args.push('--qlevel', opts.quality);
	args.push(inFile, outFile);
	execFileSync('ktx', args, { stdio: ['ignore', 'ignore', 'inherit'] });
	return readFileSync(outFile);
}

function main() {
	const opts = parseArgs(process.argv.slice(2));
	const buf = readFileSync(opts.input);
	const h = readHeader(buf);
	if (h.flags & 0x8) throw new Error('deepzoom .nxs not supported by this tool');
	if (h.nTextures === 0) throw new Error('file has no textures');

	const tableOff = HEADER_SIZE + h.nNodes * NODE_SIZE + h.nPatches * PATCH_SIZE;
	// nTextures entries; the last is a sentinel pointing at the end of the data.
	const offs = [];
	for (let i = 0; i < h.nTextures; i++)
		offs.push(buf.readUInt32LE(tableOff + i * TEXTURE_SIZE) * PADDING);

	const dataStart = offs[0];
	const head = Buffer.from(buf.subarray(0, dataStart)); // header + index + geometry, kept verbatim

	const tmp = mkdtempSync(join(tmpdir(), 'nxsktx-'));
	const blobs = [];
	const newOffs = [dataStart];
	let cursor = dataStart;
	try {
		for (let i = 0; i < h.nTextures - 1; i++) {
			const jpeg = buf.subarray(offs[i], offs[i + 1]);
			const ktx = ktxEncode(jpeg, opts, tmp);
			const padded = Buffer.alloc(pad(ktx.length));
			ktx.copy(padded);
			blobs.push(padded);
			cursor += padded.length;
			newOffs.push(cursor); // becomes offset of texture i+1 (sentinel on last iteration)
			process.stderr.write(`  texture ${i + 1}/${h.nTextures - 1}: ${jpeg.length} -> ${ktx.length} bytes\n`);
		}
	} finally {
		rmSync(tmp, { recursive: true, force: true });
	}

	for (let i = 0; i < h.nTextures; i++)
		head.writeUInt32LE(newOffs[i] / PADDING, tableOff + i * TEXTURE_SIZE);

	writeFileSync(opts.output, Buffer.concat([head, ...blobs]));
	console.error(`wrote ${opts.output} (${cursor} bytes, ${h.nTextures - 1} textures as ${opts.encode})`);
}

main();
