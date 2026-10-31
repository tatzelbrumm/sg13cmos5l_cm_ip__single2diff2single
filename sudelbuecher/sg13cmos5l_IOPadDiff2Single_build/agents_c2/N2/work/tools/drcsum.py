"""drcsum.py <lyrdb>: violation counts per rule with the first few locations"""
import sys
import klayout.rdb as rdb
db = rdb.ReportDatabase("")
db.load(sys.argv[1])
tot = 0
for cat in db.each_category():
    items = list(db.each_item_per_category(cat.rdb_id()))
    if not items:
        continue
    tot += len(items)
    locs = []
    for it in items[:4]:
        for v in it.each_value():
            locs.append(str(v)[:90])
            break
    print("  %-16s %4d  %s" % (cat.name(), len(items), " | ".join(locs)))
print("  total violations: %d" % tot)
