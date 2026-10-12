// Small Chrome DevTools driver: the same browser automation used by Puppeteer,
// without a new dependency. Requires Node's built-in WebSocket (Node 22+).
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

export async function launch({ binary = '/usr/bin/chromium', width, height }) {
  const profile = await fs.mkdtemp(path.join(os.tmpdir(), 'nexus-benchmark-chrome-'));
  const process = spawn(binary, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`,
    `--window-size=${width},${height}`, '--no-first-run', '--no-default-browser-check', '--ignore-gpu-blocklist',
    '--use-angle=swiftshader', '--enable-unsafe-swiftshader', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
  let diagnostics = '';
  let spawnError;
  process.on('error', error => { spawnError = error; });
  process.stderr.on('data', data => { diagnostics = (diagnostics + data).slice(-8000); });
  const stop = async () => { process.kill(); await new Promise(resolve => spawnError || process.exitCode !== null || process.signalCode !== null ? resolve() : process.once('exit', resolve)); await fs.rm(profile, { recursive: true, force: true, maxRetries: 10, retryDelay: 200 }); };
  let socket;
  try {
    let port;
    for (let i = 0; i < 100; ++i) {
      if (spawnError) throw spawnError;
      if (process.exitCode !== null || process.signalCode !== null) throw new Error(`Chromium exited: ${diagnostics}`);
      try { port = (await fs.readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]; } catch {}
      if (port) break;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    if (!port) throw new Error(`Chromium startup timeout: ${diagnostics}`);
    const target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page');
    socket = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
  } catch (error) { await stop(); throw error; }
  let id = 0;
  const pending = new Map(), listeners = [];
  socket.onmessage = event => {
    const message = JSON.parse(event.data);
    const call = pending.get(message.id);
    if (call) { pending.delete(message.id); message.error ? call.reject(new Error(message.error.message)) : call.resolve(message.result); }
    else for (const listener of listeners) listener(message);
  };
  socket.onclose = () => { for (const call of pending.values()) call.reject(new Error('Chromium connection closed')); pending.clear(); };
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const key = ++id; pending.set(key, { resolve, reject }); socket.send(JSON.stringify({ id: key, method, params }));
  });
  await send('Runtime.enable'); await send('Page.enable'); await send('Network.enable');
  await send('Network.setCacheDisabled', { cacheDisabled: true });
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
  const evaluate = async expression => {
    const response = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true, timeout: 300000 });
    if (response.exceptionDetails) throw new Error(response.exceptionDetails.exception?.description ?? response.exceptionDetails.text);
    return response.result.value;
  };
  return { send, evaluate, on: listener => listeners.push(listener),
    async goto(url) {
      await send('Page.navigate', { url });
      for (let i = 0; i < 300; ++i) {
        if (await evaluate(`location.href === ${JSON.stringify(url)} && !!window.bench`).catch(() => false)) return;
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      throw new Error('Benchmark page did not initialize');
    },
    async close() { socket.close(); await stop(); },
  };
}
