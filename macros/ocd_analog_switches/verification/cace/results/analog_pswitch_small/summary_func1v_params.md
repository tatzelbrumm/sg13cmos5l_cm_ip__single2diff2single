
# CACE Summary for analog_pswitch_small

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Switch resistance 10 mV / dI | ngspice              | R_sw                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current into out     | ngspice              | I_out                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current into in      | ngspice              | I_in                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current from dvdd    | ngspice              | I_dvdd               |             any |          ​ |          any |          ​ |       120 nA |          ​ |   Skip 🟧    |
| Current from avdd    | ngspice              | I_avdd               |             any |          ​ |          any |          ​ |         2 nA |          ​ |   Skip 🟧    |
| Current into enable  | ngspice              | I_en                 |             any |          ​ |          any |          ​ |      2000 pA |          ​ |   Skip 🟧    |
| Gate of the pass PMOS | ngspice              | Vg                   |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| Switch resistance 10 mV / dI | ngspice              | R_sw                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current into out     | ngspice              | I_out                |        -5000 pA |          ​ |          any |          ​ |      5000 pA |          ​ |   Skip 🟧    |
| Current into in      | ngspice              | I_in                 |        -5000 pA |          ​ |          any |          ​ |      5000 pA |          ​ |   Skip 🟧    |
| Current from dvdd    | ngspice              | I_dvdd               |             any |          ​ |          any |          ​ |       130 nA |          ​ |   Skip 🟧    |
| Current from avdd    | ngspice              | I_avdd               |             any |          ​ |          any |          ​ |         3 nA |          ​ |   Skip 🟧    |
| Current into enable  | ngspice              | I_en                 |         -800 pA |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gate of the pass PMOS | ngspice              | Vg                   |           3.5 V |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Switch resistance 10 mV / dI | ngspice              | R_sw                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current into out     | ngspice              | I_out                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current into in      | ngspice              | I_in                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current from dvdd    | ngspice              | I_dvdd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current from avdd    | ngspice              | I_avdd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current into enable  | ngspice              | I_en                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gate of the pass PMOS | ngspice              | Vg                   |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Diode (bias-tree input) voltage | ngspice              | V_in                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Switch input = iDAC node voltage | ngspice              | V_out                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Drop across the switch | ngspice              | V_drop               |             any |          ​ |          any |          ​ |        0.8 V |          ​ |   Skip 🟧    |
| avdd - iDAC node (headroom left for the iDAC) | ngspice              | V_head               |           1.0 V |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current delivered into the diode | ngspice              | I_in                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current error of the switch (in - out) / out, % | ngspice              | I_err                |           -0.05 |          ​ |          any |          ​ |         0.05 |          ​ |   Skip 🟧    |
| Current drawn from the iDAC node by one off neighbour | ngspice              | I_nb                 |         -250 pA |          ​ |          any |          ​ |       250 pA |          ​ |   Skip 🟧    |
| Current error with 18 off neighbours, % | ngspice              | I_err18              |            -0.5 |          ​ |          any |          ​ |          0.5 |          ​ |   Skip 🟧    |
| Gate of the pass PMOS | ngspice              | Vg                   |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| Gate in the on state (2 on phases, max) | ngspice              | Verr_on              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| avdd - gate in the off state (2 off phases, max) | ngspice              | Verr_off             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| Enable 50 % rise -> gate 50 % fall | ngspice              | td_on                |             any |          ​ |          any |          ​ |        50 ns |          ​ |   Skip 🟧    |
| Enable 50 % fall -> gate 50 % rise | ngspice              | td_off               |             any |          ​ |          any |          ​ |        40 ns |          ​ |   Skip 🟧    |
| Enable 50 % -> load 50 % rise (10k || 1p) | ngspice              | t_on                 |             any |          ​ |          any |          ​ |        50 ns |          ​ |   Skip 🟧    |
| Enable 50 % -> load 50 % fall | ngspice              | t_off                |             any |          ​ |          any |          ​ |        50 ns |          ​ |   Skip 🟧    |
| Load voltage / vsig in the on state | ngspice              | V_load               |             0.9 |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Charge onto a held 1 pF at turn-off | ngspice              | Q_inj                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gate in the on state (2 on phases, max) | ngspice              | Verr_on              |             any |    0.000 V |          any |    0.000 V |        0.1 V |    0.000 V |   Pass ✅    |
| avdd - gate in the off state (2 off phases, max) | ngspice              | Verr_off             |             any |    0.000 V |          any |    0.000 V |        0.1 V |    0.000 V |   Pass ✅    |
| Enable 50 % rise -> gate 50 % fall | ngspice              | td_on                |             any |   0.585 ns |          any |   0.954 ns |          any |   1.721 ns |   Pass ✅    |
| Enable 50 % fall -> gate 50 % rise | ngspice              | td_off               |             any |   0.663 ns |          any |   1.091 ns |          any |   1.654 ns |   Pass ✅    |
| Enable 50 % -> load 50 % rise (meaningless when V_load ~ 0) | ngspice              | t_on                 |             any |  -0.050 ns |          any |   0.186 ns |          any |  49.837 ns |   Pass ✅    |
| Enable 50 % -> load 50 % fall (meaningless when V_load ~ 0) | ngspice              | t_off                |             any |  -0.050 ns |          any |   0.054 ns |          any |  50.114 ns |   Pass ✅    |
| Load voltage / vsig in the on state | ngspice              | V_load               |             any | 9.75967e-10 |          any | 2.54253e-06 |          any | 0.00130997 |   Pass ✅    |
| Charge onto a held 1 pF at turn-off | ngspice              | Q_inj                |             any |  10.745 fC |          any |  11.188 fC |          any |  11.781 fC |   Pass ✅    |
| Gate in the on state: mismatch | ngspice              | Verr_on              |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| avdd - gate in the off state: mismatch | ngspice              | Verr_off             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| Enable 50 % rise -> gate 50 % fall: mismatch | ngspice              | td_on                |             any |          ​ |          any |          ​ |       500 ns |          ​ |   Skip 🟧    |
| Enable 50 % fall -> gate 50 % rise: mismatch | ngspice              | td_off               |             any |          ​ |          any |          ​ |       500 ns |          ​ |   Skip 🟧    |
| Enable 50 % -> load 50 % rise: mismatch | ngspice              | t_on                 |             any |          ​ |          any |          ​ |       500 ns |          ​ |   Skip 🟧    |
| Enable 50 % -> load 50 % fall: mismatch | ngspice              | t_off                |             any |          ​ |          any |          ​ |       500 ns |          ​ |   Skip 🟧    |
| Load voltage / vsig: mismatch | ngspice              | V_load               |             0.9 |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Charge onto a held 1 pF: mismatch | ngspice              | Q_inj                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| gate/avdd 50 us (1 off, 0 on) | ngspice              | S_50u                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| gate/avdd 1 ms       | ngspice              | S_1m                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| gate/avdd 10 ms      | ngspice              | S_10m                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| gate/avdd 100 ms     | ngspice              | S_100m               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current from avdd at 100 ms | ngspice              | I_avdd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gate error after dvdd is back (enable = prior state) | ngspice              | Verr_end             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |
| gate/avdd 50 us (1 off, 0 on): mismatch | ngspice              | S_50u                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| gate/avdd 1 ms: mismatch | ngspice              | S_1m                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| gate/avdd 10 ms: mismatch | ngspice              | S_10m                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| gate/avdd 100 ms: mismatch | ngspice              | S_100m               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Current from avdd at 100 ms: mismatch | ngspice              | I_avdd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gate error after dvdd is back: mismatch | ngspice              | Verr_end             |             any |          ​ |          any |          ​ |        0.1 V |          ​ |   Skip 🟧    |

