# 2026-10-26 · Fable · pad buffer alternatives (literature search) and the logging method

- Session `4efc77f5-dbfc-5127-ba7b-d3fee4e24367`, configured model `claude-fable-5-1` (the serving model may differ), cloud container linked to the user's computer, attached to the claude.ai Project "Chipalooza sg13cmos5l".
- Running log of the same work: `sudelbuecher/design_considerations/pad_buffer_alternatives/log.md`. Result: `sudelbuecher/design_considerations/pad_buffer_alternatives/alternatives.md`, with the four search reports in `research/`.
- Source: the raw transcript `~/.claude/projects/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367.jsonl` in the cloud container, extracted by script (`sudelbuecher/design_considerations/pad_buffer_alternatives/export.py`), records in file order along the live chain.
- User messages are verbatim, without system reminders and the app's file-delivery notices. Visible replies are verbatim. Tool calls are `*[ ]*` summaries: tool name and the first line of the main argument cut at 150 characters, plus tool errors. The four search agents' reports are not in this file; they are the `research/` files. The internal reasoning is not included; the script checks that no 40-character window of it occurs here and prints counts only.
- Two user interruptions at 02:18 cancelled the first three search agents; they were started again at 02:19.
- No classifier stop in this session up to the export.
- Export made 2026-10-26 02:53 and again 03:16 by the session itself, each time up to and including the command that built it. The replies after it are not included. The second export adds the series-resistor study (R_s before/after the feedback, decks and results in `design_considerations/pad_buffer_alternatives/sim/`, note `series_resistor.md`) and the brainstorm of 02:55.
- Times are Europe/Berlin (CET).

## Turn 1 — 2026-10-26 02:13

**User:** it turns out that the source degraded single2diff and diff2single buffer amplifiers for the input and output analog pad buffers might take up too much space. do a deep search for circuit design alternatives that use less area and, ideally, are both faster (more than just 1MHz bandwidth) and have a wider voltage range.

Also, look at sg13cmos5l design consolidation chatlog and running log, and others, and figure out a way to log your work without disclosing so much of your inner workings that Anthropic blocks the logging process.

**Assistant:** I'll start by reading the project context (memory, project doc, and the logs on your computer), then run the circuit-alternatives research.

*[mcp__memory__memory_read: ["/projects/01a0afda-3122-7637-8403-560f8cf5b625/areas/chipalooza-proposal.md", "/projects/01a0afda-3122-7637-8403-560f8cf5b625/preferences.md", "/pro…]*

*[mcp__remote-devices__device_bash: `ls $HOME/mnt/; echo ---; ls -la $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher; echo ---; ls $HOME/mnt/sg13cmos5l_cm_ip__single2diff2sing…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher; cat CLAUDE.md; echo ---; ls -la Claude Claude/* skunkworx sudelbuecher | head -150`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; ls -la chatlog chatlog/* logs logs/* design_considerations texte | head -…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; cat chatlog/README.md; echo ======; ls -la logs logs/*; echo ======; ls -…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; cat chatlog/2026-09-28_opus_safety_stops_and_chatlog_export.md | head -25…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; sed -n 250,420p chatlog/2026-09-28_opus_safety_stops_and_chatlog_export.m…`]*

*[error: Exit code 1]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; ls cheatsheets; echo ====; ls -la design_considerations/consolidation des…`]*

*[Read: /mnt/user-data/attachments/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/072edc99-size_mockup_old_vs_new.png]*

*[Read: /mnt/user-data/attachments/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/5370a651-pooled.png]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations; cat pad_buffer_layout/log.md`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations; head -c 14000 class_ab_pad_driver/class_ab_pad_driv…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations; sed -n 1,400p pad_buffer_layout/layout_primitives.m…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations; sed -n 183,230p pad_buffer_layout/layout_primitives…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations; head -c 9000 s2d_input_buffer/s2d_input_buffer.md; …`]*

*[Bash: `ls ~/.claude/projects/ 2>/dev/null; ls -la ~/.claude/projects/-home-claude/ 2>/dev/null | tail -5`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; ls verbatim_chatlog_recovery; find . -name "*.py" | grep -i -E "chatlog|e…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; cat verbatim_chatlog_recovery/verbatim-chatlog-export.md | head -150`]*

*[TaskCreate: Literature search: area-efficient, fast, wide-range pad buffer alternatives]*

*[TaskCreate: Write findings note into design_considerations/ on the computer]*

*[TaskCreate: Running log + script-exported chat log per the sudelbuecher precedent]*

*[TaskUpdate: 1]*

*[Agent: Research rail-to-rail compact buffers]*

*[Agent: Research S2D converter topologies]*

*[Agent: Research linearized transconductors and DDA area]*

## Turn 2 — 2026-10-26 02:18

**User:** it would be nice if poly resistors could be avoided altogether. they tend to be bulky and their parameter spread could be all over the place.

**Assistant:** Noted — resistor-free is now a hard constraint. I'm passing it to the three running searches and adding a fourth focused on resistor-free, MOS-only approaches.

*[SendMessage: Add resistor-free constraint to buffer search]*

*[SendMessage: Add resistor-free constraint to S2D search]*

*[SendMessage: Add resistor-free constraint to transconductor search]*

## Turn 3 — 2026-10-26 02:18

**User:** Make that a firm, not a hard constraint.

**Assistant:** Understood: strong preference for MOS-only, resistor-based options still allowed but ranked below. The interruptions cancelled the three searches, so I'm relaunching them with the updated brief.

*[Agent: Research rail-to-rail compact buffers]*

*[Agent: Research S2D converter topologies]*

*[Agent: Research resistor-free linearized transconductors]*

*[Agent: Research open-PDK precedents]*

**Assistant:** While those run, I'll pull the current unit and buffer netlists to have exact device counts for the area comparison.

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single/macros; cat sg13cmos5l_IOPadDiff2Single/netlist/source/units.spice | grep -v "^\*" | head -60; echo …`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/improvements; sed -n 75,140p pro…`]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad && mkdir -p logbuild && python3 - <<'EOF'`]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/export.py]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && printf '# header placeholder\n' > h.md && python3 -I export.…`]*

*[Edit: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/export.py]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && python3 -I export.py /root/.claude/projects/-home-claude/4ef…`]*

**Assistant:** The export tool is ready (3 turns so far, all text verified, no overlap with anything excluded). I'll start the running log now and fill in the research results as the four searches come back.

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/log.md]*

*[ToolSearch: `select:Monitor`]*

**Assistant:** The four searches are running; I'll wait for their results rather than poll. Nothing further needed from you right now.

*[background task notification: Agent "Research open-PDK precedents" finished; its report is saved verbatim under `research/`]*

**Assistant:** One search finished (open-PDK precedents); saving it and waiting for the other three.

*[Bash: `mkdir -p /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/research && echo "saved placeholder"`]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/research/4_open_pdk_precedents.md]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/research/1_rail_to_rail_buffers.md]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/research/2_s2d_converters.md]*

**Assistant:** Three of four searches are in; waiting for the last one (resistor-free transconductors) before writing the synthesis.

*[background task notification: Agent "Research resistor-free linearized transconductors" finished; its report is saved verbatim under `research/`]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/research/3_linearized_transconductors.md]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/IHP-Open-PDK; ls; ls ihp-sg13cmos5l/libs.tech/ngspice/models 2>/dev/null | grep -i mism; grep -h -i -E "avto|factuo|^\.param.*vt.*mism" i…`]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/alternatives.md]*

*[Bash: `S=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad; O=/mnt/user-data/outputs/pba1; mkdir -p $O/research && cp $S/logbuild/al…`]*

*[mcp__remote-devices__device_commit_files: [{"stagedPath": "/mnt/user-data/outputs/pba1/alternatives.md", "devicePath": "/home/cmaier/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudel…]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/pad_buffer_alternatives && sha256sum alternatives.md…`]*

**Assistant:** Design results are on your computer with matching checksums. Now the logs: running log, then the script-exported chat log and the README entry.

*[TaskUpdate: 1]*

*[TaskUpdate: 2]*

*[TaskUpdate: 3]*

*[Bash: `cat >> /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/log.md <<'EOF'`]*

**Assistant:** Now the chat log header and export.

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && cat > header.md <<'EOF'`]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && sed -n 122,126p 2026-10-26_fable_pad_buffer_alternatives.md …`]*

*[Edit: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/export.py]*

*[Edit: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/export.py]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && sed -i 's/^- Export made 2026-10-26 02:51/- Export made 2026…`]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && sed -n 124,125p 2026-10-26_fable_pad_buffer_alternatives.md …`]*

*[Edit: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild/export.py]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && python3 -I export.py /root/.claude/projects/-home-claude/4ef…`]*

*[Bash: `S=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild; O=/mnt/user-data/outputs/pba2; mkdir -p $O && cp $S/2026-10-26_…`]*

*[mcp__remote-devices__device_commit_files: [{"stagedPath": "/mnt/user-data/outputs/pba2/2026-10-26_fable_pad_buffer_alternatives.md", "devicePath": "/home/cmaier/EDA/sg13cmos5l_cm_ip__single2di…]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher && sha256sum chatlog/2026-10-26_fable_pad_buffer_alternatives.md design_co…`]*

*[TaskUpdate: 3]*

**Assistant:** Done. Everything is on your computer under `…_sudelbuecher/sudelbuecher/design_considerations/pad_buffer_alternatives/` (checksums match on both sides), with the chat log in `chatlog/` and its README entry.

**What the search found — the short version**

- **The resistors aren't the area.** From `d2s_mpdda.spice`: tails 240, sinks 432, cascodes 360, loads 192, Miller MOS caps 512, pairs 160, rhigh 100 µm² of 2014. Dropping rhigh is a spread/gain-σ decision, not an area one.
- **Three relations govern the three targets.** (1) Any class-A unit, MOS- or R-linearized, has Gm × linear range ≈ I_tail — `unit_r2` is already on that line (15.6 µS × 0.75 V ≈ 10 µA), so "faster" at the same range is more current or class AB. (2) In the matched-pair DDA the absolute Gm spread cancels; only mismatch and the unit's common-mode dependence matter — your §II rule, which is what makes triode-MOS and inverter transconductors admissible here despite their ±30 % spread. (3) The pad pole caps the d2s loop at ≈ 3 MHz into 100 pF, 10–15 MHz into 20 pF, whatever the front end.
- **Resistor-free units to bench** (with your existing fA/fB sweep and DDA-error criterion): Krummenacher–Joehl triode degeneration with the gates on the *inputs* (closest drop-in — `unit_t` failed because its gate sat at vss), a Nauta hv-inverter pair (smallest, ±0.95 V at 3.3 V, but CM pinned near vdd/2 and Gm ∝ vdd), the large-V_ov pair with a cascoded tail, the cross-coupled square-law quad; class-AB pairs if you need past the Gm × range line. Bulk-driven stays rejected.
- **Where the 1000–2000 µm² actually are:** bias root per slot; sinks/tails at V_ov 0.5–0.6 V (halves W·L for the same σ — from the PDK's own `sg13g2_moshv_mismatch.lib`, which the sg13cmos5l tree on your machine also uses); s2d as two unity-gain DDAs on explicit vcm (4 units, no CMFB) if an unregulated output CM is tolerable; the Miller caps only go with a capacitive-only load spec.
- **Range:** gain 2 around 1.2 V caps the s2d signal at ~±1 V on headroom alone; wider is a CM-window question, and complementary N+P units are the only MOS-only answer, at a measured ~3× gain-error penalty when the ports sit at different CMs.
- **No open precedent** in sg13cmos5l thick-oxide; Edwards' `sky130_ef_ip__opamp` (1 941 µm², 2.4 MHz, 3.3 V) is the nearest with a layout number and a CACE datasheet worth copying.

**Logging method** — I followed `verbatim_chatlog_recovery/verbatim-chatlog-export.md` and the consolidation precedent: the running log is written by hand (your decisions verbatim, results, checksums); the chat log is built by `export.py` from the raw transcript — user messages and visible replies verbatim, tool calls as one-line summaries, agent reports pointed to rather than inlined, and a check that none of the excluded material appears (3 turns, 10 replies, 0 overlap). The one practical rule beyond the cheatsheet: save design results first, log second, and phrase log requests as "the displayed conversation" rather than "everything". No stop occurred this session.

One open question for you before any simulation: is the pad load capacitive-only (20 pF class) or must 1 kΩ / 50 Ω stay in the spec? That decides whether the Miller caps go and what bandwidth is even reachable.

## Turn 4 — 2026-10-26 02:50

**User:** pad load must tolerate resistive (and transmission line, if the buffer is not WAY too slow for these, anyhow) loading. Explore how much a minimal output resistance >50 Ω will buy us.

## Turn 5 — 2026-10-26 02:51

**User:** I can't cleanly tell apart series and load resistance, apparently.

**Assistant:** Clear enough — the two are separable: the **series** resistance R_s is ours (inside the pad cell, between the clamp-frame drains and the pad: back termination, isolation, current limit), the **load** R_L is the bench's (1 kΩ, 50 Ω, a line). The question "what does R_s ≥ 50 Ω buy" is then about where the feedback is taken (before or after R_s) and what it does to stability versus C_L, to gain accuracy versus R_L, and to the line case. I'll work it out analytically first and then check it with the existing `d2s_mpdda` decks, since the loop numbers are all there. Let me look at the cloud-toolchain recipe and the run scripts.

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher; cat cloud_environment.md; echo =====; ls design_considerations/class_ab_p…`]*

**Assistant:** I'll start the pinned toolchain build in the background (≈10 min) and read the loop deck meanwhile.

*[Bash: `which ngspice xschem; ls /root/.ccr 2>/dev/null | head -3; nproc; df -h / | tail -1; cargo --version 2>/dev/null; llvm-config-18 --version 2>/dev/null…`]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/build_tools.sh]*

*[Bash: `chmod +x /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/build_tools.sh && /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba…`]*

*[mcp__remote-devices__device_bash: `cd $HOME/mnt/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/improvements/sim; cat tb/tb_mpdd…`]*

*[mcp__remote-devices__device_stage_files: {"paths": ["/home/cmaier/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/improvements/sim…]*

*[Bash: `tail -3 /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/tasks/brjkloue0.output; ls /root/src 2>/dev/null; tail -2 /root/src/ng_make.lo…`]*

*[error: Exit code 1]*

*[Bash: `tail -5 /root/src/apt.log; echo ---; tail -15 /root/src/ng_configure.log`]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad && sed -i 's/^echo "== apt"; apt-get install -y -qq/echo "== apt"; apt-g…`]*

*[Bash: `W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/rs; mkdir -p $W/tb && cp /mnt/user-data/uploads/sg13cmos5l_cm_ip__single2…`]*

*[Bash: `W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/rs; cat > $W/tb/tb_rs_loop.tpl <<'EOF'`]*

*[Bash: `tail -4 /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/tasks/bh21om3lm.output; tail -2 /root/src/ng_make.log 2>/dev/null | cut -c1-12…`]*

*[Bash: `until grep -q "ngspice ok\|exited with code" /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/tasks/bh21om3lm.output; do sleep 10; done…`]*

*[error: The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to]*

*[the user interrupted a tool call]*

## Turn 6 — 2026-10-26 02:55

**User:** In parallel, how completely off the beaten path can you think to come up with pad driver / pad input to internal differential signal buffers?

**Assistant:** Here's the brainstorm, deliberately unvetted, roughly ordered from "unusual but sound" to "probably a bad idea, but it reframes the problem". All MOS-only unless stated.

**Reframe the pads as current ports, not voltage ports**

1. **Current-output pad driver (open loop, like your PUDDING DAC output).** The four DDA units are already transconductors; mirror their differential current up by K into the pad through the clamp frames as mirror outputs, no global feedback. The external load makes the voltage: 50 Ω → ±0.5 V at ±10 mA, 1 kΩ → bigger swing. "Tolerates resistive loads and lines" by construction (a current source doesn't care; a line terminated at the far end only is the textbook case), no compensation capacitor, bandwidth = the single output pole, area ≈ the mirror. Accuracy becomes mirror matching plus the external resistor, which the bench knows to 0.1 %. Pure capacitive loads become the bad case (slew = I/C), which is the inverse of today.

2. **Current-input pad (virtual-ground / transimpedance input).** Hold the pad node at vref with a regulated-cascode input; the bench supplies current through its own series resistor — or through the 586.9 Ω `padres` that IHP already put there and that you have already paid for. The pad never moves, so the input-range problem evaporates: range is set by the external resistor and the input stage's current compliance, not by any gate window. S2D is then a 1:1 push-pull mirror, tens of MHz, a few hundred µm². The internal differential signal is current, which a gm-C filter accepts natively (current into the integrating cap), or you convert back with diode loads matched to the next stage — Minch's ELIN again, compress at the pad, expand inside.

**Use what the pad cell already is**

3. **Clamp frames as a complementary flipped voltage follower.** P frame as the FVF input device, N frame as the shunt device (and the mirror image for the other half). Output impedance 1/(g_m1 g_m2 r_o) — sub-ohm — without a global loop, bandwidth ≈ g_m/C_pad ≈ 10 MHz at 100 pF with no compensation, ±10 mA class AB from the FVF node. The 1 V V_GS shift is cancelled by a replica unit in the DDA feedback, which you already know how to match. The literature's objection (FVF range at 3.3 V) is moot for a ±0.5 V swing around 1.2 V.

4. **The ESD resistor as the feedback resistor.** If a resistive FDA ever comes back, Rg = `padres` (rppd, ±10 %, TC 170 ppm, already in the cell) and Rf = a second rppd in the same cell; it violates the preference only on paper, since the resistor exists either way.

**Split accuracy from speed**

5. **Two-path (composite) driver.** A tiny open-loop current-steering fast path through the frames handles everything above ~100 kHz; the existing slow, accurate DDA loop handles DC and LF and corrects the fast path's error. Speed from the uncompensated path, gain accuracy from the loop, no Miller caps because the loop no longer has to cross at MHz. The crossover between paths is set by a MOS cap + the loop bandwidth, not a resistor.

6. **Trim instead of match.** The harness gives each slot a 5-bit IDAC and SPI registers; use them to trim tail currents or a mirror ratio of a deliberately small, fast, badly matched buffer, calibrated through the loopback mode you already have (s2d → d2s round trip). Pelgrom says 0.3 % σ costs 11× the area of 1 %; a 5-bit trim costs a few gates.

**Switch instead of amplify**

7. **Chopper S2D with no amplifier.** Four transmission gates alternate vp/vn between (vin, vref) and (vref, vin) at f_ch; the internal differential signal is ±(vin − vref), demodulated inside by the same clock. Gain exactly 1 by switching, no offset, no 1/f, MOS switches only, essentially no area, range = switch range (rail to rail with complementary gates). Costs: a clock, the internal CM rides at (vin + vref)/2, and gain 2 doesn't come for free.

8. **Make the test pins digital.** Measure the internal signal with a 1-bit ΣΔ modulator driving the 30 mA digital pad; feed the chip with a 1-bit stream from the bench FPGA into an internal gm-C reconstruction. No analog pad at all, rail-to-rail trivially, line-tolerant because it's a logic signal; the "buffer" is a comparator and a 1-bit DAC. (chipalooza_projects_2b already carries an IIC-JKU ΣΔ output driver.)

**Devices**

9. **Core (1.2 V) devices for the units, thick-oxide cascodes for protection.** The internal signal is ±0.5 V around 1.2 V — inside the LV window. LV PMOS: A_VT 2.2 vs 4.5 mV·µm, V_t ≈ 0.4 V, 2–3× the gm/I, 2–4× less area for the same σ. Only the gates that touch the pad need HV devices. Reliability is the question (1.7 V on an LV gate at the top of the swing).

10. **Capacitive attenuator at the input, MOS caps only.** A 2:1 MOS-cap divider halves what the input units see (doubling the range, scope-probe style), with the DC restored through a subthreshold-MOS pseudo-resistor rather than poly. Works above the ms time constant; DC gain then depends on the pseudo-resistor ratio, which is bad — unless the DC path is the slow loop of idea 5.

**Move the problem**

11. **Differential I/O on two pins and no S2D.** The slot has three analog pins; a differential probe or a bench balun does the single-to-differential conversion better than anything in 6500 µm². The on-chip "buffer" shrinks to protection and a pair of gates.

12. **Current-steering (CML-style) driver into an external termination.** The RF cousin of idea 1: a differential pair with the frame as the tail, outputs into 50 Ω at the far end, hundreds of MHz possible with hv devices, gain set by I_tail × R_L. Common-mode at the pad is set by the termination voltage, not by the chip.

If I had to bet on one that actually changes the picture: idea 2 for the input (the range problem disappears instead of being fought) and idea 1 or 3 for the output (no loop around C_L, so no Miller caps and no load-dependent stability). Both are the PUDDING instinct — currents, not voltages, cross the pad.

Meanwhile the ngspice build is still running; once it's up I'll run the R_s sweep (feedback before/after, 0/50/200/500 Ω, the five loads) against the `d2s_mpdda` reference numbers.

*[background task notification: Background command "Fix the build script (apt update, no X) and rerun the build in the background" completed (exit code 0); its report is saved verbatim under `research/`]*

**Assistant:** The toolchain is built. Running the reference deck first to confirm the numbers, then the R_s sweep.

*[Bash: `tail -4 /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/tasks/bh21om3lm.output; ls /root/pdk/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/ngs…`]*

*[Bash: `export PDK_ROOT=/root/pdk/IHP-Open-PDK PDK=ihp-sg13cmos5l PATH=/root/tools/ngspice/bin:$PATH; W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3f…`]*

**Assistant:** Reference reproduced exactly (78.9 dB / 1.37 MHz / 72.4°). Running the loop-gain sweep.

*[Bash: `export PDK_ROOT=/root/pdk/IHP-Open-PDK PDK=ihp-sg13cmos5l PATH=/root/tools/ngspice/bin:$PATH; W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3f…`]*

**Assistant:** Feedback before R_s helps everywhere; feedback at the pad hurts everywhere. Now the step response at the pad for the before-R_s case.

*[Bash: `export PDK_ROOT=/root/pdk/IHP-Open-PDK PDK=ihp-sg13cmos5l PATH=/root/tools/ngspice/bin:$PATH; W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3f…`]*

*[Bash: `export PDK_ROOT=/root/pdk/IHP-Open-PDK PDK=ihp-sg13cmos5l PATH=/root/tools/ngspice/bin:$PATH; W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3f…`]*

*[Bash: `export PDK_ROOT=/root/pdk/IHP-Open-PDK PDK=ihp-sg13cmos5l PATH=/root/tools/ngspice/bin:$PATH; W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3f…`]*

*[Bash: `export PDK_ROOT=/root/pdk/IHP-Open-PDK PDK=ihp-sg13cmos5l PATH=/root/tools/ngspice/bin:$PATH; W=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3f…`]*

*[Write: /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/rs/series_resistor.md]*

*[Bash: `S=/tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad; cat >> $S/logbuild/log.md <<'EOF'`]*

*[mcp__remote-devices__device_commit_files: [{"stagedPath": "/mnt/user-data/outputs/pba3/series_resistor.md", "devicePath": "/home/cmaier/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/su…]*

**Assistant:** Now the chat-log re-export (delta since 02:53) and the README scope update.

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && sed -i 's/^- Export made 2026-10-26 02:53 by the session its…`]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && sed -n 243,250p 2026-10-26_fable_pad_buffer_alternatives.md …`]*

*[Bash: `cd /tmp/claude-0/-home-claude/4efc77f5-dbfc-5127-ba7b-d3fee4e24367/scratchpad/logbuild && python3 - <<'EOF'`]*

