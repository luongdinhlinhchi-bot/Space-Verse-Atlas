import re
ROLE={'Permanent':'Nhân sự biên chế (nhà nghiên cứu / kỹ sư)','Doctorant':'NCS','Post-Doctorant':'PD','CDD':'Hợp đồng có thời hạn (CDD)','Emerite':'Danh dự (émérite)','Apprenti':'Học việc'}
def cap(w):
    return '-'.join(p[:1].upper()+p[1:].lower() for p in w.split('-'))
def flip(s):
    """'DE LA TORRE Sylvain' -> 'Sylvain de la Torre'"""
    w=s.split()
    i=0
    while i<len(w) and w[i].upper()==w[i] and any(c.isalpha() for c in w[i]): i+=1
    last=w[:i]; first=w[i:]
    if not first: return ' '.join(cap(x) for x in w)
    parts=[]
    for k,x in enumerate(last):
        if x in('DE','DU','DES','LA','LE','VAN','VON','DER','DI','DA') and k<len(last)-1: parts.append(x.lower() if x not in('LE','LA') or k>0 else x.capitalize())
        else: parts.append(cap(x))
    first=' '.join(cap(f) if f[0].islower() is False and '-' in f else f for f in first)
    first=re.sub(r'-([a-zà-ÿ])',lambda m:'-'+m.group(1).upper(),first)
    return first+' '+' '.join(parts)
def group(items):
    from collections import OrderedDict
    g=OrderedDict()
    for it in items:
        t,n=it.split(':',1);g.setdefault(ROLE.get(t,t),[]).append(flip(n))
    return g
