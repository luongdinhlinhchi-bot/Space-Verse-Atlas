// Phân loại vai trò để tách người có thể hướng dẫn khỏi nghiên cứu sinh / sinh viên.
// staff: giảng viên, nghiên cứu viên chính thức, trưởng nhóm · postdoc · student · tech · emeritus · guest · unknown (nguồn không ghi hoặc gộp lẫn)
const t=(re,s)=>re.test(s);
function roleClass(role){
 const s=(role||'').toLowerCase().trim();
 if(!s) return 'unknown';
 if(t(/postdoc\s*\/\s*ncs|pd\s*\/\s*ncs|ncs\s*\/\s*nhân sự|biên chế, pd, ncs|postdoc\/ncs|nghiên cứu viên\s*\/\s*nghiên cứu sinh|nhà khoa học\s*\/\s*nghiên cứu sinh|không phân loại|chưa tách|ncs\s*\/\s*nghiên cứu viên|nghiên cứu viên trẻ\s*\/\s*ncs|nghiên cứu sinh\s*\/\s*trợ lý nghiên cứu|trợ giảng \/ trợ lý nghiên cứu \(assistant/,s)&&!t(/^nghiên cứu sinh;/,s)) return 'unknown';
 if(t(/emerit|émérite|danh dự|nghỉ hưu|đã mất|cựu |nguyên giám đốc/,s)) return 'emeritus';
 if(t(/nghiên cứu sinh|doctorant|doktorand|(^|[^a-zà-ỹ])ncs([^a-zà-ỹ]|$)|phd student|học viên|thạc sĩ|cử nhân|sinh viên|thực tập|doctorandus|aspirant(e)? fnrs|boursi.re de doctorat/,s)&&(!t(/^(giáo sư|gs|giảng viên|trưởng|nghiên cứu viên|phó|nhà khoa học|nhà nghiên cứu|nhà thiên văn)|hướng dẫn nghiên cứu sinh/,s)||t(/^nghiên cứu viên trẻ/,s))) return 'student';
 if(t(/khách|thỉnh giảng|visiting|bên ngoài|ngoài trường|ngoài viện|auswärtig|liên kết|cộng tác|associato|biệt phái|adjunct|kiêm nhiệm|học giả/,s)) return 'guest';
 if(t(/sau tiến sĩ|postdoc|post-doc|^pd( |$|;|\/)(?!\(privat)|^pd \/|\(pd\)|fellow|assegnist|borsist|grant holder|ater|junior scientist|chargé de recherches fnrs|hợp đồng có thời hạn|nghiên cứu viên hợp đồng|nghiên cứu viên trẻ|humboldt/,s)&&!t(/trưởng nhóm|max planck fellow|academy research fellow|giáo sư|^gs/,s)) return 'postdoc';
 if(t(/kỹ sư|kỹ thuật|ingénieur|engineer|tecnologo|công nghệ thông tin|cntt|xưởng|quản lý|điều phối|truyền thông|hỗ trợ|logisticien|chuyên viên|chuyên gia|nhân viên|máy tính|dữ liệu|vận hành|thiết bị quang|dự án số|kiến trúc hệ thống|spécialiste|chef de projet|aspirant(e)? \(space\)|dự án|lập trình|thư viện/,s)&&!t(/giáo sư|trưởng nhóm|nghiên cứu viên|nhà khoa học|nhà nghiên cứu|^gs|^ncv/,s)) return 'tech';
 if(t(/giáo sư|^gs|^pgs|gstn|^jp |^gd |^tn |giảng viên|privatdozent|^pd \(privat|^pdz|^pd\b.*trưởng|trưởng|giám đốc|viện trưởng|nghiên cứu viên|^ncv|nhà nghiên cứu|nhà khoa học|nhà thiên văn|nhà vật lý|astronom|ricercator|dirigente|chargé|maître|directeur|staff scientist|cán bộ|nhân sự (biên chế|học thuật|khoa học|nghiên cứu)|academy research fellow|max planck fellow|lecturer|scientist|research manager|cố vấn|lehrstuhl|akademisch|chủ nhiệm|phụ trách|ban (giám đốc|điều hành)|phó|tenure|catedr|titular|ajudant|professeur|professor|research council|finca fellow|^pi |tiến sĩ|quan sát viên|trợ lý nghiên cứu cao cấp/,s)) return 'staff';
 return 'unknown';
}
module.exports={roleClass};
