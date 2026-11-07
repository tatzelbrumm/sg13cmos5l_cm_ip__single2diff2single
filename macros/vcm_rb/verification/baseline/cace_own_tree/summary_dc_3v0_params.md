
# CACE Summary for vcm_rb

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Output, iovdd 3.3 / 3.6 V | ngspice              | Vcm                  |         1.031 V |          ​ |          any |          ​ |       1.53 V |          ​ |   Skip 🟧    |
| Block supply current (without the reference) | ngspice              | Ib                   |             any |          ​ |          any |          ​ |        25 uA |          ​ |   Skip 🟧    |
| Output, iovdd 3.0 V  | ngspice              | Vcm                  |         1.031 V |    1.120 V |          any |    1.150 V |      1.262 V |    1.193 V |   Pass ✅    |
| Block supply current (without the reference) | ngspice              | Ib                   |             any |  17.363 uA |          any |  17.453 uA |        25 uA |  17.574 uA |   Pass ✅    |
| Output, OA core / bandgap core, 3.0 V | ngspice              | Vcm                  |         1.031 V |          ​ |          any |          ​ |      1.244 V |          ​ |   Skip 🟧    |
| Block supply current (without the reference) | ngspice              | Ib                   |             any |          ​ |          any |          ​ |        35 uA |          ​ |   Skip 🟧    |
| Output, disabled     | ngspice              | Vcm                  |             any |          ​ |          any |          ​ |      0.001 V |          ​ |   Skip 🟧    |
| Block supply current, disabled | ngspice              | Ib                   |             any |          ​ |          any |          ​ |       0.1 uA |          ​ |   Skip 🟧    |
| Output - Mismatch (tt 27 C 3.3 V) | ngspice              | Vcm                  |           1.2 V |          ​ |          any |          ​ |       1.32 V |          ​ |   Skip 🟧    |
| Block supply current - Mismatch | ngspice              | Ib                   |             any |          ​ |          any |          ​ |        25 uA |          ​ |   Skip 🟧    |

