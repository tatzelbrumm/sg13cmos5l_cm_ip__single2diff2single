
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
| Bias current bp - mismatch | ngspice              | Ibp                  |         4.93 uA |   4.947 uA |          any |   5.027 uA |      5.23 uA |   5.164 uA |   Pass ✅    |
| Bias current bn - mismatch | ngspice              | Ibn                  |         4.93 uA |   4.949 uA |          any |   5.044 uA |      5.25 uA |   5.176 uA |   Pass ✅    |
| Bias current bnc - mismatch | ngspice              | Ibnc                 |         1.97 uA |   2.030 uA |          any |   2.072 uA |      2.17 uA |   2.122 uA |   Pass ✅    |
| Bias current bpc - mismatch | ngspice              | Ibpc                 |         1.83 uA |   1.880 uA |          any |   1.942 uA |      2.03 uA |   2.016 uA |   Pass ✅    |
| Bias current abp - mismatch | ngspice              | Iabp                 |          4.9 uA |   4.926 uA |          any |   5.045 uA |      5.18 uA |   5.130 uA |   Pass ✅    |
| Bias current abn - mismatch | ngspice              | Iabn                 |          4.9 uA |   4.929 uA |          any |   5.033 uA |      5.25 uA |   5.177 uA |   Pass ✅    |
| Supply current vdd - mismatch | ngspice              | Idd                  |             any |  18.802 uA |          any |  19.085 uA |          any |  19.626 uA |   Pass ✅    |
| Supply current vddo - mismatch | ngspice              | Iddo                 |             any |   4.926 uA |          any |   5.045 uA |          any |   5.130 uA |   Pass ✅    |
| Reference current at the iref pin - mismatch | ngspice              | Iref                 |             any |   5.009 uA |          any |   5.009 uA |          any |   5.009 uA |   Pass ✅    |
| Line sensitivity bp - mismatch | ngspice              | Sbp                  |             any |  0.757 %/V |          any |  0.763 %/V |          any |  0.766 %/V |   Pass ✅    |
| Line sensitivity bn - mismatch | ngspice              | Sbn                  |             any |  0.884 %/V |          any |  0.889 %/V |          any |  0.894 %/V |   Pass ✅    |
| Line sensitivity bnc - mismatch | ngspice              | Sbnc                 |             any |  0.903 %/V |          any |  0.907 %/V |          any |  0.911 %/V |   Pass ✅    |
| Line sensitivity bpc - mismatch | ngspice              | Sbpc                 |             any |  0.836 %/V |          any |  0.842 %/V |          any |  0.848 %/V |   Pass ✅    |
| Line sensitivity abp - mismatch | ngspice              | Sabp                 |             any |  0.893 %/V |          any |  0.899 %/V |          any |  0.904 %/V |   Pass ✅    |
| Line sensitivity abn - mismatch | ngspice              | Sabn                 |             any |  0.951 %/V |          any |  0.956 %/V |          any |  0.960 %/V |   Pass ✅    |
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

