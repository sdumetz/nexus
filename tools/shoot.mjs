import pw from '/home/sebastien/repositories/dpo-voyager/node_modules/playwright/index.js';
const { chromium } = pw;

const model = process.argv[2] || 'models/test_ktx.nxs';
const out = process.argv[3] || '/tmp/shot.png';

const browser = await chromium.launch({
	args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
const logs = [];
page.on('console', m => logs.push(`[${m.type()}] ${m.text()}`));
page.on('pageerror', e => logs.push(`[pageerror] ${e.message}`));

await page.goto(`http://localhost:8080/html/ktx2.html?model=${encodeURIComponent(model)}`, { waitUntil: 'load' });

try {
	await page.waitForFunction(() => window.nexusReady === true, { timeout: 30000 });
	console.log('nexusReady=true');
} catch (e) {
	console.log('TIMEOUT waiting for nexusReady; error=' + await page.evaluate(() => window.nexusError));
}
// face-on 3/4 view to show the texture, then let traversal stream node textures in
await page.evaluate(() => window.setView(Math.PI / 2 + 0.5, 0.2, 1.6));
await page.waitForTimeout(5000);
await page.screenshot({ path: out });
console.log('--- console ---');
console.log(logs.slice(-40).join('\n'));
await browser.close();
