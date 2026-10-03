Agreed. Your output buffer's load is mostly the clamp frames and the pad. The input buffer's load is gate capacitance plus routing, so class A is enough. The topology that fits is the **mirror image of your matched-pair DDA driver (`d2s_mpdda`)**: a fully differential, single-stage folded cascode, compensated by its load capacitance.

**Same unit cell, swapped roles**

Use the same split-tail PMOS unit with rhigh between the sources (unit_r). Arrange it so the loop forces:

```
f(vin − vref) + f(vin − vref)  =  f(vop − vcm) + f(vcm − von)
```

- The two input units both take `(vin, vref)`.
- The two feedback units take `(vop, vcm)` and `(vcm, von)`.
- With vop = vcm + u and von = vcm − u, the balance becomes 2f(vin − vref) = 2f(u). So u = vin − vref and vop − von = 2(vin − vref).

This is the inverse of the driver's ½. As in the driver:

- The gain is set by the count of matched units, not by R or gm.
- Each unit's nonlinearity cancels within the buffer, to the extent the units match. It doesn't just cancel in the loopback test.
- Every unit still has one gate at a reference, so the "output depends only on gp − gn" condition that unit_r passes still applies.

There's also a bonus: the pad-side reference (vref) and the internal common mode (vcm) are separate inputs. A pin reference that isn't vcm costs nothing.

**Load-compensated output stage**

Topology B's two weaknesses don't apply here:
- The output devices aren't ESD clamps, so you can cascode them freely and get the loop gain back.
- There are no resistive loads on chip, since all your internal inputs are gates.

The output nodes are the only high-impedance nodes. Phase margin rises with C_L, so switching the outputs onto `analog_bus` for test 3 only slows the buffer down; it doesn't destabilize it. A rough estimate is f_c ≈ G_m,unit / (2π·C_L). With the 15.6 µS unit and about 2 pF per side, that's around 1.2 MHz, in the same range as the driver. Bandwidth scales with the unit's G_m (its R), not with the gain.

**CMFB**

The feedback units only see the differential signal. A common-mode shift c appears as f(u + c) + f(u − c), which is second order in c. So you need a separate common-mode loop:
- Use two more identical units, `(vop, vcm)` and `(von, vcm)`, summed with the same polarity into the gates of the PMOS cascoded loads (Duque-Carrillo-style DDA CMFB).
- With an odd f, the differential signal cancels and the loop senses c linearly.
- No resistive averaging loads the high-impedance outputs.

**Things to watch**

- **Input range:** PMOS units handle `vin` down to vssio, provided vref is low enough for the ±0.5 V window. The top end runs out somewhere around 2 V. Going rail-to-rail ("should include vdd3v3") would need complementary NMOS units, and that breaks the identical-unit cancellation. I'd treat it as a non-goal.
- **Offset and noise matter more here,** because this block is first in the chain. Your improvements analysis applies directly: the offset is the folding-sink current mismatch divided by G_m. Size the sinks and the load mirror for matching, not only for headroom.

**Why not the textbook alternatives**

- **Follower plus inverting amplifier:** needs resistors that the output stages must drive. The extra delay in the inverting path turns differential signal into common mode at high frequency. The common mode is tied to vref.
- **Fully differential amplifier with resistive feedback:** loads the pad, unless you put a follower in front of it. Its input common mode also moves with the signal.

I can write the `s2d_mpdda` netlist next to `d2s_mpdda`, reusing the same unit subcircuit, if you'd like to simulate it.
