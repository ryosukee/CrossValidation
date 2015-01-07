import sys
"""
python tune_best_f.py [conlleval_file] [conlleval_file] ...
"""

files = sys.argv[1:]
maxf = 0.0
bestf = 3
bestc = 3
for fi in files:
    for line in open(fi):
        if line.startswith("accuracy:"):
            spl = filter(lambda x: x!="", line.strip().split(" "))
            f = float(spl[-1])
            if f > maxf:
                bestf = int(fi.split(".")[1])
                bestc = int(fi.split(".")[2])
                maxf = f
            break
        else:
            continue
print "f:%d c:%d bestF:%f" % (bestf, bestc, maxf)

