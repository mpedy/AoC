import numpy as np

with open("data","r") as file:
    data = file.read().split("\n")

i=-1
while i < len(data)-1:
    i+=1
    data[i] = data[i].strip().split(" ")
    j=-1
    while j < len(data[i])-1:
        j+=1
        if len(data[i][j])==0:
            del data[i][j]
            j -= 1

data = np.array(data).T

result = 0
for i in range(len(data)):
    operation = lambda x,y: x+y if data[i][-1]=="+" else x*y
    base = int(data[i][0])
    for p in range(1,len(data[i])-1):
        base = operation(base, int(data[i][p]))
    print(data[i], base)
    result = result + base

print(result)