"""Measure UV-union occupancy of uncompressed, textured NXS node atlases.

Uses pixel-center scan conversion (no dilation), not image color/alpha. Requires
Pillow. Rejects compressed geometry and shared/multiple atlases rather than
silently miscounting. Heights are DAG distances from leaves, independent of error.
"""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import struct
from PIL import Image


def coverage(triangles, width, height):
    """Union of half-open scanline spans, counted once even for overlapping UVs.

    Pixel centers; horizontal edges excluded, lower y included / upper excluded.
    Exact edge ties may differ from OpenGL's fixed-point rasterization.
    """
    rows = [[] for _ in range(height)]
    fragments = 0
    uv_area = 0.0
    for tri in triangles:
        if not all(math.isfinite(c) for p in tri for c in p):
            raise ValueError('Non-finite UV')
        a, b, c = tri
        area = abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])) / 2
        uv_area += area
        if area == 0:
            continue
        points = [(u*width, v*height) for u,v in tri]
        edges = [(points[k], points[(k+1)%3]) for k in range(3)]
        lo = max(0, math.ceil(min(p[1] for p in points)-0.5))
        hi = min(height, math.ceil(max(p[1] for p in points)-0.5))
        for y in range(lo, hi):
            center = y+0.5
            xs = [p[0]+(center-p[1])*(q[0]-p[0])/(q[1]-p[1])
                  for p,q in edges if min(p[1],q[1]) <= center < max(p[1],q[1])]
            if len(xs) != 2:
                continue
            left = max(0, math.ceil(min(xs)-0.5))
            right = min(width, math.ceil(max(xs)-0.5))
            if right > left:
                rows[y].append((left,right))
                fragments += right-left
    covered = 0
    for spans in rows:
        end = 0
        for left,right in sorted(spans):
            covered += max(0,right-max(left,end))
            end = max(end,right)
    return dict(covered_texels=covered, allocated_texels=width*height,
                occupancy=covered/(width*height), overlap_fragments=fragments-covered,
                summed_uv_triangle_area=uv_area)


def read_nxs(path):
    data = path.read_bytes()
    magic,version = struct.unpack_from('<II', data)
    if magic != 0x4E787320 or version != 2:
        raise ValueError('Expected little-endian NXS v2')
    flags, count, patch_count, texture_count = struct.unpack_from('<IIII', data, 56)
    if flags != 0:
        raise ValueError('Only uncompressed inline NXS supported')
    # Current v4 exports: position float3, UV float2, normal short3; index ushort3.
    expected = bytes([7,3,3,3,0,0,7,2])+bytes(8)
    if data[24:40] != expected or data[40:56] != bytes([4,3])+bytes(14):
        raise ValueError('Unsupported vertex/face signature')
    nodes = [struct.unpack_from('<IHHf',data,88+44*i) for i in range(count)]
    first = [struct.unpack_from('<I',data,88+44*i+40)[0] for i in range(count)]
    patch_start = 88+44*count
    patches = [struct.unpack_from('<III',data,patch_start+12*i) for i in range(patch_count)]
    texture_start = patch_start+12*patch_count
    offsets = [struct.unpack_from('<I',data,texture_start+68*i)[0]*256 for i in range(texture_count)]
    sizes = []
    for start,end in zip(offsets, offsets[1:]):
        with Image.open(io.BytesIO(data[start:end])) as image:
            sizes.append(image.size)
    heights = [0]*(count-1)
    min_depth = [count]* (count-1)
    max_depth = [0]*(count-1)
    indegree = [0]*(count-1)
    children = []
    for i in range(count-1):
        ch = sorted({p[0] for p in patches[first[i]:first[i+1]] if p[0] != count-1})
        if any(j <= i or j >= count-1 for j in ch):
            raise ValueError('Expected parent-before-child DAG ordering')
        children.append(ch)
        for j in ch:
            indegree[j] += 1
    for i in range(count-2,-1,-1):
        heights[i] = 1+max(heights[j] for j in children[i]) if children[i] else 0
    for i in range(count-1):
        if indegree[i] == 0:
            min_depth[i] = 0
        for j in children[i]:
            min_depth[j] = min(min_depth[j], min_depth[i]+1)
            max_depth[j] = max(max_depth[j], max_depth[i]+1)
    used = set()
    result = []
    for i,(offset,nv,nf,error) in enumerate(nodes[:-1]):
        tex = {p[2] for p in patches[first[i]:first[i+1]]}
        if len(tex) != 1:
            raise ValueError('Expected exactly one texture per node')
        tid = tex.pop()
        if tid in used or tid >= len(sizes):
            raise ValueError('Shared or invalid texture; requires grouping faces by atlas')
        used.add(tid)
        start = offset*256
        uvs = list(struct.iter_unpack('<ff',data[start+12*nv:start+20*nv]))
        indices = list(struct.iter_unpack('<HHH',data[start+26*nv:start+26*nv+6*nf]))
        triangles = [tuple(uvs[j] for j in face) for face in indices]
        result.append((dict(node_id=i, texture_id=tid, vertices=nv, triangles=nf,
                            stored_error=error, height_from_leaves=heights[i],
                            min_depth_from_root=min_depth[i], max_depth_from_root=max_depth[i],
                            width=sizes[tid][0],height=sizes[tid][1]), triangles, uvs, indices))
    return result, hashlib.sha256(data).hexdigest()


