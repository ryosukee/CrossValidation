#!/usr/bin/python
#coding:utf-8
import sys

out_dir = sys.argv[2]

open(out_dir+"/fp.txt", "w").write("")
open(out_dir+"/fn.txt", "w").write("")

phrase = str()
for line in open(sys.argv[1]):
    if line.strip() == "":
        try:
            if "fp" in map(lambda l:"fp" if l.split()[-2]=="O" else "x", phrase.strip().split("\n")):
                open(out_dir+"/fp.txt", "a").write(phrase+"\n")
            else:
                open(out_dir+"/fn.txt", "a").write(phrase+"\n")
        except IndexError:
            print "IndexError: pharase>"+phrase+"<"
        phrase = str()
        continue
    phrase += line
