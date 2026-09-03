# Analog Pad Buffers for IHP SG13CMOS5L

**Design notes: figures of merit, reference topologies, and a bandwidth budget**

Christoph Maier — 3 September 2026

---

## 1. Scope

Working notes toward a differential-input, analog-output pad driver (and its
dual, a single-ended-pin to differential on-chip input buffer) for the IHP
SG13CMOS5L open-source variant, in the context of a Chipalooza submission.
These notes cover:

- which figures of merit are invariant under bias-current scaling, and are
  therefore the ones worth arguing about;
- what SG13CMOS5L removes relative to SG13G2, and how each omission
  constrains the topology choice;
- a reference bibliography of class-AB output stages;
- the relationship between the Monticelli and Hogervorst/Huijsing lineages;
- a bandwidth budget with conservative / reasonable / aggressive tiers.

Nothing here is silicon-verified. Numbers marked *estimate* are
order-of-magnitude reasoning, not simulation results.

---

## 2. Figures of merit, irrespective of bias current

If $W$ and $I$ are scaled together at fixed inversion level, then $g_m$, GBW
and SR all scale $\propto I$ while noise power scales $\propto 1/I$. The
quantities that survive that scaling are exactly the dimensionless ratios and
the per-current groups.

### 2.1 Genuinely intensive (no current anywhere)

| Quantity | Units | Comment |
|---|---|---|
| $g_m/I_D$ | V$^{-1}$ | Efficiency coordinate; everything else is downstream of where you sit on this curve |
| $(g_m/I_D)\cdot f_T$ | Hz/V | The honest speed–efficiency invariant; peaks in moderate inversion, $IC \approx 0.1\ldots1$ |
| $g_m r_o$ | — | Intrinsic gain; sets static gain error $1/(\beta A_0)$. In 130 nm: $\approx 25\ldots30$ at $L_\mathrm{min}$, $100\ldots300$ at $L \approx 1$ µm |
| $I_\mathrm{out,peak}/I_Q$ | — | Class-AB current gain. Class A pins this at 1. Decent AB stages: 10–100 |
| $V_\mathrm{out,pp}/V_\mathrm{DD}$ | — | Swing efficiency, i.e. $\sum V_\mathrm{DSsat}$ lost |
| $A_{VT} = V_\mathrm{os}\sqrt{WL}$ | mV·µm | Matching constant, $\approx 3\ldots5$ mV·µm thin-oxide; useful normalized form is $V_\mathrm{os}/V_\mathrm{out,pp}$ |
| CMRR, PSRR | dB | At the frequency of interest |
| GBW$/f_T$ | — | Technology utilization; usually humiliating, and usefully so |
| $\mathrm{SR}/(\mathrm{GBW}\cdot V_\mathrm{step})$ | — | $>2\pi$ means settling is linear rather than slew-limited |
| $\eta = P_\mathrm{load}/P_\mathrm{supply}$ | — | 25 % ceiling for class A into a resistive load |

### 2.2 Per-current groups

Invariant, but only comparable at equal $C_L$ and equal swing:

- $\mathrm{FoM_{SS}} = \mathrm{GBW}\cdot C_L / I_\mathrm{DD}$ [MHz·pF/mA]
- $\mathrm{FoM_{LS}} = \mathrm{SR}\cdot C_L / I_\mathrm{DD}$ [V·pF/(µs·mA)]
- NEF / PEF, or the raw invariant $v_{n,\mathrm{in}}^2 \cdot I_\mathrm{DD}$
- HD3 or SFDR, quoted at fixed $V_\mathrm{out,pp}/V_\mathrm{DD}$ **and** fixed
  $g_m/I_D$ — otherwise it measures the overdrive choice, not the topology

### 2.3 Pad-specific, and where such buffers actually fail

- **Transparency**: $C_\mathrm{in}/C_\mathrm{tapped\ node}$, plus kickback
  charge per unit input swing. For a monitor buffer on a low-current node this
  dominates everything else — the buffer that measures the DAC must not be the
  DAC's dominant load.
- **Stability across the load corner**: phase margin over $C_L$ from ~5 pF
  (bare pad + ESD) to ~50 pF + coax. A single-number GBW is meaningless
  without the load-range envelope.
- $|Z_\mathrm{out}(f)|$ and back-drive tolerance.
- Oxide field at the pad under ESD clamp turn-on.

### 2.4 The one that is not a ratio

