const fs = require('fs');
const d3 = require('./d3.cjs');
const data = JSON.parse(fs.readFileSync('countries.geojson','utf8'));
// World view focused on Europe (all countries with data so far are European).
const focusFrame = {type:'MultiPoint',coordinates:[[-22,35],[40,35],[-22,70.5],[40,70.5],[10,71.5],[10,34]]};
const projection = d3.geoConicConformal().parallels([40,65]).rotate([-12,0]).fitExtent([[20,16],[1180,744]],focusFrame).clipExtent([[0,0],[1200,760]]);
const path = d3.geoPath(projection);
// label anchor: pole of inaccessibility (grid search) of the largest projected polygon of a country
function labelPoint(f){
 const geom=f.geometry;const polys=geom.type==='Polygon'?[geom.coordinates]:geom.type==='MultiPolygon'?geom.coordinates:[];
 let best=null,bestA=0;
 for(const poly of polys){const rings=poly.map(r=>r.map(c=>projection(c)).filter(p=>p&&Number.isFinite(p[0])));if(!rings[0]||rings[0].length<3)continue;const a=Math.abs(d3.polygonArea(rings[0]));if(a>bestA){bestA=a;best=rings}}
 if(!best)return null;
 const outer=best[0];const xs=outer.map(p=>p[0]),ys=outer.map(p=>p[1]);
 const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
 const segDist=(px,py,a,b)=>{const dx=b[0]-a[0],dy=b[1]-a[1],l=dx*dx+dy*dy;let t=l?((px-a[0])*dx+(py-a[1])*dy)/l:0;t=Math.max(0,Math.min(1,t));return Math.hypot(px-a[0]-t*dx,py-a[1]-t*dy)};
 const edge=(px,py)=>{let m=Infinity;for(const r of best)for(let i=0;i<r.length;i++){const d=segDist(px,py,r[i],r[(i+1)%r.length]);if(d<m)m=d}return m};
 const inside=(px,py)=>d3.polygonContains(outer,[px,py])&&!best.slice(1).some(h=>d3.polygonContains(h,[px,py]));
 let bx=(x0+x1)/2,by=(y0+y1)/2,bd=-1;
 const N=28;for(let i=0;i<=N;i++)for(let j=0;j<=N;j++){const px=x0+(x1-x0)*i/N,py=y0+(y1-y0)*j/N;if(!inside(px,py))continue;const d=edge(px,py);if(d>bd){bd=d;bx=px;by=py}}
 let step=Math.max(x1-x0,y1-y0)/N;for(let k=0;k<4;k++){step/=2;for(let i=-3;i<=3;i++)for(let j=-3;j<=3;j++){const px=bx+i*step,py=by+j*step;if(!inside(px,py))continue;const d=edge(px,py);if(d>bd){bd=d;bx=px;by=py}}}
 return [+bx.toFixed(1),+by.toFixed(1),+Math.max(bd,0).toFixed(1)];
}

