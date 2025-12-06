import numpy as np

with open("data","r") as file:
    data = file.read().split("\n")


ranges = []
products = []

for i in data:
    if "-" in i:
        ranges.append([int(j) for j in i.split("-")])
    else:
        if len(i)>0:
            products.append(int(i))

#new_ranges = []
def arrange_ranges(ranges):
    print("Prima: ", len(ranges))
    i=-1
    while i < len(ranges)-1:
        i += 1
        #print("Durante iterazione ",i, ": ", len(ranges))
        r = ranges[i]
        j=i
        while j < len(ranges)-1:
            j += 1
            #print("Durante iterazione ",i," e ",j, ": ", len(ranges))
            if j != i:
                try:
                    w = ranges[j]
                except Exception:
                    print("Errore: ",i,j,len(ranges))
                # disjoint cases
                #if r[0] > w[1]+1 or r[1]+1 < w[0]:
                if r[0] > w[1] or r[1] < w[0]:
                    continue
                # overlapping cases
                if r[0] >= w[0] and r[1]>= w[1]:
                    r[0] = w[0]
                    del ranges[j]
                    j = i
                    continue
                if r[0]<=w[0] and r[1]<= w[1]:
                    r[1] = w[1]
                    del ranges[j]
                    j = i
                    continue
                # contained case
                if r[0]<=w[0] and r[1]>=w[1]:
                    del ranges[j]
                    j-=1
                    continue
                if r[0]>=w[0] and r[1]<=w[1]:
                    r[0] = w[0]
                    r[1] = w[1]
                    del ranges[j]
                    j=-1
                    continue
        #new_ranges.append(r)
    print("Dopo: ", len(ranges))
    return ranges
#ranges = sorted(ranges)
ranges = arrange_ranges(ranges)
ranges = arrange_ranges(ranges)
ranges=  sorted(ranges)




result = 0

for r in ranges:
    print(f"{r[0]} - {r[1]}")
    result += (r[1]-r[0]+1)

print(result)