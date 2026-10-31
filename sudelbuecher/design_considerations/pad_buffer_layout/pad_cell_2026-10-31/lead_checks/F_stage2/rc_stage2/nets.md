# One net through the row?

Row length 331 µm. A band passes if every cell of the row has shapes of it in the band's y range and all of them are one net; the net's M3 / M4 / TM1 rail is named by the labels (x/25) on it. A band or rail passes if one net is present in every cell of the row.

| what | y (µm) | expected rail | cells with shapes | nets | result |
|---|---|---|---|---|---|
| NWell n+ | 6–61 | iovdd | 7 of 7 | 5 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| p+ ring | 65–84.4 | iovss | 7 of 7 | 1 | pass (anode/guard/iovss) |
| p+ plate | 84.5–140 | iovss | 7 of 7 | 1 | pass (anode/guard/iovss) |
| n+ in NWell | 148.35–148.65 | iovdd | 7 of 7 | 1 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| p+ | 156.85–157.15 | vss | 7 of 7 | 1 | pass (vss) |
| n+ in NWell | 166.85–167.15 | vdd | 7 of 7 | 1 | pass (vdd) |
| Metal3 rail | 7–32.5 | | 7 of 7 | 1 | pass (anode/guard/iovss) |
| Metal3 rail | 34.5–60 | | 7 of 7 | 1 | pass (anode/guard/iovss) |
| Metal3 rail | 66–91.5 | | 7 of 7 | 1 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| Metal3 rail | 93.5–119 | | 7 of 7 | 1 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| Metal3 rail | 126–134 | | 7 of 7 | 1 | pass (anode/guard/iovss) |
| Metal3 rail | 140–158 | | 7 of 7 | 1 | pass (vss) |
| Metal3 rail | 160–178 | | 7 of 7 | 1 | pass (vdd) |
| Metal4 rail | 7–32.5 | | 7 of 7 | 1 | pass (anode/guard/iovss) |
| Metal4 rail | 34.5–60 | | 7 of 7 | 1 | pass (anode/guard/iovss) |
| Metal4 rail | 66–91.5 | | 7 of 7 | 1 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| Metal4 rail | 93.5–119 | | 7 of 7 | 1 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| Metal4 rail | 126–134 | | 7 of 7 | 1 | pass (anode/guard/iovss) |
| Metal4 rail | 140–155.8 | | 7 of 7 | 1 | pass (vdd) |
| Metal4 rail | 162.2–178 | | 7 of 7 | 1 | pass (vss) |
| TopMetal1 rail | 7–32.5 | | 7 of 7 | 2 | pass (anode/guard/iovss) |
| TopMetal1 rail | 34.5–60 | | 7 of 7 | 2 | pass (anode/guard/iovss) |
| TopMetal1 rail | 66–91.5 | | 7 of 7 | 1 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| TopMetal1 rail | 93.5–119 | | 7 of 7 | 1 | pass (cathode/guard/iovdd/pad/pin1/supply) |
| TopMetal1 rail | 126–134 | | 7 of 7 | 1 | pass (anode/guard/iovss) |
