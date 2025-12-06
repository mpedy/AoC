import numpy as np

with open("data","r") as file:
    data = file.read().split("\n")

result = 0
banks = []
i = len(data[0])
while i>0:
    i -= 1
    bank = []
    j=-1
    #print(i)
    collected = False
    with_data = False
    while j < len(data)-1:
        j+=1
        if data[j][i]!=" ":
            try:
                bank.append(int(data[j][i]))
                with_data = True
            except ValueError:
                banks.append(bank)
                collected = True
                banks.append(data[j][i])
    if not collected:
        if with_data:
            banks.append(bank)
banks = banks[::-1]
print(banks)

result = 0
operation = None
operations = {
    "+": lambda x,y: x+y,
    "*": lambda x,y: x*y
}
result = 0
base = 0
for b in banks:
    if b[0]=="+" or b[0] == "*":
        operation = operations[b[0]]
        result += base
        base = None
    else:
        if base is None:
            base = int("".join([str(x) for x in b]))
        else:
            base = operation(base, int("".join([str(x) for x in b])))
result += base
print("Final result: ", result)