const esc = s => String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
const finland = JSON.parse(fs.readFileSync('finland.json','utf8'));
const unitData = JSON.parse(fs.readFileSync('finland-units.json','utf8'));
const researcherData = JSON.parse(fs.readFileSync('finland-researchers.json','utf8'));
const allUnits=Object.values(unitData.institutions).flatMap(i=>i.units);
for(const unit of allUnits){
 const roster=researcherData.units[unit.name];
 if(!roster) throw new Error(`Missing researcher record: ${unit.name}`);
 if(!roster.sources?.length) throw new Error(`Missing researcher sources: ${unit.name}`);
 const names=new Set();
 for(const person of [...(roster.people||[]),...(roster.external||[])]){
  if(!person.name?.trim()||!/^https?:\/\//.test(person.url||'')) throw new Error(`Invalid researcher in ${unit.name}`);
  const key=person.name.normalize('NFC').toLowerCase();
  if(names.has(key)) throw new Error(`Duplicate researcher ${person.name} in ${unit.name}`);
  names.add(key);
 }
 unit.researchers={people:roster.people||[],external:roster.external||[],sources:roster.sources,note:roster.note,checked:researcherData.checked};
}
finland.networks=unitData.networks;
for(const city of finland.cities) for(const institution of city.institutions){
 const details=unitData.institutions[institution.name];
 if(!details?.units?.length) throw new Error(`Missing units for ${institution.name}`);
 for(const key of details.networks) if(!unitData.networks[key]) throw new Error(`Unknown network: ${key}`);
 Object.assign(institution,details);
}
const germany = JSON.parse(fs.readFileSync('germany.json','utf8'));
germany.networks = {};
for(const city of germany.cities) for(const institution of city.institutions){ institution.units = institution.units||[]; institution.networks = institution.networks||[]; }
const germanyUnits = JSON.parse(fs.readFileSync('germany-units.json','utf8'));
const germanyResearchers = JSON.parse(fs.readFileSync('germany-researchers.json','utf8'));
const germanNames = new Set(germany.cities.flatMap(c => c.institutions.map(i => i.name)));
for(const name of Object.keys(germanyUnits.institutions)) if(!germanNames.has(name)) throw new Error(`Unknown German institution: ${name}`);
const germanReport = ['# Đức — đơn vị và nhà nghiên cứu (các cơ quan đã làm)', `\nNgày kiểm tra nguồn: ${germanyResearchers.checked}. ${germanyResearchers.scope}\n`];
for(const city of germany.cities) for(const institution of city.institutions){
 const details = germanyUnits.institutions[institution.name];
 if(!details) continue;
 germanReport.push(`## ${institution.name} — ${city.city}\n\n[Cơ cấu](${details.structureUrl}): ${details.structure}\n\n${details.scopeNote||''}\n`);
 for(const unit of details.units){
  const roster = germanyResearchers.units[institution.name+'::'+unit.name];
  if(!roster?.sources?.length) throw new Error(`Missing researcher record: ${institution.name} / ${unit.name}`);
  const names = new Set();
  for(const person of [...roster.people, ...roster.external]){
   if(!person.name?.trim() || !/^https?:\/\//.test(person.url||'')) throw new Error(`Invalid researcher in ${unit.name}`);
   const key = person.name.normalize('NFC').toLowerCase();
   if(names.has(key)) throw new Error(`Duplicate researcher ${person.name} in ${unit.name}`);
   names.add(key);
  }
  unit.researchers = {people:roster.people, external:roster.external, sources:roster.sources, note:roster.note, checked:germanyResearchers.checked};
  germanReport.push(`### [${unit.name}](${unit.url})\n\n${unit.kind}${unit.parent?'. Trực thuộc: '+unit.parent:''}.\n\n${unit.topics}\n${unit.note?'\n'+unit.note+'\n':''}`);
  for(const p of roster.people) germanReport.push(`- ${p.name} — ${p.role}`);
  if(roster.external.length){ germanReport.push('\nKhách mời / thành viên liên kết:\n'); for(const p of roster.external) germanReport.push(`- ${p.name} — ${p.role}`); }
  germanReport.push(`\nNguồn: ${roster.sources.map((u,i)=>`[${i+1}](${u})`).join(', ')}.\n`);
 }
 Object.assign(institution, details);
}
fs.writeFileSync('GERMANY-RESEARCHERS.md', germanReport.join('\n'));
const countryData = {FIN:finland, DEU:germany};
// Các nước khác: countries/<ISO3>.json do tools/merge_country.py sinh ra.
/** Load, validate, attach unit/researcher rosters, and write the Markdown report for a 3-file country dataset. */
function loadStandardCountry(prefix, reportTitle, reportFile){
 const country = JSON.parse(fs.readFileSync(`${prefix}.json`,'utf8'));
 const unitData = JSON.parse(fs.readFileSync(`${prefix}-units.json`,'utf8'));
 const researcherData = JSON.parse(fs.readFileSync(`${prefix}-researchers.json`,'utf8'));
 country.networks = unitData.networks || {};
 const instNames = new Set(country.cities.flatMap(c => c.institutions.map(i => i.name)));
 for(const name of Object.keys(unitData.institutions)) if(!instNames.has(name)) throw new Error(`Unknown institution in ${prefix}: ${name}`);
 const report = [`# ${reportTitle} — đơn vị và nhà nghiên cứu`, `\nNgày kiểm tra nguồn: ${researcherData.checked}. ${researcherData.scope||''}\n`];
 for(const city of country.cities) for(const institution of city.institutions){
  institution.units = institution.units||[];
  institution.networks = institution.networks||[];
  const details = unitData.institutions[institution.name];
  if(!details) throw new Error(`Missing units for ${institution.name}`);
  for(const key of details.networks||[]) if(!country.networks[key]) throw new Error(`Unknown network: ${key}`);
  report.push(`## ${institution.name} — ${city.city}\n\n[Cơ cấu](${details.structureUrl}): ${details.structure}\n\n${details.scopeNote||''}\n`);
  for(const unit of details.units){
   const roster = researcherData.units[institution.name+'::'+unit.name];
   if(!roster?.sources?.length) throw new Error(`Missing researcher record: ${institution.name} / ${unit.name}`);
   const names = new Set();
   for(const person of [...(roster.people||[]), ...(roster.external||[])]){
    if(!person.name?.trim() || !/^https?:\/\//.test(person.url||'')) throw new Error(`Invalid researcher in ${unit.name}`);
    const key = person.name.normalize('NFC').toLowerCase();
    if(names.has(key)) throw new Error(`Duplicate researcher ${person.name} in ${unit.name}`);
    names.add(key);
   }
   unit.researchers = {people:roster.people||[], external:roster.external||[], sources:roster.sources, note:roster.note, checked:researcherData.checked};
   report.push(`### [${unit.name}](${unit.url})\n\n${unit.kind}${unit.parent?'. Trực thuộc: '+unit.parent:''}.\n\n${unit.topics}\n${unit.note?'\n'+unit.note+'\n':''}`);
   for(const p of roster.people||[]) report.push(`- ${p.name} — ${p.role}`);
   if((roster.external||[]).length){ report.push('\nKhách mời / thành viên liên kết:\n'); for(const p of roster.external) report.push(`- ${p.name} — ${p.role}`); }
   report.push(`\nNguồn: ${roster.sources.map((u,i)=>`[${i+1}](${u})`).join(', ')}.\n`);
  }
  if((details.networks||[]).length) report.push(`Liên kết: ${details.networks.map(key=>country.networks[key].name).join('; ')}.\n`);
  Object.assign(institution, details);
 }
 if(Object.keys(country.networks).length){
  report.push('## Quan hệ liên đại học và liên viện\n');
  for(const network of Object.values(country.networks)) report.push(`### [${network.name}](${network.url})\n\n${network.kind}. ${network.topics}\n\n${network.note||''}\n`);
 }
 fs.writeFileSync(reportFile, report.join('\n'));
 return country;
}
for(const [iso, prefix, title, reportFile] of [
 ['CZE','czechia','Cộng hòa Séc','CZECHIA-RESEARCHERS.md'],
 ['POL','poland','Ba Lan','POLAND-RESEARCHERS.md'],
 ['SWE','sweden','Thụy Điển','SWEDEN-RESEARCHERS.md'],
 ['DNK','denmark','Đan Mạch','DENMARK-RESEARCHERS.md'],
 ['NOR','norway','Na Uy','NORWAY-RESEARCHERS.md'],
 ['SVK','slovakia','Slovakia','SLOVAKIA-RESEARCHERS.md'],
 ['HUN','hungary','Hungary','HUNGARY-RESEARCHERS.md'],
 ['ROU','romania','Romania','ROMANIA-RESEARCHERS.md'],
 ['BGR','bulgaria','Bulgaria','BULGARIA-RESEARCHERS.md'],
 ['UKR','ukraine','Ukraina','UKRAINE-RESEARCHERS.md'],
 ['BLR','belarus','Belarus','BELARUS-RESEARCHERS.md'],
 ['MDA','moldova','Moldova','MOLDOVA-RESEARCHERS.md'],
 ['SVN','slovenia','Slovenia','SLOVENIA-RESEARCHERS.md'],
 ['HRV','croatia','Croatia','CROATIA-RESEARCHERS.md'],
 ['BIH','bosnia','Bosnia và Herzegovina','BOSNIA-RESEARCHERS.md'],
 ['SRB','serbia','Serbia','SERBIA-RESEARCHERS.md'],
 ['MNE','montenegro','Montenegro','MONTENEGRO-RESEARCHERS.md'],
 ['KOS','kosovo','Kosovo','KOSOVO-RESEARCHERS.md'],
 ['ALB','albania','Albania','ALBANIA-RESEARCHERS.md'],
 ['MKD','macedonia','Bắc Macedonia','MACEDONIA-RESEARCHERS.md'],
 ['GRC','greece','Hy Lạp','GREECE-RESEARCHERS.md'],
]){
 if(!countryData[iso]) countryData[iso] = loadStandardCountry(prefix, title, reportFile);
}
// Các nước dạng DSL (và phần bổ sung cho nước có dữ liệu cũ) nạp sau cùng.
if(fs.existsSync('countries')) for(const f of fs.readdirSync('countries').filter(f=>/^[A-Z]{3}\.json$/.test(f))){
 const c=JSON.parse(fs.readFileSync('countries/'+f,'utf8'));
 const base=countryData[c.country];
 if(base){ // bổ sung vào dữ liệu cũ (vd. DEU): gộp thành phố theo id, nối thêm cơ quan
  for(const city of c.cities){const ex=base.cities.find(x=>x.id===city.id);if(ex)ex.institutions.push(...city.institutions);else base.cities.push(city)}
  Object.assign(base.networks=base.networks||{},c.networks||{});
 } else { c.autoView=!c.viewBox; countryData[c.country]=c; }
}
// Link cá nhân: url chỉ dùng cho đúng một người (hoặc được đánh dấu profile:true). Link dùng chung là trang danh sách.
{const people=[];const walk=o=>{if(Array.isArray(o))o.forEach(walk);else if(o&&typeof o==='object'){for(const k of ['people','external'])if(Array.isArray(o[k]))o[k].forEach(p=>{if(p&&p.name&&p.url)people.push(p)});Object.values(o).forEach(walk)}};walk(countryData);
 const n={};people.forEach(p=>n[p.url]=(n[p.url]||0)+1);people.forEach(p=>{if(p.profile===undefined)p.profile=n[p.url]===1});
 const own=people.filter(p=>p.profile).length;console.log('Personal links: '+own+' / '+people.length);}
// Gắn nhóm vai trò cho từng người (k) để giao diện tách người có thể hướng dẫn khỏi nghiên cứu sinh.
{const {roleClass}=require('./tools/roles.cjs');const cnt={};const walk=o=>{if(Array.isArray(o))o.forEach(walk);else if(o&&typeof o==='object'){for(const k of ['people','external'])if(Array.isArray(o[k]))o[k].forEach(p=>{if(p&&p.name){p.k=k==='external'&&roleClass(p.role)!=='student'?'guest':roleClass(p.role);cnt[p.k]=(cnt[p.k]||0)+1}});Object.values(o).forEach(walk)}};walk(countryData);console.log('Roles:',JSON.stringify(cnt));}
const finlandGeometry = JSON.parse(fs.readFileSync('finland-geometry.json','utf8'));
const vietnamIslands = JSON.parse(fs.readFileSync('vietnam-islands.json','utf8'));
// Hoàng Sa & Trường Sa: bộ dữ liệu 110m không có đảo nhỏ, nên thêm ký hiệu (vẽ lớn hơn kích thước thật) vào hình Việt Nam.
const withIslands = (f, radius) => ({...f, geometry:{type:'MultiPolygon', coordinates:[
 ...(f.geometry.type==='Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates),
 ...vietnamIslands.groups.flatMap(g => g.islands.map(i => d3.geoCircle().center(i.coordinates).radius(radius).precision(20)().coordinates))
]}});
let vietnamLabels = [];
const countries = data.features.map(f0 => {
 const isVietnam = f0.properties.ADM0_A3==='VNM';
 const f = isVietnam ? withIslands(f0, 0.4) : f0;
 const name = f.properties.NAME_VI || f.properties.NAME_EN;
 const hiRes = `geometry/${f.properties.ADM0_A3}.json`;
 const detailFeature = f.properties.ADM0_A3==='FIN' ? finlandGeometry : isVietnam ? withIslands(f0, 0.09) : fs.existsSync(hiRes) ? JSON.parse(fs.readFileSync(hiRes,'utf8')) : f;
 const bounds = d3.geoBounds(detailFeature);
 const west = bounds[0][0], east = bounds[1][0];
 const center = (west + (east < west ? east + 360 : east)) / 2;
 const detailProjection = d3.geoNaturalEarth1().rotate([-center,0]).fitExtent([[32,28],[728,432]],detailFeature);
 const detailPath = d3.geoPath(detailProjection)(detailFeature);
 if(isVietnam) vietnamLabels = vietnamIslands.groups.map(g => {
  const pts = g.islands.map(i => detailProjection(i.coordinates));
  return {name:g.name, x:+(pts.reduce((n,p)=>n+p[0],0)/pts.length).toFixed(1), y:+(Math.min(...pts.map(p=>p[1]))-10).toFixed(1)};
 });
 const cd = countryData[f.properties.ADM0_A3];
 if(cd) cd.cities.forEach(city => {city.point=detailProjection(city.coordinates).map(v=>+v.toFixed(1));});
 if(cd && cd.autoView){ // khung nhìn bám sát hình nước + các chấm thành phố
  const [[x0,y0],[x1,y1]]=d3.geoPath(detailProjection).bounds(detailFeature); const pad=20;
  const xs=[x0,x1,...cd.cities.map(c=>c.point[0])], ys=[y0,y1,...cd.cities.map(c=>c.point[1])];
  const L=Math.min(...xs)-pad, T=Math.min(...ys)-pad, W=Math.max(...xs)-L+pad, H=Math.max(...ys)-T+pad;
  if(W/H<1.25) cd.viewBox=[L,T,W,H].map(v=>+v.toFixed(1)).join(' ');
  delete cd.autoView;
 }
 const worldD = path(f); if(!worldD) return ''; const lp = cd ? labelPoint(f) : null;
 return `<path class="country${cd?' has-data':''}" d="${worldD}" data-code="${f.properties.ADM0_A3}" data-detail="${detailPath}" tabindex="0" role="button" aria-label="${esc(name)}" aria-pressed="false" data-name="${esc(name)}"${lp?` data-lp="${lp.join(',')}"`:''}><title>${esc(name)}</title></path>`;
}).join('\n');
const template = fs.readFileSync('template.html','utf8');
for(const [code,cd] of Object.entries(countryData)) if(!cd.cities.every(city => city.point?.every(Number.isFinite))) throw new Error('Missing map coordinates: '+code);
if(process.env.DUMP_DATA) fs.writeFileSync(process.env.DUMP_DATA, JSON.stringify(countryData));
fs.writeFileSync('dist/index.html',template.replace('/* VIETNAM LABELS */',JSON.stringify(vietnamLabels)).replace('/* COUNTRY DATA */',JSON.stringify(countryData).replaceAll('<','\\u003c')).replace('<!-- MAP -->',`<path class="ocean" d="${path({type:'Sphere'})}"/><path class="grid" d="${path(d3.geoGraticule10())}"/>${countries}`));
console.log(`Built ${data.features.length} country/territory shapes.`);
const report=['# Các đơn vị nghiên cứu tại 7 cơ quan ở Phần Lan',`\nKiểm tra nguồn chính thức: ${unitData.checked}. Các mục phân biệt nhóm, phòng nghiên cứu, đài và trung tâm; không phải số nhóm độc lập để cộng gộp.\n`];
for(const city of finland.cities) for(const institution of city.institutions){
 report.push(`## ${institution.name} — ${city.city}\n\n[Cơ cấu](${institution.structureUrl}): ${institution.structure}\n`);
 for(const unit of institution.units){
  report.push(`### [${unit.name}](${unit.url})\n\n${unit.kind}. Trực thuộc: ${unit.parent}.\n\n${unit.topics}\n`);
  if(unit.location) report.push(`Địa điểm: ${unit.location}.\n`);
  if(unit.note) report.push(`${unit.note}\n`);
  if(unit.additionalSources?.length) report.push(`Nguồn bổ sung: ${unit.additionalSources.map((url,i)=>`[${i+1}](${url})`).join(', ')}.\n`);
 }
 if(institution.networks.length)report.push(`Liên kết: ${institution.networks.map(key=>unitData.networks[key].name).join('; ')}.\n`);
}
report.push('## Quan hệ liên đại học\n');
for(const network of Object.values(unitData.networks))report.push(`### [${network.name}](${network.url})\n\n${network.kind}. ${network.topics}\n\n${network.note||''}\n`);
fs.writeFileSync('FINLAND-UNITS.md',report.join('\n'));
console.log(`Included ${Object.values(unitData.institutions).reduce((n,i)=>n+i.units.length,0)} unit records and ${Object.keys(unitData.networks).length} shared networks.`);
const peopleReport=['# Nhà nghiên cứu theo đơn vị tại Phần Lan',`\nNgày kiểm tra nguồn: ${researcherData.checked}.\n`];
for(const [institution,details] of Object.entries(unitData.institutions)){
 peopleReport.push(`## ${institution}\n`);
 for(const unit of details.units){
  const r=researcherData.units[unit.name];
  peopleReport.push(`### ${unit.name}\n`);
  for(const p of r.people||[]) peopleReport.push(`- [${p.name}](${p.url})${p.role?' — '+p.role:''}`);
  if(r.external?.length){peopleReport.push('\nThành viên liên kết / khách mời:\n');for(const p of r.external)peopleReport.push(`- [${p.name}](${p.url})${p.role?' — '+p.role:''}`);}
  if(r.note)peopleReport.push(`\n${r.note}\n`);
  if(r.auditNote)peopleReport.push(`\nĐối chiếu: ${r.auditNote}\n`);
  peopleReport.push(`\nNguồn: ${r.sources.map((url,i)=>`[${i+1}](${url})`).join(', ')}.\n`);
 }
}
fs.writeFileSync('FINLAND-RESEARCHERS.md',peopleReport.join('\n'));
