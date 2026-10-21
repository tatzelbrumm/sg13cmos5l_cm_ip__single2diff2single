
# CACE Summary for d2s_bias_bg_pd

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Bias current bp      | ngspice              | Ibp                  |         4.92 uA |          ​ |          any |          ​ |      5.12 uA |          ​ |   Skip 🟧    |
| Bias current bn      | ngspice              | Ibn                  |         4.93 uA |          ​ |          any |          ​ |      5.14 uA |          ​ |   Skip 🟧    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.97 uA |          ​ |          any |          ​ |      2.12 uA |          ​ |   Skip 🟧    |
| Bias current bpc     | ngspice              | Ibpc                 |         1.86 uA |          ​ |          any |          ​ |      2.03 uA |          ​ |   Skip 🟧    |
| Bias current abp     | ngspice              | Iabp                 |         4.87 uA |          ​ |          any |          ​ |       5.1 uA |          ​ |   Skip 🟧    |
| Bias current abn     | ngspice              | Iabn                 |         4.92 uA |          ​ |          any |          ​ |      5.13 uA |          ​ |   Skip 🟧    |
| Supply current vdd   | ngspice              | Idd                  |             any |          ​ |          any |          ​ |        39 uA |          ​ |   Skip 🟧    |
| Supply current vddo  | ngspice              | Iddo                 |             any |          ​ |          any |          ​ |       6.7 uA |          ​ |   Skip 🟧    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |          ​ |          any |          ​ |      2.7 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |          ​ |          any |          ​ |      2.9 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |          ​ |          any |          ​ |      2.9 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |          ​ |          any |          ​ |      2.8 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |          ​ |          any |          ​ |      3.4 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |          ​ |          any |          ​ |      3.0 %/V |          ​ |   Skip 🟧    |
| Bias current bp      | ngspice              | Ibp                  |          3.7 uA |   4.001 uA |          any |   5.061 uA |      6.94 uA |   6.492 uA |   Pass ✅    |
| Bias current bn      | ngspice              | Ibn                  |         3.71 uA |   4.009 uA |          any |   5.071 uA |      6.95 uA |   6.502 uA |   Pass ✅    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.54 uA |   1.644 uA |          any |   2.080 uA |      2.87 uA |   2.667 uA |   Pass ✅    |
| Bias current bpc     | ngspice              | Ibpc                 |          1.4 uA |   1.537 uA |          any |   1.944 uA |      2.64 uA |   2.494 uA |   Pass ✅    |
| Bias current abp     | ngspice              | Iabp                 |         3.68 uA |   3.984 uA |          any |   5.043 uA |      6.91 uA |   6.471 uA |   Pass ✅    |
| Bias current abn     | ngspice              | Iabn                 |         3.71 uA |   4.005 uA |          any |   5.065 uA |      6.94 uA |   6.495 uA |   Pass ✅    |
| Supply current vdd   | ngspice              | Idd                  |             any |  23.555 uA |          any |  29.696 uA |        50 uA |  37.980 uA |   Pass ✅    |
| Supply current vddo  | ngspice              | Iddo                 |             any |   3.984 uA |          any |   5.043 uA |          any |   6.471 uA |   Pass ✅    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |  1.234 %/V |          any |  1.251 %/V |          any |  1.282 %/V |   Pass ✅    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |  1.365 %/V |          any |  1.377 %/V |          any |  1.404 %/V |   Pass ✅    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |  1.389 %/V |          any |  1.394 %/V |          any |  1.420 %/V |   Pass ✅    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |  1.319 %/V |          any |  1.332 %/V |          any |  1.360 %/V |   Pass ✅    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |  1.377 %/V |          any |  1.388 %/V |          any |  1.408 %/V |   Pass ✅    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |  1.441 %/V |          any |  1.443 %/V |          any |  1.463 %/V |   Pass ✅    |
| Bias current bp - mismatch | ngspice              | Ibp                  |         4.49 uA |          ​ |          any |          ​ |       5.6 uA |          ​ |   Skip 🟧    |
| Bias current bn - mismatch | ngspice              | Ibn                  |         4.51 uA |          ​ |          any |          ​ |      5.59 uA |          ​ |   Skip 🟧    |
| Bias current bnc - mismatch | ngspice              | Ibnc                 |         1.87 uA |          ​ |          any |          ​ |      2.32 uA |          ​ |   Skip 🟧    |
| Bias current bpc - mismatch | ngspice              | Ibpc                 |         1.68 uA |          ​ |          any |          ​ |      2.12 uA |          ​ |   Skip 🟧    |
| Bias current abp - mismatch | ngspice              | Iabp                 |         4.44 uA |          ​ |          any |          ​ |      5.51 uA |          ​ |   Skip 🟧    |
| Bias current abn - mismatch | ngspice              | Iabn                 |          4.5 uA |          ​ |          any |          ​ |      5.58 uA |          ​ |   Skip 🟧    |
| Supply current vdd - mismatch | ngspice              | Idd                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Supply current vddo - mismatch | ngspice              | Iddo                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bp - mismatch | ngspice              | Sbp                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bn - mismatch | ngspice              | Sbn                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bnc - mismatch | ngspice              | Sbnc                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bpc - mismatch | ngspice              | Sbpc                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity abp - mismatch | ngspice              | Sabp                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity abn - mismatch | ngspice              | Sabn                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 1kHz | ngspice              | P_vdd_1k             |             any |          ​ |          any |          ​ |      2.2 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 100kHz | ngspice              | P_vdd_100k           |             any |          ​ |          any |          ​ |      3.6 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 1MHz | ngspice              | P_vdd_1M             |             any |          ​ |          any |          ​ |       27 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1kHz | ngspice              | P_vss_1k             |             any |          ​ |          any |          ​ |      2.3 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 100kHz | ngspice              | P_vss_100k           |             any |          ​ |          any |          ​ |      3.7 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1MHz | ngspice              | P_vss_1M             |             any |          ​ |          any |          ​ |       27 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1kHz | ngspice              | P_vddo_1k            |             any |          ​ |          any |          ​ |      2.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 100kHz | ngspice              | P_vddo_100k          |             any |          ​ |          any |          ​ |      2.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1MHz | ngspice              | P_vddo_1M            |             any |          ​ |          any |          ​ |      4.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1kHz | ngspice              | P_vsso_1k            |             any |          ​ |          any |          ​ |     0.35 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 100kHz | ngspice              | P_vsso_100k          |             any |          ​ |          any |          ​ |     0.41 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1MHz | ngspice              | P_vsso_1M            |             any |          ​ |          any |          ​ |      2.3 %/V |          ​ |   Skip 🟧    |
| Start-up time to 90 % bn current | ngspice              | t_su90               |             any |          ​ |          any |          ​ |       120 us |          ​ |   Skip 🟧    |
| bn current after start-up / dc | ngspice              | Rbn_end              |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| abp current after start-up / dc | ngspice              | Rabp_end             |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| Supply current vdd, disabled | ngspice              | Idd_off              |             any |          ​ |          any |          ​ |       5.6 nA |          ​ |   Skip 🟧    |
| Supply current vddo, disabled | ngspice              | Iddo_off             |             any |          ​ |          any |          ​ |     0.062 nA |          ​ |   Skip 🟧    |
| Largest bias current, disabled | ngspice              | Ib_off               |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Enable time, bn current | ngspice              | t_en90_bn            |             any |          ​ |          any |          ​ |      0.38 us |          ​ |   Skip 🟧    |
| Enable time, abp current | ngspice              | t_en90_abp           |             any |          ​ |          any |          ​ |      0.33 us |          ​ |   Skip 🟧    |

