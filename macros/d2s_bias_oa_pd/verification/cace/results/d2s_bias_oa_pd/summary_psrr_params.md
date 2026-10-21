
# CACE Summary for d2s_bias_oa_pd

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Bias current bp      | ngspice              | Ibp                  |         2.51 uA |          ​ |          any |          ​ |      7.76 uA |          ​ |   Skip 🟧    |
| Bias current bn      | ngspice              | Ibn                  |         2.52 uA |          ​ |          any |          ​ |      7.78 uA |          ​ |   Skip 🟧    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.06 uA |          ​ |          any |          ​ |      3.18 uA |          ​ |   Skip 🟧    |
| Bias current bpc     | ngspice              | Ibpc                 |        0.935 uA |          ​ |          any |          ​ |      2.97 uA |          ​ |   Skip 🟧    |
| Bias current abp     | ngspice              | Iabp                 |         2.47 uA |          ​ |          any |          ​ |      7.76 uA |          ​ |   Skip 🟧    |
| Bias current abn     | ngspice              | Iabn                 |         2.51 uA |          ​ |          any |          ​ |      7.78 uA |          ​ |   Skip 🟧    |
| Supply current vdd   | ngspice              | Idd                  |             any |          ​ |          any |          ​ |        50 uA |          ​ |   Skip 🟧    |
| Supply current vddo  | ngspice              | Iddo                 |             any |          ​ |          any |          ​ |       9.3 uA |          ​ |   Skip 🟧    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |          ​ |          any |          ​ |      1.7 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |          ​ |          any |          ​ |      1.9 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |          ​ |          any |          ​ |      1.9 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |          ​ |          any |          ​ |      1.8 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |          ​ |          any |          ​ |      2.3 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |          ​ |          any |          ​ |      2.0 %/V |          ​ |   Skip 🟧    |
| Bias current bp - mismatch | ngspice              | Ibp                  |         4.44 uA |          ​ |          any |          ​ |      5.73 uA |          ​ |   Skip 🟧    |
| Bias current bn - mismatch | ngspice              | Ibn                  |         4.46 uA |          ​ |          any |          ​ |      5.76 uA |          ​ |   Skip 🟧    |
| Bias current bnc - mismatch | ngspice              | Ibnc                 |         1.85 uA |          ​ |          any |          ​ |      2.38 uA |          ​ |   Skip 🟧    |
| Bias current bpc - mismatch | ngspice              | Ibpc                 |         1.71 uA |          ​ |          any |          ​ |       2.2 uA |          ​ |   Skip 🟧    |
| Bias current abp - mismatch | ngspice              | Iabp                 |         4.48 uA |          ​ |          any |          ​ |      5.68 uA |          ​ |   Skip 🟧    |
| Bias current abn - mismatch | ngspice              | Iabn                 |         4.42 uA |          ​ |          any |          ​ |      5.75 uA |          ​ |   Skip 🟧    |
| Supply current vdd - mismatch | ngspice              | Idd                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Supply current vddo - mismatch | ngspice              | Iddo                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bp - mismatch | ngspice              | Sbp                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bn - mismatch | ngspice              | Sbn                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bnc - mismatch | ngspice              | Sbnc                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bpc - mismatch | ngspice              | Sbpc                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity abp - mismatch | ngspice              | Sabp                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity abn - mismatch | ngspice              | Sabn                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 1kHz | ngspice              | P_vdd_1k             |             any |  0.690 %/V |          any |  1.117 %/V |      3.2 %/V |  2.395 %/V |   Pass ✅    |
| Supply sensitivity vdd, 100kHz | ngspice              | P_vdd_100k           |             any |  3.248 %/V |          any |  4.516 %/V |      8.4 %/V |  6.434 %/V |   Pass ✅    |
| Supply sensitivity vdd, 1MHz | ngspice              | P_vdd_1M             |             any |  3.302 %/V |          any |  4.584 %/V |      8.5 %/V |  6.467 %/V |   Pass ✅    |
| Supply sensitivity vss, 1kHz | ngspice              | P_vss_1k             |             any |  0.860 %/V |          any |  1.046 %/V |      2.0 %/V |  1.468 %/V |   Pass ✅    |
| Supply sensitivity vss, 100kHz | ngspice              | P_vss_100k           |             any |  3.185 %/V |          any |  4.430 %/V |      8.5 %/V |  6.478 %/V |   Pass ✅    |
| Supply sensitivity vss, 1MHz | ngspice              | P_vss_1M             |             any |  3.362 %/V |          any |  4.687 %/V |      9.0 %/V |  6.871 %/V |   Pass ✅    |
| Supply sensitivity vddo, 1kHz | ngspice              | P_vddo_1k            |             any |  0.848 %/V |          any |  1.225 %/V |      2.3 %/V |  1.716 %/V |   Pass ✅    |
| Supply sensitivity vddo, 100kHz | ngspice              | P_vddo_100k          |             any |  0.872 %/V |          any |  1.254 %/V |      2.4 %/V |  1.771 %/V |   Pass ✅    |
| Supply sensitivity vddo, 1MHz | ngspice              | P_vddo_1M            |             any |  2.178 %/V |          any |  2.976 %/V |      6.1 %/V |  4.678 %/V |   Pass ✅    |
| Supply sensitivity vsso, 1kHz | ngspice              | P_vsso_1k            |             any |  0.206 %/V |          any |  0.236 %/V |     0.35 %/V |  0.268 %/V |   Pass ✅    |
| Supply sensitivity vsso, 100kHz | ngspice              | P_vsso_100k          |             any |  0.261 %/V |          any |  0.301 %/V |     0.46 %/V |  0.351 %/V |   Pass ✅    |
| Supply sensitivity vsso, 1MHz | ngspice              | P_vsso_1M            |             any |  1.247 %/V |          any |  1.644 %/V |      3.4 %/V |  2.581 %/V |   Pass ✅    |
| Start-up time to 90 % bn current | ngspice              | t_su90               |             any |          ​ |          any |          ​ |       130 us |          ​ |   Skip 🟧    |
| bn current after start-up / dc | ngspice              | Rbn_end              |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| abp current after start-up / dc | ngspice              | Rabp_end             |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| Supply current vdd, disabled | ngspice              | Idd_off              |             any |          ​ |          any |          ​ |       1.4 nA |          ​ |   Skip 🟧    |
| Supply current vddo, disabled | ngspice              | Iddo_off             |             any |          ​ |          any |          ​ |     0.062 nA |          ​ |   Skip 🟧    |
| Largest bias current, disabled | ngspice              | Ib_off               |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Enable time, bn current | ngspice              | t_en90_bn            |             any |          ​ |          any |          ​ |        21 us |          ​ |   Skip 🟧    |
| Enable time, abp current | ngspice              | t_en90_abp           |             any |          ​ |          any |          ​ |        21 us |          ​ |   Skip 🟧    |

