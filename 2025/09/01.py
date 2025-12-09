import numpy as np

with open("data","r") as file:
    data = file.read().split("\n")

# x,y
# ----------- > x
# |
# |
# |
# v
#
# Y
n_cols = 0
n_rows = 0
for i in range(len(data)):
    data[i] = [int(j) for j in data[i].split(",")]
    print(data[i])
    n_cols = max(n_cols, data[i][0])
    n_rows = max(n_rows, data[i][1])
    data[i] = [data[i][1], data[i][0]]
data.sort()

result = 0
for i in data:
    for j in data:
        if i != j:
            area = (abs(i[0]-j[0])+1)*(abs(i[1]-j[1])+1)
            if result < area:
                result = area
                print("New area: ", area, " with corners ", i, j)