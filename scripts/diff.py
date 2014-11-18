import sys

phrase = str()
gBIflag = False
sBIflag = False
catchFlag = False

for line in open(sys.argv[1]):
    if line.strip() == "":
        phrase = str()
        continue
    sys = line.strip().split()[-1]
    gold = line.strip().split()[-2]
    
    if gold != "O":
        gBIflag = True
    if sys != "O":
        sBIflag = True
    if gold == "O":
        gBIflag = False
    if sys == "O":
        sBIflag = False
    
    if gold != sys:
        catchFlag = True
    
    if not gBIflag and not sBIflag:
        if catchFlag:
            print phrase
            catchFlag = False
        phrase = str()
        continue
    
    phrase += line
    
