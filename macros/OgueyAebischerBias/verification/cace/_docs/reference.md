# reference

- Description: Oguey-Aebischer resistor-free bias reference + start-up kick, for the ihp-sg13cmos5l chip template
- PDK: ihp-sg13cmos5l

## Authorship

- Designer: Christoph Maier
- Created: September 4, 2026
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
- vbp
  + Description: PMOS current-mirror bias voltage (to downstream PMOS legs)
  + Type: signal
  + Direction: output
- vbn
  + Description: NMOS current-mirror bias voltage (to downstream NMOS legs)
  + Type: signal
  + Direction: output
- vbr
  + Description: Resistor-free reference node (Oguey-Aebischer core)
  + Type: signal
  + Direction: output
- disable
  + Description: Active-high shutdown of the core and start-up kick
  + Type: digital
  + Direction: input

## Default Conditions

- vdd
  + Description: Analog power supply voltage
  + Display: VDD
  + Unit: V
  + Typical: 3.3
- corner_mos
  + Description: Process corner MOSFET
  + Display: Corner MOSFET
  + Typical: tt
- corner_r
  + Description: Process corner resistor
  + Display: Corner R
  + Typical: typ
- temp
  + Description: Ambient temperature
  + Display: Temperature
  + Unit: °C
  + Typical: 27

## Symbol

![Symbol of reference](reference_symbol.png)

## Schematic

![Schematic of reference](reference_schematic.png)
