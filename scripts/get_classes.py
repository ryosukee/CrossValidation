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

pickle.dump(l, "class_list.pkl")

