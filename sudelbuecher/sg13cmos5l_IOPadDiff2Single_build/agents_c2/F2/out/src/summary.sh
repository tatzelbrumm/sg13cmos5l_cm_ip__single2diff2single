#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# one line per checked cell of a check_cells.sh run directory: DRC verdict, exceptions, LVS verdict, sym_check summary
for d in "$1"/*/; do
  c=$(basename "$d")
  [ -f "$d/drc.log" ] || continue
  drc=$(grep -oE "Check Passed|Violated rules are : .*" "$d/drc.log" | tail -1)
  exc=$(grep -c "generated an exception" "$d/drc.log")
  lvs=$(grep -oE "PASS \(netlists match\)|FAIL[^|]*" "$d/lvs.log" | head -1)
  sym=$(grep summary "$d/sym.txt" | sed 's/^ *summary: //')
  echo "$c | DRC ${drc:-none} (exceptions $exc) | LVS ${lvs:-?} | sym: $sym"
done
