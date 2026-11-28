"""Gán lại chức danh cho người trong một #unit của file DSL dựa trên danh sách theo nhóm từ nguồn.
apply(path, unit_prefix, groups={role:[names]}, src=url, leftover='...')"""
import unicodedata,re
def norm(n):
    n=unicodedata.normalize('NFKD',n).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z ]',' ',n).split()
def key(n):
    w=norm(n); return ' '.join(w)
def match(name,idx):
    k=key(name)
    if k in idx: return idx[k]
    w=norm(name)
    for kk,r in idx.items():
        ww=kk.split()
        if not w or not ww: continue
        # same last token and first initial, or one name's tokens subset of other
        if (w[-1]==ww[-1] and w[0][0]==ww[0][0]) or (set(w)<=set(ww) and len(w)>=2) or (set(ww)<=set(w) and len(ww)>=2): return r
        if w[0]==ww[-1] and w[-1]==ww[0]: return r  # reversed order
    return None
def apply(path,unit_prefix,groups,src=None,leftover='Thành viên (trang không ghi chức danh)',only_roles=None):
    idx={}
    for role,names in groups.items():
        for n in names: idx[key(n)]=role
    L=open(path,encoding='utf8').read().split('\n')
    out=[];inside=False;stats={'matched':0,'left':0};added_src=False
    for l in L:
        if l.startswith('#unit ') or l.startswith('@inst '):
            inside=l.startswith('#unit '+unit_prefix)
        if inside and l.startswith('src:') and src and not added_src:
            out.append(l); out.append('src: '+src); added_src=True; continue
        if inside and l.startswith('p: '):
            parts=[x.strip() for x in l[3:].split('|')]
            if only_roles is None or parts[1] in only_roles:
                r=match(parts[0],idx)
                if r: parts[1]=r; stats['matched']+=1
                elif only_roles is not None: parts[1]=leftover; stats['left']+=1
            out.append('p: '+' | '.join(parts)); continue
        if inside and l.startswith('pp: '):
            role,names=l[4:].split('|',1); role=role.strip()
            if only_roles is None or role in only_roles:
                buckets={}
                for n in [x.strip() for x in names.split(';') if x.strip()]:
                    r=match(n,idx)
                    if r: stats['matched']+=1
                    else: r=leftover if only_roles is not None else role; stats['left']+=1
                    buckets.setdefault(r,[]).append(n)
                for r,ns in buckets.items(): out.append('pp: '+r+' | '+'; '.join(ns))
                continue
        out.append(l)
    open(path,'w',encoding='utf8').write('\n'.join(out))
    return stats
