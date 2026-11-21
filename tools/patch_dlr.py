"""Patch DLR Institut für Weltraumforschung (JSON-only). Idempotent."""
import json, sys
d = sys.argv[1] if len(sys.argv) > 1 else "."
U = json.load(open(d + "/germany-units.json", encoding="utf8")); R = json.load(open(d + "/germany-researchers.json", encoding="utf8"))
k = [x for x in U["institutions"] if x.startswith("DLR")][0]
key = k + "::Planetare Labore"
R["units"][key]["people"] = [{"name": "Alessandro Maturilli", "role": "Trưởng bộ phận (Abteilungsleitung)", "url": "https://www.dlr.de/de/wr/ueber-uns/abteilungen/abteilung-planetare-labore"}]
src = "https://www.dlr.de/de/wr/ueber-uns/abteilungen/abteilung-planetare-labore"
if src not in R["units"][key]["sources"]: R["units"][key]["sources"].append(src)
I = U["institutions"][k]
I["coverage"] = "limited"
I["structure"] = "Viện Nghiên cứu Vũ trụ của DLR ở Berlin-Adlershof (khoảng 300 nhân sự, 13 bộ phận), hình thành từ việc sáp nhập Viện Hệ cảm biến quang học và Viện Nghiên cứu hành tinh; giám đốc: Heinz-Wilhelm Hübers. Ở đây chỉ lấy năm bộ phận nghiên cứu hành tinh."
I["scopeNote"] = ("Ghi đủ trưởng của cả năm bộ phận nghiên cứu hành tinh. DLR không công bố danh sách nhân viên theo bộ phận: trang 'Contacts' của từng bộ phận để trống, "
  "trang bộ phận chỉ nêu trưởng bộ phận. Vì vậy cơ quan này chỉ có thể ghi ở mức trưởng bộ phận. Không đưa vào các bộ phận kỹ thuật và ứng dụng "
  "(Echtzeit-Datenprozessierung, Hochgeschwindigkeitselektronik, In-Situ Sensing, Planetare Sensorsysteme, Sicherheitsforschung und Anwendungen, Terahertz- und Laserspektroskopie, Weltrauminstrumente).")
json.dump(U, open(d + "/germany-units.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
json.dump(R, open(d + "/germany-researchers.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("ok")
