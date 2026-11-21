"""Patch Heidelberg JSON-only institutions (ZAH group members, MPIA groups). Idempotent."""
import json, sys, unicodedata
d = sys.argv[1] if len(sys.argv) > 1 else "."
U = json.load(open(d + "/germany-units.json", encoding="utf8"))
R = json.load(open(d + "/germany-researchers.json", encoding="utf8"))
RU = R["units"]
def fold(s):
    s = s.replace("ß", "ss").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue")
    s = unicodedata.normalize("NFKD", s); s = "".join(c for c in s if not unicodedata.combining(c))
    t = s.lower().replace("-", " ").split(); return (t[0], t[-1]) if t else ("", "")

ZAH = "Universität Heidelberg — Zentrum für Astronomie (ZAH)"
GROUPS = {
 "Planet Formation Group": ("http://www.ita.uni-heidelberg.de/~dullemond/group.shtml", "Hình thành hành tinh từ bụi trong đĩa tiền hành tinh bằng mô phỏng số: cấu trúc và tiến hóa đĩa, kết tụ – vỡ hạt bụi, hình thành planetesimal, tăng trưởng phôi hành tinh, tương tác N-vật; nối với quan sát qua mô hình truyền bức xạ.", [
  ("Kees Dullemond", "Giáo sư; trưởng nhóm", "Cornelis Petrus Dullemond"), ("Jiahan Shi", "Nghiên cứu sau tiến sĩ", None),
  ("Dmitry Semenov", "Nhà nghiên cứu cấp cao độc lập (hóa học thiên văn)", None),
  ("Carolin Kimmig", "Nghiên cứu sinh", None), ("Leon Hühn", "Nghiên cứu sinh", None), ("Jorge Pérez González", "Nghiên cứu sinh", None),
  ("Sören Meiners", "Học viên thạc sĩ", None), ("Kim Weiskopf", "Học viên thạc sĩ", None), ("Jakob Shoell", "Học viên thạc sĩ", None), ("Drishika Nadella", "Học viên thạc sĩ", None),
  ("Jenya Govorov", "Sinh viên", None), ("Julia Dierich", "Sinh viên", None), ("Laura Polzer", "Sinh viên", None)]),
 "Star Formation Group": ("https://klessen.org/group", "Hình thành sao và môi trường liên sao: nhiễu loạn, từ trường, phản hồi sao, sao thế hệ đầu, mô phỏng số quy mô lớn.", [
  ("Ralf Klessen", "Giáo sư; trưởng nhóm", "Ralf Stefan Klessen"), ("Simon Glover", "Nhà khoa học biên chế", "Simon C. O. Glover"),
  ("Victor Ksoll", "Trưởng nhóm độc lập", "Victor Francisco Ksoll"), ("Philipp Girichidis", "Nghiên cứu sau tiến sĩ", None), ("Stefan Reißl", "Nghiên cứu sau tiến sĩ", None),
  ("Nils Candebat", "Nghiên cứu sinh", None), ("Karin Kjellgren", "Nghiên cứu sinh", None), ("Aron Kordt", "Nghiên cứu sinh", None), ("Veronika Lipatova", "Nghiên cứu sinh", None),
  ("Jorge Saavedra Bastidas", "Nghiên cứu sinh", "Jorge Eduardo Saavedra Bastidas"), ("Shuyu Tan", "Nghiên cứu sinh", None), ("Jia Wei Teh", "Nghiên cứu sinh", None), ("Daniel Walter", "Nghiên cứu sinh", None),
  ("Lea Flach", "Sinh viên cử nhân/thạc sĩ", None), ("Maximilian Richter", "Sinh viên cử nhân/thạc sĩ", None)]),
 "Galactic Matter Cycle Group (Emmy Noether)": ("https://www.ita.uni-heidelberg.de/~mchevance/index.html", "Chu trình vật chất trong thiên hà: vòng đời đám mây phân tử, hiệu suất hình thành sao và phản hồi sao ở các thiên hà lân cận.", [
  ("Mélanie Chevance", "Trưởng nhóm Emmy Noether", "Melanie Chevance"), ("Lise Ramambason", "Nghiên cứu sau tiến sĩ", None), ("Andrea Romanelli", "Nghiên cứu sinh", None)]),
}
inst = U["institutions"][ZAH]
pools = [k for k in RU if k.startswith(ZAH + "::Danh sách nhân sự")]
for g, (src, topics, members) in GROUPS.items():
    key = ZAH + "::" + g; unit = RU[key]
    out = []
    for name, role, alias in members:
        f = fold(alias or name); found = None
        for pk in pools:
            for p in RU[pk]["people"]:
                if fold(p["name"]) == f: found = p; break
            if found: RU[pk]["people"].remove(found); break
        if not found:
            for p in unit["people"]:
                if fold(p["name"]) in (f, fold(name)): found = p
        url = (found or {}).get("url") or src
        out.append({"name": name, "role": role, "url": url})
    unit["people"] = out
    if src not in unit["sources"]: unit["sources"].append(src)
    for u in inst["units"]:
        if u["name"] == g:
            u["topics"] = topics; u["note"] = "Thành viên theo trang nhóm (11/2026); người có trong danh bạ ZAH đã được chuyển từ danh sách nhân sự của viện sang nhóm này."
inst["coverage"] = "full"
inst["scopeNote"] = ("Có đủ 31 nhóm với trưởng nhóm, và toàn bộ nhân sự theo danh bạ ZAH. Thành viên của nhóm Planet Formation, Star Formation và Galactic Matter Cycle đã được tách theo trang nhóm; "
  "các nhóm còn lại có trang nhóm cũ không tải được hoặc không có danh sách thành viên, nên thành viên vẫn nằm trong danh sách nhân sự của từng viện (ARI, ITA, LSW).")

MPIA = "Max-Planck-Institut für Astronomie"
mi = U["institutions"][MPIA]
add = [
 ({"name": "Extragalactic Group (de Graaff)", "kind": "Nhóm nghiên cứu Lise Meitner", "parent": MPIA,
   "topics": "Hình thành thiên hà và lỗ đen sớm với JWST (dẫn dắt chương trình RUBIES), các 'chấm đỏ nhỏ' (little red dots), thiên hà khối lượng lớn sớm, khảo sát Euclid, Roman, 4MOST; tài trợ Lise Meitner và ERC FIRST-GIANTS.",
   "url": "https://www.mpia.de/extragalactic-group/members", "note": ""},
  ["https://www.mpia.de/extragalactic-group", "https://www.mpia.de/extragalactic-group/members"],
  [("Anna de Graaff", "Trưởng nhóm Lise Meitner", "https://www.mpia.de/person/125421/6485843"),
   ("Thomas Harvey", "Nghiên cứu sau tiến sĩ", "https://thomas-harvey.com"), ("Raphael Hviding", "Nghiên cứu sau tiến sĩ", "https://hviding.www3.mpia.de"),
   ("Ines Berčuk", "Nghiên cứu sinh", None), ("Rashmi Gottumukkala", "Nghiên cứu sinh", None), ("Maria Teresa Nardone", "Nghiên cứu sinh", None),
   ("Jerret Peschka", "Sinh viên / thực tập", None), ("Osama Bin Feroze", "Sinh viên / thực tập", None)]),
 ({"name": "Emeritus Research Group (Henning)", "kind": "Nhóm nghiên cứu danh dự", "parent": MPIA,
   "topics": "Hình thành sao và hành tinh, đĩa tiền hành tinh, hành tinh ngoài và sao lùn nâu, vật lý – hóa học môi trường liên sao, thiên văn phòng thí nghiệm; Heidelberg Initiative for the Origins of Life.",
   "url": "https://www.mpia.de/6253118/thomas-k", "note": "Trang nhóm chỉ có hồ sơ của trưởng nhóm."},
  ["https://www.mpia.de/6253118/thomas-k"],
  [("Thomas Henning", "Giám đốc danh dự; trưởng nhóm", "https://www.mpia.de/6253118/thomas-k")]),
]
for u, srcs, ppl in add:
    mi["units"] = [x for x in mi["units"] if x["name"] != u["name"]] + [u]
    RU[MPIA + "::" + u["name"]] = {"sources": srcs, "people": [{"name": n, "role": r, "url": url or u["url"]} for n, r, url in ppl], "external": [], "note": ""}
mi["coverage"] = "full"
mi["scopeNote"] = "Đủ ba bộ phận (GC, PFE/PSF, APEx) theo danh sách toàn bộ phận, và năm nhóm độc lập: Galactic Nuclei, ExoWorlds Imaging, Stellar Spectroscopy, Extragalactic, Emeritus. Thành viên trong các bộ phận chưa tách theo nhóm con."
json.dump(U, open(d + "/germany-units.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
json.dump(R, open(d + "/germany-researchers.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("ok")
