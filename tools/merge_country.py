"""Build countries/<ISO3>.json from compact DSL files in countries/<ISO3>/*.txt.

Country header (in _country.txt):
@country NLD
checked: 2026-11-22
coordinateNote: ...
listSource: url
pin: 5

City lines (any file, before @inst):
@city <id> | <Tên thành phố> | <lon>, <lat> [| dx, dy]

Institution blocks:
@inst <full name>
city: <city id>
type: university | institute
url: ...
research: one-line summary
coverage: full | partial | leaders | limited
structure: ...
structureUrl: ...
scope: ...
#unit <unit name>
kind / parent / topics / url / note / src   (as in merge_de.py)
p: Name | role | url
pp: ROLE | n1; n2
x / xx: external members
"""
import json, sys, glob, os
sys.path.insert(0, os.path.dirname(__file__))
ROLE = {"GS": "Giáo sư", "GSTN": "Giáo sư; trưởng nhóm", "JP": "Giáo sư trẻ", "BC": "Nghiên cứu viên biên chế / trưởng nhóm",
        "NCV": "Nghiên cứu viên", "PD": "Nghiên cứu sau tiến sĩ", "NCS": "Nghiên cứu sinh", "THS": "Học viên thạc sĩ",
        "SV": "Sinh viên", "GD": "Giám đốc", "TN": "Trưởng nhóm nghiên cứu", "EM": "Danh dự (emeritus)", "KM": "Khách mời",
        "LK": "Thành viên liên kết", "TL": "Trợ lý nghiên cứu", "NH": "Đã nghỉ hưu", "TBP": "Trưởng bộ phận",
        "PGS": "Phó giáo sư", "TrGS": "Trợ lý giáo sư (assistant professor)", "GV": "Giảng viên"}

def parse(folder):
    country = {"cities": [], "networks": {}}
    cities = {}
    insts = []
    for f in sorted(glob.glob(os.path.join(folder, "*.txt"))):
        inst = None; unit = None
        def close_unit():
            if unit is not None: inst["_units"].append(unit)
        for n, raw in enumerate(open(f, encoding="utf8"), 1):
            line = raw.rstrip("\n")
            if not line.strip() or line.startswith("//"): continue
            where = f"{os.path.basename(f)}:{n}"
            if line.startswith("@country "):
                country["country"] = line[9:].strip(); inst = "COUNTRY"; continue
            if line.startswith("@city "):
                parts = [s.strip() for s in line[6:].split("|")]
                lon, lat = [float(x) for x in parts[2].split(",")]
                c = {"id": parts[0], "city": parts[1], "coordinates": [lon, lat], "institutions": []}
                if len(parts) > 3 and parts[3]: c["offset"] = [float(x) for x in parts[3].split(",")]
                cities[parts[0]] = c; continue
            if line.startswith("@inst "):
                if isinstance(inst, dict): close_unit(); insts.append(inst)
                inst = {"name": line[6:].strip(), "_units": [], "structure": "", "structureUrl": "", "scope": ""}; unit = None; continue
            if line.startswith("#unit "):
                close_unit()
                unit = {"u": {"name": line[6:].strip(), "kind": "Nhóm nghiên cứu", "parent": "", "topics": "", "url": ""}, "src": [], "p": [], "x": []}
                continue
            k, _, v = line.partition(":"); k = k.strip(); v = v.strip()
            if inst == "COUNTRY":
                country[k] = int(v) if k == "pin" else v; continue
            if inst is None: raise SystemExit(f"{where}: key outside block")
            if unit is None:
                inst[k] = v; continue
            if k in ("kind", "parent", "topics", "url", "note", "location"):
                unit["u"][k] = v
            elif k == "src":
                unit["src"] = [s.strip() for s in v.split(" ; ") if s.strip()]
            elif k in ("pp", "xx"):
                role, _, ns = v.partition("|")
                for nm in [s.strip() for s in ns.split(";") if s.strip()]:
                    unit[k[0]].append({"name": nm, "role": ROLE.get(role.strip(), role.strip()),
                                       "url": unit["src"][0] if unit["src"] else unit["u"]["url"]})
            elif k in ("p", "x"):
                parts = [s.strip() for s in v.split("|")]
                person = {"name": parts[0]}
                if len(parts) > 1 and parts[1]: person["role"] = ROLE.get(parts[1], parts[1])
                person["url"] = parts[2] if len(parts) > 2 and parts[2] else (unit["src"][0] if unit["src"] else unit["u"]["url"])
                unit[k].append(person)
            else:
                raise SystemExit(f"{where}: unknown key {k}")
        if isinstance(inst, dict): close_unit(); insts.append(inst)
    checked = country.get("checked", "")
    for inst in insts:
        cid = inst.pop("city", None)
        if cid not in cities: raise SystemExit(f"{inst['name']}: unknown city {cid}")
        units = []
        for u in inst.pop("_units"):
            if not u["u"]["url"]: u["u"]["url"] = u["src"][0] if u["src"] else inst.get("url", "")
            if not u["src"]: u["src"] = [u["u"]["url"]]
            for p in u["p"] + u["x"]:
                if not p["url"].startswith("http"): raise SystemExit(f"{inst['name']} / {u['u']['name']}: bad url for {p['name']}")
            seen = set()
            for p in u["p"] + u["x"]:
                key = p["name"].lower()
                if key in seen: raise SystemExit(f"duplicate {p['name']} in {u['u']['name']}")
                seen.add(key)
            u["u"]["researchers"] = {"people": u["p"], "external": u["x"], "sources": u["src"], "note": "", "checked": checked}
            units.append(u["u"])
        out = {"name": inst["name"], "type": inst.get("type", "institute"), "research": inst.get("research", ""), "url": inst.get("url", ""),
               "coverage": inst.get("coverage", "full"), "structure": inst["structure"], "structureUrl": inst["structureUrl"] or (units[0]["url"] if units else inst.get("url", "")),
               "scopeNote": inst["scope"], "units": units, "networks": []}
        if inst.get("note"): out["note"] = inst["note"]
        cities[cid]["institutions"].append(out)
    country["cities"] = [c for c in cities.values() if c["institutions"]]
    return country

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "countries"
    for folder in sorted(glob.glob(os.path.join(root, "*", ""))):
        code = os.path.basename(os.path.dirname(folder))
        c = parse(folder)
        assert c.get("country") == code, f"{folder}: @country must be {code}"
        json.dump(c, open(os.path.join(root, code + ".json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        n_inst = sum(len(ci["institutions"]) for ci in c["cities"])
        n_p = sum(len(u["researchers"]["people"]) + len(u["researchers"]["external"]) for ci in c["cities"] for i in ci["institutions"] for u in i["units"])
        print(code, "cities", len(c["cities"]), "institutions", n_inst, "people", n_p)
