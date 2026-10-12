// Logical WebGL allocation sizes, not driver/process VRAM measurements.
export function mipLevels(width, height) {
  const levels = [];
  for (;;) {
    levels.push({ width, height, texels: width * height, bytes: width * height * 4 });
    if (width === 1 && height === 1) return levels;
    width = Math.max(1, Math.floor(width / 2));
    height = Math.max(1, Math.floor(height / 2));
  }
}

export function unionBytes(ranges) {
  let bytes = 0, end = 0;
  for (const [a, b] of ranges.toSorted((x, y) => x[0] - y[0])) {
    bytes += Math.max(0, b - Math.max(a, end));
    end = Math.max(end, b);
  }
  return bytes;
}

export function instrumentGL(gl) {
  const buffers = new Map(), textures = new Map();
  let uploadedBufferBytes = 0, uploadedTextureBytes = 0;
  const wrap = (name, callback) => {
    const original = gl[name].bind(gl);
    gl[name] = (...args) => { const result = original(...args); callback(...args); return result; };
  };
  wrap('bufferData', (target, data) => {
    if (![gl.ARRAY_BUFFER, gl.ELEMENT_ARRAY_BUFFER].includes(target)) return;
    const binding = target === gl.ARRAY_BUFFER ? gl.ARRAY_BUFFER_BINDING : gl.ELEMENT_ARRAY_BUFFER_BINDING;
    const bytes = typeof data === 'number' ? data : data.byteLength;
    buffers.set(gl.getParameter(binding), bytes);
    uploadedBufferBytes += bytes;
  });
  wrap('deleteBuffer', buffer => buffers.delete(buffer));
  wrap('texImage2D', (...args) => {
    if (args[0] !== gl.TEXTURE_2D) return;
    const handle = gl.getParameter(gl.TEXTURE_BINDING_2D);
    const image = args[5];
    const width = args.length === 6 ? image.naturalWidth || image.width : args[3];
    const height = args.length === 6 ? image.naturalHeight || image.height : args[4];
    const format = args.length === 6 ? args[3] : args[6];
    const type = args.length === 6 ? args[4] : args[7];
    // This benchmark supports the viewers' RGBA8/sRGB8-alpha8 image uploads.
    // Keep unsupported shell textures visible as errors if Nexus owns them.
    const valid = format === gl.RGBA && type === gl.UNSIGNED_BYTE
      && [gl.RGBA, gl.RGBA8, gl.SRGB8_ALPHA8].includes(args[2]);
    const record = textures.get(handle) ?? { levels: new Map() };
    record.valid = valid;
    record.levels.set(args[1], { width, height, texels: width * height, bytes: width * height * 4 });
    textures.set(handle, record);
    uploadedTextureBytes += width * height * 4;
  });
  wrap('generateMipmap', target => {
    if (target !== gl.TEXTURE_2D) return;
    const record = textures.get(gl.getParameter(gl.TEXTURE_BINDING_2D));
    if (!record?.levels.has(0)) return;
    const { width, height } = record.levels.get(0);
    record.levels = new Map(mipLevels(width, height).map((level, i) => [i, level]));
  });
  wrap('deleteTexture', texture => textures.delete(texture));
  return { buffers, textures, uploads: () => ({ uploadedBufferBytes, uploadedTextureBytes }) };
}
