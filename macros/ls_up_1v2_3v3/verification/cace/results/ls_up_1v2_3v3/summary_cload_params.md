
# CACE Summary for ls_up_1v2_3v3

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Delay, input rising  | ngspice              | td_r                 |             any |          ​ |          any |          ​ |        10 ns |          ​ |   Skip 🟧    |
| Delay, input falling | ngspice              | td_f                 |             any |          ​ |          any |          ​ |        14 ns |          ​ |   Skip 🟧    |
| Output high level    | ngspice              | Voh                  |          2.85 V |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output low level     | ngspice              | Vol                  |             any |          ​ |          any |          ​ |       0.05 V |          ​ |   Skip 🟧    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |          ​ |          any |          ​ |   25000.0 pA |          ​ |   Skip 🟧    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |          ​ |          any |          ​ |   25000.0 pA |          ​ |   Skip 🟧    |
| Iq VDDH, input low   | ngspice              | Iq_vddh_inlo         |             any |          ​ |          any |          ​ |      4000 pA |          ​ |   Skip 🟧    |
| Iq VDDH, input high  | ngspice              | Iq_vddh_inhi         |             any |          ​ |          any |          ​ |      4000 pA |          ​ |   Skip 🟧    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |          ​ |          any |          ​ |       300 pA |          ​ |   Skip 🟧    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |          ​ |          any |          ​ |       300 pA |          ​ |   Skip 🟧    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |          ​ |          any |          ​ |       300 fC |          ​ |   Skip 🟧    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |          ​ |          any |          ​ |        50 fC |          ​ |   Skip 🟧    |
| Q VDDH, input rising | ngspice              | Q_vddh_r             |             any |          ​ |          any |          ​ |      3000 fC |          ​ |   Skip 🟧    |
| Q VDDH, input falling | ngspice              | Q_vddh_f             |             any |          ​ |          any |          ​ |      4000 fC |          ​ |   Skip 🟧    |
| Q input, input rising | ngspice              | Q_in_r               |             any |          ​ |          any |          ​ |        50 fC |          ​ |   Skip 🟧    |
| Q input, input falling | ngspice              | Q_in_f               |             any |          ​ |          any |          ​ |        50 fC |          ​ |   Skip 🟧    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |          ​ |          any |          ​ |        30 uA |          ​ |   Skip 🟧    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any |          ​ |          any |          ​ |       450 uA |          ​ |   Skip 🟧    |
| Ipk VDDH, input rising | ngspice              | Ipk_vddh_r           |             any |          ​ |          any |          ​ |      2200 uA |          ​ |   Skip 🟧    |
| Ipk VDDH, input falling | ngspice              | Ipk_vddh_f           |             any |          ​ |          any |          ​ |      1200 uA |          ​ |   Skip 🟧    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any |          ​ |          any |          ​ |       500 uA |          ​ |   Skip 🟧    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any |          ​ |          any |          ​ |       400 uA |          ​ |   Skip 🟧    |
| Energy per cycle     | ngspice              | E_cycle              |             any |          ​ |          any |          ​ | 26000.0 fW⋅s |          ​ |   Skip 🟧    |
| Delay, input rising  | ngspice              | td_r                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Delay, input falling | ngspice              | td_f                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output high level    | ngspice              | Voh                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output low level     | ngspice              | Vol                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq VDDH, input low   | ngspice              | Iq_vddh_inlo         |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq VDDH, input high  | ngspice              | Iq_vddh_inhi         |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q VDDH, input rising | ngspice              | Q_vddh_r             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q VDDH, input falling | ngspice              | Q_vddh_f             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q input, input rising | ngspice              | Q_in_r               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Q input, input falling | ngspice              | Q_in_f               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk VDDH, input rising | ngspice              | Ipk_vddh_r           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk VDDH, input falling | ngspice              | Ipk_vddh_f           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Energy per cycle     | ngspice              | E_cycle              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Delay, input rising  | ngspice              | td_r                 |             any |   0.380 ns |          any |   0.457 ns |          any |   0.567 ns |   Pass ✅    |
| Delay, input falling | ngspice              | td_f                 |             any |   0.574 ns |          any |   0.651 ns |          any |   0.759 ns |   Pass ✅    |
| Output high level    | ngspice              | Voh                  |             any |    3.300 V |          any |    3.300 V |          any |    3.300 V |   Pass ✅    |
| Output low level     | ngspice              | Vol                  |             any |    0.000 V |          any |    0.000 V |          any |    0.000 V |   Pass ✅    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |  32.933 pA |          any |  32.933 pA |          any |  32.933 pA |   Pass ✅    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |  52.597 pA |          any |  52.598 pA |          any |  52.600 pA |   Pass ✅    |
| Iq VDDH, input low   | ngspice              | Iq_vddh_inlo         |             any |   2.736 pA |          any |   2.736 pA |          any |   2.736 pA |   Pass ✅    |
| Iq VDDH, input high  | ngspice              | Iq_vddh_inhi         |             any |   1.926 pA |          any |   1.927 pA |          any |   1.927 pA |   Pass ✅    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |  19.902 pA |          any |  19.902 pA |          any |  19.902 pA |   Pass ✅    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |  16.592 pA |          any |  16.595 pA |          any |  16.595 pA |   Pass ✅    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |  -0.855 fC |          any |  -0.854 fC |          any |  -0.853 fC |   Pass ✅    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |  29.389 fC |          any |  29.396 fC |          any |  29.428 fC |   Pass ✅    |
| Q VDDH, input rising | ngspice              | Q_vddh_r             |             any | 220.994 fC |          any | 322.589 fC |          any | 529.694 fC |   Pass ✅    |
| Q VDDH, input falling | ngspice              | Q_vddh_f             |             any | 225.534 fC |          any | 226.060 fC |          any | 230.243 fC |   Pass ✅    |
| Q input, input rising | ngspice              | Q_in_r               |             any |  30.109 fC |          any |  30.181 fC |          any |  30.198 fC |   Pass ✅    |
| Q input, input falling | ngspice              | Q_in_f               |             any |  30.104 fC |          any |  30.182 fC |          any |  30.199 fC |   Pass ✅    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |  18.029 uA |          any |  18.030 uA |          any |  18.032 uA |   Pass ✅    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any | 225.030 uA |          any | 225.204 uA |          any | 225.293 uA |   Pass ✅    |
| Ipk VDDH, input rising | ngspice              | Ipk_vddh_r           |             any | 663.363 uA |          any | 956.240 uA |          any | 1047.280 uA |   Pass ✅    |
| Ipk VDDH, input falling | ngspice              | Ipk_vddh_f           |             any | 461.886 uA |          any | 465.034 uA |          any | 548.721 uA |   Pass ✅    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any | 298.315 uA |          any | 298.413 uA |          any | 298.621 uA |   Pass ✅    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any | 256.048 uA |          any | 256.513 uA |          any | 256.869 uA |   Pass ✅    |
| Energy per cycle     | ngspice              | E_cycle              |             any | 1523.330 fW⋅s |          any | 1844.630 fW⋅s |          any | 2526.860 fW⋅s |   Pass ✅    |

