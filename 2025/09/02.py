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

def check_all_green(corner_a, corner_b):
    print("Checking corners: ", corner_a, corner_b)
    xr = range(corner_b[0], corner_a[0]+1) if corner_a[0] > corner_b[0] else range(corner_a[0], corner_b[0]+1)
    yr = range(corner_b[1], corner_a[1]+1) if corner_a[1] > corner_b[1] else range(corner_a[1], corner_b[1]+1)
    y_min, y_max = min(corner_a[0], corner_b[0]), max(corner_a[0], corner_b[0])
    x_min, x_max = min(corner_a[1], corner_b[1]), max(corner_a[1], corner_b[1])
    #   angle_1 ---- angle_2
    #   |              |
    #   |              |
    #   |              |
    #   angle_3 ---- angle_4
    angle_1, angle_2, angle_3, angle_4 = [y_min, x_min], [y_min,x_max], [y_max, x_min], [y_max, x_max]
    found_1, found_2, found_3, found_4 = angle_1 in data, angle_2 in data, angle_3 in data, angle_4 in data
    if found_1:
        idx_1 = list(filter(lambda x: x[0]==y_min, data)).index(angle_1)
        if idx_1 % 2 != 0:
            print("E' False")
            return False
        if found_2:
            idx_2 = list(filter(lambda x: x[0]==y_min, data)).index(angle_2)
            if idx_2 != idx_1 + 1:
                print("E' False")
                return False
    else:
        if found_2:
            idx_2 = list(filter(lambda x: x[0]==y_min, data)).index(angle_2)
            if idx_2 % 2 != 0:
                print("E' False")
                return False
    if found_2:
        idx_2 = list(filter(lambda x: x[0]==y_min, data)).index(angle_2)
        if (idx_2 % 2 != 1 if not found_1 else idx_2 != idx_1 + 1 ):
            print("E' False")
            return False

    matrix = np.zeros((y_max-y_min+1, x_max-x_min+1), dtype=int)
    # 0 null
    # 1 green
    # 2 red
    for i in range(y_min, y_max+1):
        for j in range(x_min, x_max+1):
            if [i,j] in data:
                matrix[i - y_min, j - x_min] = 2
    print(matrix)
    a=-1
    for i in range(0, y_max+1):
        is_green = False
        for j in range(0, x_max+1):
            if [i,j] in data or (i>=y_min and j >= x_min and matrix[i-y_min, j-x_min] == 2):
                is_green = not is_green
            if i>=y_min and j >= x_min and matrix[i - y_min, j - x_min] != 2:
                matrix[i-y_min, j-x_min] = 1 if is_green else 0
    print(matrix)
    if np.any(matrix == 0):
        print("E' False")
        return False
    print("E' True")
    return True

result = 0
for i in data:
    for j in data:
        if i != j:
            area = (abs(i[0]-j[0])+1)*(abs(i[1]-j[1])+1)
            if result < area and check_all_green(i, j):
                result = area
                print("New area: ", area, " with corners ", i, j)