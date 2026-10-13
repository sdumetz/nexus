"""Targeted texture experiments on ten contrasting ISTI models.

Exports every variant from one hierarchy; retains builds for the next round.
Run --help for paths. Resume uses the frozen binary and source hashes.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import threading

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('isti_batch', HERE / 'isti-batch.py')
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)
IDS = ['RWT14', 'RWT76', 'RWT139', 'RWT256', 'RWT292', 'RWT319', 'RWT408', 'RWT471', 'RWT500', 'RWT514']


def report(out, models, variants):
    rows = []
    for model in models:
        file = out / 'models' / (model['model_id'] + '.json')
        if not file.exists(): continue
        state = json.loads(file.read_text())
        if state['status'] != 'ok': continue
        measurement = state['measurement']
        for run in measurement['runs']:
            if run['label'] == 'source': continue
            row = {k: model[k] for k in ('model_id', 'name', 'input_triangles', 'input_texels')}
            row.update(variant=run['label'], requested_error_pixels=run['tau'])
            for key in batch.RUN_FIELDS: row[key] = run.get(key)
            artifact = state['artifacts'][run['label']]
            row.update(file_bytes=artifact['file_bytes'], export_base_texels=artifact['export_base_texels'])
            for reference in variants + ['source']:
                comparisons = [c for c in measurement['comparisons'] if c['label'] == run['label'] and
                               c['reference'] == reference and c['tau'] == run['tau'] and c['mode'] == 'textured']
                if not comparisons: continue
                for key in batch.METRICS: row[f'vs_{reference}_{key}'] = comparisons[0].get(key)
                if reference != 'source':
                    previous = next(r for r in measurement['runs'] if r['label'] == reference and r['tau'] == run['tau'])
                    row[f'vs_{reference}_gpu_saving_pct'] = 100*(1-run['gpuBytes']/previous['gpuBytes'])
                    shaded = next(c for c in measurement['comparisons'] if c['label'] == run['label'] and c['reference'] == reference and c['tau'] == run['tau'] and c['mode'] == 'shaded')
                    row[f'vs_{reference}_shaded_identical'] = shaded['identical']
            rows.append(row)
    if rows:
        keys = list(dict.fromkeys(k for row in rows for k in row))
        with (out/'results.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, keys, lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--pair', type=Path, required=True)
    parser.add_argument('--node', required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--variants', default='round1,round2,fine')
    parser.add_argument('--reuse-builds', action='store_true', help='Reuse completed scratch exports under the frozen source/binary manifest')
    args = parser.parse_args()
    args.out = args.out.resolve(); args.scratch = args.scratch.resolve(); args.pair = args.pair.resolve()
    variants = args.variants.split(',')
    _, eligible, _ = batch.select_models(args.dataset, 1, 20261012)
    models = [next(m for m in eligible if m['model_id'] == mid) for mid in IDS]
    manifest = {'models': models, 'binary_sha256': batch.sha(args.pair), 'variants': variants,
                'taus': [2, 0.5, 0.1], 'distance_radii': 2.5, 'viewport': [1280,800],
                'selection': 'Purposive: prior quality outliers, savings, no-savings and original two lion cases; not representative of collection.'}
    args.out.mkdir(parents=True, exist_ok=True); args.scratch.mkdir(parents=True, exist_ok=True)
    selection = args.out/'selection.json'
    if selection.exists() and json.loads(selection.read_text()) != manifest:
        raise ValueError('Frozen experiment differs; use a new output directory')
    batch.atomic_json(selection, manifest)
    lock = threading.Lock()
    def work(model):
        mid = model['model_id']; destination = args.out/'models'/f'{mid}.json'
        if destination.exists() and json.loads(destination.read_text())['status'] == 'ok': return mid, 'resumed'
        scratch = args.scratch/mid; scratch.mkdir(parents=True, exist_ok=True)
        logs = args.out/'logs'/mid
        state = {'status':'running'}
        try:
            obj = scratch/'source'/'model.obj'
            build = scratch/'build'; build.mkdir(exist_ok=True)
            filenames = {label:build/f'model.{label}.nxs' for label in variants}
            if not (args.reuse_builds and all(f.exists() for f in filenames.values())):
                conversion = batch.execute([args.node,str(HERE/'gltf-to-obj.mjs'),model['source'],str(obj)],scratch,logs/'conversion.log',120)
                if conversion['status'] != 'ok': raise RuntimeError('Conversion failed')
                built = batch.execute([str(args.pair),str(obj),'-o',str(build/'model.nxs')],build,logs/'build.log',600)
                if built['status'] != 'ok': raise RuntimeError('Build failed')
            state['artifacts'] = {label:batch.artifact(file) for label,file in filenames.items()}
            if len({a['geometry_sha256'] for a in state['artifacts'].values()}) != 1:
                raise RuntimeError('Export variants changed geometry')
            command = [args.node,str(HERE/'run.mjs')]
            for label,file in filenames.items(): command += ['--model',f'{label}={file}']
            command += ['--source',model['source'],'--out',str(args.out/'screenshots'/mid),'--views','2.5','--taus','2,0.5,0.1']
            with lock:
                rendered = batch.execute(command,HERE.parent.parent,logs/'browser.log',1200)
            if rendered['status'] != 'ok': raise RuntimeError('Render failed')
            state['measurement'] = batch.compact_report(json.loads((args.out/'screenshots'/mid/'results.json').read_text()))
            if not all(r.get('allocationAuditPassed',True) for r in state['measurement']['runs']):
                raise RuntimeError('Allocation audit failed')
            state['status'] = 'ok'
        except Exception as error:
            state.update(status='failed',error=str(error))
        batch.atomic_json(destination,state)
        return mid,state['status']
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(work,m) for m in models]
        for future in as_completed(futures):
            print(*future.result(),flush=True)
            report(args.out,models,variants)
    rows = report(args.out,models,variants)
    if len(rows) != len(models)*len(variants)*3: raise RuntimeError('Incomplete measurements; see model JSON/logs')

if __name__ == '__main__': main()
