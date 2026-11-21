"""Convert 'TAG|Name|url' lines to DSL p: lines. Usage: raw2dsl.py file TAG=role ..."""
import sys
roles = dict(a.split("=", 1) for a in sys.argv[2:])
for line in open(sys.argv[1], encoding="utf8"):
    line = line.strip()
    if not line: continue
    tag, name, url = [s.strip() for s in line.split("|", 2)]
    if tag not in roles: continue
    print(f"p: {name} | {roles[tag]} | {url}")
