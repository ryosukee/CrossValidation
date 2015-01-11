#!/usr/bin/python
#coding:utf-8
import sys

"""
onlyBIの出力結果をn分割にする
python split_only_BI.py [result.txt] [mix_file] [others] [n] [split_dir]
"""

def min_bin_index():
    minC, index = bins[0], 0
    for i, c in enumerate(bins):
        if c < minC:
            minC = c
            index = i
    return index
       

# ビンの数, 出力ファイルを初期化
split_info = list()
bins = list()
outputs = list()
outputs_mix = list()
outputs_other = list()
for i in range(int(sys.argv[4])):
    bins.append(int())
    split_info.append(list())
    outputs.append(open(sys.argv[5]+"/split."+str(i)+".txt", "w"))
    outputs_mix.append(open(sys.argv[5]+"/split_mix."+str(i)+".txt", "w"))
    outputs_other.append(open(sys.argv[5]+"/split_other."+str(i)+".txt", "w"))


# カテゴリ毎にビンに振り分ける
for line in open(sys.argv[1]):
    spl = line.strip().split(" ")
    if line.strip() == "":
        continue
    if len(spl) == 1:
        cat = spl[0]
        continue
    index = min_bin_index()
    bins[index] += int(spl[0])
    split_info[index].append((spl[0], spl[1], cat))
    for l in open(spl[1]):
        outputs[index].write(l) 


# ここからmixの処理
sent = str()
info = list()
pre_label = "O"
sent_index = 0
for line in open(sys.argv[2]):
    sent += line
    if line.strip() == "":
        for inf in info:
            temp_tupl = filter(lambda x: x[1] == inf[0] and x[2] == inf[1], split_info[sent_index])
            if not temp_tupl:
                split_info[sent_index].append((1, inf[0], inf[1]))
            else:
                split_info[sent_index].remove(temp_tuple)
                split_info[sent_index].append(temp_tuple[0]+1, temp_tuple[1], temp_tuple[2])
        outputs_mix[sent_index].write(sent)
        sent_index += 1
        if sent_index == int(sys.argv[4]):
            sent_index = 0
        sent = str() 
    else:
        spl = line.strip().split(" ")
        label = spl[-1]
        if label == "O":
            if pre_label == "B" or pre_label == "I":
                info.append((temp_surface, temp_cat))
            pre_label = "O"
            continue
        else:
            label = spl[-1].split("-")[0]
            if pre_label == "O":
                temp_surface = spl[0]
                temp_cat = spl[-1].split("-")[1]
            elif pre_label == "B" and label == "B":
                info.append((temp_cat, temp_surface))
                temp_surface = spl[0]
                temp_cat = spl[-1].split("-")[1]
            else:
                temp_surface += spl[0]
            pre_label = label


# otherの分割
i = 0
for line in open(sys.argv[3]):
    outputs_other[i].write(line)
    if line.strip() == "":
        i += 1
        if i == int(sys.argv[4]):
            i=0
               
                
# 出力
for i, info in enumerate(split_info):
    print i
    for c, surface, cat in info:
        print c, surface, cat
    print


## 分割するファイル群を決める
#files = []
#count = 0
#temp = []
#remain = []
#for line in open("./result.txt"):
#   count += int(line.strip().split(" ")[0])
#   temp.append(line.strip().split(" ")[1])
#   if count >= per:
#       count = 0
#       temp = list(set(temp))
#       files.append(temp)
#       temp = [] 
#
## 分割する(10を超えてたらbreakして追記)
#i = 0
#for ff in files:
#    if i >= 10:
#       remain = files[i:]
#       break 
#    fw = open("../splits/split."+str(i)+".txt", "w")
#
#    print ",".join(files[i]), "->split.", str(i)+".txt"
#    for f in ff:
#         for line in open("./"+f):
#             fw.write(line)
#    fw.close()
#    i += 1
#
#i = 0
#for ff in remain:
#    for f in ff:
#        fw = open("../splits/split."+str(i)+".txt", "a")
#        print f, "->split.", str(i)+".txt"
#        for line in open("./"+f):
#            fw.write(line)
#        fw.close()
#        i += 1
#        if i>=10:
#            i=0
#
## othersを分割して追記
#i = 0
#print "others"
#fw = open("../splits/split."+str(i)+".txt", "a")
#for line in open("./others"):
#    fw.write(line)
#    if line.strip() == "":
#        fw.close()
#        i += 1
#        if i>=10:
#            i=0
#        fw = open("../splits/split."+str(i)+".txt", "a")
#fw.close()
#
