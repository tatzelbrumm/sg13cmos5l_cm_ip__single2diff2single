# d2s_miller_biased

- Description: Class-AB pad driver + bias fixture, differential in / single-ended out, gain 1/2, Miller compensated (proof of concept)
- PDK: ihp-sg13cmos5l

## Authorship

- Designer: Christoph Maier
- Created: October 2, 2026
- License: Apache-2.0 WITH SHL-2.1
- Company: None
- Last modified: None

## Pins

- vdd
  + Description: Positive analog power supply
  + Type: power
  + Direction: inout
  + Vmin: 3.0
  + Vmax: 3.6
- vss
  + Description: Analog ground
  + Type: ground
  + Direction: inout
- vinp
  + Description: Differential input, positive (vout - vref = (vinp - vinn) / 2)
  + Type: signal
  + Direction: input
- vinn
  + Description: Differential input, negative
  + Type: signal
  + Direction: input
- vref
  + Description: Output reference (feedback pair, other gate)
  + Type: signal
  + Direction: input
- vout
  + Description: Pad output (output devices = ESD clamp frames)
  + Type: signal
  + Direction: inout
- vfb
  + Description: Feedback input (feedback pair gate), tied to vout in the application
  + Type: signal
  + Direction: input
- vbp
  + Description: Bias, PMOS tail current sources (20 uA reference)
  + Type: signal
  + Direction: inout
- vbn
  + Description: Bias, NMOS folding sinks (50 uA reference)
  + Type: signal
  + Direction: inout
- vbpc
  + Description: Bias, PMOS mirror cascode
  + Type: signal
  + Direction: inout
- vbnc
  + Description: Bias, NMOS folding cascode
  + Type: signal
  + Direction: inout
- vabp
  + Description: Bias, class-AB control PMOS (translinear reference)
  + Type: signal
  + Direction: inout
- vabn
  + Description: Bias, class-AB control NMOS (translinear reference)
  + Type: signal
  + Direction: inout

## Default Conditions

- vdd
  + Description: Analog power supply voltage
  + Display: VDD
  + Unit: V
  + Typical: 3.3
- vref
  + Description: Output reference voltage
  + Display: Vref
  + Unit: V
  + Typical: 1.65
- vicm
  + Description: Input common-mode voltage
  + Display: Vicm
  + Unit: V
  + Typical: 1.65
- corner_mos
  + Description: Process corner MOSFET
  + Display: Corner MOSFET
  + Typical: tt
- corner_r
  + Description: Process corner resistor
  + Display: Corner R
  + Typical: typ
- corner_c
  + Description: Process corner MOM capacitor
  + Display: Corner C
  + Typical: typ
- temp
  + Description: Ambient temperature
  + Display: Temperature
  + Unit: °C
  + Typical: 27
- rload
  + Description: Load resistance, vout to vterm
  + Display: Rload
  + Unit: Ω
  + Typical: 1000
- vterm
  + Description: Load termination voltage
  + Display: Vterm
  + Unit: V
  + Typical: 1.65
- cload
  + Description: Load capacitance, vout to ground
  + Display: Cload
  + Unit: pF
  + Typical: 100
- ibias_err
  + Description: Common error of the six bias reference currents
  + Display: Ibias error
  + Unit: %
  + Typical: 0
- va_bias
  + Description: Early voltage of the bias reference sources (R_k = va_bias / I_k)
  + Display: VA bias
  + Unit: V
  + Typical: 1e12

## Symbol

![Symbol of d2s_miller_biased](d2s_miller_biased_symbol.svg)

## Schematic

![Schematic of d2s_miller_biased](d2s_miller_biased_schematic.svg)
