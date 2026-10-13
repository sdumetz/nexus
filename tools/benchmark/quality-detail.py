"""Diagnose softening with foreground-interior luminance gradient energy.

Pillow L conversion uses integer BT.601 luminance. RMS adjacent-pixel gradients
are measured in both images over the SAME mask: both pixels of the edge must
be foreground in both images. Image boundaries and silhouette edges excluded.
This is a softening diagnostic, not a standalone perceptual-quality score.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

p=argparse.ArgumentParser(description=__doc__);p.add_argument('out',type=Path);a=p.parse_args()
s=json.loads((a.out/'selection.json').read_text())

def mask(image):
    diff=ImageChops.difference(image,Image.new('RGB',image.size,(32,35,38)))
    r,g,b=diff.split()
    return ImageChops.lighter(ImageChops.lighter(r,g),b).point(lambda v:255 if v>2 else 0)

def energy_pair(reference,candidate):
    with Image.open(reference) as file:ref=file.convert('RGB')
    with Image.open(candidate) as file:img=file.convert('RGB')
    common=ImageChops.multiply(mask(ref),mask(img));ref=ref.convert('L');img=img.convert('L')
    w,h=ref.size; totals=[0,0]; edges=0
    for left,right in [((0,0,w-1,h),(1,0,w,h)),((0,0,w,h-1),(0,1,w,h))]:
        valid=ImageChops.multiply(common.crop(left),common.crop(right))
        n=valid.histogram()[255];edges+=n
        for k,image in enumerate([ref,img]):
            diff=ImageChops.difference(image.crop(left),image.crop(right))
            if n:totals[k]+=ImageStat.Stat(diff,valid).rms[0]**2*n
    return dict(reference_gradient_rms=(totals[0]/edges)**0.5 if edges else 0,
                candidate_gradient_rms=(totals[1]/edges)**0.5 if edges else 0,
                retained_gradient_fraction=(totals[1]/totals[0])**0.5 if totals[0] else 1,
                foreground_interior_edges=edges)
rows=[]
for model in s['models']:
    mid=model['model_id'];root=a.out/'screenshots'/mid
    for factor in s['factors']:
        label='factor'+format(factor,'g').replace('.','_')
        metrics=energy_pair(root/'upstream-v0-t2-textured.png',root/f'{label}-v0-t2-textured.png')
        rows.append(dict(model_id=mid,factor=factor,**metrics))
(a.out/'detail-diagnostics.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows:
    if row['factor'] in [.75,1,1.5,2]:print(row['model_id'],row['factor'],round(row['retained_gradient_fraction'],3))
