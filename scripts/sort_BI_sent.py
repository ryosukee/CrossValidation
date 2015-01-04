import sys
"""
d[cat] = [(count, surface),...]
"""

d =dict()
for line in open(sys.argv[1]):
    sp = line.strip().split(" ")
    d[sp[2]] = d.get(sp[2], list())
    d[sp[2]].append((int(sp[0]), sp[1]))


for cat in d.keys():
    print cat
    for count, surface in sorted(d[cat], key=lambda x:-x[0]):
        print count, surface
    print

