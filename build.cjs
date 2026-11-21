const fs = require('fs');
const d3 = require('./d3.cjs');
const data = JSON.parse(fs.readFileSync('countries.geojson','utf8'));
const projection = d3.geoNaturalEarth1().fitExtent([[25,20],[1175,610]],data);
const path = d3.geoPath(projection);
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
// Link cá nhân: url chỉ dùng cho đúng một người (hoặc được đánh dấu profile:true). Link dùng chung là trang danh sách.
{const people=[];const walk=o=>{if(Array.isArray(o))o.forEach(walk);else if(o&&typeof o==='object'){for(const k of ['people','external'])if(Array.isArray(o[k]))o[k].forEach(p=>{if(p&&p.name&&p.url)people.push(p)});Object.values(o).forEach(walk)}};walk(countryData);
 const n={};people.forEach(p=>n[p.url]=(n[p.url]||0)+1);people.forEach(p=>{if(p.profile===undefined)p.profile=n[p.url]===1});
 const own=people.filter(p=>p.profile).length;console.log('Personal links: '+own+' / '+people.length);}
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
 const detailFeature = f.properties.ADM0_A3==='FIN' ? finlandGeometry : isVietnam ? withIslands(f0, 0.09) : f;
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
 return `<path class="country${cd?' has-data':''}" d="${path(f)}" data-code="${f.properties.ADM0_A3}" data-detail="${detailPath}" tabindex="0" role="button" aria-label="${esc(name)}" aria-pressed="false" data-name="${esc(name)}"><title>${esc(name)}</title></path>`;
}).join('\n');
const template = fs.readFileSync('template.html','utf8');
for(const [code,cd] of Object.entries(countryData)) if(!cd.cities.every(city => city.point?.every(Number.isFinite))) throw new Error('Missing map coordinates: '+code);
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
