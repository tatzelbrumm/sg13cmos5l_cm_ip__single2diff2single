
# CACE Summary for d2s_bias_out_pd

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Bias current bp      | ngspice              | Ibp                  |         4.93 uA |   5.066 uA |          any |   5.112 uA |      5.22 uA |   5.170 uA |   Pass ✅    |
| Bias current bn      | ngspice              | Ibn                  |         4.93 uA |   5.036 uA |          any |   5.060 uA |      5.12 uA |   5.090 uA |   Pass ✅    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.97 uA |   2.048 uA |          any |   2.076 uA |      2.14 uA |   2.104 uA |   Pass ✅    |
| Bias current bpc     | ngspice              | Ibpc                 |         1.93 uA |   1.945 uA |          any |   1.964 uA |      2.03 uA |   1.981 uA |   Pass ✅    |
| Bias current abp     | ngspice              | Iabp                 |         4.93 uA |   5.038 uA |          any |   5.095 uA |      5.19 uA |   5.147 uA |   Pass ✅    |
| Bias current abn     | ngspice              | Iabn                 |         4.93 uA |   5.029 uA |          any |   5.055 uA |      5.11 uA |   5.086 uA |   Pass ✅    |
| Supply current vdd   | ngspice              | Idd                  |             any |  24.162 uA |          any |  24.322 uA |        32 uA |  24.506 uA |   Pass ✅    |
| Supply current vddo  | ngspice              | Iddo                 |             any |   5.038 uA |          any |   5.095 uA |       6.7 uA |   5.147 uA |   Pass ✅    |
| Reference current at the iref pin | ngspice              | Iref                 |             any |   5.029 uA |          any |   5.051 uA |          any |   5.078 uA |   Pass ✅    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |  1.357 %/V |          any |  1.670 %/V |      2.7 %/V |  2.042 %/V |   Pass ✅    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |  0.740 %/V |          any |  0.899 %/V |      1.5 %/V |  1.103 %/V |   Pass ✅    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |  0.758 %/V |          any |  0.923 %/V |      1.5 %/V |  1.124 %/V |   Pass ✅    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |  1.400 %/V |          any |  1.737 %/V |      2.9 %/V |  2.159 %/V |   Pass ✅    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |  1.369 %/V |          any |  1.784 %/V |      3.4 %/V |  2.558 %/V |   Pass ✅    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |  0.784 %/V |          any |  0.971 %/V |      1.7 %/V |  1.237 %/V |   Pass ✅    |
| Bias current bp - mismatch | ngspice              | Ibp                  |         4.93 uA |          ​ |          any |          ​ |      5.28 uA |          ​ |   Skip 🟧    |
| Bias current bn - mismatch | ngspice              | Ibn                  |         4.93 uA |          ​ |          any |          ​ |      5.15 uA |          ​ |   Skip 🟧    |
| Bias current bnc - mismatch | ngspice              | Ibnc                 |         1.97 uA |          ​ |          any |          ​ |      2.14 uA |          ​ |   Skip 🟧    |
| Bias current bpc - mismatch | ngspice              | Ibpc                 |         1.87 uA |          ​ |          any |          ​ |      2.04 uA |          ​ |   Skip 🟧    |
| Bias current abp - mismatch | ngspice              | Iabp                 |         4.93 uA |          ​ |          any |          ​ |      5.25 uA |          ​ |   Skip 🟧    |
| Bias current abn - mismatch | ngspice              | Iabn                 |         4.93 uA |          ​ |          any |          ​ |      5.15 uA |          ​ |   Skip 🟧    |
| Supply current vdd - mismatch | ngspice              | Idd                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Supply current vddo - mismatch | ngspice              | Iddo                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Reference current at the iref pin - mismatch | ngspice              | Iref                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bp - mismatch | ngspice              | Sbp                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bn - mismatch | ngspice              | Sbn                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bnc - mismatch | ngspice              | Sbnc                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bpc - mismatch | ngspice              | Sbpc                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity abp - mismatch | ngspice              | Sabp                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity abn - mismatch | ngspice              | Sabn                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 1kHz | ngspice              | P_vdd_1k             |             any |          ​ |          any |          ​ |      1.4 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 100kHz | ngspice              | P_vdd_100k           |             any |          ​ |          any |          ​ |      1.5 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 1MHz | ngspice              | P_vdd_1M             |             any |          ​ |          any |          ​ |      3.0 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1kHz | ngspice              | P_vss_1k             |             any |          ​ |          any |          ​ |      1.7 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 100kHz | ngspice              | P_vss_100k           |             any |          ​ |          any |          ​ |      1.7 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1MHz | ngspice              | P_vss_1M             |             any |          ​ |          any |          ​ |      3.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1kHz | ngspice              | P_vddo_1k            |             any |          ​ |          any |          ​ |      2.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 100kHz | ngspice              | P_vddo_100k          |             any |          ​ |          any |          ​ |      2.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1MHz | ngspice              | P_vddo_1M            |             any |          ​ |          any |          ​ |      4.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1kHz | ngspice              | P_vsso_1k            |             any |          ​ |          any |          ​ |     0.35 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 100kHz | ngspice              | P_vsso_100k          |             any |          ​ |          any |          ​ |     0.41 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1MHz | ngspice              | P_vsso_1M            |             any |          ​ |          any |          ​ |      2.3 %/V |          ​ |   Skip 🟧    |
| Start-up time to 90 % bn current | ngspice              | t_su90               |             any |          ​ |          any |          ​ |        71 us |          ​ |   Skip 🟧    |
| bn current after start-up / dc | ngspice              | Rbn_end              |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| abp current after start-up / dc | ngspice              | Rabp_end             |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| Supply current vdd, disabled | ngspice              | Idd_off              |             any |          ​ |          any |          ​ |       1.5 nA |          ​ |   Skip 🟧    |
| Supply current vddo, disabled | ngspice              | Iddo_off             |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Current at the iref pin, disabled | ngspice              | Iref_off             |             any |          ​ |          any |          ​ |      0.49 nA |          ​ |   Skip 🟧    |
| Largest bias current, disabled | ngspice              | Ib_off               |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Enable time, bn current | ngspice              | t_en90_bn            |             any |          ​ |          any |          ​ |       0.2 us |          ​ |   Skip 🟧    |
| Enable time, abp current | ngspice              | t_en90_abp           |             any |          ​ |          any |          ​ |       0.2 us |          ​ |   Skip 🟧    |

