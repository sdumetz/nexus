# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 80 | 2.473 | 3.167 | 5.639 | 5.420 |
| fine | 0 | 2 | 80 | 2.473 | 3.167 | 5.639 | 5.420 |
| reconstruction | 0 | 2 | 45 | 1.465 | 0.937 | 2.403 | 2.471 |
| reconstructionFine | 0 | 2 | 45 | 1.465 | 0.937 | 2.403 | 2.471 |
| round1 | 0 | 0.5 | 154 | 4.487 | 24.833 | 29.320 | 21.066 |
| fine | 0 | 0.5 | 154 | 4.487 | 24.833 | 29.320 | 21.066 |
| reconstruction | 0 | 0.5 | 129 | 3.827 | 13.500 | 17.327 | 13.742 |
| reconstructionFine | 0 | 0.5 | 129 | 3.827 | 13.500 | 17.327 | 13.742 |
| round1 | 0 | 0.1 | 221 | 6.077 | 95.166 | 101.244 | 60.142 |
| fine | 0 | 0.1 | 221 | 6.077 | 60.205 | 66.283 | 42.176 |
| reconstruction | 0 | 0.1 | 221 | 6.077 | 95.166 | 101.244 | 60.142 |
| reconstructionFine | 0 | 0.1 | 221 | 6.077 | 60.205 | 66.283 | 42.176 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.39 | 48.681% | 0.99879 |
| round1 / source | 0 | 2 | shaded | 29.20 | 20.090% | 0.99884 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.39 | 48.681% | 0.99879 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 29.20 | 20.090% | 0.99884 |
| reconstruction / round1 | 0 | 2 | textured | 24.73 | 50.515% | 0.99916 |
| reconstruction / fine | 0 | 2 | textured | 24.73 | 50.515% | 0.99916 |
| reconstruction / source | 0 | 2 | textured | 24.70 | 60.598% | 0.99821 |
| reconstruction / round1 | 0 | 2 | shaded | 33.41 | 6.156% | 0.99920 |
| reconstruction / fine | 0 | 2 | shaded | 33.41 | 6.156% | 0.99920 |
| reconstruction / source | 0 | 2 | shaded | 28.02 | 23.752% | 0.99825 |
| reconstructionFine / round1 | 0 | 2 | textured | 24.73 | 50.515% | 0.99916 |
| reconstructionFine / fine | 0 | 2 | textured | 24.73 | 50.515% | 0.99916 |
| reconstructionFine / reconstruction | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | textured | 24.70 | 60.598% | 0.99821 |
| reconstructionFine / round1 | 0 | 2 | shaded | 33.41 | 6.156% | 0.99920 |
| reconstructionFine / fine | 0 | 2 | shaded | 33.41 | 6.156% | 0.99920 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 28.02 | 23.752% | 0.99825 |
| round1 / source | 0 | 0.5 | textured | 29.65 | 28.911% | 0.99970 |
| round1 / source | 0 | 0.5 | shaded | 29.88 | 18.344% | 0.99976 |
| fine / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 29.65 | 28.911% | 0.99970 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 29.88 | 18.344% | 0.99976 |
| reconstruction / round1 | 0 | 0.5 | textured | 30.95 | 16.790% | 0.99978 |
| reconstruction / fine | 0 | 0.5 | textured | 30.95 | 16.790% | 0.99978 |
| reconstruction / source | 0 | 0.5 | textured | 28.28 | 35.605% | 0.99957 |
| reconstruction / round1 | 0 | 0.5 | shaded | 42.66 | 0.721% | 0.99983 |
| reconstruction / fine | 0 | 0.5 | shaded | 42.66 | 0.721% | 0.99983 |
| reconstruction / source | 0 | 0.5 | shaded | 29.75 | 18.796% | 0.99959 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 30.95 | 16.790% | 0.99978 |
| reconstructionFine / fine | 0 | 0.5 | textured | 30.95 | 16.790% | 0.99978 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | textured | 28.28 | 35.605% | 0.99957 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | 42.66 | 0.721% | 0.99983 |
| reconstructionFine / fine | 0 | 0.5 | shaded | 42.66 | 0.721% | 0.99983 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 29.75 | 18.796% | 0.99959 |
| round1 / source | 0 | 0.1 | textured | 31.92 | 19.423% | 0.99998 |
| round1 / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 32.70 | 16.745% | 0.99996 |
| fine / source | 0 | 0.1 | textured | 31.64 | 21.067% | 0.99998 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | textured | 32.70 | 16.745% | 0.99996 |
| reconstruction / source | 0 | 0.1 | textured | 31.92 | 19.423% | 0.99998 |
| reconstruction / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | 32.70 | 16.745% | 0.99996 |
| reconstructionFine / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | 32.70 | 16.745% | 0.99996 |
| reconstructionFine / source | 0 | 0.1 | textured | 31.64 | 21.067% | 0.99998 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
