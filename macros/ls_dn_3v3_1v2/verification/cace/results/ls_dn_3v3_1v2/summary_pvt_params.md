
# CACE Summary for ls_dn_3v3_1v2

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Delay, input rising  | ngspice              | td_r                 |             any |   0.045 ns |          any |   0.065 ns |      0.15 ns |   0.097 ns |   Pass ✅    |
| Delay, input falling | ngspice              | td_f                 |             any |   0.661 ns |          any |   1.138 ns |       3.5 ns |   2.560 ns |   Pass ✅    |
| Output high level    | ngspice              | Voh                  |             1 V |    1.080 V |          any |    1.200 V |          any |    1.320 V |   Pass ✅    |
| Output low level     | ngspice              | Vol                  |             any |    0.000 V |          any |    0.000 V |       0.05 V |    0.000 V |   Pass ✅    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |   0.001 pA |          any |   0.035 pA |       100 pA |  73.978 pA |   Pass ✅    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |   0.001 pA |          any |   0.166 pA |       100 pA |  10.202 pA |   Pass ✅    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |   0.000 pA |          any |   0.000 pA |        10 pA |   0.000 pA |   Pass ✅    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |   0.000 pA |          any |   0.000 pA |        10 pA |   0.001 pA |   Pass ✅    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |  -4.955 fC |          any |  -3.921 fC |       300 fC |  -2.987 fC |   Pass ✅    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |  28.207 fC |          any |  32.000 fC |        50 fC |  35.975 fC |   Pass ✅    |
| Q input, input rising | ngspice              | Q_in_r               |             any |  10.048 fC |          any |  12.081 fC |        20 fC |  14.586 fC |   Pass ✅    |
| Q input, input falling | ngspice              | Q_in_f               |             any |  10.060 fC |          any |  12.115 fC |        20 fC |  14.438 fC |   Pass ✅    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |  46.998 uA |          any |  66.296 uA |       110 uA |  88.190 uA |   Pass ✅    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any |  52.158 uA |          any |  65.108 uA |       110 uA |  77.264 uA |   Pass ✅    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any | 116.584 uA |          any | 163.580 uA |       260 uA | 203.597 uA |   Pass ✅    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any | 119.183 uA |          any | 142.304 uA |       260 uA | 165.213 uA |   Pass ✅    |
| Energy per cycle     | ngspice              | E_cycle              |             any | 26.935 fW⋅s |          any | 33.713 fW⋅s |      55 fW⋅s | 41.271 fW⋅s |   Pass ✅    |
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

