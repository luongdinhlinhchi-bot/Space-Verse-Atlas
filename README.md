# Space-Verse Atlas

Bản đồ thế giới tương tác về các cơ quan nghiên cứu thiên văn, vật lý thiên văn và vũ trụ học, dành cho sinh viên Việt Nam muốn tìm hiểu cơ hội học tập và thực tập ngành vũ trụ.

Bấm vào một nước để xem các thành phố. Bấm vào thành phố để xem cơ quan nghiên cứu. Bấm vào cơ quan để xem từng đơn vị hoặc nhóm và danh sách nhà nghiên cứu, kèm đường dẫn và nguồn.

Dự án đi cùng [Space-Verse](https://thithilia.github.io/Space-Verse).

## Tiến độ

| Nước | Trạng thái |
|---|---|
| Phần Lan | Đủ, đây là bản thử nghiệm đầu tiên |
| Đức | 40 cơ quan, khoảng 200 đơn vị, khoảng 2.900 người. 30 cơ quan đủ danh sách, 10 cơ quan còn thiếu một phần (xem `GERMANY-SOURCES.md`) |
| Bỉ, Hà Lan, Thụy Sĩ, Áo, Pháp, Luxembourg | Dữ liệu trong `countries/<ISO3>.json` và `geometry/<ISO3>.json` |
| Cộng hòa Séc | 7 cơ quan tại 5 thành phố, 12 đơn vị, 258 người không trùng tên (4 đủ, 1 thiếu một phần, 2 mới có trưởng nhóm — xem `CZECHIA-SOURCES.md`) |
| Ba Lan | 7 cơ quan tại 5 thành phố, 8 đơn vị, 284 người không trùng tên (6 đủ, 1 thiếu một phần — xem `POLAND-SOURCES.md`) |
| Thụy Điển | 6 cơ quan tại 5 thành phố, 7 đơn vị, 128 người không trùng tên (1 đủ, 3 thiếu một phần, 2 mới có trưởng nhóm — xem `SWEDEN-SOURCES.md`) |
| Đan Mạch | 3 cơ quan tại 2 thành phố, 5 đơn vị, 87 người không trùng tên (3 thiếu một phần — xem `DENMARK-SOURCES.md`) |
| Na Uy | 4 cơ quan tại 4 thành phố, 5 đơn vị, 122 người không trùng tên (2 đủ, 2 mới có trưởng nhóm — xem `NORWAY-SOURCES.md`) |
| Slovakia | 3 cơ quan tại 3 thành phố, 3 đơn vị, 60 người không trùng tên (1 đủ, 2 lãnh đạo — xem `SLOVAKIA-SOURCES.md`) |
| Hungary | 3 cơ quan tại 2 thành phố, 3 đơn vị, 175 người không trùng tên (1 đủ, 1 thiếu một phần, 1 lãnh đạo — xem `HUNGARY-SOURCES.md`) |
| Romania | 4 cơ quan tại 3 thành phố, 6 đơn vị, 62 người không trùng tên (3 đủ, 1 thiếu một phần — xem `ROMANIA-SOURCES.md`) |
| Bulgaria | 4 cơ quan tại 3 thành phố, 4 đơn vị, 35 người không trùng tên (2 đủ, 2 lãnh đạo — xem `BULGARIA-SOURCES.md`) |
| Ukraina | 6 cơ quan tại 5 thành phố, 6 đơn vị, 171 người không trùng tên (3 đủ, 3 lãnh đạo — xem `UKRAINE-SOURCES.md`) |
| Belarus | 1 cơ quan tại 1 thành phố, 1 đơn vị, 1 người (lãnh đạo — xem `BELARUS-SOURCES.md`) |
| Moldova | 1 cơ quan tại 1 thành phố, 1 đơn vị, 1 người (lãnh đạo — xem `MOLDOVA-SOURCES.md`) |
| Slovenia | 2 cơ quan tại 2 thành phố, 2 đơn vị, 29 người không trùng tên (1 đủ, 1 thiếu một phần — xem `SLOVENIA-SOURCES.md`) |
| Croatia | 3 cơ quan tại 3 thành phố, 3 đơn vị, 25 người không trùng tên (3 đủ — xem `CROATIA-SOURCES.md`) |
| Bosnia và Herzegovina | 1 cơ quan tại 1 thành phố, 1 đơn vị, 1 người (lãnh đạo — xem `BOSNIA-SOURCES.md`) |
| Serbia | 2 cơ quan tại 1 thành phố, 2 đơn vị, 14 người không trùng tên (1 thiếu một phần, 1 lãnh đạo — xem `SERBIA-SOURCES.md`) |
| Montenegro | 1 cơ quan tại 1 thành phố, 1 đơn vị, 3 người (lãnh đạo — xem `MONTENEGRO-SOURCES.md`) |
| Kosovo | 1 cơ quan tại 1 thành phố, 1 đơn vị, 1 người (lãnh đạo — xem `KOSOVO-SOURCES.md`) |
| Albania | 1 cơ quan tại 1 thành phố, 1 đơn vị, 1 người (lãnh đạo — xem `ALBANIA-SOURCES.md`) |
| Bắc Macedonia | 1 cơ quan tại 1 thành phố, 1 đơn vị, 4 người không trùng tên (1 đủ — xem `MACEDONIA-SOURCES.md`) |
| Hy Lạp | 4 cơ quan tại 3 thành phố, 4 đơn vị, 69 người không trùng tên (3 đủ, 1 lãnh đạo — xem `GREECE-SOURCES.md`) |

Trên bản đồ:
- Chấm xanh: thành phố đã đủ danh sách nhà nghiên cứu.
- Chấm vàng: thành phố có cơ quan chưa đủ danh sách hoặc mới có trưởng nhóm.
- Nước tô màu: nước đã có dữ liệu.

Bản đồ thể hiện Hoàng Sa và Trường Sa thuộc Việt Nam.

## Cấu trúc

| Tệp / thư mục | Nội dung |
|---|---|
| `template.html` | Giao diện và mã JavaScript của trang |
| `build.cjs` | Script dựng trang: ghép bản đồ (D3, phép chiếu Natural Earth) và dữ liệu thành một tệp `dist/index.html` |
| `countries.geojson`, `d3.cjs` | Ranh giới các nước và thư viện D3 (để sẵn, không cần cài gói) |
| `finland*.json` | Dữ liệu Phần Lan |
| `germany.json` | Thành phố và cơ quan ở Đức |
| `germany-units.json` | Đơn vị, nhóm, cơ cấu và mức độ đầy đủ (`coverage`) của từng cơ quan |
| `germany-researchers.json` | Nhà nghiên cứu theo `Cơ quan::Đơn vị`, kèm nguồn |
| `germany-data-sources/` | Dữ liệu gốc dạng văn bản cho từng cơ quan |
| `tools/merge_de.py` | Gộp các tệp trong `germany-data-sources/` vào hai tệp JSON của Đức |
| `link-sources/` | Link trang cá nhân lấy từ danh bạ của từng viện (tên → URL) |
| `tools/apply_links.py` | Gán link trang cá nhân từ `link-sources/` cho từng người; chạy lại sau mỗi lần gộp dữ liệu |
| `tools/check_de.py` | Kiểm tra trang đã dựng trên trình duyệt (Playwright) |
| `*-SOURCES.md`, `*-RESEARCHERS.md`, `*-UNITS.md` | Báo cáo nguồn và danh sách, `build.cjs` tự sinh lại |

## Chạy trên máy

Chỉ cần Node.js, không cần `npm install`.

```bash
node build.cjs
# mở dist/index.html bằng trình duyệt
```

Sau khi sửa dữ liệu dạng văn bản của Đức:

```bash
python3 tools/merge_de.py . germany-data-sources 2026-11-21
python3 tools/apply_links.py .
node build.cjs
```

Lưu ý: một số cơ quan (MPIA, MPE, MPIK, AIP, ZAH, DLR, MPA, Uni Potsdam) được sửa trực tiếp trong JSON và không có tệp trong `germany-data-sources/`.

## Link của từng người

Tên có gạch chân dẫn tới trang cá nhân của người đó. Nếu viện không có trang riêng cho người này, tên hiện dạng chữ thường, kèm chữ "nguồn" nhỏ dẫn tới danh sách chung có tên họ.

## Xuất bản

Mỗi lần đẩy lên nhánh `main`, GitHub Actions (`.github/workflows/pages.yml`) sẽ dựng lại trang và đăng lên GitHub Pages.

## Nguồn dữ liệu

Dữ liệu lấy từ trang nhân sự chính thức của từng viện, báo cáo thường niên của Hội Thiên văn Đức (Mitteilungen der Astronomischen Gesellschaft) và danh bạ của các trường. Mỗi danh sách đều ghi nguồn. Danh sách người chỉ chính xác đến thời điểm thu thập (11/2026).
