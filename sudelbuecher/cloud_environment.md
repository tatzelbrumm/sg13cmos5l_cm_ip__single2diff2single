<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Cloud simulation environment for agent sessions

2026-10-06. Agent sessions run in a fresh cloud container that has none of the EDA tools. This
note pins what they build there, so that their netlists and numbers come from the same versions as
Christoph's IIC-OSIC-TOOLS image. It replaces the "Cloud setup" lines of the kickoff files.

## Reference: IIC-OSIC-TOOLS 2026.10 (from 2026-10-29; 2026.09 before)

The image's pins are in `_build/tool_metadata.yml` (tools) and `_build/images/iic-osic-tools/skel/headless/scripts/install_eda.sh`
(Python packages) at tag 2026.10 of github.com/iic-jku/IIC-OSIC-TOOLS (tagged 2026-10-14).

| tool | source | 2026.10 pin | 2026.09 pin |
|---|---|---|---|
| xschem | github.com/StefanSchippers/xschem | `d76e6cc74fdfa5de573a8ba14124ef00c611a9b6` (3.4.8RC) | `ddc734480d53…` (3.4.8RC) |
| ngspice | github.com/danchitnis/ngspice-sf-mirror | tag `ngspice-47` | same |
| OpenVAF | github.com/arpadbuermen/OpenVAF | `dd05b5e2f97fcc8256a1dbf7144755a1ad3bf90a`, branch `mb-experimental`; the image runs `cargo update` before building | `5ed9e63afe70…` |
| KLayout | www.klayout.org, Ubuntu-24 package (DRC / LVS); `klayout` on PyPI for the runners' `import klayout.db` | `0.30.12` | same |
| magic | github.com/RTimothyEdwards/magic | tag `8.3.685` | `8.3.684` |
| netgen | github.com/RTimothyEdwards/netgen | tag `1.5.324` | `1.5.323` |
| klayout-pex | PyPI | `0.6.8` (`kpex extract …`; the template's plain `kpex --pdk …` still runs, with a deprecation warning) | `0.4.4` |
| `sak-*` scripts | IIC-OSIC-TOOLS `_build/images/iic-osic-tools/skel/foss/tools/sak/` | tag `2026.10` | tag `2026.09` |
| IHP PDKs | github.com/iic-jku/IHP-Open-PDK, branch dev (not IHP-GmbH) | provisional `df4c5054ee8ca481c3eb873687274f28cdb50b1e`, see below | `c271a7e97a7bab201c1d0a399215969d2ee19573` |
| gf180mcuD | open_pdks via ciel | `1689ac3f2dc763876eaf967227c7dfe831b031ae` (not rechecked for 2026.10) | same |

The IHP PDK isn't pinned in the IIC-OSIC-TOOLS repo: the image clones the fork's dev head when it is
built and writes it to `$PDK_ROOT/ihp-sg13cmos5l/COMMIT`. `df4c5054` is the dev head on the tag day
(2026-10-14 14:25); dev moved on from 2026-10-15. Read `COMMIT` in the 2026.10 image and replace it
here and in the scripts below. 2026.09's commit, `c271a7e9`, was read by Christoph on 2026-10-06.

For sg13cmos5l, `c271a7e9..df4c5054` brings: guard-ring PCells `ptap1_ring` / `ntap1_ring` with
xschem symbols; DRC `--precheck_drc` renamed `--minimum_drc` (that mode now skips off-grid and angle
checks; the main deck's rules are unchanged); LVS without the RF-MOS model mapping; RF-MOS minimum W
0.39 µm; `cap_cmomi` / `cap_cmomf` OSDI no longer tracked (compiled like the others); xschem views of
the sg13cmos5l standard cells.

## Building it in the container

Ubuntu 24.04, about 10 minutes in all. All sources come from GitHub through the git proxy.
SourceForge (ngspice's own repository) and the GitHub API (which `ciel enable` uses) are blocked
(403).

```
# build dependencies
apt-get install -y build-essential autoconf automake libtool bison flex zstd \
  libx11-dev libxpm-dev libxrender-dev libxcb1-dev libx11-xcb-dev libcairo2-dev libjpeg-dev tcl-dev tk-dev \
  libreadline-dev libfftw3-dev libxaw7-dev libxmu-dev libxext-dev libxft-dev libfontconfig1-dev \
  llvm-18-dev clang-18 libclang-18-dev
# plus Rust (rustup, stable) for OpenVAF

# xschem, 15 s
git clone https://github.com/StefanSchippers/xschem && cd xschem
git checkout d76e6cc74fdfa5de573a8ba14124ef00c611a9b6
./configure --prefix=$TOOLS/xschem && make -j8 && make install

# ngspice-47, about 5 min, with the image's configure options
git clone --filter=blob:none https://github.com/danchitnis/ngspice-sf-mirror ngspice && cd ngspice
git checkout ngspice-47 && ./autogen.sh
./configure --disable-debug --enable-openmp --with-x --with-readline=yes --enable-pss --enable-xspice \
  --with-fftw3=yes --enable-osdi --enable-klu --prefix=$TOOLS/ngspice
make -j8 && make install

# OpenVAF, about 2 min; the PDK script calls it as openvaf-r
git clone --filter=blob:none https://github.com/arpadbuermen/OpenVAF && cd OpenVAF
git checkout dd05b5e2f97fcc8256a1dbf7144755a1ad3bf90a && cargo update
cargo build --release --features llvm18 --bin openvaf-r      # -> target/release/openvaf-r

# IHP PDK: sparse checkout of the fork. The cmos5l models and Verilog-A sources are symlinks into
# ihp-sg13g2, so its ngspice and verilog-a dirs must be checked out too. 15 MB.
git clone --filter=blob:none --no-checkout https://github.com/iic-jku/IHP-Open-PDK && cd IHP-Open-PDK
git sparse-checkout set --no-cone /ihp-sg13cmos5l/libs.tech/xschem/ /ihp-sg13cmos5l/libs.tech/ngspice/ \
  /ihp-sg13cmos5l/libs.tech/verilog-a/ /ihp-sg13g2/libs.tech/xschem/ /ihp-sg13g2/libs.tech/ngspice/ \
  /ihp-sg13g2/libs.tech/verilog-a/              # add klayout, libs.ref/... only if the task needs them
git checkout df4c5054ee8ca481c3eb873687274f28cdb50b1e     # provisional, see the table
# OSDI the way the image builds it: into libs.tech/ngspice/osdi, so the PDK's .spiceinit works as is. 22 s.
cd ihp-sg13cmos5l/libs.tech/verilog-a && PATH=<dir of openvaf-r>:$PATH ./openvaf-compile-va.sh --compile-model-generic

# gf180mcuD, the image's open_pdks build. ciel's CLI fails on the GitHub API, but the release asset downloads.
curl -L -o common.tar.zst https://github.com/fossi-foundation/ciel-releases/releases/download/gf180mcu-1689ac3f2dc763876eaf967227c7dfe831b031ae/common.tar.zst
tar --zstd -xf common.tar.zst -C $PDK_ROOT 'gf180mcuD/libs.tech/xschem/*' 'gf180mcuD/libs.tech/ngspice/*' 'gf180mcuD/.config/*'
```

To run:
- Export `PDK_ROOT` and `PDK`.
- Copy the PDK's `libs.tech/ngspice/.spiceinit` into the run directory. Keep no `~/.spiceinit`,
  because an old one loads stale OSDI files.
- The project `xschemrc` files are used as shipped.

gf180mcuD's `.config/nodeinfo.json` lists the options MIM_2P0 (2 fF/µm² MIM) and METAL5. Its
xschemrc sets `$::180MCU_MODELS` to `$PDK_ROOT/gf180mcuD/libs.tech/ngspice`.

## Checked on 2026-10-06 with this recipe (IHP at `c271a7e9`)

- `class_ab_pad_driver/improvements/xschem/check_xschem.py`: MISMATCHES: 0 on every sheet,
  including the bandgap with pnpMPA.
- `tb_mpdda_loop`: 78.9 dB, 1.37 MHz, 72.4°.
- `tb_mpdda_thd`: 0.119 %.
- Both are the reference values in `results_improvements.txt`.
- gf180mcuD: an `nfet_03v3` operating point runs with `design.ngspice` + `sm141064.ngspice typical`.

## No longer needed

These were cloud-only workarounds for apt's xschem 3.4.4 and ngspice 42:

- **The `ev7` stand-in in a scratch xschemrc.** xschem has `ev7` since 3.4.6, and pnpMPA.sym
  needs it.
- **Patching OSDI files from version 0.4 to 0.3.** OpenVAF 5ed9e63 writes OSDI 0.4. ngspice 42
  accepted only 0.3; ngspice-47 reads 0.4.

## What stays in the container

Build trees, the PDK checkout, scratch netlists and raw ngspice output are never shipped:

- The numbers that matter go into the `results_*.txt` files and the logs.
- For waveforms, run the deck in the image; the decks plot interactively there.

## Claude Code cloud sessions (the cloud credit), from 2026-10-29

Only Claude Code cloud sessions draw on the cloud-session credit ($250 on Max, until November 4,
11:59 PM PT = November 5, 08:59 CET). Chat and Cowork sessions, Projects, Routines (scheduled
tasks) and Remote Control are not covered
(support.claude.com/en/articles/17152539-cloud-sessions-bonus-credit-promotion). While the credit
lasts, these sessions don't count toward the plan limits.

A cloud session is a fresh Ubuntu 24.04 VM (4 vCPU, 16 GB, 30 GB disk) with a clone of one GitHub
repository at one branch. It can't reach the computer; results come back only as pushed branches.
Its tools come from the environment's setup script, which runs as root before Claude starts and
costs no tokens. When the script finishes in about 5 minutes, the VM is snapshotted and later
sessions start with the tools on disk (rebuilt after about 7 days or when the script changes)
(code.claude.com/docs/en/cloud-environments).

### The environment `sg13cmos5l` (claude.ai/code, environment dialog)

- **Network access:** "Limited" ("Sessions reach only what you allow below"); **Allowed domains**,
  one per line: `www.klayout.org`, `github.com`; **Allow package managers** checked (apt, pip,
  cargo). Set up so on 2026-10-30; the dialog's options were None / Limited / Full, not the docs'
  Trusted / Custom (screenshots `chatlog/pix/2026-10-30_opus_cloud_setup_08…13`). Network secrets: none.
- **Environment variables:**
  ```
  PDK_ROOT=/foss/pdks
  PDK=ihp-sg13cmos5l
  BASH_DEFAULT_TIMEOUT_MS=600000
  ```
  `source .designinit` then sets PDKPATH, KLAYOUT_PATH etc. as in the image.
- **Setup script:** the recipe above with the 2026.10 pins, plus KLayout, magic, netgen, klayout-pex and
  the `sak-*` scripts, in parallel.
  Log with times: `/foss/setup.log`.

```bash
#!/bin/bash
# Chipalooza sg13cmos5l toolchain for Claude Code cloud sessions (pins: IIC-OSIC-TOOLS 2026.10,
# sudelbuecher/cloud_environment.md on branch sudel_buecher). Must exit 0. Log: /foss/setup.log
export DEBIAN_FRONTEND=noninteractive
F=/foss; mkdir -p $F/pdks $F/tools $F/src; L=$F/setup.log; cd $F/src
t0=$(date +%s); ok() { echo "$1_OK $(( $(date +%s) - t0 ))s" >> $L; }
g() { git clone -q --filter=blob:none "$1" "$2" && git -C "$2" checkout -q "$3"; }    # url dir pin
curl -fsSLo klayout.deb https://www.klayout.org/downloads/Ubuntu-24/klayout_0.30.12-1_amd64.deb >> $L 2>&1 \
  || echo "KLAYOUT_DEB_FAILED" >> $L
apt-get update -qq >> $L 2>&1
apt-get install -y -qq --no-install-recommends $( [ -s klayout.deb ] && echo ./klayout.deb ) \
  build-essential autoconf automake libtool bison flex gawk m4 tcsh libncurses-dev libglu1-mesa-dev \
  libx11-dev libxpm-dev libxrender-dev libxcb1-dev libx11-xcb-dev libcairo2-dev libjpeg-dev tcl-dev tk-dev \
  libreadline-dev libfftw3-dev libxaw7-dev libxmu-dev libxext-dev libxft-dev libfontconfig1-dev \
  llvm-18-dev clang-18 libclang-18-dev >> $L 2>&1 && ok APT
pip install -q --break-system-packages klayout==0.30.12 klayout-pex==0.6.8 >> $L 2>&1 && ok PIP
( g https://github.com/StefanSchippers/xschem xschem d76e6cc74fdfa5de573a8ba14124ef00c611a9b6 && cd xschem \
  && ./configure --prefix=$F/tools/xschem && make -j4 && make install && ok XSCHEM ) >> $L 2>&1 &
( g https://github.com/RTimothyEdwards/magic magic 8.3.685 && cd magic \
  && ./configure --prefix=$F/tools/magic && make -j4 && make install && ok MAGIC ) >> $L 2>&1 &
( g https://github.com/RTimothyEdwards/netgen netgen 1.5.324 && cd netgen \
  && ./configure --prefix=$F/tools/netgen && make -j4 && make install && ok NETGEN ) >> $L 2>&1 &
( g https://github.com/danchitnis/ngspice-sf-mirror ngspice ngspice-47 && cd ngspice && ./autogen.sh \
  && ./configure --disable-debug --enable-openmp --with-x --with-readline=yes --enable-pss --enable-xspice \
       --with-fftw3=yes --enable-osdi --enable-klu --prefix=$F/tools/ngspice \
  && make -j4 && make install && ok NGSPICE ) >> $L 2>&1 &
( g https://github.com/arpadbuermen/OpenVAF OpenVAF dd05b5e2f97fcc8256a1dbf7144755a1ad3bf90a && cd OpenVAF \
  && cargo update -q && cargo build -q --release --features llvm18 --bin openvaf-r \
  && install -m 755 target/release/openvaf-r /usr/local/bin/ && ok OPENVAF ) >> $L 2>&1 &
( git clone -q --depth 1 --branch 2026.10 --filter=blob:none --no-checkout https://github.com/iic-jku/IIC-OSIC-TOOLS iic \
  && cd iic && git sparse-checkout set --no-cone /_build/images/iic-osic-tools/skel/foss/tools/sak/ \
  && git checkout -q 2026.10 && cp -r _build/images/iic-osic-tools/skel/foss/tools/sak $F/tools/ && ok SAK ) >> $L 2>&1 &
( git clone -q --filter=blob:none --no-checkout https://github.com/iic-jku/IHP-Open-PDK $F/pdks/IHP-Open-PDK \
  && cd $F/pdks/IHP-Open-PDK \
  && git sparse-checkout set --no-cone /ihp-sg13cmos5l/ /ihp-sg13g2/libs.tech/klayout/python/ \
       /ihp-sg13g2/libs.tech/xschem/ /ihp-sg13g2/libs.tech/ngspice/ /ihp-sg13g2/libs.tech/verilog-a/ \
  && git checkout -q df4c5054ee8ca481c3eb873687274f28cdb50b1e \
  && git submodule update -q --init --depth 1 ihp-sg13g2/libs.tech/klayout/python/pycell4klayout-api \
       ihp-sg13g2/libs.tech/klayout/python/pypreprocessor \
  && ln -sfn $F/pdks/IHP-Open-PDK/ihp-sg13cmos5l $F/pdks/ihp-sg13cmos5l && ok PDK ) >> $L 2>&1 &
wait
( cd $F/pdks/ihp-sg13cmos5l/libs.tech/verilog-a && ./openvaf-compile-va.sh --compile-model-generic && ok OSDI ) >> $L 2>&1
chmod +x $F/tools/sak/*        # the sak scripts come without exec bits
K=$(command -v kpex) && mv $K $K.pip && printf '#!/bin/bash\n# kpex 0.6.8 takes ihp-sg13cmos5l; the template Makefile passes ihp_sg13cmos5l\nexec %s.pip "${@/ihp_sg13cmos5l/ihp-sg13cmos5l}"\n' $K > $K && chmod +x $K
for b in $F/tools/{xschem,magic,netgen,ngspice}/bin/* $F/tools/sak/sak-*; do ln -sf "$b" /usr/local/bin/; done
cd / && rm -rf $F/src
echo "SETUP_DONE $(( $(date +%s) - t0 ))s" >> $L
exit 0
```

Tested on 2026-10-29 in a 2-core Ubuntu 24.04 container, each part on its own, except the KLayout
download (klayout.org isn't reachable from there). With the 2026.09 pins: apt, xschem and the PDK
sparse checkout with both PCell submodules 39 s together; ngspice-47 214 s. With the 2026.10 pins:
xschem 36 s, magic 8.3.685 42 s, netgen 1.5.324 8 s, the `sak-*` scripts 1 s, klayout-pex 0.6.8 with
KLayout 0.30.12 from PyPI under 20 s; the OpenVAF commit resolves on `mb-experimental` (its build and
the OSDI compile as in the recipe above, not timed again).

The macro Makefiles (the template's targets: `magic-drc`, `magic-lvs-netlist`, `magic-lvs`,
`magic-pex EXT_MODE=1|2|3`, `klayout-pex`, `klayout-drc`, `klayout-lvs`) run as in the image after
`source .designinit`: the `sak-*` scripts need only `PDK_ROOT`, `PDK` and `PDKPATH`, and use
`$PDKPATH/libs.tech/magic/ihp-sg13cmos5l.magicrc` and `$PDK_ROOT/$PDK/libs.tech/netgen/ihp-sg13cmos5l_setup.tcl`,
the same files as the harness's `magic/run_extract_*.sh` and `validate/run_lvs_*.sh`. Not in it:
CACE (`sim-cace`), sak-render, gf180mcuD.

Two template findings from the bg_core_pd run in the Cowork session (2026-10-29, 2026.10 tools, PDK
df4c5054): the PEX targets call `$(SCRIPTS_DIR)/check_pex_ports.py` with `SCRIPTS_DIR := scripts`,
relative to the macro, but the script is in the repository root, so pass `SCRIPTS_DIR=../../scripts`
to make. kpex 0.6.8 rejects the template's `--pdk ihp_sg13cmos5l` (it takes `ihp-sg13cmos5l`); the
setup script wraps `kpex` to fix the spelling. With both, all targets pass for bg_core_pd: DRC clean,
LVS match, `magic-pex` 1/2/3 and `klayout-pex` 2 with all ports connected, each in about 1 s.

### Starting a session

Start a plain cloud session, not inside a Project or a Routine: claude.ai/code, the Desktop app
(environment under **Cloud**), or `claude --cloud` in a terminal. Repository
`tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`, branch `toplevel` (the macros aren't on `main` yet), environment `sg13cmos5l`.
The first message points at one brief in `sudelbuecher/cloud_sessions/` on `sudel_buecher`.

### Git in a cloud session

The clone is the session's own, on the VM, so the `index.lock` problem of the connected folders
doesn't arise there, and git is the only way results come back. CLAUDE.md's "no git commands
without asking first" still holds: each brief says exactly which commands and branches are
allowed. The pattern:
- `sudel_buecher` goes into a separate worktree (`git worktree add ../sudel ...`); never switch
  the main checkout to it.
- Results are committed only on `claude/<task>` (from the cloned branch) and `claude/<task>-sudel` (from
  `sudel_buecher`), and only those are pushed. Never `main` or `sudel_buecher`, no tags, no force
  pushes, no merges. Christoph merges.
