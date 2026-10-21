
# CACE Summary for sg13cmos5l_IOPadSingle2Diff

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Gain, positive output | ngspice              | Gp                   |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gain, negative output | ngspice              | Gn                   |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Offset, positive output | ngspice              | Vos_p                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Offset, negative output | ngspice              | Vos_n                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Common-mode error    | ngspice              | Vcm_err              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| IO ring supply current | ngspice              | Iio                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Input range, low end | ngspice              | Vin_min              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Input range, high end | ngspice              | Vin_max              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Differential gain    | ngspice              | Ad_dB                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Bandwidth            | ngspice              | f3dB                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR iovdd 1 kHz     | ngspice              | PSRR_1k              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR iovdd 100 kHz   | ngspice              | PSRR_100k            |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| IO ring current, off | ngspice              | Iio_pd               |             any |   0.022 nA |          any | 232.354 nA |          any | 597.072 nA |   Pass ✅    |
| Core ring current, off | ngspice              | Icore_pd             |             any |  -0.000 nA |          any |   0.118 nA |          any |   4.831 nA |   Pass ✅    |
| Pad input leakage, off | ngspice              | Ipad_pd              |             any |  -7.640 nA |          any |   0.162 nA |          any |   8.417 nA |   Pass ✅    |
| Internal enable      | ngspice              | Ven3                 |             any |    0.000 V |          any |    0.000 V |          any |    0.000 V |   Pass ✅    |

