
# CACE Summary for en_ctrl_3v3

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |      2500 nA |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |        50 nA |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |      1900 nA |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |      2300 nA |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |       0.3 nA |          ​ |   Skip 🟧    |
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |      2500 nA |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |        50 nA |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |      1900 nA |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |      2300 nA |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |       0.3 nA |          ​ |   Skip 🟧    |
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |      2500 nA |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |        50 nA |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |      1900 nA |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |      2300 nA |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |       0.3 nA |          ​ |   Skip 🟧    |
| Enable delay         | ngspice              | td_on                |             any |   1.141 ns |          any |   1.868 ns |       4.8 ns |   3.716 ns |   Pass ✅    |
| Disable delay        | ngspice              | td_off               |             any |   1.718 ns |          any |   2.741 ns |         7 ns |   5.416 ns |   Pass ✅    |
| Supply-loss response | ngspice              | t_pg                 |             any |          ​ |          any |          ​ |       1.2 us |          ​ |   Skip 🟧    |
| en_3v3 after the loss | ngspice              | Ven_end              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |

