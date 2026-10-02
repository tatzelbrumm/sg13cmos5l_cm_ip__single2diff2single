# References — 2026-10-02 — Edwards & Cauwenberghs log-domain search session

Sources consulted for
[`../2026-10-02_sonnet_edwards_cauwenberghs_log_domain_references_in_donotlitter.md`](../2026-10-02_sonnet_edwards_cauwenberghs_log_domain_references_in_donotlitter.md),
indexed per this directory's rule (index, do not copy). The PDFs below are the
user's own files on his computer under `~/DoNotLitter/`, read in place and never
copied into this repository.

## Earlier claude.ai chats (found with conversation search)

- [Hardware Engineer in der Halbleiterindustrie Stuttgart](https://claude.ai/chat/38cfba28-1036-41ea-a703-f016edf3603e)
  (2026-04-12) — the user asked there for a Sphinx doc of linear integrators with
  hints to the Edwards/Cauwenberghs ISCAS Monterey work; the three-paper list used
  at the start of this session (ISCAS 1997, ISCAS 1998, 2000) comes from that chat.
- [SMA connectors for differential signals](https://claude.ai/chat/3dcdeb4e-a216-4a2e-bfb4-36f51940cdb7)
  (2026-05-29) — surfaced by the same search; contains the user's own reference to
  Tim Edwards's Pot Box page. Not otherwise used.

## The three requested papers, as found in `~/DoNotLitter/`

- **ISCAS 1997**, "A Mixed-Signal Correlator for Acoustic Transient Classification"
  (Edwards, Cauwenberghs, Pineda) — **no copy in the folder** (title scan of all 4,100
  PDFs, first three pages each). Only cited, in `LangcheZeng_Cauwenberghs/vitae.pdf`,
  `TimEdwards/thesis.pdf` and `TimEdwards/defense.pdf`.
- **ISCAS 1998**, "A Second-Order Log-Domain Bandpass Filter for Audio Frequency
  Applications" (Edwards, Cauwenberghs) — `TimEdwards/iscas98_log.pdf`, 4 pages.
  Added by the user after the searches in the log, so the log's Turns 3–7 predate it.
- **2000**, "Synthesis of Log-Domain Filters from First-Order Building Blocks", Analog
  Integrated Circuits and Signal Processing 22, pp. 177–186 —
  `LogDomain/EdwardsCauwenberghs.AnalogIC_SigProc.2000.pdf` and
  `LogDomain/aicsp00_log.pdf` (two copies); matching entry in `LogDomain/LogDomain.bib`.

## Also added by the user after the searches

- `TimEdwards/jssc99_atp.pdf` — "Mixed-Mode Correlator for Micropower Acoustic Transient
  Classification", Edwards and Cauwenberghs, IEEE J. Solid-State Circuits, vol. 34,
  no. 10, Oct. 1999, 6 pages. The journal paper on the same correlator line of work as
  the missing ISCAS 1997 paper; whether it covers that paper's content was not checked.

## Other files in `~/DoNotLitter/` read this session

- `TimEdwards/thesis.pdf`, `thesis2side.pdf` — R. T. Edwards, JHU dissertation,
  "Time-Frequency Acoustic Processing and Recognition: Analysis and Analog VLSI
  Implementations" (contents list: log-domain filtering, acoustic transient processing).
- `TimEdwards/defense.pdf` — defense slides; cites the 1998 log-domain bandpass work.
- `TimEdwards/potbox.pdf` — "Pot Box mark II", Stanford, 4 June 1992.
- `LangcheZeng_Cauwenberghs/vitae.pdf` — Cauwenberghs's CV; lists the ISCAS 1997 and
  ISCAS 1998 papers.
- `LogDomain/Minch.TCAS2.2001JAN.pdf` — B. A. Minch, "Multiple-Input Translinear Element
  Log-Domain Filters", IEEE TCAS-II 48(1), Jan. 2001.
- `FloatingGate/Minch97.pdf` — B. A. Minch, Caltech PhD thesis, "Analysis, Synthesis, and
  Implementation of Networks of Multiple-Input Translinear Elements", 1997, 218 pages.
- `TimEdwardsMultiplier/` — `TimEdwardsMultiplier.bib` and Edwards papers
  (`00541978.pdf` ISCAS 1996 wavelet transform, `00856061.pdf` ISCAS 2000 field-programmable
  mixed-signal array, `B3_Edwards_P.pdf` 1999 FPAA module architecture).
- `Potentiostat/04012345.pdf` — Genov et al., IEEE TCAS-I, Nov. 2006; the only hit of the
  title scan, a false positive (mentions "a second-order log-domain anti-aliasing filter").

## Not usable / dead ends (noted so a future session doesn't retry)

- Background jobs started from one `device_bash` call (even with `setsid nohup`) were gone
  by the next call; the whole-collection PDF scan only finished when run in the foreground
  in chunks of about 1,700 files (`pdftotext -l 3`, 8 in parallel, under the 180 s limit).
- `$HOME` in `device_bash` is the sandbox's own home (`/sessions/<id>/`), not the user's
  home directory; scratch files written there never reach his disk.
