"""Compare a precision-factor sweep directly to unmodified v4-fixes exports.

Builds share geometry and baking inputs; every browser job starts a fresh,
unbounded cache and audits actual WebGL allocation. Resume completed models.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import hashlib
import json
import os
import shutil
from pathlib import Path
import threading

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('batch', HERE/'isti-batch.py')
batch = importlib.util.module_from_spec(spec); spec.loader.exec_module(batch)
def sha256(file): return hashlib.sha256(file.read_bytes()).hexdigest()
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--pair', type=Path, required=True)
p.add_argument('--upstream', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--scratch', type=Path, required=True)
p.add_argument('--sources', type=Path, default=Path('/tmp/nexus-texture-precision-10'))
p.add_argument('--selection', type=Path, default=HERE.parent.parent/'doc/measurements/isti-precision-10/selection.json')
p.add_argument('--node', default='/home/sebastien/.nvm/versions/node/v24.2.0/bin/node')
p.add_argument('--factors', default='0.5,0.75,1,1.5,2,3,4')
p.add_argument('--build-tag', default='sweep', help='Separate scratch hierarchy for concurrently run sweeps')
p.add_argument('--taus', default='2')
p.add_argument('--reuse-captures',type=Path)
a = p.parse_args()
models = json.loads(a.selection.read_text())['models']
factors = a.factors.split(',')
taus = [float(t) for t in a.taus.split(',')]
os.environ['NEXUS_BENCH_FACTORS'] = a.factors
labels = ['factor'+f.replace('.', '_') for f in factors]
a.out.mkdir(parents=True, exist_ok=True); a.scratch.mkdir(parents=True, exist_ok=True)
manifest = dict(models=models, factors=[float(f) for f in factors], requested_errors=taus,
    precision_binary_sha256=sha256(a.pair), upstream_binary_sha256=sha256(a.upstream),
    source_selection=str(a.selection), upstream_revision='1fe489d', viewport=[1280,800], distance_radii=2.5,
    notes='Purposive ten-model sample. Factor is precision; larger retains more. Source-relative quality; direct upstream renders.')
selection = a.out/'selection.json'
if selection.exists(): assert json.loads(selection.read_text()) == manifest, 'Changed inputs: choose new output directory'
batch.atomic_json(selection, manifest)
lock = threading.Lock()

def work(model):
    mid = model['model_id']; dest = a.out/'models'/f'{mid}.json'
    if dest.exists() and json.loads(dest.read_text())['status']=='ok': return mid, 'resumed'
    logs = a.out/'logs'/mid
    root = a.scratch/mid; root.mkdir(parents=True, exist_ok=True)
    obj = a.sources/mid/'source/model.obj'
    state = dict(status='running')
    try:
        assert sha256(Path(model['source'])) == model['source_sha256']
        upstream = root/'upstream'; upstream.mkdir(exist_ok=True)
        control = upstream/'test.nxs'
        if not control.exists():
            result = batch.execute([str(a.upstream),str(obj)],upstream,logs/'upstream-build.log',600)
            assert result['status']=='ok', result
        build = root/a.build_tag; build.mkdir(exist_ok=True)
        files = {label:build/f'model.{label}.nxs' for label in labels}
        if not all(file.exists() for file in files.values()):
            result = batch.execute([str(a.pair),str(obj),'-o',str(build/'model.nxs')],build,logs/'sweep-build.log',1200)
            assert result['status']=='ok', result
        files = dict(upstream=control, **files)
        state['artifacts'] = {label:batch.artifact(file) for label,file in files.items()}
        assert len({art['geometry_sha256'] for art in state['artifacts'].values()})==1, 'Geometry changed'
        # Current factor 1/2 must reproduce the previous corrected experiment.
        prior = json.loads((a.selection.parent/'models'/f'{mid}.json').read_text())
        for label, old in [('factor1','divisor1'),('factor2','divisor2')]:
            if label not in files: continue
            for key in ['geometry_sha256','texture_sha256','texture_sizes']:
                assert state['artifacts'][label][key]==prior['artifacts'][old][key], (mid,label,key)
        command = [a.node,str(HERE/'run.mjs')]
        for label,file in files.items(): command += ['--model',f'{label}={file}']
        command += ['--source',model['source'],'--out',str(a.out/'screenshots'/mid),
                    '--views','2.5','--taus',a.taus,'--comparison-mode','baseline']
        measurement=None
        if a.reuse_captures:
            oldfile=a.reuse_captures/'screenshots'/mid/'results.json'
            if oldfile.exists():
                old=json.loads(oldfile.read_text())
                old['runs']=[r for r in old['runs'] if r['label']=='source' or r['tau'] in taus]
                old['comparisons']=[c for c in old['comparisons'] if c['tau'] in taus]
                if len(old['runs'])==1+len(files)*len(taus):
                    destination=a.out/'screenshots'/mid;destination.mkdir(parents=True,exist_ok=True)
                    for image in oldfile.parent.glob('*.png'):
                        if image.name.startswith('source-') or any(f'-t{format(t,"g")}-' in image.name for t in taus):
                            shutil.copy2(image,destination/image.name)
                    batch.atomic_json(destination/'results.json',old)
                    measurement=old
        if measurement is None:
            with lock: result = batch.execute(command,HERE.parent.parent,logs/'browser.log',2400)
            assert result['status']=='ok', result
            measurement = json.loads((a.out/'screenshots'/mid/'results.json').read_text())
        assert len(measurement['runs'])==1+len(files)*len(taus)
        assert all(r.get('allocationAuditPassed',True) for r in measurement['runs'])
        assert measurement['poses']==prior['measurement']['poses']
        state['measurement']=batch.compact_report(measurement)
        state['status']='ok'
    except Exception as error: state.update(status='failed', error=str(error))
    batch.atomic_json(dest,state)
    return mid,state['status']

with ThreadPoolExecutor(max_workers=2) as pool:
    for future in as_completed([pool.submit(work, model) for model in models]):
        print(*future.result(),flush=True)
assert all(json.loads((a.out/'models'/f"{m['model_id']}.json").read_text())['status']=='ok' for m in models), 'Incomplete sweep'
