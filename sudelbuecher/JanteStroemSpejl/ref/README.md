<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# ref/: sources for [REPORT.md](../REPORT.md)

Rule as in `chatlog/ref/`: index, don't copy. The only copy here is Christoph's own lecture.

## In this folder

- [2019-03-11_Maier_UiO_test_lecture_analog_IC_design.pdf](2019-03-11_Maier_UiO_test_lecture_analog_IC_design.pdf):
  C. Maier, *What's All This Analog IC Design Stuff, Anyhow? How to Think Like an
  Analog IC Designer*, test lecture, UiO, 11 March 2019. 49 slides, from the
  [lecture downloads on Bitbucket](https://bitbucket.org/cmucsd/analogdesignlecture/downloads/).

## Elsewhere in this directory

- [../6ad0a469-05d8-83eb-889f-0b6d945ad274.pdf](../6ad0a469-05d8-83eb-889f-0b6d945ad274.pdf):
  print of the ChatGPT session "Russische Etymologie Nemez", 53 pages, 2026-10-15 17:11
  ([chatgpt.com/c/6ad0a469-05d8-83eb-889f-0b6d945ad274](https://chatgpt.com/c/6ad0a469-05d8-83eb-889f-0b6d945ad274)).
- [../JanteStroemSpejl_chat_export/](../JanteStroemSpejl_chat_export/): ChatGPT's own export,
  with [chat_verbatim.md](../JanteStroemSpejl_chat_export/chat_verbatim.md),
  [MANIFEST.md](../JanteStroemSpejl_chat_export/MANIFEST.md), its `ref/` and `pix/`.
- [../README.txt](../README.txt): fix log for the CACE testbench.

## External

- C. H. Maier, *Equivalent circuit models and interface circuits for CMOS microsensors*,
  Diss. ETH No. 13532, 2000, section "Quodlibet", p. 167:
  [cmucsd.bitbucket.io/akademix/PhD.pdf#page=168](https://cmucsd.bitbucket.io/akademix/PhD.pdf#page=168)
- LinkedIn posts by C. Maier:
  - 2026-10-15, "Hierdie woordspeling val op dowe ore …" (Doofe Ohren, Адмирал немец):
    [lnkd.in/p/ez5utx59](https://lnkd.in/p/ez5utx59)
  - 2026-10-12, "Albert Einstein on Discovery", with the Olsen-banden comments:
    [urn:li:activity:7515330936675401728](https://www.linkedin.com/feed/update/urn:li:activity:7515330936675401728/)
  - 2026-10-11, "Hearing aid, reimagined" (Quodlibet):
    [urn:li:activity:7515076170397425664](https://www.linkedin.com/feed/update/urn:li:activity:7515076170397425664/)
  - 2026-10-07, "Kommer Nobelpriset i kemi …":
    [urn:li:activity:7513535125842739201](https://www.linkedin.com/feed/update/urn:li:activity:7513535125842739201/)
  - 2026-10-06, "Nyheter från Stockholm":
    [urn:li:activity:7513177256240930817](https://www.linkedin.com/feed/update/urn:li:activity:7513177256240930817/)
- A. Einstein, "Einstein on the Atomic Bomb", *The Atlantic*, November 1945:
  [theatlantic.com/magazine/archive/1945/11/einstein-on-the-atomic-bomb/656626/](https://www.theatlantic.com/magazine/archive/1945/11/einstein-on-the-atomic-bomb/656626/)
- R. P. Feynman, "Personal Observations on Reliability of Shuttle", Appendix F of
  *Report of the Presidential Commission on the Space Shuttle Challenger Accident*, Vol. 2, 1986.
  Quoted as Appendix F of the report: "For a successful technology, reality must take
  precedence over public relations, for nature cannot be fooled."
  [nasa.gov/history/rogersrep/v2appf.htm](https://www.nasa.gov/history/rogersrep/v2appf.htm)
- C. Maier, Flickr album "Quodlibet":
  [flickr.com/photos/89067995@N00/albums/72177720303647432](https://www.flickr.com/photos/89067995@N00/albums/72177720303647432/)
- C. Maier, Flickr collection "Zur Elektrodynamik bewegter Körper", with the albums
  [A Swiss Train Wreck](https://www.flickr.com/photos/89067995@N00/albums/72177720309808338/) and
  [Don't Try This At Home!](https://www.flickr.com/photos/89067995@N00/albums/72177720305759654/):
  [flickr.com/photos/89067995@N00/collections/72157650447623077](https://www.flickr.com/photos/89067995@N00/collections/72157650447623077/)
- Eriksholm Research Centre, "Partner with Eriksholm":
  [eriksholm.com/partner-with-eriksholm](https://eriksholm.com/partner-with-eriksholm/)
- IHP SG13CMOS5L process specification, §2.1.1 NMOS (V_GS ≤ 1.65 V @ 125 °C, BV_DSS ≥ 2.0 V),
  at the commit in IIC-OSIC-TOOLS 2026.09:
  [SG13CMOS5L_os_process_spec.pdf @ c271a7e9](https://github.com/iic-jku/IHP-Open-PDK/blob/c271a7e97a7bab201c1d0a399215969d2ee19573/ihp-sg13cmos5l/libs.doc/doc/SG13CMOS5L_os_process_spec.pdf)
- IHP mismatch models (cmos5l symlinks to these sg13g2 files), A_VT = `delvto_mm`, 3.9 mV·µm (LV) and 7.0 mV·µm (HV):
  [sg13g2_moslv_mismatch.lib](https://github.com/iic-jku/IHP-Open-PDK/blob/c271a7e97a7bab201c1d0a399215969d2ee19573/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moslv_mismatch.lib),
  [sg13g2_moshv_mismatch.lib](https://github.com/iic-jku/IHP-Open-PDK/blob/c271a7e97a7bab201c1d0a399215969d2ee19573/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moshv_mismatch.lib)
- CACE 2.11.0 (the version in IIC-OSIC-TOOLS 2026.09), `cace/parameter/parameter.py` and
  `parameter_ngspice.py`: [pypi.org/project/cace/2.11.0](https://pypi.org/project/cace/2.11.0/)
- IIC-OSIC-TOOLS 2026.09 tool pins, `_build/tool_metadata.yml`:
  [github.com/iic-jku/IIC-OSIC-TOOLS/tree/2026.09](https://github.com/iic-jku/IIC-OSIC-TOOLS/tree/2026.09)
