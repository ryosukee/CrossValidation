#import sys; map(lambda tp: sys.stdout.write(tp[0]+" "+tp[1]+"\n"), sorted(map(lambda tok: (tok.split("----")[0]+tok.split("----")[2], tok.split("----")[1]), set("".join(map(lambda line: "||||" if line.strip()=="" else line.strip().split()[0]+"----"+line.strip().split()[-1][2:]+"----" if line.strip().split()[-1][0]=="B" else line.strip().split()[0]+"----"+line.strip().split()[-2][2:]+"----" if line.strip().split()[-1]=="O" and line.strip().split()[-2][0]=="B" else line.strip().split()[0], open(sys.argv[1]))).split("||||")[:-1])), key=lambda x: x[1]))

import sys

word = list()
l = list()
for line in open(sys.argv[1]):
    if line.strip() == "":
        l.append(("///".join(word), cl))
        word = list()
        continue
    if line.strip().split()[-1][0]=="B":
        cl = line.strip().split()[-1][2:]
        word.append(line.strip().split()[0])
    elif line.strip().split()[-1]=="O" and line.strip().split()[-2][0]=="B":
        word.append(line.strip().split()[0])
        cl = line.strip().split()[-2][2:]
    else:
        word.append(line.strip().split()[0])

for item in sorted(set(l), key=lambda x:x[1]):
    print item[0].replace("///",""), item[1], "\t"+item[0]


