
# CACE Summary for sg13cmos5l_IOPadSingle2Diff

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Gain, positive output | ngspice              | Gp                   |             any |        1.0 |          any |        1.0 |          any |        1.0 |   Pass ✅    |
| Gain, negative output | ngspice              | Gn                   |             any |       -1.0 |          any |       -1.0 |          any |       -1.0 |   Pass ✅    |
| Offset, positive output | ngspice              | Vos_p                |             any |  -0.001 mV |          any |  -0.000 mV |          any |  -0.000 mV |   Pass ✅    |
| Offset, negative output | ngspice              | Vos_n                |             any |   0.000 mV |          any |   0.000 mV |          any |   0.001 mV |   Pass ✅    |
| Common-mode error    | ngspice              | Vcm_err              |             any |   0.000 mV |          any |   0.000 mV |          any |   0.000 mV |   Pass ✅    |
| IO ring supply current | ngspice              | Iio                  |             any |  25.040 uA |          any |  25.460 uA |          any |  25.956 uA |   Pass ✅    |
| Input range, low end | ngspice              | Vin_min              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Input range, high end | ngspice              | Vin_max              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Differential gain    | ngspice              | Ad_dB                |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Bandwidth            | ngspice              | f3dB                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR iovdd 1 kHz     | ngspice              | PSRR_1k              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR iovdd 100 kHz   | ngspice              | PSRR_100k            |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| IO ring current, off | ngspice              | Iio_pd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Core ring current, off | ngspice              | Icore_pd             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Pad input leakage, off | ngspice              | Ipad_pd              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Internal enable      | ngspice              | Ven3                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |

