
# CACE Summary for en_ctrl_3v3

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
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
| en_3v3 error         | ngspice              | Verr_en              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| sel_3v3 error        | ngspice              | Verr_sel             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| I vddh               | ngspice              | I_vddh               |             any |          ​ |          any |          ​ |       240 nA |          ​ |   Skip 🟧    |
| I vddl               | ngspice              | I_vddl               |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd1v2_sense       | ngspice              | I_s12                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I vdd3v3_sense       | ngspice              | I_s33                |             any |          ​ |          any |          ​ |         1 nA |          ​ |   Skip 🟧    |
| I en_1v2             | ngspice              | I_en                 |             any |          ​ |          any |          ​ |       0.3 nA |          ​ |   Skip 🟧    |
| Enable delay         | ngspice              | td_on                |             any |          ​ |          any |          ​ |        40 ns |          ​ |   Skip 🟧    |
| Disable delay        | ngspice              | td_off               |             any |          ​ |          any |          ​ |       410 ns |          ​ |   Skip 🟧    |
| Enable delay, vddl off | ngspice              | td_on                |             any |   1.063 ns |          any |   1.659 ns |        40 ns |   2.423 ns |   Pass ✅    |
| Disable delay, vddl off | ngspice              | td_off               |             any |  57.132 ns |          any |  68.453 ns |       410 ns |  81.399 ns |   Pass ✅    |
| en_3v3 after disable | ngspice              | Ven_end              |             any |    0.000 V |          any |    0.000 V |        0.1 V |    0.000 V |   Pass ✅    |

