export function imageDiff(a, b, background = [32, 35, 38]) {
  if (a.length !== b.length || a.length % 4) throw new Error('Image dimensions differ');
  let squared = 0, absolute = 0, modelPixels = 0, changed = 0, intersection = 0, identical = true;
  const heat = new Uint8Array(a.length);
  const isBackground = (image, i) => background.every((v, c) => Math.abs(image[i + c] - v) <= 2);
  for (let i = 0; i < a.length; i += 4) {
    const ma = !isBackground(a, i), mb = !isBackground(b, i);
    if (ma && mb) intersection++;
    let largest = 0;
    for (let c = 0; c < 3; ++c) {
      const d = Math.abs(a[i + c] - b[i + c]);
      if (d) identical = false;
      heat[i + c] = Math.min(255, d * 4);
      largest = Math.max(largest, d);
      if (ma || mb) { squared += d * d; absolute += d; }
    }
    heat[i + 3] = 255;
    if (a[i + 3] !== b[i + 3]) identical = false;
    if (ma || mb) { modelPixels++; if (largest > 8) changed++; }
  }
  const mse = modelPixels ? squared / (3 * modelPixels) : 0;
  return { metrics: {
    modelPixels, mse, psnrDb: mse ? 10 * Math.log10(255 * 255 / mse) : null,
    identical, meanAbsoluteChannelDifference: modelPixels ? absolute / (3 * modelPixels) : 0,
    changedPixelsOver8Fraction: modelPixels ? changed / modelPixels : 0,
    silhouetteIoU: modelPixels ? intersection / modelPixels : 1,
  }, heat };
}
