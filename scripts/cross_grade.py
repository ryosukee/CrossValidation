#!/usr/bin/python
#coding:utf-8
import sys
import pickle
from collections import defaultdict

dump_files = sys.argv[1:]
cross_num = len(dump_files)

Eval = defaultdict(dict)
evals = list()
for dump_file in dump_files:
    evals.append(pickle.load(open(dump_file)))

# 平均の計算
for key in evals[0].keys():
    if key != "F":
        for c in evals[0]["Ac"].keys():
            Eval[key][c] = sum(e[key][c] for e in evals)/cross_num
    else:
        for c in evals[0]["F"].keys():
            Eval[key][c] = sum(e[key][c] for e in evals)/cross_num


print "Cross validation Evaluations"
for c in evals[0]["Ac"].keys():
    if c == "Macro" or c == "Micro":
        continue
    print c
    print "Acuracy = %f" % Eval["Ac"][c]
    print "Precision = %f" % Eval["Pr"][c]
    print "Recall = %f" % Eval["Re"][c]
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

