from z3 import *

try:
    with open("2024/24/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()

data = data.split("\n\n")
data[0] = data[0].split("\n")
data[1] = data[1].split("\n")

variables = {}
s = Solver()

for i in range(len(data[0])):
    row = data[0][i].split(": ")
    variables[row[0]] = BitVec(row[0],1)
    s.add(variables[row[0]] == int(row[1]))

for i in range(len(data[1])):
    row = data[1][i].split(" -> ")
    row[0] = row[0].split(" ")
    a,op,b = row[0][0], row[0][1], row[0][2]
    if row[1] not in variables.keys():
        variables[row[1]] = BitVec(row[1],1)
    if a not in variables.keys():
        variables[a] = BitVec(a,1)
    if b not in variables.keys():
        variables[b] = BitVec(b,1)
    if op == "XOR":
        s.add(variables[row[1]] == (variables[a] ^ variables[b]))
    elif op == "OR":
        s.add(variables[row[1]] == (variables[a] | variables[b]))
    elif op == "AND":
        s.add(variables[row[1]] == (variables[a] & variables[b]))

if s.check() == sat:
    max_z = 0
    print(s.model())
    for k in s.model():
        if str(k).startswith("z"):
            max_z = max(max_z, int(str(k)[1:]))
            print(k, s.model()[k])
    print("Max Z: ", max_z)
    result = []
    for i in range(max_z+1):
        print(f"z_{i} = ",s.model()[variables[f"z{i:02}"]])
        result.append(s.model()[variables[f"z{i:02}"]])
    print(int("0b" + "".join([str(i) for i in result[::-1]]),2))