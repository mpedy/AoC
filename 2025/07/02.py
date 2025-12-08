import numpy as np

with open("data","r") as file:
    data = file.read().split("\n")

for i in range(len(data)):
    data[i] = list(data[i])

scie = set()
starting_point = None
for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] == "S":
            scie.add((i,j))
            starting_point = (i,j)
            break
    if len(scie) == 1:
        break

while len(scie) > 0:
    s_index = 0
    while len(scie) > 0:
        try:
            s = list(scie)[s_index]
        except:
            print("Eccezione con s_index=", s_index, scie)
        found = False
        s_index += 1
        for j in range(s[0]+1,len(data)):
            if data[j][s[1]] == ".":
                data[j][s[1]] = "|"
            elif data[j][s[1]] == "|":
                break
            elif data[j][s[1]] == "^":
                scie.remove(s)
                print("From scia ", s, " Creating two new scie: ", (j,s[1]-1), " and ", (j,s[1]+1))
                data[j][s[1]-1] = "|"
                data[j][s[1]+1] = "|"
                scie.add((j,s[1]-1))
                scie.add((j,s[1]+1))
                s_index=0
                found = True
                break
        if not found:
            scie.remove(s)
            s_index = 0
for i in data:
    print("".join(i))

def printdata(data):
    for k in data:
        print("".join(k))

nodes = {}
# j for columns
# i for rows
n_cols = len(data[0])
n_rows = len(data)
k = -1
while k < n_cols-1:
    k += 1
    i = -1
    temp = 1
    while i < n_cols-1:
        i += 1
        j = n_rows-k
        while j > 0:
            #printdata(data)
            j -= 1
            if data[j][i] == "|":
                if j<n_rows-1 and data[j+1][i] == "^":
                    temp = nodes.get((j+1,i),0)
                data[j][i] = " "
                if i-1>=0 and data[j][i-1] == "^":
                    nodes[(j, i-1)] = nodes.get((j,i-1),0) + temp
                if i+1<n_cols-1 and data[j][i+1] == "^":
                    nodes[(j, i+1)] = nodes.get((j,i+1),0) + temp
            elif data[j][i] == "^" or data[j][i] == "." or data[j][i] == "S":
                if data[j][i] == "S":
                    nodes[(j, i)] = nodes.get((j,i),0) + temp
                j = - 1
                break
print("Nodes:", nodes)
print("Starting point:", starting_point)
print("Result: ", nodes[starting_point])