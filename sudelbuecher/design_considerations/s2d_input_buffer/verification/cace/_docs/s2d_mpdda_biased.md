# s2d_mpdda_biased

- Description: Pad input buffer + bias fixture, single-ended in / fully differential out, gain 2, load compensated (proof of concept)
- PDK: ihp-sg13cmos5l

## Authorship

- Designer: Christoph Maier
- Created: October 20, 2026
- License: Apache-2.0
- Company: None
- Last modified: None

## Pins

- vdd
  + Description: Positive analog power supply (slot vdd_3v3)
  + Type: power
  + Direction: inout
  + Vmin: 3.0
  + Vmax: 3.6
- vss
  + Description: Analog ground (slot vss_3v3)
  + Type: ground
  + Direction: inout
- vin
  + Description: Pad input, from IOPadAnalog padres (behind 586.9 ohm and the secondary clamps)
  + Type: signal
  + Direction: input
- vref
  + Description: Pad reference (input units, other gate); vin = vref +- 0.5 V
  + Type: signal
  + Direction: input
- vcm
  + Description: Internal common mode (feedback and CMFB units); gate only
  + Type: signal
  + Direction: input
- voutp
  + Description: Differential output, positive (voutp - voutn = 2 (vin - vref))
  + Type: signal
  + Direction: output
- voutn
  + Description: Differential output, negative
  + Type: signal
  + Direction: output
- vfbp
  + Description: Feedback / CMFB sense, tied to voutp in the application
  + Type: signal
  + Direction: input
- vfbn
  + Description: Feedback / CMFB sense, tied to voutn in the application
  + Type: signal
  + Direction: input
- vbp
  + Description: Bias, PMOS unit tails (5 uA reference)
  + Type: signal
  + Direction: inout
- vbn
  + Description: Bias, NMOS fold sinks (5 uA reference)
  + Type: signal
  + Direction: inout
- vbpc
  + Description: Bias, PMOS load and diode cascodes (2 uA reference)
  + Type: signal
  + Direction: inout
- vbnc
  + Description: Bias, NMOS fold cascodes (2 uA reference)
  + Type: signal
  + Direction: inout

## Default Conditions

- vdd
  + Description: Analog power supply voltage
  + Display: VDD
  + Unit: V
  + Typical: 3.3
- vref
  + Description: Pad reference voltage
  + Display: Vref
  + Unit: V
  + Typical: 1.2
- vcm
  + Description: Internal common-mode voltage
  + Display: Vcm
  + Unit: V
  + Typical: 1.2
- corner_mos
  + Description: Process corner MOSFET
  + Display: Corner MOSFET
  + Typical: tt
- corner_r
  + Description: Process corner resistor (rhigh)
  + Display: Corner R
  + Typical: typ
- temp
  + Description: Ambient temperature
  + Display: Temperature
  + Unit: °C
  + Typical: 27
- cload
  + Description: External load capacitance per output, to ground
  + Display: Cload
  + Unit: pF
  + Typical: 0.5
- ibias_err
  + Description: Common error of the four bias reference currents
  + Display: Ibias error
  + Unit: %
  + Typical: 0
- va_bias
  + Description: Early voltage of the bias reference sources (R_k = va_bias / I_k)
  + Display: VA bias
  + Unit: V
  + Typical: 1e12

## Symbol

![Symbol of s2d_mpdda_biased](s2d_mpdda_biased_symbol.svg)

## Schematic

![Schematic of s2d_mpdda_biased](s2d_mpdda_biased_schematic.svg)
