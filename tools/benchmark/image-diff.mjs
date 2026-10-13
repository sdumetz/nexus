export function imageDiff(a, b, background = [32, 35, 38], width) {
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
  const structural = width ? structureDiff(a, b, width, background) : {};
  return { metrics: {
    ...structural,
    modelPixels, mse, psnrDb: mse ? 10 * Math.log10(255 * 255 / mse) : null,
    identical, meanAbsoluteChannelDifference: modelPixels ? absolute / (3 * modelPixels) : 0,
    changedPixelsOver8Fraction: modelPixels ? changed / modelPixels : 0,
    silhouetteIoU: modelPixels ? intersection / modelPixels : 1,
  }, heat };
}

// Foreground-weighted, nonoverlapping 8x8 luminance SSIM blocks. This diagnostic
// is explicitly block SSIM, not the Gaussian-window implementation of SSIM.
function structureDiff(a, b, width, background) {
  const height = a.length / (4 * width);
  if (!Number.isInteger(height) || width < 1) throw new Error('Invalid image width');
  const foreground = (v, i) => background.some((c, k) => Math.abs(v[i + k] - c) > 2);
  const luminance = (v, i) => 0.2126*v[i] + 0.7152*v[i+1] + 0.0722*v[i+2];
  let sum = 0, weight = 0, edgeError = 0, edges = 0;
  for (let y = 0; y < height; y += 8) for (let x = 0; x < width; x += 8) {
    let n = 0, fg = 0, sa = 0, sb = 0, aa = 0, bb = 0, ab = 0;
    for (let dy = 0; dy < 8 && y+dy < height; dy++) for (let dx = 0; dx < 8 && x+dx < width; dx++) {
      const i = ((y+dy)*width+x+dx)*4, va = luminance(a,i), vb = luminance(b,i);
      n++; sa+=va; sb+=vb; aa+=va*va; bb+=vb*vb; ab+=va*vb;
      if (foreground(a,i) || foreground(b,i)) {
        fg++;
        for (const offset of [dx+x+1 < width ? 4 : 0, dy+y+1 < height ? width*4 : 0]) {
          if (!offset || !(foreground(a,i+offset) || foreground(b,i+offset))) continue;
          const error = (luminance(a,i+offset)-va)-(luminance(b,i+offset)-vb);
          edgeError+=error*error; edges++;
        }
      }
    }
    if (!fg) continue;
    const ma=sa/n, mb=sb/n, varianceA=Math.max(0,aa/n-ma*ma), varianceB=Math.max(0,bb/n-mb*mb), covariance=ab/n-ma*mb;
    const c1=6.5025, c2=58.5225;
    sum+=fg*((2*ma*mb+c1)*(2*covariance+c2))/((ma*ma+mb*mb+c1)*(varianceA+varianceB+c2)); weight+=fg;
  }
  return { blockSsim: weight ? sum/weight : 1, luminanceGradientRmse: edges ? Math.sqrt(edgeError/edges) : 0 };
}
