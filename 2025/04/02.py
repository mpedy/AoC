import numpy as np

with open("data","r") as file:
    data = file.read().split("\n")

matrix = []

for line in data:
    row = [0 if x == "." else 1 for x in list(line)]
    matrix.append(row)

matrix = np.array(matrix)
kernel = np.array([[1,1,1],[1,1,1],[1,1,1]])

def convolve2d(matrix, kernel):
    m, n = matrix.shape
    km, kn = kernel.shape
    pad_m, pad_n = km // 2, kn // 2
    padded_matrix = np.pad(matrix, ((pad_m, pad_m), (pad_n, pad_n)), mode='constant', constant_values=0)
    convolved = np.zeros_like(matrix)
    can_remove = True
    removed = []
    convolved = matrix.copy()
    while can_remove:
        matrix = convolved
        for i in range(m):
            for j in range(n):
                region = padded_matrix[i:i+km, j:j+kn]
                if matrix[i,j] == 0:
                    convolved[i,j] = 0
                else:
                    if np.sum(region * kernel)<4+1:
                        convolved[i, j] = 2
        to_remove = np.sum(convolved == 2)
        print(str(convolved).replace('0', '.').replace('1', '@').replace("2","x").replace('[', ' ').replace(']', ''))
        print("result: ", np.sum(convolved == 2))
        if to_remove >0:
            removed.append(to_remove)
            can_remove = True
            convolved[convolved == 2] =0
            print("After removed: \n", str(convolved).replace('0', '.').replace('1', '@').replace("2","x").replace('[', ' ').replace(']', ''))
            padded_matrix = np.pad(convolved, ((pad_m, pad_m), (pad_n, pad_n)), mode='constant', constant_values=0)

        else:
            can_remove = False
    return convolved, removed

o_matrix = matrix.copy()
matrix, removed = convolve2d(matrix, kernel)
print(matrix)
print("\n\n")
print(str(matrix).replace('0', '.').replace('1', '@').replace("2","x").replace('[', ' ').replace(']', ''))

print("result: ", np.sum(matrix == 2))
print("removed in each iteration: ", np.sum(removed))