"""Small JSON-only status patches (idempotent)."""
import json, sys
d = sys.argv[1] if len(sys.argv) > 1 else "."
R = json.load(open(d + "/germany-researchers.json", encoding="utf8"))
k = "Universität Potsdam — Lehrstuhl für Astrophysik::Experimental Astroparticle Physics (Stegmann / Egberts)"
for p in R["units"].get(k, {}).get("people", []):
    if p["name"] == "Kathrin Egberts" and "TU Berlin" not in p["role"]:
        p["role"] += " (trang TU Berlin 11/2026 ghi bà là giáo sư Strukturprofessur Astrophysik ở TU Berlin)"
        p["url"] = "https://www.tu.berlin/vcard/egberts/175372"
json.dump(R, open(d + "/germany-researchers.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("ok")