**Area.** Offset and matching drag it in through $A_{VT}/\sqrt{WL}$, so any
FoM table that omits area is quietly comparing a 40 µm² driver to a 4000 µm²
one.

---

## 3. What SG13CMOS5L takes away

SG13CMOS5L is not SG13G2 minus the HBTs. Per IHP's open-source page, it
carries the SG13CMOS front end but has **no isolated NMOS, no MIM capacitor,
four thin metals and a single 2 µm TopMetal**. Three of those hit an output
driver directly.

### 3.1 No MIM capacitor

The compensation capacitor becomes a thick-oxide MOScap in accumulation or a
MOM comb on M1–M4. With only four thin metals, MOM density is poor and the
capacitor sits low in the stack where it couples to substrate. A MOScap is
voltage-dependent even in accumulation.

**Consequence:** any topology whose stability depends on precise pole–zero
cancellation — Miller with nulling resistor, nested Miller, active-feedback
compensation — becomes a corner-analysis problem. This is the strongest single
steer in the whole exercise:

> Prefer **load-compensated single-stage** architectures, where the dominant
> pole is $C_L$ at the pad and $C_c$ is either absent or non-critical. Folded
> cascode or current-mirror OTA with a class-AB output — not a two-stage
> Miller amplifier.

It also devalues the multistage-compensation literature (Leung & Mok
damping-factor control, Ho/Mok active feedback), which assumes a
well-characterized linear $C_c$.

### 3.2 No deep n-well / isolated NMOS

Every NMOS bulk is the global p-substrate, shared with whatever digital
neighbour the shuttle places next door.

- NMOS source followers take full body effect with no escape ⇒ PMOS devices in
  their own n-well become the preferred followers and level shifters.
- Substrate-coupled noise enters the output stage's NMOS side unfiltered ⇒
  keep the signal path PMOS-dominant where possible, and **carry the signal
  off-chip differentially rather than single-ended** if the measurement setup
  permits. If it must be single-ended at the pad, route a reference pad
  alongside as a pseudo-differential return and budget for the substrate noise
  that cannot be filtered.

### 3.3 One TopMetal, 2 µm, no TM2

Supply distribution to the output stage and the ESD return path are both
thinner than in SG13G2. This caps peak drive current and makes IR drop across
the pad ring a real term in the swing budget. It also removes a shielding
layer: with four thin metals, one must be spent on a shield plane over the
input pair, which is expensive when M4 is also the best MOM plate and the best
local supply mesh.

### 3.4 Revised FoM weighting

Given the above, the discriminating figures for this process are:

1. swing efficiency $V_\mathrm{out,pp}/\sum V_\mathrm{DSsat}$ on the 3.3 V
   thick-oxide rail;
2. phase margin across the full $C_L$ envelope **with $C_c$ at its ±30 %
   MOScap corner**;
3. PSRR and substrate-coupling rejection — a first-class spec here, not an
   afterthought;
4. area, since MOM/MOScap compensation is area-hungry and shuttle slots are
   small.

$g_m/I_D$ and intrinsic gain still set the design point but no longer
differentiate between candidates; the compensation and isolation constraints
do.

---

## 4. Reference designs — class-AB output stages

