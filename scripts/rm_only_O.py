import sys
"""
python rm_only_O.py [train.txt]
"""

flag = False
sent = str()
for line in open(sys.argv[1]):
    sent += line
    if line.strip() != "" and line.strip().split()[-1] != "O":
        flag = True
    if line.strip() == "":
        if flag:
            print sent
        flag = False
        sent = str()


