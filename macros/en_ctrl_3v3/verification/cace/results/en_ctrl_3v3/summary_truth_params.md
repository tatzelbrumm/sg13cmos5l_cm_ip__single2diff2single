
# CACE Summary for en_ctrl_3v3

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| en_3v3 error         | ngspice              | Verr_en              |             any |    0.000 V |          any |    0.000 V |        0.1 V |    0.000 V |   Pass ✅    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |    0.000 V |          any |    0.000 V |        0.1 V |    0.000 V |   Pass ✅    |
| I vddh               | ngspice              | I_vddh               |             any |  49.860 nA |          any |  99.718 nA |       240 nA | 149.576 nA |   Pass ✅    |
| I vddl               | ngspice              | I_vddl               |             any |  -0.000 nA |          any |  -0.000 nA |         1 nA |  -0.000 nA |   Pass ✅    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |  -0.000 nA |          any |  -0.000 nA |         1 nA |  -0.000 nA |   Pass ✅    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |  -0.000 nA |          any |  -0.000 nA |         1 nA |  -0.000 nA |   Pass ✅    |
| I en_1v2             | ngspice              | I_en                 |             any |  -0.000 nA |          any |  -0.000 nA |       0.3 nA |  -0.000 nA |   Pass ✅    |
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |       240 nA |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |       0.3 nA |          ​ |   Skip 🟧    |
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |       240 nA |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |       0.3 nA |          ​ |   Skip 🟧    |
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |       240 nA |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |       0.3 nA |          ​ |   Skip 🟧    |
| Enable delay         | ngspice              | td_on                |             any |          ​ |          any |          ​ |        40 ns |          ​ |   Skip 🟧    |
| Disable delay        | ngspice              | td_off               |             any |          ​ |          any |          ​ |       410 ns |          ​ |   Skip 🟧    |
| Enable delay, vddl off | ngspice              | td_on                |             any |          ​ |          any |          ​ |        40 ns |          ​ |   Skip 🟧    |
| Disable delay, vddl off | ngspice              | td_off               |             any |          ​ |          any |          ​ |       410 ns |          ​ |   Skip 🟧    |
| en_3v3 after disable | ngspice              | Ven_end              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |

