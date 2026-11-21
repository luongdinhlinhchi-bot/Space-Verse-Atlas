"""Generate countries/BEL/liege.txt from raw STAR member list (name|uid|role|group)."""
import sys
URL = "https://www.star.uliege.be/cms/c_4265233/en/directory?uid="
PART = {"de", "van", "der", "den", "del", "da", "di", "du", "le", "la"}
def name(n):
    toks = n.split(); i = 0
    while i < len(toks) and (toks[i].isupper() or toks[i].replace("-", "").isupper()): i += 1
    last = " ".join(t.title() if t.lower() not in PART or j == 0 else t.lower() for j, t in enumerate(toks[:i]))
    last = last.replace("Suárez", "Suárez")
    return (" ".join(toks[i:]) + " " + last).strip()
RULES = [("Professeur ordinaire", "Giáo sư chính thức"), ("Professeur associé", "Phó giáo sư"), ("Professeur de recherche", "Giáo sư nghiên cứu"),
         ("Professeur", "Giáo sư"), ("Directeur de recherches FNRS", "Giám đốc nghiên cứu FNRS"), ("Maître de recherches FNRS", "Nghiên cứu viên cao cấp FNRS"),
         ("Chargé de cours", "Giảng viên chính"), ("Chargée de cours", "Giảng viên chính"), ("Maître de conférences", "Giảng viên"),
         ("Chercheur qualifié", "Nghiên cứu viên biên chế FNRS"), ("Chercheuse qualifiée", "Nghiên cứu viên biên chế FNRS"),
         ("Chargé de recherches", "Nghiên cứu viên FNRS (sau tiến sĩ)"), ("Chargée de recherches", "Nghiên cứu viên FNRS (sau tiến sĩ)"),
         ("Post-Doctorat", "Nghiên cứu sau tiến sĩ"), ("Doctorant", "Nghiên cứu sinh"), ("Boursier de doctorat", "Nghiên cứu sinh"),
         ("Chef de projet principal", "Trưởng dự án chính"), ("Chef de projet système", "Trưởng dự án hệ thống"), ("Chef de projet", "Trưởng dự án"),
         ("Cheffe de projet", "Trưởng dự án"), ("Spécialiste", "Chuyên gia"), ("Ingénieur de recherches", "Kỹ sư nghiên cứu"),
         ("logisticien de recherche", "Chuyên viên hỗ trợ nghiên cứu"), ("Logisticien de recherche", "Chuyên viên hỗ trợ nghiên cứu"),
         ("Aspirant (Space)", "Kỹ sư tập sự"), ("Aspirante (Space)", "Kỹ sư tập sự"), ("Licencié attaché", "Kỹ sư nghiên cứu"),
         ("Chercheuse visiteuse", "Nhà nghiên cứu khách mời"), ("Assistant", "Trợ giảng / trợ lý nghiên cứu"), ("Assistante", "Trợ giảng / trợ lý nghiên cứu")]
def role(r):
    if not r: return "Nhân viên (trang không ghi chức danh)"
    vi = []
    for k, v in RULES:
        if k in r and v not in vi:
            if v == "Nghiên cứu sinh" and any(x.startswith("Nghiên cứu sinh") for x in vi): continue
            vi.append(v)
        if len(vi) == 2: break
    return "; ".join(vi) + f" ({r})"
UNITS = [
 ("PSILab", "PSILab — Planetary & Stellar systems Imaging Laboratory", "Chụp ảnh tương phản cao hành tinh ngoài và đĩa quanh sao, coronagraph (kính VLT/ELT, METIS), giao thoa kế.", "https://www.psilab.uliege.be/"),
 ("COMETA", "COMETA — Comets, Meteors and Asteroids", "Sao chổi, thiên thạch và tiểu hành tinh; vận hành kính TRAPPIST (TRAPPIST-North/South) và SPECULOOS.", "http://www.cometa.uliege.be/"),
 ("ASTA", "ASTA — Theoretical Stellar Astrophysics and Asteroseismology", "Vật lý sao lý thuyết và địa chấn học sao.", "http://www.asta.uliege.be/"),
 ("GAPHE", "GAPHE — High Energy Astrophysics Group", "Sao khối lượng lớn đa bước sóng (vô tuyến đến tia X), sao đôi, Gaia.", "https://www.gaphe.uliege.be/"),
 ("MEGA", "MEGA — Multi-wavelength Extragalactic and Galactic Astrophysics", "Thiên văn ngoài thiên hà và Ngân Hà đa bước sóng: thấu kính hấp dẫn, quasar, sao khối lượng lớn; kính gương lỏng ILMT.", "https://www.star.uliege.be/"),
 ("LPAP", "LPAP — Laboratoire de Physique Atmosphérique et Planétaire", "Khí quyển hành tinh và cực quang (Sao Mộc, Juno, Sao Hỏa).", "http://www.lpap.uliege.be/"),
 ("IFPA", "IFPA — Fundamental Interactions in Physics and Astrophysics", "Tương tác cơ bản trong vật lý và vật lý thiên văn, vật lý hạt thiên văn.", "http://www.theo.phys.ulg.ac.be/wiki/Welcome_to_IFPA"),
 ("GW", "Sóng hấp dẫn (OGrav)", "Thiên văn sóng hấp dẫn, tham gia hợp tác Virgo và Einstein Telescope.", "https://www.theo.phys.ulg.ac.be/wiki/Welcome_to_IFPA"),
 ("SPACE", "Sciences spatiales", "Khoa học không gian (nhóm thuộc AGO).", "https://www.star.uliege.be/"),
 ("CSL", "CSL — Centre Spatial de Liège", "Trung tâm nghiên cứu ứng dụng của ULiège: thiết kế, chế tạo và thử nghiệm thiết bị quan sát không gian (quang học, buồng chân không thử nghiệm).", "http://www.csl.uliege.be/"),
 ("", "Nghiên cứu sinh và thành viên chưa ghi nhóm", "Thành viên STAR mà danh bạ không ghi phòng thí nghiệm.", "https://www.star.uliege.be/cms/c_4958328/en/star-members"),
]
rows = [l.rstrip("\n").split("|") for l in open(sys.argv[1], encoding="utf8") if l.strip()]
out = ["@city liege | Liège | 5.57, 50.63", "",
 "@inst Université de Liège — STAR Institute (Space sciences, Technologies and Astrophysics Research)",
 "city: liege", "type: university", "url: https://www.star.uliege.be/",
 "research: Hành tinh học, vật lý sao, thiên văn ngoài thiên hà và hạt thiên văn, thiết bị không gian; hơn 100 nhà nghiên cứu.",
 "coverage: full",
 "structure: Viện STAR gồm các phòng thí nghiệm của Khoa Vật lý thiên văn, Địa vật lý và Hải dương học (AGO) và Centre Spatial de Liège (CSL).",
 "structureUrl: https://www.star.uliege.be/cms/c_4951572/en/star-star-institute",
 "scope: Danh sách đầy đủ theo trang Members của STAR (11/2026), mỗi người có trang danh bạ ULiège riêng. Phòng thí nghiệm lấy theo dòng đơn vị ghi trong danh bạ; người có hai phòng được xếp theo phòng ghi đầu tiên.", ""]
for code, uname, topics, url in UNITS:
    ppl = [r for r in rows if (r[3].split(",")[0] if r[3] else "") == code]
    if not ppl: continue
    out += [f"#unit {uname}", "parent: STAR Institute", f"topics: {topics}", f"url: {url}", "src: https://www.star.uliege.be/cms/c_4958328/en/star-members"]
    for n, uid, r, g in ppl: out.append(f"p: {name(n)} | {role(r)} | {URL}{uid}")
    out.append("")
open(sys.argv[2], "w", encoding="utf8").write("\n".join(out))
print(len(rows))
