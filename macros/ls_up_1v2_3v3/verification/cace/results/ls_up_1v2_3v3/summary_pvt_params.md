
# CACE Summary for ls_up_1v2_3v3

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Delay, input rising  | ngspice              | td_r                 |             any |   0.165 ns |          any |   0.431 ns |        10 ns |   6.965 ns |   Pass ✅    |
| Delay, input falling | ngspice              | td_f                 |             any |   0.305 ns |          any |   0.624 ns |        14 ns |  10.409 ns |   Pass ✅    |
| Output high level    | ngspice              | Voh                  |          2.85 V |    3.000 V |          any |    3.300 V |          any |    3.600 V |   Pass ✅    |
| Output low level     | ngspice              | Vol                  |             any |    0.000 V |          any |    0.000 V |       0.05 V |    0.000 V |   Pass ✅    |
| Iq VDDL, input low   | ngspice              | Iq_vddl_inlo         |             any |   2.817 pA |          any |  43.851 pA |   25000.0 pA | 4147.250 pA |   Pass ✅    |
| Iq VDDL, input high  | ngspice              | Iq_vddl_inhi         |             any |   0.028 pA |          any |  52.593 pA |   25000.0 pA | 17573.700 pA |   Pass ✅    |
| Iq VDDH, input low   | ngspice              | Iq_vddh_inlo         |             any |   0.012 pA |          any |   4.150 pA |      4000 pA | 2672.440 pA |   Pass ✅    |
| Iq VDDH, input high  | ngspice              | Iq_vddh_inhi         |             any |   0.012 pA |          any |   3.109 pA |      4000 pA | 2263.660 pA |   Pass ✅    |
| Iq input, input low  | ngspice              | Iq_in_inlo           |             any |   2.813 pA |          any |  19.902 pA |       300 pA | 146.734 pA |   Pass ✅    |
| Iq input, input high | ngspice              | Iq_in_inhi           |             any |   1.380 pA |          any |  16.593 pA |       300 pA | 196.978 pA |   Pass ✅    |
| Q VDDL, input rising | ngspice              | Q_vddl_r             |             any |  -1.139 fC |          any |  -0.835 fC |       300 fC |  -0.596 fC |   Pass ✅    |
| Q VDDL, input falling | ngspice              | Q_vddl_f             |             any |  18.374 fC |          any |  29.428 fC |        50 fC |  35.100 fC |   Pass ✅    |
| Q VDDH, input rising | ngspice              | Q_vddh_r             |             any | 165.332 fC |          any | 269.226 fC |      3000 fC | 2339.760 fC |   Pass ✅    |
| Q VDDH, input falling | ngspice              | Q_vddh_f             |             any | 127.119 fC |          any | 223.324 fC |      4000 fC | 3258.950 fC |   Pass ✅    |
| Q input, input rising | ngspice              | Q_in_r               |             any |  24.905 fC |          any |  30.203 fC |        50 fC |  35.631 fC |   Pass ✅    |
| Q input, input falling | ngspice              | Q_in_f               |             any |  21.031 fC |          any |  30.224 fC |        50 fC |  35.819 fC |   Pass ✅    |
| Ipk VDDL, input rising | ngspice              | Ipk_vddl_r           |             any |  14.486 uA |          any |  18.029 uA |        30 uA |  22.751 uA |   Pass ✅    |
| Ipk VDDL, input falling | ngspice              | Ipk_vddl_f           |             any | 141.974 uA |          any | 225.030 uA |       450 uA | 347.389 uA |   Pass ✅    |
| Ipk VDDH, input rising | ngspice              | Ipk_vddh_r           |             any | 439.736 uA |          any | 882.096 uA |      2200 uA | 1676.080 uA |   Pass ✅    |
| Ipk VDDH, input falling | ngspice              | Ipk_vddh_f           |             any | 245.724 uA |          any | 480.201 uA |      1200 uA | 871.241 uA |   Pass ✅    |
| Ipk input, input rising | ngspice              | Ipk_in_r             |             any | 218.559 uA |          any | 284.220 uA |       500 uA | 371.372 uA |   Pass ✅    |
| Ipk input, input falling | ngspice              | Ipk_in_f             |             any | 206.825 uA |          any | 256.167 uA |       400 uA | 311.065 uA |   Pass ✅    |
| Energy per cycle     | ngspice              | E_cycle              |             any | 918.356 fW⋅s |          any | 1699.740 fW⋅s | 26000.0 fW⋅s | 20183.300 fW⋅s |   Pass ✅    |
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

