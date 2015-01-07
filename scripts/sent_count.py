import sys

count = 0
continuity_flag = False
files = sys.argv[1:]

for f in files:
    for line in open(f):
        if line.strip() == "":
            if not continuity_flag:
                count += 1
            continuity_flag = True
            continue
        continuity_flag = False

print count

