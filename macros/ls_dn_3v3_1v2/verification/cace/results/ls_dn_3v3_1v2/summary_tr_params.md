
# CACE Summary for ls_dn_3v3_1v2

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Delay, input rising  | ngspice              | td_r                 |             any |          ​ |          any |          ​ |      0.15 ns |          ​ |   Skip 🟧    |
| Delay, input falling | ngspice              | td_f                 |             any |          ​ |          any |          ​ |       3.5 ns |          ​ |   Skip 🟧    |
| Output high level    | ngspice              | Voh                  |             1 V |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output low level     | ngspice              | Vol                  |             any |          ​ |          any |          ​ |       0.05 V |          ​ |   Skip 🟧    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |          ​ |          any |          ​ |       100 pA |          ​ |   Skip 🟧    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |          ​ |          any |          ​ |       100 pA |          ​ |   Skip 🟧    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |          ​ |          any |          ​ |        10 pA |          ​ |   Skip 🟧    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |          ​ |          any |          ​ |        10 pA |          ​ |   Skip 🟧    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |          ​ |          any |          ​ |       300 fC |          ​ |   Skip 🟧    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |          ​ |          any |          ​ |        50 fC |          ​ |   Skip 🟧    |
| Q input, input rising | ngspice              | Q_in_r               |             any |          ​ |          any |          ​ |        20 fC |          ​ |   Skip 🟧    |
| Q input, input falling | ngspice              | Q_in_f               |             any |          ​ |          any |          ​ |        20 fC |          ​ |   Skip 🟧    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |          ​ |          any |          ​ |       110 uA |          ​ |   Skip 🟧    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any |          ​ |          any |          ​ |       110 uA |          ​ |   Skip 🟧    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any |          ​ |          any |          ​ |       260 uA |          ​ |   Skip 🟧    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any |          ​ |          any |          ​ |       260 uA |          ​ |   Skip 🟧    |
| Energy per cycle     | ngspice              | E_cycle              |             any |          ​ |          any |          ​ |      55 fW⋅s |          ​ |   Skip 🟧    |
| Delay, input rising  | ngspice              | td_r                 |             any |  -1.750 ns |          any |   0.053 ns |          any |   0.073 ns |   Pass ✅    |
| Delay, input falling | ngspice              | td_f                 |             any |   1.151 ns |          any |   1.182 ns |          any |   5.348 ns |   Pass ✅    |
| Output high level    | ngspice              | Voh                  |             any |    1.200 V |          any |    1.200 V |          any |    1.200 V |   Pass ✅    |
| Output low level     | ngspice              | Vol                  |             any |    0.000 V |          any |    0.000 V |          any |    0.000 V |   Pass ✅    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |   0.035 pA |          any |   0.035 pA |          any |   0.035 pA |   Pass ✅    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |   0.054 pA |          any |   0.055 pA |          any |   0.056 pA |   Pass ✅    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |   0.000 pA |          any |   0.000 pA |          any |   0.000 pA |   Pass ✅    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |   0.000 pA |          any |   0.000 pA |          any |   0.003 pA |   Pass ✅    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |  -4.314 fC |          any |  -3.936 fC |          any |  -3.883 fC |   Pass ✅    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |  30.140 fC |          any |  31.168 fC |          any |  32.702 fC |   Pass ✅    |
| Q input, input rising | ngspice              | Q_in_r               |             any |  12.048 fC |          any |  12.108 fC |          any |  12.122 fC |   Pass ✅    |
| Q input, input falling | ngspice              | Q_in_f               |             any |  12.081 fC |          any |  12.108 fC |          any |  12.145 fC |   Pass ✅    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |   0.682 uA |          any |  21.428 uA |          any | 225.699 uA |   Pass ✅    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any |  13.798 uA |          any |  27.520 uA |          any | 268.026 uA |   Pass ✅    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any |   1.885 uA |          any |  52.977 uA |          any | 624.529 uA |   Pass ✅    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any |   1.465 uA |          any |  48.394 uA |          any | 645.717 uA |   Pass ✅    |
| Energy per cycle     | ngspice              | E_cycle              |             any | 30.992 fW⋅s |          any | 32.679 fW⋅s |          any | 34.554 fW⋅s |   Pass ✅    |
| Delay, input rising  | ngspice              | td_r                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Delay, input falling | ngspice              | td_f                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output high level    | ngspice              | Voh                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output low level     | ngspice              | Vol                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q input, input rising | ngspice              | Q_in_r               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q input, input falling | ngspice              | Q_in_f               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Energy per cycle     | ngspice              | E_cycle              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |

