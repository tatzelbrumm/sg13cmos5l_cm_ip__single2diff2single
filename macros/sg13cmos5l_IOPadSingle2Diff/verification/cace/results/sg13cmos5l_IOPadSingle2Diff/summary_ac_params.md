
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
| Differential gain    | ngspice              | Ad_dB                |             any |   6.021 dB |          any |   6.021 dB |          any |   6.021 dB |   Pass ✅    |
| Bandwidth            | ngspice              | f3dB                 |             any | 1000.000 MHz |          any | 1000.000 MHz |          any | 1000.000 MHz |   Pass ✅    |
| PSRR iovdd 1 kHz     | ngspice              | PSRR_1k              |             any | 135.810 dB |          any | 140.621 dB |          any | 140.831 dB |   Pass ✅    |
| PSRR iovdd 100 kHz   | ngspice              | PSRR_100k            |             any | 100.444 dB |          any | 100.621 dB |          any | 100.831 dB |   Pass ✅    |
| IO ring current, off | ngspice              | Iio_pd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Core ring current, off | ngspice              | Icore_pd             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Pad input leakage, off | ngspice              | Ipad_pd              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Internal enable      | ngspice              | Ven3                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |

