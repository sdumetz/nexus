"""Relate fixed-view cache savings to prior texture burden and refinement.

Does not infer finite-budget stalls from unbounded-cache measurements.
"""
import argparse
import csv
import json
import math
from pathlib import Path
import statistics

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('current',type=Path)
p.add_argument('--historical',type=Path,default=Path('doc/measurements/isti-100'))
a=p.parse_args()
selection=json.loads((a.current/'selection.json').read_text())
comparisons={r['model_id']:r for r in csv.DictReader((a.current/'comparison-factor-1_5.csv').open())}
historical_rows={r['model_id']:r for r in csv.DictReader((a.historical/'graph.csv').open()) if r['quality_target_pixels']=='2' and r['status']=='ok'}
rows=[]
for model in selection['models']:
    mid=model['model_id'];state=json.loads((a.current/'models'/f'{mid}.json').read_text())
    report=state['measurement']
    upstream=next(r for r in report['runs'] if r['label']=='upstream' and r['tau']==2)
    candidate=next(r for r in report['runs'] if r['label']=='factor1_5' and r['tau']==2)
    oldfile=a.historical/'models'/f'{mid}.json'
    old=json.loads(oldfile.read_text()) if oldfile.exists() else None
    fine=next((r for r in old['measurement']['runs'] if r['label']=='control' and r['tau']==0.1),None) if old else None
    q=comparisons[mid]
    if old:
        baseline=next(r for r in old['measurement']['runs'] if r['label']=='control' and r['tau']==2)
        for k in ['gpuBytes','geometryBytes','textureBytes','residentNodes','drawnTriangles']:assert upstream[k]==baseline[k]
    rows.append(dict(model_id=mid,name=model['name'],input_triangles=model['input_triangles'],
        gpu_saving_pct=float(q['gpu_saving_pct']),upstream_gpu_mib=upstream['gpuBytes']/1048576,
        candidate_gpu_mib=candidate['gpuBytes']/1048576,
        upstream_texture_mib=upstream['textureBytes']/1048576,upstream_geometry_mib=upstream['geometryBytes']/1048576,
        candidate_texture_mib=candidate['textureBytes']/1048576,candidate_geometry_mib=candidate['geometryBytes']/1048576,
        upstream_texture_geometry_ratio=upstream['textureBytes']/upstream['geometryBytes'],
        upstream_texture_cache_fraction=upstream['textureBytes']/upstream['gpuBytes'],
        upstream_texture_bytes_per_drawn_triangle=upstream['textureBytes']/upstream['drawnTriangles'],
        upstream_resident_nodes=upstream['residentNodes'],candidate_resident_nodes=candidate['residentNodes'],total_nodes=upstream['totalNodes'],
        upstream_resident_node_fraction=upstream['residentNodes']/upstream['totalNodes'],
        upstream_drawn_triangles=upstream['drawnTriangles'],candidate_drawn_triangles=candidate['drawnTriangles'],
        drawn_triangle_change_pct=100*(candidate['drawnTriangles']/upstream['drawnTriangles']-1),
        source_psnr_change_db=float(q['source_psnr_change_db']),source_block_ssim_change=float(q['source_block_ssim_change']),
        retained_upstream_gradient_fraction=float(q['retained_upstream_gradient_fraction']),
        upstream_0_1px_gpu_mib=fine['gpuBytes']/1048576 if fine else None,
        upstream_2px_to_0_1px_cache_fraction=upstream['gpuBytes']/fine['gpuBytes'] if fine else None,
        upstream_0_1px_resident_node_fraction=fine['residentNodes']/fine['totalNodes'] if fine else None,
        upstream_0_1px_drawn_triangle_fraction=fine['drawnTriangles']/model['input_triangles'] if fine else None,
        historical_round2_vs_round1_2px_gpu_saving_pct=float(historical_rows[mid]['round2_vs_round1_gpu_saving_pct']) if mid in historical_rows else None))
with (a.current/'cache-correlation.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)

def rank(values):
    sorted_values=sorted(values)
    return [statistics.mean(i+1 for i,v in enumerate(sorted_values) if v==value) for value in values]

def pearson(x,y):
    mx,my=statistics.mean(x),statistics.mean(y)
    return sum((u-mx)*(v-my) for u,v in zip(x,y))/math.sqrt(sum((u-mx)**2 for u in x)*sum((v-my)**2 for v in y))

def correlation(field):
    subset=[r for r in rows if r[field] is not None]
    return dict(models=len(subset),spearman=pearson(rank([r[field] for r in subset]),rank([r['gpu_saving_pct'] for r in subset])))
fields=['upstream_texture_geometry_ratio','upstream_texture_bytes_per_drawn_triangle',
    'upstream_resident_node_fraction','upstream_2px_to_0_1px_cache_fraction',
    'historical_round2_vs_round1_2px_gpu_saving_pct']
saving={r['model_id'] for r in rows if r['gpu_saving_pct']>0}
top={r['model_id'] for r in sorted(rows,key=lambda r:r['upstream_texture_geometry_ratio'],reverse=True)[:len(saving)]}
summary=dict(models=len(rows),saving_models=sorted(saving),largest_texture_burden_models=sorted(top),
    saving_models_exactly_top_texture_burden=saving==top,correlations={field:correlation(field) for field in fields},
    upstream_2px_to_0_1px_cache_fraction_range=[min(r['upstream_2px_to_0_1px_cache_fraction'] for r in rows if r['upstream_2px_to_0_1px_cache_fraction'] is not None),max(r['upstream_2px_to_0_1px_cache_fraction'] for r in rows if r['upstream_2px_to_0_1px_cache_fraction'] is not None)],
    note='Small purposive sample; descriptive correlations, not significance tests. No finite-budget stall measurements exist in these runs.')
(a.current/'cache-correlation.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
for r in rows:print(r['model_id'],round(r['upstream_texture_geometry_ratio'],2),round(r['drawn_triangle_change_pct'],1),round(r['gpu_saving_pct'],1))
