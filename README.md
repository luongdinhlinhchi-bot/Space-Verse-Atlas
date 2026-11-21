# Space-Verse Atlas

Bản đồ thế giới tương tác về các cơ quan nghiên cứu thiên văn, vật lý thiên văn và vũ trụ học, dành cho sinh viên Việt Nam muốn tìm hiểu cơ hội học tập và thực tập ngành vũ trụ.

Bấm vào một nước để xem các thành phố. Bấm vào thành phố để xem cơ quan nghiên cứu. Bấm vào cơ quan để xem từng đơn vị hoặc nhóm và danh sách nhà nghiên cứu, kèm đường dẫn và nguồn.

Dự án đi cùng [Space-Verse](https://thithilia.github.io/Space-Verse).

## Tiến độ

| Nước | Trạng thái |
|---|---|
| Phần Lan | Đủ, đây là bản thử nghiệm đầu tiên |
| Đức | 40 cơ quan, khoảng 200 đơn vị, khoảng 2.900 người. 30 cơ quan đủ danh sách, 10 cơ quan còn thiếu một phần (xem `GERMANY-SOURCES.md`) |

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
node build.cjs
```

Lưu ý: một số cơ quan (MPIA, MPE, MPIK, AIP, ZAH, DLR, MPA, Uni Potsdam) được sửa trực tiếp trong JSON và không có tệp trong `germany-data-sources/`.

## Xuất bản

Mỗi lần đẩy lên nhánh `main`, GitHub Actions (`.github/workflows/pages.yml`) sẽ dựng lại trang và đăng lên GitHub Pages.

## Nguồn dữ liệu

Dữ liệu lấy từ trang nhân sự chính thức của từng viện, báo cáo thường niên của Hội Thiên văn Đức (Mitteilungen der Astronomischen Gesellschaft) và danh bạ của các trường. Mỗi danh sách đều ghi nguồn. Danh sách người chỉ chính xác đến thời điểm thu thập (11/2026).
