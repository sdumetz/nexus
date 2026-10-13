"""Analytic fixtures for occupancy union, clipping and byte weighting."""
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('occupancy',Path(__file__).with_name('texture-occupancy.py'))
occ=importlib.util.module_from_spec(spec); spec.loader.exec_module(occ)

class OccupancyTests(unittest.TestCase):
    def test_square_and_overlap(self):
        a=((0,0),(1,0),(0,1)); b=((1,0),(1,1),(0,1))
        self.assertEqual(occ.coverage([a,b],8,8)['covered_texels'],64)
        doubled=occ.coverage([a,b,a,b],8,8)
        self.assertEqual(doubled['covered_texels'],64)
        self.assertEqual(doubled['overlap_fragments'],64)
        self.assertEqual(doubled['summed_uv_triangle_area'],2)

    def test_orientation_and_degenerate(self):
        a=((0,0),(1,0),(0,1))
        self.assertEqual(occ.coverage([a],8,8)['covered_texels'],28)
        self.assertEqual(occ.coverage([tuple(reversed(a))],8,8)['covered_texels'],28)
        self.assertEqual(occ.coverage([((0,0),(0,0),(1,1))],8,8)['covered_texels'],0)

    def test_clip(self):
        tris=[((-1,-1),(2,-1),(-1,2)),((2,-1),(2,2),(-1,2))]
        self.assertEqual(occ.coverage(tris,4,4)['covered_texels'],16)

    def test_weighting(self):
        rows=[dict(model_id='x',variant='test',height_from_leaves=0,allocated_texels=100,
                   covered_texels=10,occupancy=.1,reference_512_occupancy=.1),
              dict(model_id='x',variant='test',height_from_leaves=0,allocated_texels=900,
                   covered_texels=810,occupancy=.9,reference_512_occupancy=.9)]
        s=occ.summarize(rows)[0]
        self.assertAlmostEqual(s['mean_occupancy'],.5)
        self.assertAlmostEqual(s['texel_weighted_occupancy'],.82)
        self.assertAlmostEqual(s['stddev_occupancy'],.4)

if __name__=='__main__': unittest.main()
