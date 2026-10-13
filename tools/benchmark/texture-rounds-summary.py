"""Summarize targeted texture CSVs; validate exports and audited residency."""
import argparse
import csv
import json
from pathlib import Path
import statistics
import hashlib


def summarize(directory, comparisons, previous_directory=None, divisor_baseline=None):
    rows = list(csv.DictReader((directory/'results.csv').open()))
    models = json.loads((directory/'selection.json').read_text())['models']
    variants = json.loads((directory/'selection.json').read_text())['variants']
    if previous_directory and not {'round1','fine'}.issubset(variants):
        raise ValueError('--previous validation requires the historical round1/fine variants')
    assert len(rows) == len(models)*len(variants)*3
    indexed = {(r['model_id'],r['variant'],r['requested_error_pixels']):r for r in rows}
    assert len(indexed) == len(rows)
    previous_checks = []
    for model in models:
        state = json.loads((directory/'models'/f"{model['model_id']}.json").read_text())
        assert state['status'] == 'ok'
        assert len({a['geometry_sha256'] for a in state['artifacts'].values()}) == 1
        for r in state['measurement']['runs']:
            if r['label']=='source': continue
            assert r['allocationAuditPassed'] is True
            assert r['gpuBytes']==r['geometryBytes']+r['textureBytes']
        for variant in ['fine','reconstructionFine','divisor1','divisor2']:
            if variant in state['artifacts']:
                assert all(w%4==0 and h%4==0 for w,h in state['artifacts'][variant]['texture_sizes'])
        if 'reconstruction' in variants:
            for a,b in [('round1','reconstruction'),('fine','reconstructionFine')]:
                if a not in state['artifacts'] or b not in state['artifacts']: continue
                assert state['artifacts'][a]['texture_sha256']==state['artifacts'][b]['texture_sha256']
                assert state['artifacts'][a]['texture_sizes']==state['artifacts'][b]['texture_sizes']
        if 'divisor1' in variants and 'divisor2' in variants:
            assert all(w2>=w1 and h2>=h1 for (w1,h1),(w2,h2) in zip(
                state['artifacts']['divisor1']['texture_sizes'],state['artifacts']['divisor2']['texture_sizes']))
        if previous_directory:
            old = json.loads((previous_directory/'models'/f"{model['model_id']}.json").read_text())
            for variant in ['round1','fine']:
                for key in ('geometry_sha256','texture_sha256','texture_sizes','file_bytes'):
                    assert state['artifacts'][variant][key] == old['artifacts'][variant][key]
                for tau in [2,0.5,0.1]:
                    new_run = next(r for r in state['measurement']['runs'] if r['label']==variant and r['tau']==tau)
                    old_run = next(r for r in old['measurement']['runs'] if r['label']==variant and r['tau']==tau)
                    for key in ('gpuBytes','geometryBytes','textureBytes','residentNodes','drawnTriangles'):
                        assert new_run[key] == old_run[key]
                    for mode in ['textured','shaded']:
                        stem = f'{variant}-v0-t{tau}-{mode}.png'
                        new_png = directory/'screenshots'/model['model_id']/stem
                        old_png = previous_directory/'screenshots'/model['model_id']/stem
                        assert hashlib.sha256(new_png.read_bytes()).digest()==hashlib.sha256(old_png.read_bytes()).digest()
            previous_checks.append(dict(model_id=model['model_id'], semantic_exports_match=True,
                allocations_match=True, baseline_screenshots_byte_identical=True))
        if divisor_baseline:
            old = json.loads((divisor_baseline/'models'/f"{model['model_id']}.json").read_text())
            for variant,reference in [('round1','round1'),('divisor1','reconstructionFine')]:
                for key in ('geometry_sha256','texture_sha256','texture_sizes','file_bytes'):
                    assert state['artifacts'][variant][key] == old['artifacts'][reference][key]
                for tau in [2,0.5,0.1]:
                    new_run = next(r for r in state['measurement']['runs'] if r['label']==variant and r['tau']==tau)
                    old_run = next(r for r in old['measurement']['runs'] if r['label']==reference and r['tau']==tau)
                    for key in ('gpuBytes','geometryBytes','textureBytes','residentNodes','drawnTriangles'):
                        assert new_run[key] == old_run[key]
                    for mode in ['textured','shaded']:
                        new_png = directory/'screenshots'/model['model_id']/f'{variant}-v0-t{tau}-{mode}.png'
                        old_png = divisor_baseline/'screenshots'/model['model_id']/f'{reference}-v0-t{tau}-{mode}.png'
                        assert hashlib.sha256(new_png.read_bytes()).digest()==hashlib.sha256(old_png.read_bytes()).digest()
            previous_checks.append(dict(model_id=model['model_id'], semantic_exports_match=True,
                allocations_match=True, baseline_screenshots_byte_identical=True))
    if previous_directory or divisor_baseline:
        (directory/'previous-round-validation.json').write_text(json.dumps(previous_checks,indent=2)+'\n')
    graph = []
    for row in rows:
        item = {k:row[k] for k in ('model_id','name','variant','requested_error_pixels','residentNodes','drawnTriangles')}
        for key in ('gpuBytes','geometryBytes','textureBytes','file_bytes'):
            item[key.replace('Bytes','MiB').replace('_bytes','_mib')] = int(row[key])/1048576
        for key,value in row.items():
            if key.endswith('gpu_saving_pct') or key.endswith('psnrDb') or key.endswith('shaded_identical'):
                item[key] = value
            if key.endswith('changedPixelsOver8Fraction'):
                item[key.replace('changedPixelsOver8Fraction','changed_pixels_over_8_pct')] = float(value)*100 if value else ''
        graph.append(item)
    with (directory/'graph.csv').open('w',newline='') as stream:
        keys = list(dict.fromkeys(k for row in graph for k in row))
        writer=csv.DictWriter(stream,keys,lineterminator='\n');writer.writeheader();writer.writerows(graph)
    summary = []
    for candidate,reference in comparisons:
        for tau in ['2','0.5','0.1']:
            current = [indexed[m['model_id'],candidate,tau] for m in models]
            previous = [indexed[m['model_id'],reference,tau] for m in models]
            saving = [100*(1-int(a['gpuBytes'])/int(b['gpuBytes'])) for a,b in zip(current,previous)]
            source_deltas = [float(a['vs_source_psnrDb'])-float(b['vs_source_psnrDb']) for a,b in zip(current,previous)]
            prefix = f'vs_{reference}_'
            summary.append(dict(candidate=candidate,reference=reference,requested_error_pixels=float(tau),models=len(models),
                median_gpu_saving_pct=statistics.median(saving),
                weighted_gpu_saving_pct=100*(1-sum(int(a['gpuBytes']) for a in current)/sum(int(b['gpuBytes']) for b in previous)),
                models_saving=sum(s>1e-6 for s in saving),models_identical=sum(a[prefix+'identical']=='True' for a in current),
                models_changed_over_1pct=sum(float(a[prefix+'changedPixelsOver8Fraction'])>0.01 for a in current),
                models_shaded_identical=sum(a[prefix+'shaded_identical']=='True' for a in current),
                median_source_psnr_change_db=statistics.median(source_deltas),worst_source_psnr_change_db=min(source_deltas)))
    with (directory/'aggregate.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,list(summary[0]),lineterminator='\n'); writer.writeheader();writer.writerows(summary)
    (directory/'aggregate.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--compare',action='append',required=True,help='candidate=reference')
    parser.add_argument('--previous',type=Path,help='Validate round1/fine exports, allocations and PNGs against round 3')
    parser.add_argument('--divisor-baseline',type=Path,help='Validate round1/divisor1 against the frozen original round 4 run')
    args=parser.parse_args()
    summarize(args.directory,[tuple(c.split('=')) for c in args.compare],args.previous,args.divisor_baseline)
