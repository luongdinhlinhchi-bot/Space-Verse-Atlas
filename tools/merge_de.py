"""Merge compact institution data files (data/*.txt) into germany-units.json and germany-researchers.json.

Format:
@inst <exact institution name in germany.json>
structure: ...
structureUrl: ...
scope: ...
#unit <unit name>
kind: ...           (default: Nhóm nghiên cứu)
parent: ...
topics: ...
url: ...
note: ...
src: url1 ; url2    (first is default person url)
p: Name | role | url     (role, url optional)
x: Name | role | url     (guest / associate)
"""
import json, sys, glob, os
ROLE = {"GS": "Giáo sư", "GSTN": "Giáo sư; trưởng nhóm", "JP": "Giáo sư trẻ (Juniorprofessor)", "BC": "Nghiên cứu viên biên chế / trưởng nhóm",
        "NCV": "Nghiên cứu viên", "PD": "Nghiên cứu sau tiến sĩ", "NCS": "Nghiên cứu sinh", "THS": "Học viên thạc sĩ",
        "SV": "Sinh viên", "GD": "Giám đốc", "TN": "Trưởng nhóm nghiên cứu", "EM": "Danh dự (emeritus)", "KM": "Khách mời",
        "LK": "Thành viên liên kết", "TL": "Trợ lý nghiên cứu", "NH": "Đã nghỉ hưu", "PDZ": "Privatdozent", "TBP": "Trưởng bộ phận"}
d = sys.argv[1]
U = json.load(open(d + "/germany-units.json", encoding="utf8"))
R = json.load(open(d + "/germany-researchers.json", encoding="utf8"))
G = json.load(open(d + "/germany.json", encoding="utf8"))
names = {i["name"] for c in G["cities"] for i in c["institutions"]}
for f in sorted(glob.glob(os.path.join(sys.argv[2], "*.txt"))):
    inst = None; unit = None; units = []
    def close():
        if unit: units.append(unit)
    for raw in open(f, encoding="utf8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.startswith("//"): continue
        if line.startswith("@inst "):
            inst = {"name": line[6:].strip(), "structure": "", "structureUrl": "", "scope": ""}
            continue
        if line.startswith("#unit "):
            close()
            unit = {"u": {"name": line[6:].strip(), "kind": "Nhóm nghiên cứu", "parent": "", "topics": "", "url": ""}, "src": [], "p": [], "x": []}
            continue
        k, _, v = line.partition(":")
        k = k.strip(); v = v.strip()
        if unit is None:
            inst[k] = v; continue
        if k in ("kind", "parent", "topics", "url", "note"):
            unit["u"][k] = v
        elif k == "src":
            unit["src"] = [s.strip() for s in v.split(" ; ") if s.strip()]
        elif k in ("pp", "xx"):
            role, _, ns = v.partition("|")
            for n in [s.strip() for s in ns.split(";") if s.strip()]:
                person = {"name": n, "role": ROLE.get(role.strip(), role.strip())}
                person["url"] = unit["src"][0] if unit["src"] else unit["u"]["url"]
                unit[k[0]].append(person)
        elif k in ("p", "x"):
            parts = [s.strip() for s in v.split("|")]
            person = {"name": parts[0]}
            if len(parts) > 1 and parts[1]: person["role"] = ROLE.get(parts[1], parts[1])
            person["url"] = parts[2] if len(parts) > 2 and parts[2] else (unit["src"][0] if unit["src"] else unit["u"]["url"])
            unit[k].append(person)
        else:
            raise SystemExit(f"{f}: unknown key {k}")
    close()
    if inst["name"] not in names: raise SystemExit(f"{f}: unknown institution {inst['name']}")
    for u in units:
        if not u["u"]["url"]: u["u"]["url"] = u["src"][0]
        if not u["src"]: u["src"] = [u["u"]["url"]]
    old_cov = U["institutions"].get(inst["name"], {}).get("coverage")
    U["institutions"][inst["name"]] = {"coverage": inst.get("coverage") or old_cov or "full", "structure": inst["structure"], "structureUrl": inst["structureUrl"] or units[0]["src"][0],
                                       "scopeNote": inst["scope"], "units": [u["u"] for u in units], "networks": []}
    for k in [k for k in R["units"] if k.startswith(inst["name"] + "::")]: del R["units"][k]
    for u in units:
        R["units"][inst["name"] + "::" + u["u"]["name"]] = {"sources": u["src"], "people": u["p"], "external": u["x"], "note": ""}
    print(os.path.basename(f), len(units), sum(len(u["p"]) + len(u["x"]) for u in units))
R["checked"] = U["checked"] = sys.argv[3] if len(sys.argv) > 3 else U["checked"]
json.dump(U, open(d + "/germany-units.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
json.dump(R, open(d + "/germany-researchers.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("institutions", len(U["institutions"]), "units", len(R["units"]), "people", len({p["name"] for r in R["units"].values() for p in r["people"] + r["external"]}))
