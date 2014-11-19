#!/usr/bin/python
#coding:utf-8
# ラベルをリストにしてdumpする

import sys
import pickle

files = sys.argv[1:]
l = []
append = l.append
for f in files:
    for line in open(f):
        if line.strip() == "":
            continue
        append(line.strip().split(" ")[-1])

l = list(set(l))
pickle.dump(l, open("./dumps/class_list.pkl", "w"))

