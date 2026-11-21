#!/usr/bin/env python3
"""Gán link trang cá nhân cho nhà nghiên cứu từ các tệp trong link-sources/.

Định dạng tệp (mỗi tệp một nguồn):
    #inst  <một phần tên cơ quan, có thể nhiều dòng #inst>
    #prefix <tiền tố URL, nối với phần đuôi ở mỗi dòng>
    #slug  (tùy chọn: mỗi dòng là slug kiểu "ten-ho-abc123", tên lấy từ slug)
    Tên người | url-hoặc-đuôi-url
Chỉ thay link của người đang dùng link chung (trang danh sách) trong đúng cơ quan đó.
Dùng: python3 tools/apply_links.py [thư-mục-repo]
"""
import json, re, sys, unicodedata, pathlib
from urllib.parse import unquote
from collections import Counter, defaultdict

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
TITLES = {'prof', 'dr', 'rer', 'nat', 'habil', 'phil', 'ing', 'dipl', 'phys', 'inf', 'msc', 'bsc', 'apl', 'pd', 'priv', 'doz', 'h', 'c', 'univ', 'mr', 'ms', 'frau', 'herr', 'i', 'r'}

def fold(s):
    s = s.lower()
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        s = s.replace(a, b)
    s = unicodedata.normalize('NFKD', s)
    return ''.join(ch for ch in s if not unicodedata.combining(ch))

def tokens(name):
    name = name.strip()
    if ',' in name:                      # "Ho, Ten" -> "Ten Ho"
        last, first = name.split(',', 1)
        name = first + ' ' + last
    t = [x for x in re.split(r'[^a-z0-9]+', fold(name)) if x]
    return [x for x in t if x not in TITLES]

def keys(name):
    t = tokens(name)
    if not t:
        return []
    k = ['full:' + ' '.join(sorted(t)), 'fl:' + t[0] + ' ' + t[-1]]
    k.append('il:' + t[0][0] + ' ' + t[-1])  # chữ cái đầu + họ
    return k

def load_sources():
    out = []
    for f in sorted((root / 'link-sources').glob('*.txt')):
        insts, prefix, suffix, slug, entries = [], '', '', False, []
        for line in f.read_text(encoding='utf8').splitlines():
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            if line.startswith('#inst'):
                insts.append(line[5:].strip())
            elif line.startswith('#prefix'):
                prefix = line[7:].strip()
            elif line.startswith('#suffix'):
                suffix = line[7:].strip()
            elif line.startswith('#slug'):
                slug = True
            elif slug and '|' not in line:
                for s in line.split():
                    nm = re.sub(r'-[0-9a-f]{6,}$', '', unquote(s)).replace('-', ' ')
                    entries.append((nm, prefix + s + suffix))
            else:
                nm, url = [x.strip() for x in line.split('|', 1)]
                entries.append((nm, url if url.startswith('http') else prefix + url))
        out.append((f.name, insts, entries))
    return out

def main():
    R = json.loads((root / 'germany-researchers.json').read_text(encoding='utf8'))
    use = Counter(p.get('url') for r in R['units'].values() for p in r['people'] + r['external'])
    changed = Counter()
    for fname, insts, entries in load_sources():
        idx = defaultdict(set)
        for nm, url in entries:
            for k in keys(nm):
                idx[k].add(url)
        for key, r in R['units'].items():
            inst = key.split('::')[0]
            if not any(i in inst for i in insts):
                continue
            for p in r['people'] + r['external']:
                if use[p.get('url')] <= 1 and not p.get('profile') is False:
                    continue  # đã có link riêng
                for k in keys(p['name']):
                    if k.startswith('il:') and not k[3:].split(' ')[1:]:
                        continue
                    hit = idx.get(k)
                    if hit and len(hit) == 1:
                        url = next(iter(hit))
                        if p.get('url') != url:
                            if p.get('url') and p.get('url') not in r.setdefault('sources', []):
                                r['sources'].append(p['url'])
                            p['url'] = url
                            p['profile'] = True
                            changed[fname] += 1
                        break
    # Dùng lại link cá nhân của cùng một người (trưởng nhóm/giáo sư) đã có ở cơ quan khác
    lead = re.compile(r'giám đốc|trưởng|giáo sư|\bGS\b|\bTN\b|\bGD\b|leader|Prof|Privatdoz|director', re.I)
    use = Counter(p.get('url') for r in R['units'].values() for p in r['people'] + r['external'])
    known = defaultdict(set)
    for r in R['units'].values():
        for p in r['people'] + r['external']:
            if p.get('profile') or use[p.get('url')] == 1:
                known[keys(p['name'])[0] if keys(p['name']) else ''].add(p['url'])
    for r in R['units'].values():
        for p in r['people'] + r['external']:
            if p.get('profile') or use[p.get('url')] <= 1 or not lead.search(p.get('role', '')):
                continue
            k = keys(p['name'])
            hit = known.get(k[0]) if k else None
            if hit and len(hit) == 1:
                old = p.get('url')
                if old and old not in r.setdefault('sources', []):
                    r['sources'].append(old)
                p['url'] = next(iter(hit)); p['profile'] = True; changed['(dùng lại từ cơ quan khác)'] += 1
    (root / 'germany-researchers.json').write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding='utf8')
    for f, n in changed.most_common():
        print(f'{n:4d}  {f}')
    print('total', sum(changed.values()))

if __name__ == '__main__':
    main()
