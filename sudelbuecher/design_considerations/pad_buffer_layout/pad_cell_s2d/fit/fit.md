# Tentative fit of the s2d blocks into template version 4

Free region: 10638 µm² (x 1.8–78.2, y 32.68–180.0, minus the protection zone, the rppds and the iovdd risers with 1.5 / 0.5 µm keep-out). Placement only, no wiring.

| block | cell | group | drawn w × h (µm) | area µm² |
|---|---|---|---|---:|
| inputs | `s2d_inputs` | xa | 47.00 × 28.80 | 1354 |
| tails | `s2d_tails` | xa | 45.79 × 23.76 | 1088 |
| loads | `s2d_loads` | xa | 45.79 × 15.76 | 722 |
| casc_p | `s2d_casc_p` | xa | 52.41 × 13.86 | 726 |
| casc_n | `s2d_casc_n` | xa | 67.66 × 14.94 | 1011 |
| sinks | `sinks_6x6_s2d_c2` | xa | 16.51 × 51.68 | 853 |
| sinks_cmfb | `s2d_sinks_cmfb` | xa | 32.87 × 18.12 | 596 |
| rhigh | `s2d_rhigh` | xa | 20.20 × 19.90 | 402 |
| pd_p | `s2d_pd_p` | xa | 3.20 × 2.24 | 7 |
| pd_n | `s2d_pd_n` | xa | 2.50 × 2.04 | 5 |
| cload | `s2d_cload` | xa (cload) | 26.50 × 14.61 | 387 |
| tree_n | `bias_tree_n` | xt | 27.42 × 11.11 | 305 |
| tree_p | `bias_tree_p` | xt | 18.79 × 11.63 | 219 |
| tree_sw | `bias_tree_sw` | xt | 2.50 × 2.04 | 5 |
| tree_swp | `bias_tree_swp` | xt | 2.37 × 4.00 | 9 |

## Variant A: drawn cells, 2 µm between boxes

- placed: casc_n, casc_p, inputs, tails, loads, sinks_cmfb, tree_n, cload, rhigh, tree_p, sinks, pd_p, pd_n, tree_sw, tree_swp
- left out: none
- cells placed 7689 of 7689 µm² (xa 6764 / 6764, cload 387 / 387, xt 538 / 538); 72% of the free region
- highest placed box top: y 178.3

## Variant B: drawn cells, 4 µm between boxes

- placed: inputs, tails, casc_n, sinks, casc_p, loads, sinks_cmfb, rhigh, tree_p, tree_swp, pd_p, pd_n, tree_sw
- left out: cload, tree_n
- cells placed 6997 of 7689 µm² (xa 6764 / 6764, cload 0 / 387, xt 233 / 538); 66% of the free region
- highest placed box top: y 175.6

## Variant C: C2-compacted box estimates, 4 µm between boxes

- placed: cload, loads, tree_sw, tails, casc_n, pd_p, casc_p, sinks, tree_swp, sinks_cmfb, inputs, pd_n, tree_n, rhigh, tree_p
- left out: none
- cells placed 7259 of 7259 µm² (xa 6428 / 6428, cload 387 / 387, xt 444 / 444); 68% of the free region
- highest placed box top: y 178.8
