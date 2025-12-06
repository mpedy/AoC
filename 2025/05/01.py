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

results = []

for p in products:
    fresh = False
    for r in ranges:
        if (p>=r[0] and p<=r[1]):
            fresh = True
            results.append(p)
            break
    #print("Product ", p , " is Fresh? ", fresh)

print("Result: ", len(results))
