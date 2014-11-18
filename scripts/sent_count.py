import sys
count = 0
for line in open(sys.argv[1]):
    if line.strip() == "":
        count += 1
print count

