import numpy as np

with open("data test","r") as file:
    data = file.read().split("\n")

for i in range(len(data)):
    data[i] = list(data[i])

scie = set()
for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] == "S":
            scie.add((i,j))
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

result = 0
for i in range(1,len(data)):
    for j in range(len(data[0])):
        if data[i][j] == "^" and data[i-1][j] == "|":
            result += 1
print("Result:", result)