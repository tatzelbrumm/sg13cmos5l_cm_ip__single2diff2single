
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
| Delay, input rising  | ngspice              | td_r                 |             any |   0.404 ns |          any |   0.511 ns |          any |   4.604 ns |   Pass ✅    |
| Delay, input falling | ngspice              | td_f                 |             any |   0.624 ns |          any |   0.655 ns |          any |   1.393 ns |   Pass ✅    |
| Output high level    | ngspice              | Voh                  |             any |    3.300 V |          any |    3.300 V |          any |    3.300 V |   Pass ✅    |
| Output low level     | ngspice              | Vol                  |             any |    0.000 V |          any |    0.000 V |          any |    0.000 V |   Pass ✅    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |  32.933 pA |          any |  32.933 pA |          any |  32.933 pA |   Pass ✅    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |  52.583 pA |          any |  52.598 pA |          any |  52.599 pA |   Pass ✅    |
| Iq VDDH, input low   | ngspice              | Iq_vddh_inlo         |             any |   2.736 pA |          any |   2.736 pA |          any |   2.736 pA |   Pass ✅    |
| Iq VDDH, input high  | ngspice              | Iq_vddh_inhi         |             any |   1.926 pA |          any |   1.927 pA |          any |   1.929 pA |   Pass ✅    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |  19.902 pA |          any |  19.902 pA |          any |  19.902 pA |   Pass ✅    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |  16.593 pA |          any |  16.594 pA |          any |  16.611 pA |   Pass ✅    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |  -0.981 fC |          any |  -0.691 fC |          any |  14.267 fC |   Pass ✅    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |  29.416 fC |          any |  29.541 fC |          any |  46.436 fC |   Pass ✅    |
| Q VDDH, input rising | ngspice              | Q_vddh_r             |             any | 273.884 fC |          any | 284.447 fC |          any | 852.100 fC |   Pass ✅    |
| Q VDDH, input falling | ngspice              | Q_vddh_f             |             any | 216.676 fC |          any | 233.975 fC |          any | 291.752 fC |   Pass ✅    |
| Q input, input rising | ngspice              | Q_in_r               |             any |  29.991 fC |          any |  30.130 fC |          any |  30.188 fC |   Pass ✅    |
| Q input, input falling | ngspice              | Q_in_f               |             any |  30.082 fC |          any |  30.160 fC |          any |  30.194 fC |   Pass ✅    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |   2.631 uA |          any |   8.252 uA |          any |  71.991 uA |   Pass ✅    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any |  30.636 uA |          any | 140.787 uA |          any | 304.463 uA |   Pass ✅    |
| Ipk VDDH, input rising | ngspice              | Ipk_vddh_r           |             any | 846.518 uA |          any | 906.284 uA |          any | 918.707 uA |   Pass ✅    |
| Ipk VDDH, input falling | ngspice              | Ipk_vddh_f           |             any | 453.754 uA |          any | 461.456 uA |          any | 464.468 uA |   Pass ✅    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any |  49.545 uA |          any | 116.050 uA |          any | 1209.750 uA |   Pass ✅    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any |  40.462 uA |          any |  89.539 uA |          any | 1121.160 uA |   Pass ✅    |
| Energy per cycle     | ngspice              | E_cycle              |             any | 1687.870 fW⋅s |          any | 1736.840 fW⋅s |          any | 3847.560 fW⋅s |   Pass ✅    |
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

