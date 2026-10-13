import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mipLevels, unionBytes, instrumentGL } from './accounting.mjs';
import { imageDiff } from './image-diff.mjs';

test('exact mip sums include rectangular and terminal 1x1 levels', () => {
  assert.equal(mipLevels(4, 4).reduce((n, level) => n + level.bytes, 0), 84);
  assert.equal(mipLevels(1, 8).reduce((n, level) => n + level.bytes, 0), 60);
  assert.deepEqual(mipLevels(3, 5).map(x => [x.width, x.height]), [[3, 5], [1, 2], [1, 1]]);
  assert.equal(mipLevels(1, 1)[0].bytes, 4);
});
test('overlapping geometry-tail and texture ranges are counted once', () => {
  assert.equal(unionBytes([[0, 88], [88, 256], [256, 1024], [512, 768], [900, 1100]]), 1100);
  assert.equal(unionBytes([[20, 30], [0, 10], [25, 40]]), 30);
});
test('allocation ledger counts unique live handles, reallocations, generated mips and deletion', () => {
  const gl = { ARRAY_BUFFER: 1, ELEMENT_ARRAY_BUFFER: 2, ARRAY_BUFFER_BINDING: 3, ELEMENT_ARRAY_BUFFER_BINDING: 4,
    TEXTURE_2D: 5, TEXTURE_BINDING_2D: 6, RGBA: 7, RGBA8: 8, SRGB8_ALPHA8: 9, UNSIGNED_BYTE: 10,
    getParameter(key) { return key === 6 ? this.texture : this.buffer; },
    bufferData() {}, deleteBuffer() {}, texImage2D() {}, generateMipmap() {}, deleteTexture() {} };
  const ledger = instrumentGL(gl), buffer = {}, texture = {};
  gl.buffer = buffer; gl.bufferData(gl.ARRAY_BUFFER, new Uint8Array(128), 0);
  gl.bufferData(gl.ARRAY_BUFFER, 64, 0);
  assert.equal(ledger.buffers.size, 1); assert.equal(ledger.buffers.get(buffer), 64);
  gl.texture = texture;
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, { width: 1, height: 8 });
  gl.generateMipmap(gl.TEXTURE_2D);
  assert.equal([...ledger.textures.get(texture).levels.values()].reduce((n, x) => n + x.bytes, 0), 60);
  gl.deleteBuffer(buffer); gl.deleteTexture(texture);
  assert.equal(ledger.buffers.size, 0); assert.equal(ledger.textures.size, 0);
});
test('image differences use model pixels instead of diluting errors with background', () => {
  const background = [32, 35, 38, 255];
  const a = new Uint8Array([...background, 255, 255, 255, 255]);
  const same = imageDiff(a, a).metrics;
  assert.equal(same.identical, true); assert.equal(same.modelPixels, 1); assert.equal(same.psnrDb, null);
  const b = new Uint8Array([...background, 245, 255, 255, 255]);
  const different = imageDiff(a, b).metrics;
  assert.equal(different.modelPixels, 1); assert.equal(different.changedPixelsOver8Fraction, 1);
  assert.equal(different.meanAbsoluteChannelDifference, 10 / 3);
  const backgroundChange = new Uint8Array([...background, ...background]);
  const almostBackground = backgroundChange.slice(); almostBackground[0]++;
  assert.equal(imageDiff(backgroundChange, almostBackground).metrics.identical, false);
});

test('structural diagnostics detect detail loss even when mean luminance is preserved', () => {
  const sharp = new Uint8Array(8*8*4), soft = new Uint8Array(sharp.length);
  for (let i=0; i<64; i++) {
    const value = i%2 ? 200 : 56;
    sharp.set([value,value,value,255],i*4);
    soft.set([128,128,128,255],i*4);
  }
  const same=imageDiff(sharp,sharp,[32,35,38],8).metrics;
  const blur=imageDiff(sharp,soft,[32,35,38],8).metrics;
  assert.equal(same.blockSsim,1);
  assert.equal(same.luminanceGradientRmse,0);
  assert.ok(blur.blockSsim<0.02);
  assert.ok(blur.luminanceGradientRmse>90);
});
