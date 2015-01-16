import sys
"""
python conll_calc.py [conll_evaled1] [conll_evaled2] ...
"""

d = dict()
sumnum = len(sys.argv[1:])
for f in sys.argv[1:]:
    for line in open(f):
        spl = line.strip().split(";")
        # all
        if line.startswith("accuracy"):
            acc = float(spl[0].split()[-1].split("%")[0])
            pre = float(spl[1].split()[-1].split("%")[0])
            rec = float(spl[2].split()[-1].split("%")[0])
            f = float(spl[3].split()[-1].split("%")[0])
            tc = int(correct*100/pre)


            d[0] = d.get(0, dict())
            d[0]["Accuracy"] = d[0].get("Accuracy", float()) + acc
            d[0]["Precision"] = d[0].get("Precision", float()) + pre
            d[0]["Recall"] = d[0].get("Recall", float()) + rec
            d[0]["F-value"] = d[0].get("F-value", float()) + f
            d[0]["Total_Correct"] = d[0].get("Total_Correct", int()) + tc
            continue
        elif line.startswith("processed"):
            total = int(spl[1].split()[-2])
            correct = int(spl[-1].split()[-1][:-1])
            d[0]["Total"] = d[0].get("Total", int()) + total
            d[0]["Correct"] = d[0].get("Correct", int()) + correct
            continue
        # each 
        else:
            name = line.split(":")[0].split()[-1]
            spl = filter(lambda x: len(x)!=0, line.strip().split())
            pre = float(spl[2].split("%")[0])
            rec = float(spl[4].split("%")[0])
            f = float(spl[6].split("%")[0])

            d[name] = d.get(name, dict())
            d[name]["Precision"] = d[name].get("Precision", float()) + pre
            d[name]["Recall"] = d[name].get("Recall", float()) + rec
            d[name]["F-value"] = d[name].get("F-value", float()) + f

# outputs
ac = ("%.2f" % (d[0]["Accuracy"]/sumnum)).rjust(6)
pr = ("%.2f" % (d[0]["Precision"]/sumnum)).rjust(6)
re = ("%.2f" % (d[0]["Recall"]/sumnum)).rjust(6)
f =  ("%.2f" % (d[0]["F-value"]/sumnum)).rjust(6)
print "Average"
print "Accuracy: %s%%; Precision: %s%%; Recall: %s%%; F: %s" % (ac, pr, re, f)

del d[0]
for name, dd in d.items():
    pr = ("%.2f" % (dd["Precision"]/sumnum)).rjust(6)
    re = ("%.2f" % (dd["Recall"]/sumnum)).rjust(6)
    f = ("%.2f" % (dd["F-value"]/sumnum)).rjust(6)
    print "%17s: Precision: %s%%; Recall: %s%%; F: %s" % (name, pr, re, f)


