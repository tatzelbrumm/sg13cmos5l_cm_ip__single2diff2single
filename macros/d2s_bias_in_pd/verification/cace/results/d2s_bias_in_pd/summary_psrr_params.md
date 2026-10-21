
# CACE Summary for d2s_bias_in_pd

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Bias current bp      | ngspice              | Ibp                  |         4.93 uA |          ​ |          any |          ​ |      5.12 uA |          ​ |   Skip 🟧    |
| Bias current bn      | ngspice              | Ibn                  |         4.93 uA |          ​ |          any |          ​ |      5.13 uA |          ​ |   Skip 🟧    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.97 uA |          ​ |          any |          ​ |      2.14 uA |          ​ |   Skip 🟧    |
| Bias current bpc     | ngspice              | Ibpc                 |         1.91 uA |          ​ |          any |          ​ |      2.03 uA |          ​ |   Skip 🟧    |
| Bias current abp     | ngspice              | Iabp                 |         4.93 uA |          ​ |          any |          ​ |      5.09 uA |          ​ |   Skip 🟧    |
| Bias current abn     | ngspice              | Iabn                 |         4.93 uA |          ​ |          any |          ​ |      5.13 uA |          ​ |   Skip 🟧    |
| Supply current vdd   | ngspice              | Idd                  |             any |          ​ |          any |          ​ |        26 uA |          ​ |   Skip 🟧    |
| Supply current vddo  | ngspice              | Iddo                 |             any |          ​ |          any |          ​ |       6.6 uA |          ​ |   Skip 🟧    |
| Reference current at the iref pin | ngspice              | Iref                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |          ​ |          any |          ​ |      1.3 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |          ​ |          any |          ​ |      1.5 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |          ​ |          any |          ​ |      1.5 %/V |          ​ |   Skip 🟧    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |          ​ |          any |          ​ |      1.4 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |          ​ |          any |          ​ |      2.0 %/V |          ​ |   Skip 🟧    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |          ​ |          any |          ​ |      1.6 %/V |          ​ |   Skip 🟧    |
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
| Supply sensitivity vdd, 1kHz | ngspice              | P_vdd_1k             |             any |  0.812 %/V |          any |  0.953 %/V |      1.4 %/V |  1.056 %/V |   Pass ✅    |
| Supply sensitivity vdd, 100kHz | ngspice              | P_vdd_100k           |             any |  0.822 %/V |          any |  0.962 %/V |      1.4 %/V |  1.064 %/V |   Pass ✅    |
| Supply sensitivity vdd, 1MHz | ngspice              | P_vdd_1M             |             any |  1.589 %/V |          any |  1.655 %/V |      2.3 %/V |  1.713 %/V |   Pass ✅    |
| Supply sensitivity vss, 1kHz | ngspice              | P_vss_1k             |             any |  0.788 %/V |          any |  0.910 %/V |      1.5 %/V |  1.147 %/V |   Pass ✅    |
| Supply sensitivity vss, 100kHz | ngspice              | P_vss_100k           |             any |  0.811 %/V |          any |  0.929 %/V |      1.6 %/V |  1.158 %/V |   Pass ✅    |
| Supply sensitivity vss, 1MHz | ngspice              | P_vss_1M             |             any |  1.985 %/V |          any |  2.053 %/V |      2.8 %/V |  2.101 %/V |   Pass ✅    |
| Supply sensitivity vddo, 1kHz | ngspice              | P_vddo_1k            |             any |  0.920 %/V |          any |  1.225 %/V |      2.1 %/V |  1.557 %/V |   Pass ✅    |
| Supply sensitivity vddo, 100kHz | ngspice              | P_vddo_100k          |             any |  0.963 %/V |          any |  1.254 %/V |      2.1 %/V |  1.580 %/V |   Pass ✅    |
| Supply sensitivity vddo, 1MHz | ngspice              | P_vddo_1M            |             any |  2.954 %/V |          any |  2.986 %/V |      4.1 %/V |  3.088 %/V |   Pass ✅    |
| Supply sensitivity vsso, 1kHz | ngspice              | P_vsso_1k            |             any |  0.207 %/V |          any |  0.236 %/V |     0.35 %/V |  0.265 %/V |   Pass ✅    |
| Supply sensitivity vsso, 100kHz | ngspice              | P_vsso_100k          |             any |  0.271 %/V |          any |  0.287 %/V |     0.41 %/V |  0.309 %/V |   Pass ✅    |
| Supply sensitivity vsso, 1MHz | ngspice              | P_vsso_1M            |             any |  1.597 %/V |          any |  1.644 %/V |      2.3 %/V |  1.744 %/V |   Pass ✅    |
| Start-up time to 90 % bn current | ngspice              | t_su90               |             any |          ​ |          any |          ​ |        70 us |          ​ |   Skip 🟧    |
| bn current after start-up / dc | ngspice              | Rbn_end              |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| abp current after start-up / dc | ngspice              | Rabp_end             |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| Supply current vdd, disabled | ngspice              | Idd_off              |             any |          ​ |          any |          ​ |      0.91 nA |          ​ |   Skip 🟧    |
| Supply current vddo, disabled | ngspice              | Iddo_off             |             any |          ​ |          any |          ​ |     0.062 nA |          ​ |   Skip 🟧    |
| Current at the iref pin, disabled | ngspice              | Iref_off             |             any |          ​ |          any |          ​ |      0.47 nA |          ​ |   Skip 🟧    |
| Largest bias current, disabled | ngspice              | Ib_off               |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Enable time, bn current | ngspice              | t_en90_bn            |             any |          ​ |          any |          ​ |      0.21 us |          ​ |   Skip 🟧    |
| Enable time, abp current | ngspice              | t_en90_abp           |             any |          ​ |          any |          ​ |     0.092 us |          ​ |   Skip 🟧    |

