import sys
d =dict()
for line in open(sys.argv[1]):
    sp = line.strip().split(" ")
    d[sp[2]] = d.get(sp[2], list())
    d[sp[2]].append((int(sp[0]), sp[1]))

for key in d.keys():
    d[key] = sorted(d[key], key=lambda x:-x[0])

for i in range(0, max([len(x) for x in d.values()])):
    for key in d.keys():
        if len(d[key]) <= i:
            continue
        print d[key][i][0], d[key][i][1], key
    