def obj_triangles(path):
    uv, triangles = [], []
    for line in path.open():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == 'vt':
            uv.append(tuple(map(float,fields[1:3])))
        elif fields[0] == 'f':
            if len(fields) != 4:
                raise ValueError('Source OBJ must be triangulated')
            ids = [int(f.split('/')[1]) for f in fields[1:]]
            triangles.append(tuple(uv[j-1 if j>0 else j] for j in ids))
    return triangles


def write_csv(path, rows):
    with path.open('w',newline='') as stream:
        writer = csv.DictWriter(stream,list(rows[0]),lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)


def quantile(values, q):
    values = sorted(values)
    t = (len(values)-1)*q; lo = math.floor(t); hi = math.ceil(t)
    return values[lo]+(values[hi]-values[lo])*(t-lo)


def summarize(rows):
    groups = sorted({(r['model_id'],r['variant'],r['height_from_leaves']) for r in rows})
    groups += sorted({(r['model_id'],r['variant'],'all') for r in rows})
    summaries = []
    for model,variant,level in groups:
        subset = [r for r in rows if r['model_id']==model and r['variant']==variant
                  and (level=='all' or r['height_from_leaves']==level)]
        values = [r['occupancy'] for r in subset]
        allocated = sum(r['allocated_texels'] for r in subset)
        covered = sum(r['covered_texels'] for r in subset)
        summaries.append(dict(model_id=model,variant=variant,height_from_leaves=level,nodes=len(subset),
            allocated_texels=allocated,covered_texels=covered,unused_texels=allocated-covered,
            texel_weighted_occupancy=covered/allocated,mean_occupancy=statistics.mean(values),
            stddev_occupancy=statistics.pstdev(values),p10_occupancy=quantile(values,.1),
            median_occupancy=statistics.median(values),p90_occupancy=quantile(values,.9),
            min_occupancy=min(values),max_occupancy=max(values),
            reference_512_texel_weighted_occupancy=sum(r['reference_512_occupancy'] for r in subset)/len(subset)))
    return summaries


def export_obj(path, uvs, indices):
    # Dummy geometry: occupancy depends only on UVs. Use UV-plane positions to
    # avoid degenerate triangles in independent TexMetro validation.
    with path.open('w') as stream:
        for u,v in uvs: stream.write(f'v {u:.17g} {v:.17g} 0\n')
        for u,v in uvs: stream.write(f'vt {u:.17g} {v:.17g}\n')
        for face in indices: stream.write('f '+' '.join(f'{j+1}/{j+1}' for j in face)+'\n')


