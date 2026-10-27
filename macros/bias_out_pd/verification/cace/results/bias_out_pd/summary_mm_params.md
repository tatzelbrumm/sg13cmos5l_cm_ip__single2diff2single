
# CACE Summary for d2s_bias_out_pd

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Bias current bp      | ngspice              | Ibp                  |         4.93 uA |          ​ |          any |          ​ |      5.22 uA |          ​ |   Skip 🟧    |
| Bias current bn      | ngspice              | Ibn                  |         4.93 uA |          ​ |          any |          ​ |      5.12 uA |          ​ |   Skip 🟧    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.97 uA |          ​ |          any |          ​ |      2.14 uA |          ​ |   Skip 🟧    |
| Bias current bpc     | ngspice              | Ibpc                 |         1.93 uA |          ​ |          any |          ​ |      2.03 uA |          ​ |   Skip 🟧    |
| Bias current abp     | ngspice              | Iabp                 |         4.93 uA |          ​ |          any |          ​ |      5.19 uA |          ​ |   Skip 🟧    |
| Bias current abn     | ngspice              | Iabn                 |         4.93 uA |          ​ |          any |          ​ |      5.11 uA |          ​ |   Skip 🟧    |
| Supply current vdd   | ngspice              | Idd                  |             any |          ​ |          any |          ​ |        32 uA |          ​ |   Skip 🟧    |
| Supply current vddo  | ngspice              | Iddo                 |             any |          ​ |          any |          ​ |       6.7 uA |          ​ |   Skip 🟧    |
| Reference current at the iref pin | ngspice              | Iref                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |          ​ |          any |          ​ |      2.7 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |          ​ |          any |          ​ |      1.5 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |          ​ |          any |          ​ |      1.5 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |          ​ |          any |          ​ |      2.9 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |          ​ |          any |          ​ |      3.4 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |          ​ |          any |          ​ |      1.7 %/V |          ​ |   Skip 🟧    |
| Bias current bp - mismatch | ngspice              | Ibp                  |         4.93 uA |   5.014 uA |          any |   5.099 uA |      5.28 uA |   5.198 uA |   Pass ✅    |
| Bias current bn - mismatch | ngspice              | Ibn                  |         4.93 uA |   5.020 uA |          any |   5.060 uA |      5.15 uA |   5.104 uA |   Pass ✅    |
| Bias current bnc - mismatch | ngspice              | Ibnc                 |         1.97 uA |   2.054 uA |          any |   2.075 uA |      2.14 uA |   2.097 uA |   Pass ✅    |
| Bias current bpc - mismatch | ngspice              | Ibpc                 |         1.87 uA |   1.908 uA |          any |   1.967 uA |      2.04 uA |   2.028 uA |   Pass ✅    |
| Bias current abp - mismatch | ngspice              | Iabp                 |         4.93 uA |   5.048 uA |          any |   5.103 uA |      5.25 uA |   5.180 uA |   Pass ✅    |
| Bias current abn - mismatch | ngspice              | Iabn                 |         4.93 uA |   5.002 uA |          any |   5.057 uA |      5.15 uA |   5.106 uA |   Pass ✅    |
| Supply current vdd - mismatch | ngspice              | Idd                  |             any |  24.159 uA |          any |  24.288 uA |          any |  24.515 uA |   Pass ✅    |
| Supply current vddo - mismatch | ngspice              | Iddo                 |             any |   5.048 uA |          any |   5.103 uA |          any |   5.180 uA |   Pass ✅    |
| Reference current at the iref pin - mismatch | ngspice              | Iref                 |             any |   5.051 uA |          any |   5.052 uA |          any |   5.052 uA |   Pass ✅    |
| Line sensitivity bp - mismatch | ngspice              | Sbp                  |             any |  1.635 %/V |          any |  1.647 %/V |          any |  1.657 %/V |   Pass ✅    |
| Line sensitivity bn - mismatch | ngspice              | Sbn                  |             any |  0.890 %/V |          any |  0.893 %/V |          any |  0.897 %/V |   Pass ✅    |
| Line sensitivity bnc - mismatch | ngspice              | Sbnc                 |             any |  0.908 %/V |          any |  0.912 %/V |          any |  0.914 %/V |   Pass ✅    |
| Line sensitivity bpc - mismatch | ngspice              | Sbpc                 |             any |  1.711 %/V |          any |  1.726 %/V |          any |  1.742 %/V |   Pass ✅    |
| Line sensitivity abp - mismatch | ngspice              | Sabp                 |             any |  1.774 %/V |          any |  1.783 %/V |          any |  1.794 %/V |   Pass ✅    |
| Line sensitivity abn - mismatch | ngspice              | Sabn                 |             any |  0.957 %/V |          any |  0.960 %/V |          any |  0.964 %/V |   Pass ✅    |
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