| # | Design / paper | Venue | Link |
|---|---|---|---|
| 1 | Monticelli, *A quad CMOS single-supply op amp with rail-to-rail output swing* — the floating-battery AB mesh | JSSC SC-21(6), 1986, 1026–1034 | [PDF (Iowa State)](http://class.ece.iastate.edu/djchen/ee501/2008/MonticelliRailToRailOutSwing.pdf) · [doi:10.1109/JSSC.1986.1052645](https://doi.org/10.1109/jssc.1986.1052645) |
| 2 | Carvajal, Ramírez-Angulo et al., *The flipped voltage follower* — FVF/DFVF taxonomy | TCAS-I 52, 2005, 1276–1291 | [doi:10.1109/TCSI.2005.851387](https://doi.org/10.1109/TCSI.2005.851387) |
| 3 | Sawigun & Demosthenous, *A compact rail-to-rail class-AB CMOS buffer with slew-rate enhancement* | TCAS-II, 2012 | [IEEE Xplore](https://ieeexplore.ieee.org/document/6236111/) |
| 4 | *High-speed rail-to-rail class-AB buffer with compact adaptive biasing for FPD* | MDPI Electronics 9(12), 2020 | [open access](https://www.mdpi.com/2079-9292/9/12/2018) |
| 5 | Ramírez-Angulo / Carvajal et al., *Class-AB output stages with accurate quiescent current control by dynamic biasing* | Analog Integr. Circ. Sig. Process. | [Springer](https://link.springer.com/article/10.1023/A:1024453731969) |
| 6 | *Low-voltage class-AB output stages using floating capacitors* — the sub-$2V_{GS}$ alternative to Monticelli | Electron. Lett. lineage | [PDF](https://www.academia.edu/22725840/Low_voltage_class_AB_output_stages_for_CMOS_op_amps_using_floating_capacitors) |
| 7 | Hogervorst et al., *Rail-to-rail constant-$g_m$ input stage and class-AB output stage* | Analog Integr. Circ. Sig. Process. | [Springer](https://link.springer.com/article/10.1007/BF01239246) |
| 8 | *Rail-to-rail low-power high-slew-rate CMOS analogue buffer* — <32 fF input capacitance | — | [Academia](https://www.academia.edu/10744243/Rail_to_rail_low_power_high_slew_rate_CMOS_analogue_buffer) |
| 9 | *Rail-to-rail high-speed class-AB CMOS buffer with enhanced slew rate* — 1 nF at 3.5 µA $I_Q$ | — | [ResearchGate](https://www.researchgate.net/publication/274173822_A_Rail-To-Rail_Hign_Speed_Class-AB_CMOS_Buffer_with_Low_Power_and_Enhanced_Slew_Rate) |
| 10 | López-Martín et al., *The Flipped Voltage Follower: Theory and Applications* | Springer LNEE | [chapter](https://link.springer.com/chapter/10.1007/978-3-642-36329-0_12) |

**Bibliography only (link not verified; all appear in the reference lists of
the above):**

- F. You, S. H. K. Embabi, E. Sánchez-Sinencio, "Low-voltage class-AB buffers
  with quiescent current control," *JSSC* 33(6), 1998, 915–920.
- M. de Langen, J. H. Huijsing, *JSSC* 33(10), 1998, 1482–1496.
- G. Giustolisi, G. Palmisano, "1.2-V op-amp with a dynamically biased output
  stage," *JSSC* 35(4), 2000, 632–636.
- M. D. Pardoen, M. G. Degrauwe, "A rail-to-rail CMOS input/output power
  amplifier," *JSSC* 25(4), 1990, 501–504.
- J. A. Fisher, R. Koch, "A highly linear CMOS buffer amplifier," *JSSC* 22,
  1987, 330–334.
- R. Hogervorst, J. P. Tero, R. G. H. Eschauzier, J. H. Huijsing, "A compact
  power-efficient 3 V CMOS rail-to-rail input/output operational amplifier for
  VLSI cell libraries," *JSSC* 29(12), Dec. 1994, 1505–1513.

### 4.1 Reading order for this process

Items 1 and 6 should be read against each other: Monticelli's mesh costs more
than $2V_{GS}$ of headroom but needs no capacitor, whereas the
floating-capacitor variants buy headroom back by spending exactly the
component SG13CMOS5L does not provide. Items 3 and 4 are the useful pair on
slew enhancement. Item 2 is the compactness reference whose offset and PSRR
must be characterized independently, since the papers largely do not.

---

## 5. Monticelli vs. Hogervorst & Huijsing — different axes

They are not the same topology, and the confusion is worth dissolving because
the two names sit on **different axes**.

**Monticelli (1986)** is about a class-AB *output* stage plus quiescent-current
control. Its input stage is a conventional single pair: the abstract claims an
output swing to either rail together with an input common-mode range that
includes ground — ground-sensing, *not* rail-to-rail input.

**Hogervorst & Huijsing**'s headline contribution is precisely what Monticelli
lacks: the **constant-$g_m$ rail-to-rail input stage**, two complementary pairs
with tail-current steering so $g_{m,\mathrm{tot}}$ stays flat as the common
mode sweeps. They publish output stages too, but the usual pairing in the
literature is *Hogervorst input + some floating class-AB output*, and that
output can perfectly well be Monticelli's mesh. **They compose rather than
compete.**

### 5.1 Where they do overlap

Both output stages belong to Huijsing's **feedforward** class-AB control
family: a floating voltage source (translinear loop) between the two output
gates. This is distinct from **feedback** control with an explicit
minimum-current selector — the de Langen & Huijsing branch (*JSSC* 1998),
which senses the smaller of the two output currents and regulates it, giving
tighter $I_Q$ over corners at the cost of a loop that can ring.

So Monticelli and the Hogervorst compact output stage are cousins; the Delft
feedback-controlled stages are a different animal.

### 5.2 Two practical differences

**Headroom.** Monticelli's mesh needs roughly $2V_{GS} + 2V_\mathrm{DSsat}$ of
stack. That is exactly the criticism levelled by the floating-capacitor
school, whose stated advantage is accurate quiescent control at supplies near
one threshold, where Monticelli's requires more than $2V_{GS}$. On a 3.3 V
thick-oxide rail with $V_T \approx 0.5\ldots0.7$ V this is affordable; on the
1.2 V core it is not.

**Drive asymmetry.** The mesh is not symmetric in the small-signal path. One
output device's gate is driven directly by the cascode current; the
complementary device is driven *through* the mesh, which behaves as an
additional cascode stage with a pole set by $1/g_m$ of the mesh device and the
capacitance at that node — contributing a non-dominant pole and extra delay on
that path only. This shows up as unequal rising/falling settling, and it
interacts badly with a compensation capacitor of uncertain value. Treat that
pole's location as a corner variable and simulate it explicitly rather than
trusting a nominal phase margin.

---

## 6. Hogervorst et al. 1994 as a donor design

*R. Hogervorst, J. P. Tero, R. G. H. Eschauzier, J. H. Huijsing, "A Compact
Power-Efficient 3 V CMOS Rail-to-Rail Input/Output Operational Amplifier for
VLSI Cell Libraries," JSSC 29(12), Dec. 1994, 1505–1513.*

Verdict: usable as an **output-stage donor, not as a cell to copy**.

### 6.1 Keep — the output stage and its biasing (Figs. 5, 8, 11)

The floating class-AB control $M_{19}/M_{20}$ shifted *into* the folded-cascode
summing circuit means the AB control contributes neither noise nor offset: the
two bias sources $I_{b6}/I_{b7}$ that would otherwise sit in parallel with the
cascodes $M_{14}/M_{16}$ are eliminated outright. The floating current source
$M_{27}$–$M_{28}$, built with the *same* translinear structure as the AB
control so that its supply dependence cancels the control's, yields an $I_Q$
that does not walk with $V_\mathrm{DD}$. A real solution to a real problem, at
a cost of two transistors.

Table I of that paper was measured at exactly 3.3 V — the same rail as IOVDD
on the 5L shuttle — with two stacked $V_{GS}$ in the output stage, which on
IHP thick-oxide devices ($V_T \approx 0.5\ldots0.7$ V) leaves room.

### 6.2 Discard — the constant-$g_m$ rail-to-rail input apparatus (Section II)

For a differential *on-chip* input at fixed, known common mode, everything in
their Figs. 1–4 is pure cost: the complementary pairs, the two current
switches, the 3× mirrors $M_6$–$M_7$ and $M_9$–$M_{10}$, plus $M_{29}$–$M_{31}$
whose only job is to keep the positive-feedback loop from arming below 2.9 V.

What it buys in defects, from their own Table I and Section VI:

- CMRR collapses to **43 dB** in the take-over ranges, against 70 dB elsewhere;
- offset shifts about **2 mV per take-over range**;
- slew rate changes by a **factor of two** depending where the common mode
  sits (2 → 4 V/µs Miller; 4 → 8 V/µs cascoded-Miller).

A single PMOS pair at fixed common mode gives constant $g_m$, constant SR, no
take-over artifacts, better CMRR, a bulk-tied-to-source device in its own
n-well (which matters with no deep n-well available), and roughly 40 % of the
area back.

### 6.3 The porting obstacle — $C_{M1}/C_{M2}$

They are Miller capacitors tied from $V_o$ to the output-device gates, so the
**full output swing stands across them**. With MIM that is free; in 5L it means
MOM fingers on four thin metals, or a thick-oxide MOScap that will traverse
accumulation-to-depletion as the output swings — a compensation capacitor that
changes value with the signal it is compensating.

Two mitigations available from the paper itself:

1. The plain-Miller version has **66° phase margin** versus **53°** for
   cascoded-Miller. Take the Fig. 13 variant and spend the margin on capacitor
   uncertainty rather than on bandwidth.
2. They note cascoded-Miller can peak at high output current and recommend
   plain Miller above ~3 mA — which points the same way for a driver.

### 6.4 Two numbers that will not survive the port

- **Gain.** Their 85 dB came from 1 µm devices. On 130 nm thick-oxide with the
  same cascoding, budget 60–70 dB (*estimate*); their own pointer to Bult &
  Geelen gain boosting on $M_{14}/M_{16}$ becomes less optional.
- **Load.** 10 kΩ ‖ 10 pF at 3 mA peak is a *chip-level* buffer. A metre of
  coax plus a scope front end is 100 pF and change. Scaling the output devices
  for that raises $C_{GS,\mathrm{out}}$, drags the output pole down, and forces
  $C_M$ up — straight back into the capacitor problem. Size that loop before
  committing.

Their figure of merit, $F = B/P_\mathrm{sup}$ at $C_L = 10$ pF, is
supply-referred rather than current-referred; convert to
$\mathrm{GBW}\cdot C_L/I_\mathrm{DD}$ to compare against anything modern.

### 6.5 Incidental

The Fig. 6 → 8 → 9 → 10 → 11 progression, in which each figure repairs one
named defect of its predecessor, is unusually clean design-rationale writing.
If the shuttle wants documentation rather than only a GDS, that structure is
worth reusing as a template.

---

## 7. Bandwidth budget

### 7.1 The load sets everything on the output side

For a load-compensated single stage,

$$\mathrm{GBW} = \frac{g_m}{2\pi C_L}$$

$C_L$ is not the pad. It is pad (a few hundred fF) + ESD (~1 pF) + bond wire +
PCB trace + whatever instrument is attached. A 10× scope probe alone is
10–15 pF. **Budget $C_L \approx 15$ pF** as the honest bench number, and
50–100 pF if anyone ever hangs un-terminated coax on it.

At $C_L = 15$ pF:

| Target GBW | Required $g_m$ | $I_D$ at $g_m/I_D = 10$ V$^{-1}$ |
|---|---|---|
| 10 MHz | 0.94 mS | ≈ 95 µA |
| 100 MHz | 9.4 mS | ≈ 1 mA |

Current is not the wall. **The non-dominant poles are.** A thick-oxide 3.3 V
device at $L \approx 1$ µm in moderate inversion has $f_T$ of perhaps
1–3 GHz (*estimate*), and the mirror and cascode poles will land in the low
hundreds of MHz. Pushing GBW to 100 MHz puts the unity-gain crossing
uncomfortably close to them — while the compensation capacitor's value is
uncertain because there is no MIM.

### 7.2 Slew usually binds first

Full-power bandwidth requires $\mathrm{SR} = 2\pi f V_\mathrm{pk}$, i.e. peak
current $I = C_L \cdot \mathrm{SR}$. For 1 V peak at 10 MHz into 15 pF that is
≈ 0.94 mA of peak drive — comfortable for a class-AB stage running 50 µA
quiescent. At 100 MHz it is 9.4 mA, which on a single 2 µm TopMetal supply
route starts consuming the swing budget in IR drop.

**Quote small-signal GBW and full-power bandwidth separately.** They are not
the same spec, and the gap between them is the entire point of class AB.

### 7.3 Calibration tiers — output buffer (differential in → single-ended pin)

| Tier | GBW | FPBW at 1 V$_\mathrm{pk}$ | Risk |
|---|---|---|---|
| Conservative | 1–5 MHz | ~1–2 MHz | first silicon works, no drama |
| **Reasonable** | **10–30 MHz** | **5–10 MHz** | sweet spot; poles comfortably clear |
| Aggressive | 50–100 MHz | 20 MHz | pole management becomes the whole design; MOScap $C_c$ uncertainty acute |
| Don't | > 200 MHz | — | stop calling it a buffer |

Above roughly 100 MHz through a wire-bonded pad into an unknown board, the
problem stops being "amplifier" and becomes "transmission line": an
impedance-matched 50 Ω driver is wanted, the load turns resistive, and power
rises by an order of magnitude. Different project.

### 7.4 The input buffer is an easier problem

Single-ended pin → differential on-chip drives only internal capacitance —
call it 200–500 fF. 50 MHz needs under 100 µS of $g_m$. The limits here are
the ESD structure's series RC, the input pair's own matching and noise, and
the fact that deliberate band-limiting is usually *wanted* for anti-aliasing
and noise.

**50–100 MHz is comfortable; 20 MHz is conservative.** The asymmetry between
the two directions is real — roughly a decade of headroom.

### 7.5 Two arguments for staying low

- Noise scales as $\sqrt{\mathrm{BW}}$. If the path characterizes anything
  quiet, excess bandwidth is a direct loss of resolution.
- Keeping GBW modest lets $C_L$ be the dominant pole and lets the Miller
  capacitor be dropped entirely — the cleanest escape from the no-MIM problem
  of §3.1.

### 7.6 Working stake

**20 MHz out, 50 MHz in.** With the caveat that the right answer depends on
what is being observed: DC bias characterization needs 1 MHz; observing a
settling transient needs whatever bandwidth resolves the settling constant of
interest.

---

## 8. FPBW — definition

**Full-Power Bandwidth**: the highest frequency at which the amplifier still
delivers its *full rated output swing* without the waveform being distorted by
slew-rate limiting.

The derivation is one line. For $V_\mathrm{out} = V_\mathrm{pk}\sin(2\pi f t)$,
the maximum rate of change occurs at the zero crossing:

$$\left.\frac{dV}{dt}\right|_\mathrm{max} = 2\pi f V_\mathrm{pk}$$

The amplifier can only supply $dV/dt$ up to its slew rate. Setting them equal:

$$\boxed{\ \mathrm{FPBW} = \frac{\mathrm{SR}}{2\pi V_\mathrm{pk}}\ }$$

Above that frequency the output stops being a sine and becomes a triangle
wave: the amplifier is charging $C_L$ with all the current it has and cannot
turn around fast enough. This is a hard, ugly, large-signal nonlinearity, not
a gentle roll-off.

### 8.1 Why it is separate from GBW

GBW is a **small-signal** spec — how fast the amplifier responds to a wiggle
small enough that everything stays linear. FPBW is **large-signal** — how fast
it responds when asked for the whole swing.

A class-A stage with fixed tail current $I$ has $\mathrm{SR} = I/C_L$, and its
FPBW can be a factor of ten or more below its GBW. It then looks fast on a
Bode plot and turns a 1 V sine into a triangle. Closing that gap is exactly
what class AB is for: on a large step the output devices deliver many times
the quiescent current, so SR is no longer pinned to $I_Q$.

The ratio $\mathrm{SR}/(\mathrm{GBW}\cdot V_\mathrm{step})$ from §2.1 is the
same idea in dimensionless form. Above about $2\pi$, the amplifier settles by
linear exponential decay and the FPBW spec does not constrain; below it,
slewing dominates the settling time and GBW is a fiction.

### 8.2 Consistency check

1 V peak at 10 MHz needs $\mathrm{SR} = 2\pi\times10^7\times1 \approx 63$ V/µs;
into 15 pF, $I = C\cdot\mathrm{SR} \approx 0.94$ mA — the same figure as §7.1.
The peak-current and FPBW framings are one calculation wearing two hats.

---

## 9. Open questions before committing

1. Does `ihp-sg13cmos5l` ship an **analog pad cell** — an unbuffered pad with a
   characterized ESD network and known parasitic capacitance — or only digital
   I/O cells? If digital-only, the choice is between designing an ESD
   structure (probably not sign-off-able on a shared shuttle) and living with a
   digital pad's diode clamps in the analog path.
2. What does the Chipalooza floorplan allow for **pad allocation**, and is an
   analog supply domain separate from IOVDD available at all?
3. Is the far end of the link a **differential receiver**? If so, do not
   collapse to single-ended on chip (§3.2).
4. What is the actual $C_L$ envelope of the intended bench setup? Everything in
   §7 hangs on it.

---

## 10. Provenance and caveats

- The SG13CMOS5L device/BEOL inventory is taken from IHP's open-source request
  page, which described the open PDK as under development for early 2026. Verify
  against the `IHP-GmbH/ihp-sg13cmos5l` repository rather than the marketing
  page.
- Items 1–10 in §4 have verified links. The bibliography-only list does not;
  those citations come from the reference lists of the linked papers.
- The Monticelli-vs-Huijsing feedforward/feedback taxonomy in §5.1 is asserted
  from secondary sources. Huijsing's *Operational Amplifier Theory and Design*
  carries the canonical version and should be checked before the distinction
  carries weight in a design justification.
- Every number marked *estimate* is order-of-magnitude reasoning. Nothing here
  has been simulated in SG13CMOS5L.
