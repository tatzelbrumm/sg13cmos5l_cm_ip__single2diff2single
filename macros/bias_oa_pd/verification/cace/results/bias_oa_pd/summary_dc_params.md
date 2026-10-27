
# CACE Summary for d2s_bias_oa_pd

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Bias current bp      | ngspice              | Ibp                  |         2.51 uA |   3.085 uA |          any |   5.052 uA |      7.76 uA |   7.125 uA |   Pass ✅    |
| Bias current bn      | ngspice              | Ibn                  |         2.52 uA |   3.090 uA |          any |   5.061 uA |      7.78 uA |   7.141 uA |   Pass ✅    |
| Bias current bnc     | ngspice              | Ibnc                 |         1.06 uA |   1.277 uA |          any |   2.076 uA |      3.18 uA |   2.907 uA |   Pass ✅    |
| Bias current bpc     | ngspice              | Ibpc                 |        0.935 uA |   1.181 uA |          any |   1.941 uA |      2.97 uA |   2.745 uA |   Pass ✅    |
| Bias current abp     | ngspice              | Iabp                 |         2.47 uA |   3.057 uA |          any |   5.033 uA |      7.76 uA |   7.122 uA |   Pass ✅    |
| Bias current abn     | ngspice              | Iabn                 |         2.51 uA |   3.085 uA |          any |   5.056 uA |      7.78 uA |   7.135 uA |   Pass ✅    |
| Supply current vdd   | ngspice              | Idd                  |             any |  16.866 uA |          any |  27.393 uA |        50 uA |  38.445 uA |   Pass ✅    |
| Supply current vddo  | ngspice              | Iddo                 |             any |   3.057 uA |          any |   5.033 uA |       9.3 uA |   7.122 uA |   Pass ✅    |
| Line sensitivity bp  | ngspice              | Sbp                  |             any |  0.660 %/V |          any |  0.911 %/V |      1.7 %/V |  1.307 %/V |   Pass ✅    |
| Line sensitivity bn  | ngspice              | Sbn                  |             any |  0.780 %/V |          any |  1.028 %/V |      1.9 %/V |  1.424 %/V |   Pass ✅    |
| Line sensitivity bnc | ngspice              | Sbnc                 |             any |  0.804 %/V |          any |  1.048 %/V |      1.9 %/V |  1.423 %/V |   Pass ✅    |
| Line sensitivity bpc | ngspice              | Sbpc                 |             any |  0.711 %/V |          any |  0.974 %/V |      1.8 %/V |  1.356 %/V |   Pass ✅    |
| Line sensitivity abp | ngspice              | Sabp                 |             any |  0.663 %/V |          any |  1.028 %/V |      2.3 %/V |  1.745 %/V |   Pass ✅    |
| Line sensitivity abn | ngspice              | Sabn                 |             any |  0.820 %/V |          any |  1.090 %/V |      2.0 %/V |  1.478 %/V |   Pass ✅    |
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
| Supply sensitivity vdd, 1kHz | ngspice              | P_vdd_1k             |             any |          ​ |          any |          ​ |      3.2 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 100kHz | ngspice              | P_vdd_100k           |             any |          ​ |          any |          ​ |      8.4 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vdd, 1MHz | ngspice              | P_vdd_1M             |             any |          ​ |          any |          ​ |      8.5 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1kHz | ngspice              | P_vss_1k             |             any |          ​ |          any |          ​ |      2.0 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 100kHz | ngspice              | P_vss_100k           |             any |          ​ |          any |          ​ |      8.5 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vss, 1MHz | ngspice              | P_vss_1M             |             any |          ​ |          any |          ​ |      9.0 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1kHz | ngspice              | P_vddo_1k            |             any |          ​ |          any |          ​ |      2.3 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 100kHz | ngspice              | P_vddo_100k          |             any |          ​ |          any |          ​ |      2.4 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vddo, 1MHz | ngspice              | P_vddo_1M            |             any |          ​ |          any |          ​ |      6.1 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1kHz | ngspice              | P_vsso_1k            |             any |          ​ |          any |          ​ |     0.35 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 100kHz | ngspice              | P_vsso_100k          |             any |          ​ |          any |          ​ |     0.46 %/V |          ​ |   Skip 🟧    |
| Supply sensitivity vsso, 1MHz | ngspice              | P_vsso_1M            |             any |          ​ |          any |          ​ |      3.4 %/V |          ​ |   Skip 🟧    |
| Start-up time to 90 % bn current | ngspice              | t_su90               |             any |          ​ |          any |          ​ |       130 us |          ​ |   Skip 🟧    |
| bn current after start-up / dc | ngspice              | Rbn_end              |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| abp current after start-up / dc | ngspice              | Rabp_end             |            0.95 |          ​ |          any |          ​ |         1.05 |          ​ |   Skip 🟧    |
| Supply current vdd, disabled | ngspice              | Idd_off              |             any |          ​ |          any |          ​ |       1.4 nA |          ​ |   Skip 🟧    |
| Supply current vddo, disabled | ngspice              | Iddo_off             |             any |          ​ |          any |          ​ |     0.062 nA |          ​ |   Skip 🟧    |
| Largest bias current, disabled | ngspice              | Ib_off               |             any |          ​ |          any |          ​ |      0.22 nA |          ​ |   Skip 🟧    |
| Enable time, bn current | ngspice              | t_en90_bn            |             any |          ​ |          any |          ​ |        21 us |          ​ |   Skip 🟧    |
| Enable time, abp current | ngspice              | t_en90_abp           |             any |          ​ |          any |          ​ |        21 us |          ​ |   Skip 🟧    |

