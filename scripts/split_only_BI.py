#!/usr/bin/python
#coding:utf-8

# onlyBIの出力結果を10分割にする

#まず全文数を数える
count = 0
for line in open("./result.txt"):
    count += int(line.strip().split(" ")[0])


# 10で割ると割り切れずに9分割とかになったりするから
# 先に細かく割っとく, 後で分割するときに2周して追記する
per = count / 20

# 分割するファイル群を決める
files = []
count = 0
temp = []
remain = []
for line in open("./result.txt"):
   count += int(line.strip().split(" ")[0])
   temp.append(line.strip().split(" ")[1])
   if count >= per:
       count = 0
       temp = list(set(temp))
       files.append(temp)
       temp = [] 

# 分割する(10を超えてたらbreakして追記)
i = 0
for ff in files:
    if i >= 10:
       remain = files[i:]
       break 
    fw = open("../splits/split."+str(i)+".txt", "w")

    print ",".join(files[i]), "->split.", str(i)+".txt"
    for f in ff:
         for line in open("./"+f):
             fw.write(line)
    fw.close()
    i += 1

i = 0
for ff in remain:
    for f in ff:
        fw = open("../splits/split."+str(i)+".txt", "a")
        print f, "->split.", str(i)+".txt"
        for line in open("./"+f):
            fw.write(line)
        fw.close()
        i += 1
        if i>=10:
            i=0

# othersを分割して追記
i = 0
print "others"
fw = open("../splits/split."+str(i)+".txt", "a")
for line in open("./others"):
    fw.write(line)
    if line.strip() == "":
        fw.close()
        i += 1
        if i>=10:
            i=0
        fw = open("../splits/split."+str(i)+".txt", "a")
fw.close()

