"""Layer numbers and metal design rules, read from the PDK files (nothing hard-coded).

Sources (ihp-sg13cmos5l): libs.tech/klayout/tech/sg13cmos5l.lyp   layer name -> GDS layer/datatype
                          libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json   rule values
"""
import json, os, re
import xml.etree.ElementTree as ET

PDK = os.environ.get("PDK_ROOT", "/foss/pdks") + "/ihp-sg13cmos5l"
TECH = PDK + "/libs.tech/klayout/tech"
METALS = ["Metal1", "Metal2", "Metal3", "Metal4", "TopMetal1"]   # the whole stack of this PDK (M1-M4-TM1)
POLY = "GatPoly"                                                 # art layer below Metal1 (no Activ underneath)
# GDS layer numbers that are not FEOL: metals, vias, TopVia, prBoundary, TEXT
NON_FEOL = {8, 10, 30, 50, 126, 19, 29, 49, 125, 189, 63}


def layer_numbers():
    """{'Metal1.drawing': (8, 0), ...} from the .lyp file."""
    root = ET.parse(TECH + "/sg13cmos5l.lyp").getroot()
    out = {}
    for p in root.iter("properties"):
        name, src = p.findtext("name"), p.findtext("source")
        if name and src and re.match(r"^\d+/\d+", src):
            l, d = src.split("@")[0].split("/")
            out[name.strip()] = (int(l), int(d))
    return out


def rules():
    with open(TECH + "/drc/rule_decks/sg13cmos5l_tech_default.json") as f:
        return json.load(f)["drc_rules"]


def metal_rules():
    """Per metal: min width, min space, wide-line spacing rules (a/b/e/f/g/i/j/k) in um."""
    r = rules()
    out = {}
    for m in METALS:
        if m == "Metal1":
            k = "M1"
            out[m] = dict(w=r["M1_a"], s=r["M1_b"], e_s=r["M1_e"], e_w=r["M1_e_w"], e_l=r["M1_e_cr"],
                          f_s=r["M1_f"], f_w=r["M1_f_w"], f_l=r["M1_f_cr"], s45=r["M1_i"], w45=r["M1_g"],
                          dmin=r["M1_j"], dmax=r["M1_k"], area=r["M1_d"], fill_h=r["MFil_h"], fill_k=r["MFil_k"])
        elif m == "TopMetal1":
            out[m] = dict(w=r["TM1_a"], s=r["TM1_b"], dmin=r["TM1_c"], dmax=r["TM1_d"], fill_space=r["TM1Fil_c"])
        else:
            out[m] = dict(w=r["Mn_a"], s=r["Mn_b"], e_s=r["Mn_e"], e_w=r["Mn_e_w"], e_l=r["Mn_e_cr"],
                          f_s=r["Mn_f"], f_w=r["Mn_f_w"], f_l=r["Mn_f_cr"], s45=r["Mn_i"], w45=r["Mn_g"],
                          dmin=r["Mn_j"], dmax=r["Mn_k"], area=r["Mn_d"], fill_h=r["MFil_h"], fill_k=r["MFil_k"])
    out[POLY] = dict(w=r["Gat_a"], s=r["Gat_b"])
    return out


def drawing_layers():
    ln = layer_numbers()
    return {m: ln[m + ".drawing"] for m in [POLY] + METALS}


if __name__ == "__main__":
    ln = layer_numbers()
    for m, v in drawing_layers().items():
        print(m, v, metal_rules()[m])
