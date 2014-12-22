import sys
"""
python conll_calc.py [conll_evaled1] [conll_evaled2] ...
"""

#TODO maicro
d = dict()
sumnum = len(sys.argv[1:])
for f in sys.argv[1:]:
    for line in open(f):
        if line.startswith("processed"):
            continue
        spl = line.strip().split(";")
        # all
        if line.startswith("accuracy"):
            acc = float(spl[0].split()[-1].split("%")[0])
            pre = float(spl[1].split()[-1].split("%")[0])
            rec = float(spl[2].split()[-1].split("%")[0])
            f = float(spl[3].split()[-1].split("%")[0])

            d[0] = d.get(0, dict())
            d[0]["Accuracy"] = d[0].get("Accuracy", float()) + acc
            d[0]["Precision"] = d[0].get("Precision", float()) + pre
            d[0]["Recall"] = d[0].get("Recall", float()) + rec
            d[0]["F-value"] = d[0].get("F-value", float()) + f
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
print "Maccro"
print "Accuracy: %5f%%; Precision: %5f%%; Recall: %df%%; F: %5f" % \
        (round(d[0]["Accuracy"]/sumnum,5), round(d[0]["Precision"]/sumnum,5), round(d[0]["Recall"]/sumnum,5), round(d[0]["F-value"]/sumnum,5),)

del d[0]
for name, dd in d.items():
    print "%17s: Precision: %5f%%; Recall: %5f%%; F: %5f" % \
        (name, round(dd["Precision"]/sumnum, 5), round(dd["Recall"]/sumnum, 5), round(dd["F-value"]/sumnum, 5))


