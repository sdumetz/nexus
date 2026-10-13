"""Merge disjoint factor sweeps after validating identical baseline measurements."""
import argparse
import json
from pathlib import Path
import shutil

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('target',type=Path);p.add_argument('extension',type=Path)
a=p.parse_args()
base=json.loads((a.target/'selection.json').read_text());extra=json.loads((a.extension/'selection.json').read_text())
for key in ['models','requested_errors','precision_binary_sha256','upstream_binary_sha256','viewport','distance_radii']:
    assert base[key]==extra[key], key
assert not set(base['factors']) & set(extra['factors']), 'Factors overlap'
for model in base['models']:
    mid=model['model_id']; file=a.target/'models'/f'{mid}.json'
    original=json.loads(file.read_text());extended=json.loads((a.extension/'models'/f'{mid}.json').read_text())
    assert original['status']==extended['status']=='ok'
    assert original['artifacts']['upstream']==extended['artifacts']['upstream']
    r=original['measurement'];e=extended['measurement']
    assert r['poses']==e['poses'] and r['viewport']==e['viewport']
    for label in ['source','upstream']:
        for old_run in [v for v in r['runs'] if v['label']==label]:
            new_run=next(v for v in e['runs'] if v['label']==label and v['tau']==old_run['tau'])
            for key in ['gpuBytes','geometryBytes','textureBytes','residentNodes','drawnTriangles']:
                assert old_run.get(key)==new_run.get(key), (mid,key)
    for c in [c for c in r['comparisons'] if c['label']=='upstream']:
        counterpart=next(v for v in e['comparisons'] if all(v[k]==c[k] for k in ['label','reference','tau','mode','view']))
        for key in ['psnrDb','blockSsim','luminanceGradientRmse','silhouetteIoU']:
            assert c[key]==counterpart[key], (mid,key)
    original['artifacts'].update(extended['artifacts'])
    r['runs'] += [v for v in e['runs'] if v['label'] not in ['upstream','source']]
    r['comparisons'] += [v for v in e['comparisons'] if v['label']!='upstream']
    r['models'] += [v for v in e['models'] if v['label']!='upstream']
    file.write_text(json.dumps(original,indent=2)+'\n')
    # Keep the raw report as well as the compact report in models/.
    rawfile=a.target/'screenshots'/mid/'results.json'
    raw=json.loads(rawfile.read_text());newraw=json.loads((a.extension/'screenshots'/mid/'results.json').read_text())
    for key in ['runs','comparisons','models']:
        raw[key]+=[v for v in newraw[key] if v['label'] not in ['upstream','source']]
    rawfile.write_text(json.dumps(raw,indent=2)+'\n')
    for image in (a.extension/'screenshots'/mid).glob('factor*.png'):
        shutil.copy2(image,a.target/'screenshots'/mid/image.name)
base['factors']=sorted(base['factors']+extra['factors'])
(a.target/'selection.json').write_text(json.dumps(base,indent=2)+'\n')
print('Merged',len(base['models']),'models;',len(base['factors']),'factors')
