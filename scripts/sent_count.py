import sys

count = 0
continuity_flag = False
for line in open(sys.argv[1]):
    if line.strip() == "":
        if not continuity_flag:
            count += 1
        continuity_flag = True
        continue
    continuity_flag = False

print count

