
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
| Supply sensitivity vdd, 1kHz | ngspice              | P_vdd_1k             |             any |  0.795 %/V |          any |  0.969 %/V |      1.4 %/V |  1.065 %/V |   Pass ✅    |
| Supply sensitivity vdd, 100kHz | ngspice              | P_vdd_100k           |             any |  0.821 %/V |          any |  0.990 %/V |      1.5 %/V |  1.085 %/V |   Pass ✅    |
| Supply sensitivity vdd, 1MHz | ngspice              | P_vdd_1M             |             any |  2.149 %/V |          any |  2.231 %/V |      3.0 %/V |  2.302 %/V |   Pass ✅    |
| Supply sensitivity vss, 1kHz | ngspice              | P_vss_1k             |             any |  0.834 %/V |          any |  1.022 %/V |      1.7 %/V |  1.276 %/V |   Pass ✅    |
| Supply sensitivity vss, 100kHz | ngspice              | P_vss_100k           |             any |  0.856 %/V |          any |  1.041 %/V |      1.7 %/V |  1.292 %/V |   Pass ✅    |
| Supply sensitivity vss, 1MHz | ngspice              | P_vss_1M             |             any |  2.078 %/V |          any |  2.190 %/V |      3.1 %/V |  2.352 %/V |   Pass ✅    |
| Supply sensitivity vddo, 1kHz | ngspice              | P_vddo_1k            |             any |  0.920 %/V |          any |  1.224 %/V |      2.1 %/V |  1.557 %/V |   Pass ✅    |
| Supply sensitivity vddo, 100kHz | ngspice              | P_vddo_100k          |             any |  0.962 %/V |          any |  1.254 %/V |      2.1 %/V |  1.579 %/V |   Pass ✅    |
| Supply sensitivity vddo, 1MHz | ngspice              | P_vddo_1M            |             any |  2.950 %/V |          any |  2.982 %/V |      4.1 %/V |  3.087 %/V |   Pass ✅    |
| Supply sensitivity vsso, 1kHz | ngspice              | P_vsso_1k            |             any |  0.207 %/V |          any |  0.235 %/V |     0.35 %/V |  0.265 %/V |   Pass ✅    |
| Supply sensitivity vsso, 100kHz | ngspice              | P_vsso_100k          |             any |  0.271 %/V |          any |  0.287 %/V |     0.41 %/V |  0.309 %/V |   Pass ✅    |
| Supply sensitivity vsso, 1MHz | ngspice              | P_vsso_1M            |             any |  1.614 %/V |          any |  1.662 %/V |      2.3 %/V |  1.765 %/V |   Pass ✅    |
| Start-up time to 90 % bn current | ngspice              | t_su90               |             any |          ​ |          any |          ​ |        71 us |          ​ |   Skip 🟧    |
| bn current after start-up / dc | ngspice              | Rbn_end              |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| abp current after start-up / dc | ngspice              | Rabp_end             |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| Supply current vdd, disabled | ngspice              | Idd_off              |             any |          ​ |          any |          ​ |       1.5 nA |          ​ |   Skip 🟧    |
| Supply current vddo, disabled | ngspice              | Iddo_off             |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Current at the iref pin, disabled | ngspice              | Iref_off             |             any |          ​ |          any |          ​ |      0.49 nA |          ​ |   Skip 🟧    |
| Largest bias current, disabled | ngspice              | Ib_off               |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Enable time, bn current | ngspice              | t_en90_bn            |             any |          ​ |          any |          ​ |       0.2 us |          ​ |   Skip 🟧    |
| Enable time, abp current | ngspice              | t_en90_abp           |             any |          ​ |          any |          ​ |       0.2 us |          ​ |   Skip 🟧    |

