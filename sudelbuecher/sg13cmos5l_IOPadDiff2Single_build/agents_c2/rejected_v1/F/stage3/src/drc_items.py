# list DRC markers of a run dir: python3 drc_items.py <run_dir> [max]
import sys, glob, xml.etree.ElementTree as ET
f = glob.glob(sys.argv[1] + "/*full.lyrdb")[0]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 50
for k, it in enumerate(ET.parse(f).getroot().iter("item")):
    if k >= n: break
    print(it.find("category").text, it.find("cell").text, [x.text[:160] for x in it.find("values").findall("value")])
