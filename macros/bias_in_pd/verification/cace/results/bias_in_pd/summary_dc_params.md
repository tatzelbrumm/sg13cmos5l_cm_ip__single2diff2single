
# CACE Summary for d2s_bias_in_pd

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Bias current bp      | ngspice              | Ibp                  |         4.93 uA |   5.039 uA |          any |   5.062 uA |      5.12 uA |   5.089 uA |   Pass ✅    |
| Bias current bn      | ngspice              | Ibn                  |         4.93 uA |   5.046 uA |          any |   5.071 uA |      5.13 uA |   5.102 uA |   Pass ✅    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.97 uA |   2.052 uA |          any |   2.080 uA |      2.14 uA |   2.109 uA |   Pass ✅    |
| Bias current bpc     | ngspice              | Ibpc                 |         1.91 uA |   1.933 uA |          any |   1.945 uA |      2.03 uA |   1.956 uA |   Pass ✅    |
| Bias current abp     | ngspice              | Iabp                 |         4.93 uA |   5.005 uA |          any |   5.043 uA |      5.09 uA |   5.070 uA |   Pass ✅    |
| Bias current abn     | ngspice              | Iabn                 |         4.93 uA |   5.039 uA |          any |   5.065 uA |      5.13 uA |   5.097 uA |   Pass ✅    |
| Supply current vdd   | ngspice              | Idd                  |             any |  19.120 uA |          any |  19.223 uA |        26 uA |  19.344 uA |   Pass ✅    |
| Supply current vddo  | ngspice              | Iddo                 |             any |   5.005 uA |          any |   5.043 uA |       6.6 uA |   5.070 uA |   Pass ✅    |
| Reference current at the iref pin | ngspice              | Iref                 |             any |   5.008 uA |          any |   5.009 uA |          any |   5.011 uA |   Pass ✅    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |  0.627 %/V |          any |  0.784 %/V |      1.3 %/V |  0.950 %/V |   Pass ✅    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |  0.743 %/V |          any |  0.900 %/V |      1.5 %/V |  1.095 %/V |   Pass ✅    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |  0.759 %/V |          any |  0.914 %/V |      1.5 %/V |  1.115 %/V |   Pass ✅    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |  0.671 %/V |          any |  0.848 %/V |      1.4 %/V |  1.065 %/V |   Pass ✅    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |  0.627 %/V |          any |  0.888 %/V |      2.0 %/V |  1.470 %/V |   Pass ✅    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |  0.787 %/V |          any |  0.968 %/V |      1.6 %/V |  1.227 %/V |   Pass ✅    |
| Bias current bp - mismatch | ngspice              | Ibp                  |         4.93 uA |          ​ |          any |          ​ |      5.23 uA |          ​ |   Skip 🟧    |
| Bias current bn - mismatch | ngspice              | Ibn                  |         4.93 uA |          ​ |          any |          ​ |      5.25 uA |          ​ |   Skip 🟧    |
| Bias current bnc - mismatch | ngspice              | Ibnc                 |         1.97 uA |          ​ |          any |          ​ |      2.17 uA |          ​ |   Skip 🟧    |
| Bias current bpc - mismatch | ngspice              | Ibpc                 |         1.83 uA |          ​ |          any |          ​ |      2.03 uA |          ​ |   Skip 🟧    |
| Bias current abp - mismatch | ngspice              | Iabp                 |          4.9 uA |          ​ |          any |          ​ |      5.18 uA |          ​ |   Skip 🟧    |
| Bias current abn - mismatch | ngspice              | Iabn                 |          4.9 uA |          ​ |          any |          ​ |      5.25 uA |          ​ |   Skip 🟧    |
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
| Supply sensitivity vdd, 100kHz | ngspice              | P_vdd_100k           |             any |          ​ |          any |          ​ |      1.4 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 1MHz | ngspice              | P_vdd_1M             |             any |          ​ |          any |          ​ |      2.3 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1kHz | ngspice              | P_vss_1k             |             any |          ​ |          any |          ​ |      1.5 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 100kHz | ngspice              | P_vss_100k           |             any |          ​ |          any |          ​ |      1.6 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1MHz | ngspice              | P_vss_1M             |             any |          ​ |          any |          ​ |      2.8 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1kHz | ngspice              | P_vddo_1k            |             any |          ​ |          any |          ​ |      2.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 100kHz | ngspice              | P_vddo_100k          |             any |          ​ |          any |          ​ |      2.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1MHz | ngspice              | P_vddo_1M            |             any |          ​ |          any |          ​ |      4.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1kHz | ngspice              | P_vsso_1k            |             any |          ​ |          any |          ​ |     0.35 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 100kHz | ngspice              | P_vsso_100k          |             any |          ​ |          any |          ​ |     0.41 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1MHz | ngspice              | P_vsso_1M            |             any |          ​ |          any |          ​ |      2.3 %/V |          ​ |   Skip 🟧    |
| Start-up time to 90 % bn current | ngspice              | t_su90               |             any |          ​ |          any |          ​ |        70 us |          ​ |   Skip 🟧    |
| bn current after start-up / dc | ngspice              | Rbn_end              |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| abp current after start-up / dc | ngspice              | Rabp_end             |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| Supply current vdd, disabled | ngspice              | Idd_off              |             any |          ​ |          any |          ​ |      0.91 nA |          ​ |   Skip 🟧    |
| Supply current vddo, disabled | ngspice              | Iddo_off             |             any |          ​ |          any |          ​ |     0.062 nA |          ​ |   Skip 🟧    |
| Current at the iref pin, disabled | ngspice              | Iref_off             |             any |          ​ |          any |          ​ |      0.47 nA |          ​ |   Skip 🟧    |
| Largest bias current, disabled | ngspice              | Ib_off               |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Enable time, bn current | ngspice              | t_en90_bn            |             any |          ​ |          any |          ​ |      0.21 us |          ​ |   Skip 🟧    |
| Enable time, abp current | ngspice              | t_en90_abp           |             any |          ​ |          any |          ​ |     0.092 us |          ​ |   Skip 🟧    |

