# Aggregate ISTI results

Completed 100 of 100 selected models.

[Plotting CSV](graph.csv) · [Detailed CSV](results.csv) · [Method and columns](README.md)

GPU savings compare round 2 with round 1 at the same camera and quality target. Models receive equal weight in medians; byte-weighted savings compare the sum of cache bytes.

| Target pixels | Valid models | Models saving cache | Median saving | Mean saving | Byte-weighted saving | Models saving ≥25% | Models with >1% changed pixels |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 98 | 8 | 0.00% | 2.08% | 5.81% | 3 | 3 |
| 0.1 | 98 | 61 | 4.63% | 16.63% | 23.00% | 31 | 2 |

Changed pixels use an 8/255 maximum RGB-channel difference over foreground pixels. This threshold is a diagnostic, not a perceptual equivalence guarantee.

| Target pixels | All nodes resident in round 1 | Identical textured images | Identical shaded images | Median round 1/control cache ratio | Median source-relative PSNR improvement, round 1/control | Median source-relative PSNR change, round 2/round 1 |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0 | 92 | 98 | 3.642 | 2.533 dB | 0.000 dB |
| 0.1 | 96 | 40 | 98 | 1.000 | 0.000 dB | -0.013 dB |

Model status counts: `{"failed": 2, "ok": 98}`.

Control/round 1 geometry mismatches: 0. Round 1/round 2 geometry mismatches: 0.

## Cases to inspect

| Model | Target | Cache saving | Textured PSNR between rounds | Pixels differing >8/255 | Captures |
|---|---:|---:|---:|---:|---|
| RWT256 | 2 | 17.29% | 41.38 dB | 2.11% | [PNGs](screenshots/RWT256/) |
| RWT292 | 2 | 51.88% | 41.48 dB | 2.02% | [PNGs](screenshots/RWT292/) |
| RWT292 | 0.1 | 68.56% | 41.91 dB | 1.69% | [PNGs](screenshots/RWT292/) |
| RWT319 | 0.1 | 57.23% | 37.71 dB | 3.85% | [PNGs](screenshots/RWT319/) |
| RWT471 | 2 | 79.10% | 41.67 dB | 1.29% | [PNGs](screenshots/RWT471/) |
