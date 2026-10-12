import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { Nexus3D, Cache } from '/runtime/Nexus3D.js';
import { instrumentGL, mipLevels, unionBytes } from './accounting.mjs';
import { imageDiff } from './image-diff.mjs';

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);
const gl = renderer.getContext(), ledger = instrumentGL(gl);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x202326);
scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 1.5));
const camera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.01, 1000);
const light = new THREE.DirectionalLight(0xffffff, 1.5);
light.position.set(0.5, 1, 1); camera.add(light); scene.add(camera);
const textured = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0 });
const shaded = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0, map: false });
let nx, source, frozen = false, drawCalls = 0, drawnTriangles = 0;
const ownedBuffers = new Set(), ownedTextures = new Set(), textureSizes = new Map();
let requestedNodes = 0, suppressedCandidates = 0;

const draw = gl.drawElements.bind(gl);
gl.drawElements = (mode, count, ...args) => {
  drawCalls++; if (mode === gl.TRIANGLES) drawnTriangles += count / 3;
  return draw(mode, count, ...args);
};
// Infinite budget must not turn view completion into full-model prefetch.
const update = Cache.update.bind(Cache);
Cache.update = function () {
  const previous = this.candidates;
  this.candidates = frozen ? [] : previous.filter(c => c.id < c.mesh.nroots || c.error >= this.currentError);
  suppressedCandidates += previous.length - this.candidates.length;
  return update();
};
const request = Cache.requestNode.bind(Cache);
Cache.requestNode = (...args) => { requestedNodes++; return request(...args); };

function render() {
  drawCalls = drawnTriangles = 0;
  // Nexus uploads and draws through raw GL, bypassing three's state cache.
  // Reconcile that cache every frame; timing is deliberately outside scope.
  renderer.resetState();
  renderer.render(scene, camera);
}
function capture() {
  render();
  return renderer.domElement.toDataURL('image/png').split(',')[1];
}
function shade(mode) {
  if (nx) { nx.material = mode === 'shaded' ? shaded : textured; nx.updateMaterials(); }
  source?.traverse(o => { if (o.isMesh) o.material = mode === 'shaded' ? shaded : o.userData.textured; });
}
function stats() {
  const error = gl.getError();
  if (error !== gl.NO_ERROR) throw new Error(`WebGL error invalidates allocation audit: ${error}`);
  const m = nx.mesh;
  const resident = [...(Cache.nodes.get(m) ?? [])].filter(id => m.status[id] === 1);
  const indexBytes = 88 + m.nodesCount * 44 + m.patchesCount * 12 + m.texturesCount * 68;
  const ranges = [[0, indexBytes]], referencedTextures = new Set();
  let expectedGeometry = 0;
  for (const id of resident) {
    expectedGeometry += m.nvertices[id] * m.vsize + m.nfaces[id] * 6;
    ranges.push([m.noffsets[id], m.noffsets[id + 1]]);
    if (m.vertex.texCoord) for (let p = m.nfirstpatch[id]; p < m.nfirstpatch[id + 1]; ++p)
      if (m.patches[p * 3 + 2] !== 0xffffffff) referencedTextures.add(m.patches[p * 3 + 2]);
  }
  let expectedTexture = 0;
  for (const id of referencedTextures) {
    const sizes = textureSizes.get(id);
    if (!sizes) throw new Error(`Resident texture ${id} has no recorded upload`);
    expectedTexture += sizes.bytes;
    ranges.push([m.textures[id], m.textures[id + 1]]);
  }
  const geometryBytes = [...ownedBuffers].reduce((sum, h) => sum + (ledger.buffers.get(h) ?? 0), 0);
  let textureBytes = 0, baseTexels = 0, mipTexels = 0, liveTextures = 0;
  for (const handle of ownedTextures) {
    const allocation = ledger.textures.get(handle);
    if (!allocation) continue;
    if (!allocation.valid) throw new Error('Unsupported Nexus texture allocation format');
    liveTextures++;
    baseTexels += allocation.levels.get(0).texels;
    for (const level of allocation.levels.values()) { textureBytes += level.bytes; mipTexels += level.texels; }
  }
  // Cross-check the GL ledger against decoded node counts and image dimensions.
  if (geometryBytes !== expectedGeometry || textureBytes !== expectedTexture)
    throw new Error(`Allocation audit failed: geometry ${geometryBytes}/${expectedGeometry}, texture ${textureBytes}/${expectedTexture}`);
  return {
    residentNodes: resident.length, totalNodes: m.nodesCount - 1, residentNodeIds: resident,
    requestedNodes, liveTextures, baseTexels, mipTexels,
    geometryBytes, textureBytes, gpuBytes: geometryBytes + textureBytes,
    legacyEstimatedCacheBytes: Cache.cacheSize, allocationAuditPassed: true,
    residentEncodedRangeBytes: unionBytes(ranges), indexBytes,
    drawCalls, drawnTriangles, suppressedCandidates,
    textures: [...textureSizes].map(([id, value]) => ({ id, ...value })),
  };
}

