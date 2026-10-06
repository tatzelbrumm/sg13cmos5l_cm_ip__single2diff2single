<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Cloud simulation environment for agent sessions

2026-10-06. Agent sessions run in a fresh cloud container that has none of the EDA tools. This
note pins what they build there, so that their netlists and numbers come from the same versions as
Christoph's IIC-OSIC-TOOLS image. It replaces the "Cloud setup" lines of the kickoff files.

## Reference: IIC-OSIC-TOOLS 2026.09

The image's pins are in `_build/tool_metadata.yml` at tag 2026.09 of
github.com/iic-jku/IIC-OSIC-TOOLS (tagged 2026-09-22).

How we know this is the image in use:
- The ngspice raw files written on 2026-09-27 in the main repo say "ngspice-47, Build Tue Sep 22",
  the tag's date.
- Hand-saved sheets carry `xschem version=3.4.8RC`.
- `cheatsheets/iic-osic-tools_cheatsheet.md` still names 2026.08.

| tool | source | pin |
|---|---|---|
| xschem | github.com/StefanSchippers/xschem | `ddc734480d5326fb787993dad24f4062e5d28434` (3.4.8RC) |
| ngspice | github.com/danchitnis/ngspice-sf-mirror | tag `ngspice-47` |
| OpenVAF | github.com/arpadbuermen/OpenVAF | `5ed9e63afe70ac95129a78af7b3732e7d431b1e5` |
| IHP PDKs | github.com/iic-jku/IHP-Open-PDK, branch dev (not IHP-GmbH) | `c271a7e97a7bab201c1d0a399215969d2ee19573` (2026-09-21) |
| gf180mcuD | open_pdks via ciel | `1689ac3f2dc763876eaf967227c7dfe831b031ae` |

The IHP commit is the one in the image's `$PDK_ROOT/ihp-sg13cmos5l/COMMIT`, read by Christoph on
2026-10-06. When the image changes, read it again.

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
git checkout ddc734480d5326fb787993dad24f4062e5d28434
./configure --prefix=$TOOLS/xschem && make -j8 && make install

# ngspice-47, about 5 min, with the image's configure options
git clone --filter=blob:none https://github.com/danchitnis/ngspice-sf-mirror ngspice && cd ngspice
git checkout ngspice-47 && ./autogen.sh
./configure --disable-debug --enable-openmp --with-x --with-readline=yes --enable-pss --enable-xspice \
  --with-fftw3=yes --enable-osdi --enable-klu --prefix=$TOOLS/ngspice
make -j8 && make install

# OpenVAF, about 2 min; the PDK script calls it as openvaf-r
git clone --filter=blob:none https://github.com/arpadbuermen/OpenVAF && cd OpenVAF
git checkout 5ed9e63afe70ac95129a78af7b3732e7d431b1e5
cargo build --release --features llvm18 --bin openvaf-r      # -> target/release/openvaf-r

# IHP PDK: sparse checkout of the fork. The cmos5l models and Verilog-A sources are symlinks into
# ihp-sg13g2, so its ngspice and verilog-a dirs must be checked out too. 15 MB.
git clone --filter=blob:none --no-checkout https://github.com/iic-jku/IHP-Open-PDK && cd IHP-Open-PDK
git sparse-checkout set --no-cone /ihp-sg13cmos5l/libs.tech/xschem/ /ihp-sg13cmos5l/libs.tech/ngspice/ \
  /ihp-sg13cmos5l/libs.tech/verilog-a/ /ihp-sg13g2/libs.tech/xschem/ /ihp-sg13g2/libs.tech/ngspice/ \
  /ihp-sg13g2/libs.tech/verilog-a/              # add klayout, libs.ref/... only if the task needs them
git checkout c271a7e97a7bab201c1d0a399215969d2ee19573     # the image's COMMIT
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
