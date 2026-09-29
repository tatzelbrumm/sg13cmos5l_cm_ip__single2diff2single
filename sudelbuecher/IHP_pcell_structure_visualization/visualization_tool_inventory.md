# Tool inventory — IHP pcell tree / class / import visualizations

Session 2026-09-29, Claude (configured model `claude-opus-5-5`), cloud container
(Ubuntu 24.04, x86_64). Nothing below was installed on your machine.

## Sources read

| what | where | revision |
|---|---|---|
| IHP-Open-PDK, `ihp-sg13cmos5l/libs.tech/klayout` + symlink targets in `ihp-sg13g2/libs.tech/klayout/python` | github.com/IHP-GmbH/IHP-Open-PDK, branch `dev` (sg13cmos5l is not on `main`) | `0488153` (2026-09-28) |
| pycell4klayout-api (package `cni`), git submodule | github.com/IHP-GmbH/pycell4klayout-api | `ad47f5f` (commit pinned by the PDK) |
| pypreprocessor, git submodule | github.com/IHP-GmbH/pypreprocessor | `cf1ff9b` (commit pinned by the PDK) |

The PDK was cloned with `--filter=blob:none` + sparse checkout of the three paths above.

## Already present in the container

| tool | version | used for |
|---|---|---|
| Python | 3.11.15 | `ast` module: class/base extraction; tree walk; SVG writing |
| git | 2.43.0 | clone, sparse checkout, `ls-remote`, `ls-tree` |
| Playwright (Python) + headless Chromium | 1.56.0 / chromium-1194 (`/opt/pw-browsers`) | screenshots of the SVGs to check that they render |
| ImageMagick `convert` | 6.9.12-98 | tried for SVG → PNG; failed (no SVG delegate); not used |

Not present: `tree`, `rsvg-convert`, `inkscape`, `cairosvg`, `klayout` / `klayout.db`.

## Installed this session

| tool | version | how | used for |
|---|---|---|---|
| Graphviz (`dot`, `unflatten`) | Debian package 2.42.2-9ubuntu0.1 (`dot -V` reports 2.43.0) | `apt-get install graphviz` | DOT → SVG/PNG layout |
| pylint, which contains **pyreverse** | 4.0.9 | `pip install --break-system-packages pylint` | UML class and package/import diagrams from source (static analysis) |
| (pulled in by pylint) astroid, dill, isort, mccabe, platformdirs, tomlkit | 4.0.4, 0.4.1, 9.0.2, 0.7.0, 4.9.6, 0.15.1 | pip dependencies | astroid is pyreverse's parser; the rest are unused here |

## Throwaway scripts (scratchpad, not delivered, not part of the design repo)

| script | makes |
|---|---|
| `mktree.py` | `ihp_sg13cmos5l_klayout_tree.txt` + `.svg` (one walk, two renderings; class annotations via `ast`, `[R]` from `moduleNames`) |
| `mkuml.py` | `ihp_pcell_classes_uml.dot` (bases via `ast`; associations written by hand from reading `__init__.py`, `cni/dlo.py`, `cni/tech.py`) |
| `shot.py` | PNG crops of SVGs through Chromium, for visual checks only |

## Commands

```sh
# UML class diagram
dot -Tsvg ihp_pcell_classes_uml.dot -o ihp_pcell_classes_uml.svg

# pyreverse import graph (run on a copy with symlinks resolved: cp -rL)
PYTHONPATH=src pyreverse -o dot -p ihp -k src/sg13cmos5l_pycell_lib src/cni
#   -> packages_ihp.dot; then relaid out: rankdir BT -> LR, label prefix
#      'sg13cmos5l_pycell_lib.' stripped; edges untouched
dot -Tsvg pyreverse_packages_ihp.dot -o pyreverse_packages_ihp.svg
```

## Known limitations of the outputs

* pyreverse could not resolve `cni` (no `__init__.py`, namespace package), so the import
  graph lacks all `cni` edges. It also cannot see the registrar's
  `importlib.import_module(f"...ihp.{moduleName}")`: the edge that actually loads every
  cell is invisible to static analysis. `sg13cmos5l_pycell_lib` → cells shows as unconnected.
* The UML diagram omits the cni geometry classes (Box, Point, Layer, Shape, …): cells
  instantiate them but don't inherit from them.
* Everything reflects GitHub `dev` at the revisions above. The container copy at
  `/foss/pdks/ihp-sg13cmos5l` may differ.
