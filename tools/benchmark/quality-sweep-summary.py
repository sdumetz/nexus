"""Produce graphable quality/cache curves and conservative quality-matched choices.

Accept quality if PSNR loss <=0.1dB, block SSIM loss <=0.002, and
source-relative luminance-gradient RMSE growth <=2%. All three constraints
are per model, never applied to a mean that can cancel quality losses.
"""
import argparse
import csv
import json
from pathlib import Path
import statistics

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('out',type=Path)
p.add_argument('--allow-partial',action='store_true')
p.add_argument('--psnr-loss',type=float,default=0.1)
p.add_argument('--ssim-loss',type=float,default=0.002)
p.add_argument('--gradient-growth',type=float,default=2)
p.add_argument('--min-detail-retention',type=float,default=0)
a=p.parse_args()
selection=json.loads((a.out/'selection.json').read_text())
detail_file=a.out/'detail-diagnostics.json'
details={(r['model_id'],r['factor']):r for r in json.loads(detail_file.read_text())} if detail_file.exists() else {}
if a.min_detail_retention>0: assert details, 'Run quality-detail.py first'
rows=[]; checks=[]
for model in selection['models']:
    file=a.out/'models'/f"{model['model_id']}.json"
    if not file.exists() or json.loads(file.read_text())['status']!='ok':
        if a.allow_partial: continue
        raise ValueError(f'Incomplete: {file}')
    state=json.loads(file.read_text()); report=state['measurement']
    assert len({v['geometry_sha256'] for v in state['artifacts'].values()})==1
    runs={(r['label'],r['tau']):r for r in report['runs'] if r['label']!='source'}
    metrics={(c['label'],c['tau'],c['reference'],c['mode']):c for c in report['comparisons']}
    prior_file=a.out.parent/'isti-precision-10/models'/f"{model['model_id']}.json"
    prior_match=None
    if prior_file.exists():
        prior=json.loads(prior_file.read_text())
        for label,previous_label in [('factor1','divisor1'),('factor2','divisor2')]:
            if label not in state['artifacts']:continue
            for key in ['geometry_sha256','texture_sha256','texture_sizes']:
                assert state['artifacts'][label][key]==prior['artifacts'][previous_label][key]
            for tau in selection['requested_errors']:
                old_run=next(r for r in prior['measurement']['runs'] if r['label']==previous_label and r['tau']==tau)
                for key in ['gpuBytes','geometryBytes','textureBytes','residentNodes','drawnTriangles']:
                    assert runs[label,tau][key]==old_run[key]
                old_metric=next(c for c in prior['measurement']['comparisons'] if c['label']==previous_label and c['reference']=='source' and c['tau']==tau and c['mode']=='textured')
                for key in ['psnrDb','meanAbsoluteChannelDifference','changedPixelsOver8Fraction','silhouetteIoU','modelPixels']:
                    assert metrics[label,tau,'source','textured'][key]==old_metric[key]
        prior_match=True
    historical=a.out.parent/'isti-100/models'/f"{model['model_id']}.json"
    historical_match=None
    if historical.exists():
        old=json.loads(historical.read_text())
        assert old['status']=='ok'
        for key in ['geometry_sha256','texture_sha256','texture_sizes','file_bytes']:
            assert state['artifacts']['upstream'][key]==old['artifacts']['control'][key], (model['model_id'],key)
        assert report['poses']==old['measurement']['poses']
        for tau in [t for t in [2,0.1] if t in selection['requested_errors']]:
            old_run=next(r for r in old['measurement']['runs'] if r['label']=='control' and r['tau']==tau)
            for key in ['gpuBytes','geometryBytes','textureBytes','residentNodes','drawnTriangles']:
                assert runs['upstream',tau][key]==old_run[key]
            old_metric=next(c for c in old['measurement']['comparisons'] if c['label']=='control' and c['reference']=='source' and c['tau']==tau and c['mode']=='textured')
            for key in ['psnrDb','meanAbsoluteChannelDifference','changedPixelsOver8Fraction','silhouetteIoU','modelPixels']:
                assert metrics['upstream',tau,'source','textured'][key]==old_metric[key]
        historical_match=True
    for tau in selection['requested_errors']:
        ref=runs['upstream',tau]; quality=metrics['upstream',tau,'source','textured']
        assert ref['allocationAuditPassed']
        for factor in selection['factors']:
            label='factor'+format(factor,'g').replace('.','_')
            r=runs[label,tau]; q=metrics[label,tau,'source','textured']; direct=metrics[label,tau,'upstream','textured']
            assert r['allocationAuditPassed'] and r['gpuBytes']==r['geometryBytes']+r['textureBytes']
            psnr=q['psnrDb']-quality['psnrDb']; ssim=q['blockSsim']-quality['blockSsim']
            gradient=100*(q['luminanceGradientRmse']/quality['luminanceGradientRmse']-1)
            artifact=state['artifacts'][label]; control=state['artifacts']['upstream']
            retained=details.get((model['model_id'],factor),{}).get('retained_gradient_fraction')
            rows.append(dict(model_id=model['model_id'],name=model['name'],requested_error_pixels=tau,factor=factor,
                upstream_gpu_mib=ref['gpuBytes']/1048576,gpu_mib=r['gpuBytes']/1048576,
                gpu_saving_pct=100*(1-r['gpuBytes']/ref['gpuBytes']),
                upstream_geometry_mib=ref['geometryBytes']/1048576,geometry_mib=r['geometryBytes']/1048576,
                upstream_texture_mib=ref['textureBytes']/1048576,texture_mib=r['textureBytes']/1048576,
                upstream_source_psnr_db=quality['psnrDb'],source_psnr_db=q['psnrDb'],source_psnr_change_db=psnr,
                upstream_source_block_ssim=quality['blockSsim'],source_block_ssim=q['blockSsim'],source_block_ssim_change=ssim,
                upstream_source_gradient_rmse=quality['luminanceGradientRmse'],source_gradient_rmse=q['luminanceGradientRmse'],source_gradient_change_pct=gradient,
                retained_upstream_gradient_fraction=retained,
                quality_accepted=psnr>=-a.psnr_loss and ssim>=-a.ssim_loss and gradient<=a.gradient_growth
                    and (not a.min_detail_retention or retained>=a.min_detail_retention),
                strict_quality_accepted=psnr>=-0.1 and ssim>=-0.002 and gradient<=2,
                vs_upstream_changed_pixels_fraction=direct['changedPixelsOver8Fraction'],
                vs_upstream_silhouette_iou=direct['silhouetteIoU'],
                shaded_identical=metrics[label,tau,'upstream','shaded']['identical'],
                upstream_file_bytes=control['file_bytes'],file_bytes=artifact['file_bytes'],
                file_saving_pct=100*(1-artifact['file_bytes']/control['file_bytes']),
                upstream_base_texels=control['export_base_texels'],base_texels=artifact['export_base_texels']))
    checks.append(dict(model_id=model['model_id'],geometry_match=True,all_allocation_audits_passed=True,
        historical_upstream_payloads_camera_allocations_and_metrics_match=historical_match,
        prior_factor1_factor2_payloads_allocations_and_metrics_match=prior_match))

