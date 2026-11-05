| group | quantity | unit | limit | worst | runs | verdict |
|---|---|---|---:|---:|---:|---|
| dc_params | Gain |  | >= 1.99 | 1.998 | 135 | pass |
| dc_params | Gain |  | <= 2.01 | 1.999 | 135 | pass |
| dc_params | Input offset (systematic) | mV | >= -1 | -3.143e-05 | 135 | pass |
| dc_params | Input offset (systematic) | mV | <= 1 | 0.0005802 | 135 | pass |
| dc_params | Integral nonlinearity | mV | <= 2 | 1.069 | 135 | pass |
| dc_params | Output common-mode error | mV | >= -30 | 5.003 | 135 | pass |
| dc_params | Output common-mode error | mV | <= 30 | 18.05 | 135 | pass |
| dc_params | IO ring current | uA | <= 135 | 116.9 | 135 | pass |
| range_params | Gain vs vref and vcm |  |  any | 1.95 .. 2.038 | 96 | report |
| range_params | Integral nonlinearity vs vref and vcm | mV |  any | 0.189 .. 172.3 | 96 | report |
| range_params | Output common-mode error vs vref and vcm | mV |  any | 3.317 .. 15.46 | 96 | report |
| window_params | Input range, low end | V | <= 0.1 | 0.08702 | 27 | pass |
| window_params | Input range, high end | V | >= 1.0 | 1.057 | 27 | pass |
| dc_sel_params | Gain vs bias select |  | >= 1.99 | 1.999 | 45 | pass |
| dc_sel_params | Gain vs bias select |  | <= 2.01 | 1.999 | 45 | pass |
| dc_sel_params | Input offset (systematic) vs bias select | mV | >= -1 | -8.895e-06 | 45 | pass |
| dc_sel_params | Input offset (systematic) vs bias select | mV | <= 1 | 0.0005477 | 45 | pass |
| dc_sel_params | Integral nonlinearity vs bias select | mV | <= 2 | 0.4376 | 45 | pass |
| dc_sel_params | Output common-mode error vs bias select | mV | >= -30 | 6.367 | 45 | pass |
| dc_sel_params | Output common-mode error vs bias select | mV | <= 30 | 14.15 | 45 | pass |
| dc_sel_params | IO ring current vs bias select | uA | <= 220 | 173.6 | 45 | pass |
| dc_sel3_params | Gain, sel 11 |  |  any | 1.998 .. 1.999 | 15 | report |
| dc_sel3_params | Input offset (systematic), sel 11 | mV |  any | -4.471e-05 .. 0.0005477 | 15 | report |
| dc_sel3_params | Integral nonlinearity, sel 11 | mV |  any | 0.4011 .. 6.66 | 15 | report |
| dc_sel3_params | Output common-mode error, sel 11 | mV |  any | 6.66 .. 16.4 | 15 | report |
| dc_sel3_params | IO ring current, sel 11 | uA |  any | 196.7 .. 294.7 | 15 | report |
| dc_ibias_params | Gain vs ibias |  | >= 1.99 | 1.999 | 15 | pass |
| dc_ibias_params | Gain vs ibias |  | <= 2.01 | 1.999 | 15 | pass |
| dc_ibias_params | Input offset (systematic) vs ibias | mV | >= -1 | -8.898e-06 | 15 | pass |
| dc_ibias_params | Input offset (systematic) vs ibias | mV | <= 1 | -6.346e-06 | 15 | pass |
| dc_ibias_params | Integral nonlinearity vs ibias | mV |  any | 0.03629 .. 0.3522 | 15 | report |
| dc_ibias_params | Output common-mode error vs ibias | mV | >= -30 | 8.667 | 15 | pass |
| dc_ibias_params | Output common-mode error vs ibias | mV | <= 30 | 11.68 | 15 | pass |
| dc_ibias_params | IO ring current vs ibias | uA |  any | 69.71 .. 161.4 | 15 | report |
| ac_params | Closed-loop gain at 1 kHz | dB |  any | 6.015 .. 6.017 | 15 | report |
| ac_params | Closed-loop -3 dB bandwidth | MHz | >= 1 | 1.353 | 15 | pass |
| ac_params | Output common-mode response to iovdd at 1 kHz | dB | <= -30 | -53.85 | 15 | pass |
| tran_params | Rise time 10-90 % | ns |  any | 104.1 .. 259 | 18 | report |
| tran_params | Settling time to 1 % | ns | <= 1000 | 546 | 18 | pass |
| tran_params | Overshoot | % | <= 5 | 0.002001 | 18 | pass |
| tran_params | Largest output common-mode deviation during the step | mV | <= 50 | 15.65 | 18 | pass |
| noise_params | Input noise density at 1 kHz | nV/rtHz | <= 1000 | 726.5 | 15 | pass |
| noise_params | Input noise density at 100 kHz | nV/rtHz | <= 250 | 157.1 | 15 | pass |
| noise_params | Differential output noise, 10 Hz - 10 MHz | uV | <= 1000 | 440.7 | 15 | pass |
| pd_params | IO ring current, off | nA | <= 1000 | 597.1 | 24 | pass |
| pd_params | Core ring current, off | nA | <= 100 | 4.831 | 24 | pass |
| pd_params | Pad input leakage, off | nA | >= -100 | -7.64 | 24 | pass |
| pd_params | Pad input leakage, off | nA | <= 100 | 5.876 | 24 | pass |
| pd_params | Internal enable | V | <= 0.1 | 3.602e-07 | 24 | pass |
| pd_params | Differential output, off | mV | >= -1 | -0.000654 | 24 | pass |
| pd_params | Differential output, off | mV | <= 1 | 1.12e-05 | 24 | pass |
| pd_params | Output common mode, off | mV | >= -1 | -8.807e-07 | 24 | pass |
| pd_params | Output common mode, off | mV | <= 1 | 0.0004674 | 24 | pass |
| enable_params | Enable time | us | <= 3 | 1.43 | 9 | pass |
| enable_params | Output CM glitch, high | V |  any | 0.2108 .. 0.2705 | 9 | report |
| enable_params | Output CM glitch, low | V |  any | -0.01117 .. -0.003362 | 9 | report |
| enable_params | Differential output at the end | V |  any | 0.4998 .. 0.4998 | 9 | report |
| enable_params | IO ring current, enabled | uA |  any | 115.2 .. 116.1 | 9 | report |
