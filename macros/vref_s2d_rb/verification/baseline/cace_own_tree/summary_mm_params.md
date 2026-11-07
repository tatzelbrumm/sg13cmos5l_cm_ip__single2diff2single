
# CACE Summary for vref_s2d_rb

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Output at 27 C (pad range from 0 V) | ngspice              | Vref                 |          0.47 V |          ​ |          any |          ​ |       0.51 V |          ​ |   Skip 🟧    |
| Block supply current (without the reference) | ngspice              | Ib                   |             any |          ​ |          any |          ​ |         8 uA |          ​ |   Skip 🟧    |
| Output at 125 C (above the S2D input INL edge, <= 0.542 V) | ngspice              | Vref                 |          0.55 V |          ​ |          any |          ​ |        0.7 V |          ​ |   Skip 🟧    |
| Block supply current (without the reference) | ngspice              | Ib                   |             any |          ​ |          any |          ​ |         8 uA |          ​ |   Skip 🟧    |
| Output at -40 C (pad range from 0 V) | ngspice              | Vref                 |          0.35 V |          ​ |          any |          ​ |        0.5 V |          ​ |   Skip 🟧    |
| Block supply current (without the reference) | ngspice              | Ib                   |             any |          ​ |          any |          ​ |         8 uA |          ​ |   Skip 🟧    |
| Output, disabled     | ngspice              | Vref                 |             any |          ​ |          any |          ​ |      0.001 V |          ​ |   Skip 🟧    |
| Block supply current, disabled | ngspice              | Ib                   |             any |          ​ |          any |          ​ |       0.1 uA |          ​ |   Skip 🟧    |
| Output - Mismatch (tt 27 C 3.3 V) | ngspice              | Vref                 |          0.47 V |    0.484 V |          any |    0.493 V |       0.52 V |    0.501 V |   Pass ✅    |
| Block supply current - Mismatch | ngspice              | Ib                   |             any |   5.325 uA |          any |   5.457 uA |         8 uA |   5.590 uA |   Pass ✅    |

