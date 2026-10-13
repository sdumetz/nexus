"""Join corrected precision measurements to compatible audited v4-fixes controls.

Only the shared 2px/0.1px views are compared. Validate identical camera/source,
round1 semantic payloads, allocations and source-relative image metrics first.
"""
import argparse
import csv
import json
from pathlib import Path
import statistics

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('current',type=Path)
parser.add_argument('upstream',type=Path)
args=parser.parse_args()
current_selection=json.loads((args.current/'selection.json').read_text())
old_selection=json.loads((args.upstream/'selection.json').read_text())
old_models={m['model_id']:m for m in old_selection['models']}
rows=[]; checks=[]; excluded=[]
for model in current_selection['models']:
    mid=model['model_id']; oldfile=args.upstream/'models'/f'{mid}.json'
    if mid not in old_models or not oldfile.exists():
        excluded.append(dict(model_id=mid,reason='Not in historical 100-model control sample'));continue
    new=json.loads((args.current/'models'/f'{mid}.json').read_text())
    old=json.loads(oldfile.read_text())
    assert new['status']==old['status']=='ok'
    for key in ('source_sha256','texture_sha256','buffer_sha256'):
        assert model[key]==old_models[mid][key]
    for key in ('geometry_sha256','texture_sha256','texture_sizes'):
        assert new['artifacts']['round1'][key]==old['artifacts']['round1'][key]
    assert new['measurement']['poses']==old['measurement']['poses']
    assert new['measurement']['viewport']==old['measurement']['viewport']
    for tau in [2,0.1]:
        nr={r['label']:r for r in new['measurement']['runs'] if r['tau']==tau}
        obr={r['label']:r for r in old['measurement']['runs'] if r['tau']==tau}
        nc={c['label']:c for c in new['measurement']['comparisons'] if c['reference']=='source' and c['tau']==tau and c['mode']=='textured'}
        oc={c['label']:c for c in old['measurement']['comparisons'] if c['reference']=='source' and c['tau']==tau and c['mode']=='textured'}
        for key in ('gpuBytes','geometryBytes','textureBytes','residentNodes','drawnTriangles'):
            assert nr['round1'][key]==obr['round1'][key]
        for key in ('psnrDb','meanAbsoluteChannelDifference','changedPixelsOver8Fraction','silhouetteIoU','modelPixels'):
            assert nc['round1'][key]==oc['round1'][key]
        assert obr['control']['allocationAuditPassed'] is True
        for variant in ['divisor1','divisor2']:
            r=nr[variant];ref=obr['control']
            rows.append(dict(model_id=mid,name=model['name'],requested_error_pixels=tau,variant=variant,
                upstream_gpu_mib=ref['gpuBytes']/1048576,gpu_mib=r['gpuBytes']/1048576,
                upstream_geometry_mib=ref['geometryBytes']/1048576,geometry_mib=r['geometryBytes']/1048576,
                upstream_texture_mib=ref['textureBytes']/1048576,texture_mib=r['textureBytes']/1048576,
                gpu_saving_pct=100*(1-r['gpuBytes']/ref['gpuBytes']),
                source_psnr_change_db=nc[variant]['psnrDb']-oc['control']['psnrDb'],
                source_psnr_db=nc[variant]['psnrDb'],upstream_source_psnr_db=oc['control']['psnrDb']))
    checks.append(dict(model_id=mid,source_and_camera_match=True,semantic_round1_payloads_match=True,
        baseline_allocations_and_source_metrics_match=True))
with (args.current/'upstream-comparison.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
summary=[]
for variant in ['divisor1','divisor2']:
    for tau in [2,0.1]:
        group=[r for r in rows if r['variant']==variant and r['requested_error_pixels']==tau]
        summary.append(dict(variant=variant,requested_error_pixels=tau,models=len(group),
            median_gpu_saving_pct=statistics.median(r['gpu_saving_pct'] for r in group),
            weighted_gpu_saving_pct=100*(1-sum(r['gpu_mib'] for r in group)/sum(r['upstream_gpu_mib'] for r in group)),
            median_source_psnr_change_db=statistics.median(r['source_psnr_change_db'] for r in group),
            worst_source_psnr_change_db=min(r['source_psnr_change_db'] for r in group)))
with (args.current/'upstream-aggregate.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,list(summary[0]),lineterminator='\n');writer.writeheader();writer.writerows(summary)
(args.current/'upstream-validation.json').write_text(json.dumps(dict(checks=checks,excluded=excluded,summary=summary),indent=2)+'\n')
print(json.dumps(summary,indent=2))
