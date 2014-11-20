#!/usr/bin/python
#coding:utf-8
import sys
from collections import defaultdict
import pickle

target_file = sys.argv[1]
class_dict = sys.argv[2]
eval_dump = sys.argv[3]
output_diff = sys.argv[4]

classes = pickle.load(open(class_dict))
tp = defaultdict(int)
fp = defaultdict(int)
tn = defaultdict(int)
fn = defaultdict(int)

Eval = defaultdict(dict)

total = 0
for line in open(target_file):
    if line.strip() != "":
        total += 1
        gold = line.strip().split("\t")[-2]
        sys = line.strip().split("\t")[-1]

        if sys == gold:
            tp[sys] += 1
            open(output_diff+"/"+sys+"tp", "a").write(line)
            for c in classes:
                if c == sys:
                    continue
                tn[c] += 1
                open(output_diff+"/"+c+"tn", "a").write(line)
        else:
            fp[sys] += 1
            fn[gold] += 1
            open(output_diff+"/"+sys+"fp", "a").write(line)
            open(output_diff+"/"+gold+"fn", "a").write(line)
            for c in classes:
                if c == sys or c == gold:
                    continue
                tn[c] += 1
                open(output_diff+"/"+c+"tn", "a").write(line)

print "total:", total
for c in classes:
    print "class:%s,\ttp:%6d,\ttn:%6d,\tfp:%d,\tfn:%d,\tsum:%d" % (c, tp[c], tn[c], fp[c], fn[c], tp[c]+fp[c]+tn[c]+fn[c])

for c in classes:
    print
    print c
    Eval["Ac"][c] = float(tp[c]+tn[c])/total
    try:
        Eval["Pr"][c] = float(tp[c])/(tp[c]+fp[c])
    except ZeroDivisionError:
        Eval["Pr"][c] = .0
    try:
        Eval["Re"][c] = float(tp[c])/(tp[c]+fn[c])
    except ZeroDivisionError:
        Eval["Re"][c] = .0
    print "Accuracy =\t%f" % Eval["Ac"][c]
    print "Precision =\t%f" % Eval["Pr"][c]
    print "Recall =\t%f" % Eval["Re"][c]

Eval["Ac"]["Macro"] = (sum(Eval["Ac"][c] for c in classes)/len(classes))
Eval["Pr"]["Macro"] = (sum(Eval["Pr"][c] for c in classes)/len(classes))
Eval["Re"]["Macro"] = (sum(Eval["Re"][c] for c in classes)/len(classes))
Eval["F"]["Macro"] = 2*Eval["Pr"]["Macro"]*Eval["Re"]["Macro"]/(Eval["Pr"]["Macro"]+Eval["Re"]["Macro"])

Eval["Ac"]["Micro"] = (float(sum((tp[c]+tn[c]) for c in classes))/(total*len(classes)))
Eval["Pr"]["Micro"] = (float(sum(tp[c] for c in classes))/sum(tp[c]+fp[c] for c in classes))
Eval["Re"]["Micro"] = (float(sum(tp[c] for c in classes))/sum(tp[c]+fn[c] for c in classes))
Eval["F"]["Micro"] = 2*Eval["Pr"]["Micro"]*Eval["Re"]["Micro"]/(Eval["Pr"]["Micro"]+Eval["Re"]["Micro"])

print
print "Macro Accuracy = %f" % Eval["Ac"]["Macro"]
print "Macro Precision = %f" % Eval["Pr"]["Macro"]
print "Macro Recall = %f" % Eval["Re"]["Macro"]
print "Macro F-measure = %f" % Eval["F"]["Macro"]
print
print "Micro Accuricy = %f" % Eval["Ac"]["Micro"]
print "Micro Precision = %f" % Eval["Pr"]["Micro"]
print "Micro Recill = %f" % Eval["Re"]["Micro"]
print "Micro F-measure = %f" % Eval["F"]["Micro"]

pickle.dump(dict(Eval), open(eval_dump, "w"))