window.bench = {
  async run({ url, kind = 'nexus', pose, tau = 2, timeoutMs = 120000 }) {
    camera.position.fromArray(pose.position); camera.up.fromArray(pose.up ?? [0, 1, 0]);
    camera.near = pose.near; camera.far = pose.far; camera.fov = pose.fov ?? 45;
    camera.lookAt(new THREE.Vector3().fromArray(pose.target)); camera.updateProjectionMatrix(); camera.updateMatrixWorld();
    if (kind === 'source') {
      const gltf = await new GLTFLoader().loadAsync(url);
      source = gltf.scene;
      source.traverse(o => {
        if (!o.isMesh) return;
        o.userData.textured = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0, map: o.material.map });
        o.material = o.userData.textured;
      });
      scene.add(source); render();
      return { source: true, threeRevision: THREE.REVISION };
    }
    Object.assign(Cache, { maxCacheSize: Infinity, minFps: 0, targetError: tau, currentError: tau, maxPending: 3, cortopath: '/codecs' });
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('Nexus header/index timeout')), timeoutMs);
      nx = new Nexus3D(url, renderer, { material: textured, onLoad: () => { clearTimeout(timer); resolve(); } });
    });
    if (nx.mesh.meco || nx.mesh.deepzoom) throw new Error('This harness supports raw NXS and Corto NXZ; MECO/Deepzoom are unsupported');
    // Existing three.js integration passes a Vector4 to a traversal expecting an array.
    const updateView = nx.traversal.updateView.bind(nx.traversal);
    nx.traversal.updateView = (v, ...rest) => updateView(v.isVector4 ? [v.x, v.y, v.z, v.w] : v, ...rest);
    const createGeometry = nx.mesh.createNodeGeometry;
    nx.mesh.createNodeGeometry = (id, geometry) => {
      createGeometry(id, geometry);
      ownedBuffers.add(nx.vbo[id]); ownedBuffers.add(nx.ibo[id]);
    };
    const createTexture = nx.mesh.createTexture;
    nx.mesh.createTexture = (id, image) => {
      createTexture(id, image);
      ownedTextures.add(nx.textures[id]);
      const allocation = ledger.textures.get(nx.textures[id]);
      const levels = [...allocation.levels.values()];
      textureSizes.set(id, { width: image.width, height: image.height, levels: levels.length,
        bytes: levels.reduce((n, level) => n + level.bytes, 0) });
      const expected = mipLevels(image.width, image.height).reduce((n, level) => n + level.bytes, 0);
      if (levels.length > 1 && textureSizes.get(id).bytes !== expected) throw new Error('Mipmap accounting mismatch');
    };
    scene.add(nx);
    const start = performance.now();
    let signature = '', quiet = 0;
    while (quiet < 12) {
      render();
      const m = nx.mesh, t = nx.traversal;
      let complete = !!t.visited;
      for (let id = 0; id < m.nodesCount - 1; ++id) {
        if ((id < m.nroots || t.visited?.[id] && t.instance_errors[id] >= tau) && m.status[id] !== 1) complete = false;
        if (m.status[id] > 1) complete = false; // Includes image decode after its HTTP request completes.
      }
      const now = `${requestedNodes}/${m.availableNodes}/${textureSizes.size}`;
      quiet = complete && Cache.pending === 0 && now === signature ? quiet + 1 : 0;
      signature = now;
      if (performance.now() - start > timeoutMs) throw new Error('View did not settle; no measurement emitted');
      await new Promise(resolve => requestAnimationFrame(resolve));
    }
    frozen = true;
    render();
    return { ...stats(), threeRevision: THREE.REVISION, unboundedCache: true, prefetchBelowTarget: false };
  },
  capture(mode) { shade(mode); return capture(); },
  async compare(reference, mode) {
    shade(mode); render();
    const image = new Image(); image.src = `data:image/png;base64,${reference}`; await image.decode();
    const canvas = document.createElement('canvas'); canvas.width = innerWidth; canvas.height = innerHeight;
    const ctx = canvas.getContext('2d'); ctx.drawImage(image, 0, 0);
    const previous = ctx.getImageData(0, 0, innerWidth, innerHeight).data;
    ctx.drawImage(renderer.domElement, 0, 0);
    const current = ctx.getImageData(0, 0, innerWidth, innerHeight).data;
    const { metrics, heat } = imageDiff(previous, current);
    ctx.putImageData(new ImageData(new Uint8ClampedArray(heat), innerWidth, innerHeight), 0, 0);
    return { ...metrics, heatPng: canvas.toDataURL('image/png').split(',')[1] };
  },
};