def finest_comparison(rows, sources, models):
    result=[]
    for model in models:
        mid=model['model_id']
        source=next(s for s in sources if s['model_id']==mid)
        for variant in sorted({r['variant'] for r in rows}):
            finest=[r for r in rows if r['model_id']==mid and r['variant']==variant
                    and r['height_from_leaves']==0]
            faces=sum(r['triangles'] for r in finest)
            if faces != model['input_triangles']:
                raise ValueError(f'{mid}: finest cut has {faces} triangles, expected {model["input_triangles"]}')
            allocated=sum(r['allocated_texels'] for r in finest)
            covered=sum(r['covered_texels'] for r in finest)
            result.append(dict(model_id=mid,name=model['name'],variant=variant,
                source_triangles=model['input_triangles'],finest_triangles=faces,finest_nodes=len(finest),
                source_occupancy=source['occupancy'],finest_texel_weighted_occupancy=covered/allocated,
                occupancy_change_percentage_points=100*(covered/allocated-source['occupancy']),
                source_allocated_texels=source['allocated_texels'],finest_allocated_texels=allocated,
                finest_to_source_allocated_texels_ratio=allocated/source['allocated_texels'],
                source_covered_texels=source['covered_texels'],finest_covered_texels=covered))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selection',type=Path,default=Path('doc/measurements/isti-quality-2px-10/selection.json'))
    p.add_argument('--scratch',type=Path,default=Path('/tmp/nexus-quality-sweep-10'))
    p.add_argument('--sources',type=Path,default=Path('/tmp/nexus-texture-precision-10'))
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--nxs',action='append',help='Standalone mode: LABEL=/path/model.nxs (repeatable)')
    p.add_argument('--model-id',default='model',help='Model ID for standalone mode')
    a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    if a.nxs:
        rows=[]; inputs=[]
        for value in a.nxs:
            label,filename=value.split('=',1)
            nodes,digest=read_nxs(Path(filename))
            inputs.append(dict(variant=label,file=filename,sha256=digest))
            for info,triangles,uvs,indices in nodes:
                row=dict(model_id=a.model_id,variant=label,**info)
                row.update(coverage(triangles,info['width'],info['height']))
                row['reference_512_occupancy']=coverage(triangles,512,512)['occupancy']
                rows.append(row)
        write_csv(a.out/'nodes.csv',rows)
        write_csv(a.out/'summary.csv',summarize(rows))
        (a.out/'provenance.json').write_text(json.dumps(inputs,indent=2)+'\n')
        return
    models=json.loads(a.selection.read_text())['models']; rows=[]; sources=[]; inputs=[]
    variants={'upstream':'upstream/test.nxs','factor1_5':'sweep/model.factor1_5.nxs','factor2':'sweep/model.factor2.nxs'}
    for model in models:
        mid=model['model_id']
        obj=a.sources/mid/'source/model.obj'
        source=dict(model_id=mid,name=model['name'],width=model['input_texture_width'],height=model['input_texture_height'])
        source.update(coverage(obj_triangles(obj),source['width'],source['height']))
        sources.append(source)
        for variant,relative in variants.items():
            path=a.scratch/mid/relative
            nodes,digest=read_nxs(path)
            inputs.append(dict(model_id=mid,variant=variant,file=str(path),sha256=digest))
            for info,triangles,uvs,indices in nodes:
                row=dict(model_id=mid,variant=variant,**info)
                row.update(coverage(triangles,info['width'],info['height']))
                row['reference_512_occupancy']=coverage(triangles,512,512)['occupancy']
                rows.append(row)
            # Two representative upstream nodes/model for independent raster checks.
            if variant=='upstream':
                for height in (0,1):
                    choices=[n for n in nodes if n[0]['height_from_leaves']==height]
                    if choices:
                        info,triangles,uvs,indices=max(choices,key=lambda n:n[0]['triangles'])
                        export_obj(a.out/f'{mid}-height{height}-node{info["node_id"]}.obj',uvs,indices)
            print(mid,variant,len(nodes),flush=True)
    write_csv(a.out/'nodes.csv',rows)
    write_csv(a.out/'summary.csv',summarize(rows))
    write_csv(a.out/'source-occupancy.csv',sources)
    write_csv(a.out/'finest-comparison.csv',finest_comparison(rows,sources,models))
    (a.out/'provenance.json').write_text(json.dumps(dict(selection=str(a.selection),inputs=inputs,
        metric='Pixel-center UV triangle union / actual atlas texels; no padding dilation',
        reference_resolution=[512,512],source_obj_sha256={m['model_id']:hashlib.sha256((a.sources/m['model_id']/'source/model.obj').read_bytes()).hexdigest() for m in models}),indent=2)+'\n')

if __name__=='__main__': main()
