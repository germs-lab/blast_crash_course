import sys

# Usage: 

d = {}

with open(sys.argv[1], "r") as reader:
    for record in reader:
        record = record.strip()
        if len(record) != 0 and record[0] == ">":
            dat = record.split(' ', 1)
            id1 = dat[0][1:]
            id2 = dat[1]
            d[id1] = id2


for n, line in enumerate(open(sys.argv[2], "r")):
    dat = line.strip().split('\t')
    #print(dat)
    if n > 0:
        ann = d[dat[0]]
        dat.insert(1, ann)
    else:
        dat.insert(0, "Gene ID")
        dat.insert(1, "Gene Annotation")
    print('\t'.join(dat))

