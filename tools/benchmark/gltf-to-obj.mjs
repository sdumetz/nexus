#!/usr/bin/env node
// Adapted from not-voyager/experiments/LOD/tools/bench/gltf2obj.mjs.
// Uncompressed glTF with external buffers/images -> OBJ + MTL, for
// nxsbuild (v3 reads PLY/OBJ/STL only). Every TRIANGLES primitive of every mesh node, world transforms baked,
// one `usemtl` per material; the MTL points at the source's base colour images (copied next to the OBJ).
//   node tools/benchmark/gltf-to-obj.mjs source.gltf /tmp/model/model.obj
import fs from "node:fs";
import path from "node:path";

const [src, dst] = process.argv.slice(2);
const dir = path.dirname(src), outDir = path.dirname(dst);
fs.mkdirSync(outDir, { recursive: true });
const gltf = JSON.parse(fs.readFileSync(src, "utf8"));
const buffers = gltf.buffers.map((b) => (b.uri ? fs.readFileSync(path.join(dir, decodeURIComponent(b.uri))) : null));

const COMP = { 5120: [Int8Array, 127], 5121: [Uint8Array, 255], 5122: [Int16Array, 32767], 5123: [Uint16Array, 65535], 5125: [Uint32Array, 0], 5126: [Float32Array, 0] };
const NCOMP = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 };
function read(i) {
  const a = gltf.accessors[i], bv = gltf.bufferViews[a.bufferView];
  const [T, norm] = COMP[a.componentType], n = NCOMP[a.type];
  const buf = buffers[bv.buffer];
  const stride = bv.byteStride || n * T.BYTES_PER_ELEMENT;
  const base = buf.byteOffset + (bv.byteOffset ?? 0) + (a.byteOffset ?? 0);
  const out = new Float64Array(a.count * n);
  const dv = new DataView(buf.buffer);
  const get = { 5120: "getInt8", 5121: "getUint8", 5122: "getInt16", 5123: "getUint16", 5125: "getUint32", 5126: "getFloat32" }[a.componentType];
  for (let k = 0; k < a.count; k++)
    for (let c = 0; c < n; c++) {
      let v = dv[get](base + k * stride + c * T.BYTES_PER_ELEMENT, true);
      if (a.normalized && norm) v = Math.max(v / norm, -1);
      out[k * n + c] = v;
    }
  return out;
}

const mul = (a, b) => { const r = new Array(16).fill(0); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) for (let k = 0; k < 4; k++) r[j * 4 + i] += a[k * 4 + i] * b[j * 4 + k]; return r; };
function local(n) {
  if (n.matrix) return n.matrix;
  const [x, y, z, w] = n.rotation ?? [0, 0, 0, 1], [sx, sy, sz] = n.scale ?? [1, 1, 1], [tx, ty, tz] = n.translation ?? [0, 0, 0];
  return [
    (1 - 2 * (y * y + z * z)) * sx, 2 * (x * y + z * w) * sx, 2 * (x * z - y * w) * sx, 0,
    2 * (x * y - z * w) * sy, (1 - 2 * (x * x + z * z)) * sy, 2 * (y * z + x * w) * sy, 0,
    2 * (x * z + y * w) * sz, 2 * (y * z - x * w) * sz, (1 - 2 * (x * x + y * y)) * sz, 0, tx, ty, tz, 1];
}
const items = [];
const walk = (i, parent) => {
  const n = gltf.nodes[i], m = mul(parent, local(n));
  if (n.mesh !== undefined) items.push([n.mesh, m]);
  (n.children ?? []).forEach((c) => walk(c, m));
};
const I = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
(gltf.scenes[gltf.scene ?? 0].nodes).forEach((r) => walk(r, I));

// materials -> MTL
const imgFile = (tex) => {
  const img = gltf.images[gltf.textures[tex.index].source];
  const name = decodeURIComponent(img.uri);
  if (!fs.existsSync(path.join(outDir, path.basename(name)))) fs.copyFileSync(path.join(dir, name), path.join(outDir, path.basename(name)));
  return path.basename(name);
};
const mtlName = path.basename(dst).replace(/\.obj$/, ".mtl");
let mtl = "";
(gltf.materials ?? []).forEach((m, i) => {
  const pbr = m.pbrMetallicRoughness ?? {};
  const c = pbr.baseColorFactor ?? [1, 1, 1, 1];
  mtl += `newmtl m${i}\nKd ${c[0]} ${c[1]} ${c[2]}\n`;
  if (pbr.baseColorTexture) mtl += `map_Kd ${imgFile(pbr.baseColorTexture)}\n`;
  mtl += "\n";
});
fs.writeFileSync(path.join(outDir, mtlName), mtl);

const fd = fs.openSync(dst, "w");
let chunk = [];
const flush = (force) => { if (force || chunk.length > 20000) { fs.writeSync(fd, chunk.join("")); chunk = []; } };
chunk.push(`mtllib ${mtlName}\n`);
let vbase = 1, tris = 0;
for (const [mi, m] of items) {
  for (const p of gltf.meshes[mi].primitives) {
    if ((p.mode ?? 4) !== 4) continue;
    const pos = read(p.attributes.POSITION), n = pos.length / 3;
    const nor = p.attributes.NORMAL !== undefined ? read(p.attributes.NORMAL) : null;
    const uv = p.attributes.TEXCOORD_0 !== undefined ? read(p.attributes.TEXCOORD_0) : null;
    for (let k = 0; k < n; k++) {
      const x = pos[k * 3], y = pos[k * 3 + 1], z = pos[k * 3 + 2];
      chunk.push(`v ${m[0] * x + m[4] * y + m[8] * z + m[12]} ${m[1] * x + m[5] * y + m[9] * z + m[13]} ${m[2] * x + m[6] * y + m[10] * z + m[14]}\n`);
      if (uv) chunk.push(`vt ${uv[k * 2]} ${1 - uv[k * 2 + 1]}\n`);
      if (nor) {
        const a = nor[k * 3], b = nor[k * 3 + 1], c = nor[k * 3 + 2];
        let nx = m[0] * a + m[4] * b + m[8] * c, ny = m[1] * a + m[5] * b + m[9] * c, nz = m[2] * a + m[6] * b + m[10] * c;
        const l = Math.hypot(nx, ny, nz) || 1;
        chunk.push(`vn ${nx / l} ${ny / l} ${nz / l}\n`);
      }
      flush();
    }
    chunk.push(`usemtl m${p.material ?? 0}\n`);
    const idx = p.indices !== undefined ? read(p.indices) : Float64Array.from({ length: n }, (_, i) => i);
    const f = (i) => { const v = vbase + i; return uv && nor ? `${v}/${v}/${v}` : uv ? `${v}/${v}` : nor ? `${v}//${v}` : `${v}`; };
    for (let k = 0; k < idx.length; k += 3) { chunk.push(`f ${f(idx[k])} ${f(idx[k + 1])} ${f(idx[k + 2])}\n`); flush(); }
    tris += idx.length / 3;
    vbase += n;
  }
}
flush(true);
fs.closeSync(fd);
console.error(`${dst}: ${vbase - 1} vertices, ${tris} triangles, ${(gltf.materials ?? []).length} materials`);
