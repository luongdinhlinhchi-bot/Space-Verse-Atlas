"""Gắn #unit (danh sách người theo nhóm vai trò) vào một @inst trong file DSL.
add(path, inst_prefix, unit, topics, url, srcs, groups:{role:[names]}, coverage='full', scope=None, ext:{role:[names]}=None)"""
def add(path,inst_prefix,unit,topics,url,srcs,groups,coverage='full',scope=None,ext=None):
    L=open(path,encoding='utf8').read().split('\n')
    start=[i for i,l in enumerate(L) if l.startswith('@inst '+inst_prefix)]
    assert len(start)==1,(inst_prefix,start)
    s=start[0]; e=s+1
    while e<len(L) and not L[e].startswith('@inst ') and not L[e].startswith('@city '): e+=1
    for i in range(s,e):
        if L[i].startswith('coverage:'): L[i]='coverage: '+coverage
        if L[i].startswith('scope:') and scope: L[i]='scope: '+scope
    block=['',f'#unit {unit}',f'parent: {inst_prefix.split(" — ")[0]}',f'topics: {topics}',f'url: {url}']+[f'src: {x}' for x in srcs]
    for r,ns in groups.items():
        ns=[n.strip() for n in ns if n.strip()]
        if ns: block.append(f'pp: {r} | '+'; '.join(ns))
    for r,ns in (ext or {}).items():
        ns=[n.strip() for n in ns if n.strip()]
        if ns: block.append(f'xx: {r} | '+'; '.join(ns))
    while e>s and L[e-1].strip()=='': e-=1
    L[e:e]=block
    open(path,'w',encoding='utf8').write('\n'.join(L))
def sp(s): return [x.strip() for x in s.replace('\n',';').split(';') if x.strip()]
