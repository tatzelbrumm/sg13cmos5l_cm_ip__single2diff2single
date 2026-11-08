# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Run tb_states and tb_powerup of en_ctrl_3v3 (v2) at 11 corner / temperature / supply points; write the table.

usage (repo env, from this directory): python3 -I run_states.py   -> results/states.txt (decks and logs in runs/)

tb_states walks the cell through the harness's supply states: slot vdd_3v3 and vdd_1v2 behind PMOS power switches
as in the harness, vdd_1v2 off (discharged) and floating at 0.62 V, vdd_3v3 floating at 0.6 V; enable and sel0 as
valid 1.2 V levels throughout. Currents are the cell's own (ammeters on its supply pins), averaged over 2 us at the end
of each state. tb_powerup ramps vdd_3v3 with enable already high and vdd_1v2 off (the default mode).
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
RES = HERE / "results"
POINTS = [("tt", 27, 3.3, 1.2), ("ss", -40, 3.0, 1.08), ("ss", -40, 3.6, 1.08), ("ff", 125, 3.6, 1.32),
          ("ff", 125, 3.0, 1.32), ("fs", 125, 3.6, 1.32), ("sf", -40, 3.0, 1.08), ("sf", 125, 3.6, 1.32),
          ("fs", -40, 3.0, 1.08), ("tt", -40, 3.3, 1.2), ("tt", 125, 3.3, 1.2)]
CUR = ["ih_off0", "ih_en", "ih_ensel", "ih_dis", "ih_en_l0", "ih_dis_l0b", "ih_dis_lfl", "ih_en_lfl"]
LOGIC = [("v_en", 1), ("v_dis", 0), ("v_en_l0", 1), ("v_dis_l0", 0), ("v_en_lfl", 1), ("s0_on", 1), ("s0_off", 0),
         ("s0_l0", 1)]


def run(tb, c, t, vh, vl):
    deck = (HERE / tb).read_text()
    for k, v in (("@C@", c), ("@T@", t), ("@VH@", vh), ("@VL@", vl), ("@VH2@", vh / 2)):
        deck = deck.replace(k, str(v))
    f = RUNS / f"{tb.split('.')[0]}_{c}_{t}_{vh}.spice"
    f.write_text(deck)
    log = subprocess.run(["ngspice", "-b", f.name], cwd=RUNS, capture_output=True, text=True).stdout
    f.with_suffix(".log").write_text(log)
    vals = dict(re.findall(r"^(\w+)\s+=\s+(\S+)", log, re.M))
    vals["stalls"] = log.count("Timestep too small")
    return vals


def main():
    RUNS.mkdir(exist_ok=True)
    RES.mkdir(exist_ok=True)
    lines = ["# en_ctrl_3v3 v2: supply states (tb_states) and power-up with enable high (tb_powerup)",
             "# currents in nA (cell's vddh pin), delays in ns (50 fF on en_3v3 / en_3v3_b); logic: ok = within 5 % of"
             " vddh of the wanted level",
             "# states: off0 = powered, en 0 | en = enabled | ensel = enabled, sel0 1 | dis = disabled | en_l0 = enabled,"
             " sel0 1, vdd_1v2 off | dis_l0b = disabled, vdd_1v2 off | dis_lfl / en_lfl = vdd_1v2 floating at 0.62 V",
             "corner  T    vddh " + " ".join(f"{k[3:]:>8s}" for k in CUR) + "  logic(8)  t_en t_dis  powerup  stalls"]
    bad = 0
    for c, t, vh, vl in POINTS:
        s = run("tb_states.spice.in", c, t, vh, vl)
        p = run("tb_powerup.spice.in", c, t, vh, vl)
        cur = " ".join(f"{float(s[k]) * 1e9:8.1f}" if k in s else "      --" for k in CUR)
        ok = all(k in s and abs(float(s[k]) - w * vh) < 0.05 * vh for k, w in LOGIC)
        pu = "pu_en" in p and abs(float(p["pu_en"]) - vh) < 0.05 * vh
        bad += (not ok) + (not pu) + s["stalls"] + p["stalls"]
        lines.append(f"{c:3s} {t:5d} {vh:4.1f}  {cur}  {'ok' if ok else 'BAD':8s} {float(s['t_en']) * 1e9:5.1f}"
                     f" {float(s['t_dis']) * 1e9:5.0f}  {'ok' if pu else 'BAD':7s}  {s['stalls']}/{p['stalls']}")
    lines.append(f"# {'all states correct' if bad == 0 else f'{bad} failures'}")
    (RES / "states.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
