import sys

phrase=str()
Bflag = False
for line in open(sys.argv[1]):
    if line.strip()=="":
        continue
    gol = line.strip().split()[-2]
    sys = line.strip().split()[-1]
    
    if gol[0] == "B" and sys[0] == "B" and not Bflag:
        Bflag = True
        phrase+=line
    elif gol[0] == "I" and sys[0] == "I" and Bflag:
        phrase+=line
    elif gol[0] == "B" and sys[0] == "B":
        print phrase
        phrase = line
    else:
        Bflag = False
        if phrase:
            print phrase
            phrase=str()