def write(name, data):
    if not data: return
    with (a.out/name).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,list(data[0]),lineterminator='\n');writer.writeheader();writer.writerows(data)

def aggregate(group):
    return dict(models=len(group),quality_accepted=sum(r['quality_accepted'] for r in group),
        median_gpu_saving_pct=statistics.median(r['gpu_saving_pct'] for r in group),
        weighted_gpu_saving_pct=100*(1-sum(r['gpu_mib'] for r in group)/sum(r['upstream_gpu_mib'] for r in group)),
        median_source_psnr_change_db=statistics.median(r['source_psnr_change_db'] for r in group),
        worst_source_psnr_change_db=min(r['source_psnr_change_db'] for r in group),
        worst_source_block_ssim_change=min(r['source_block_ssim_change'] for r in group),
        worst_source_gradient_change_pct=max(r['source_gradient_change_pct'] for r in group),
        worst_retained_upstream_gradient_fraction=min(r['retained_upstream_gradient_fraction'] for r in group) if details else None,
        median_file_saving_pct=statistics.median(r['file_saving_pct'] for r in group),
        weighted_file_saving_pct=100*(1-sum(r['file_bytes'] for r in group)/sum(r['upstream_file_bytes'] for r in group)))
write('graph.csv',rows)
summary=[]; matched=[]; global_choices=[]
for tau in selection['requested_errors']:
    for factor in selection['factors']:
        group=[r for r in rows if r['requested_error_pixels']==tau and r['factor']==factor]
        if group: summary.append(dict(requested_error_pixels=tau,factor=factor,**aggregate(group)))
    choices=[r for r in summary if r['requested_error_pixels']==tau and r['quality_accepted']==r['models']]
    if choices: global_choices.append(min(choices,key=lambda r:-r['weighted_gpu_saving_pct']))
    for model in selection['models']:
        group=[r for r in rows if r['requested_error_pixels']==tau and r['model_id']==model['model_id']]
        accepted=[r for r in group if r['quality_accepted']]
        if accepted: matched.append(min(accepted,key=lambda r:r['gpu_mib']))
write('aggregate.csv',summary);write('matched-per-model.csv',matched);write('global-matched.csv',global_choices)
matched_summary=[]
for tau in selection['requested_errors']:
    group=[r for r in matched if r['requested_error_pixels']==tau]
    if group: matched_summary.append(dict(requested_error_pixels=tau,**aggregate(group)))
write('matched-aggregate.csv',matched_summary)
(a.out/'validation.json').write_text(json.dumps(dict(criteria=dict(psnr_loss_db=a.psnr_loss,block_ssim_loss=a.ssim_loss,
    gradient_rmse_growth_pct=a.gradient_growth if a.gradient_growth!=float('inf') else None,
    minimum_upstream_gradient_retention=a.min_detail_retention),
    checks=checks,global_choices=global_choices,matched_summary=matched_summary),indent=2)+'\n')
print(json.dumps(dict(global_choices=global_choices,matched_summary=matched_summary),indent=2))
