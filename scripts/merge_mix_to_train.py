#coding:utf-8
import sys
"""
mixに対してラベルを直して処理するだけ
python merge_mix_to_train.py [splits_dir] [train_dir] [splits_info.txt] [n]
"""

pare_list = list()
max_i = int(sys.argv[4])
for line in open(sys.argv[3]):
    spl = line.strip().split(" ")
    if line.strip() == "":
        # ここで処理
        fw_train = open(sys.argv[2]+"/train."+str(i)+".txt", "a")
        for j in range(max_i):
            if j == i:
                continue
            
            sent = list()
            pre_label = "O"
            ii = 0
            for l in open(sys.argv[1]+"/split_mix."+str(j)+".txt"):
                if l.strip() == "":
                    # ここで書き換えて書き込む
                    for si, ei, su in info:
                        if su in (s for s,c in pare_list):
                            for ind in range(si, ei+1):
                                sent[ind][-1] = "O"
                    if not all(tok[-1] == "O" for tok in sent):
                        for lll in sent:
                            fw_train.write(" ".join(lll))
                        fw_train.write("")
                    ii = 0
                    sent = list()
                    pre_label = "O"
                else:
                    # ラベルのついた箇所のindexとsurfaceをとっておく
                    spl = l.strip().split(" ")
                    sent.append(spl)
                    label = spl[-1]
                    if label == "O":
                        if pre_label == "B" or pre_label == "I":
                             endi = ii-1
                             info.append((starti, endi, surface))
                    else:
                        label = spl[-1].split("-")[0]
                        if pre_label == "O":
                            starti = ii
                            surface = spl[0]
                        elif label == "B":
                            endi = ii-1
                            info.append((starti, endi, surface))
                            starti = ii
                            surface = spl[0]
                        else:
                            surface += spl[0]
                    ii += 1
                             
        pare_list = list()
    elif len(spl) == 1:
        i = int(spl[0])
    else:
        pare_list.append((spl[1].split(".txt")[0], spl[2]))

