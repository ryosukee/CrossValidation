#!/usr/bin/python
#coding:utf-8

# onlyBIの出力結果を10分割にする
import sys

#まず全文数を数える
count = 0
for line in open("./result"):
    count += int(line.strip().split(" ")[0])

per = count / 10

# 分割するファイル群を決める
files = []
count = 0
temp = []
remain = []
for line in open("./result"):
   count += int(line.strip().split(" ")[0])
   temp.append(line.strip().split(" ")[1])
   if count >= per:
       count = 0
       temp = list(set(temp))
       files.append(temp)
       temp = [] 

# 分割する(10を超えてたらbreakして追記)
for i in range(len(files)):
    if i >= 10:
       remain = files[i:]
       break 
    fw = open("../splits/split."+str(i)+".txt", "w")

    print ",".join(files[i]), "->split.", str(i)+".txt"
    for ff in files:
       for f in ff:
            for line in open("./"+f):
                fw.write(line)

i = 0
for ff in remain:
    for f in ff:
        fw = open("../splits/split."+str(i)+".txt", "a")
        print f, "->split.", str(i)+".txt"
        i += 1
        if i>=10:
            i=0
