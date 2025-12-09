import numpy as np

with open("data","r") as file:
    data = file.read().split("\n")

for i in range(len(data)):
    data[i] = [int(j) for j in data[i].split(",")]

matrix = np.zeros((len(data), len(data)))
for i in range(len(data)):
    for j in range(len(data)):
        if i == j:
            matrix[i,j] = np.inf
        else:
            matrix[i,j] = np.linalg.norm(np.array(data[i])-np.array(data[j]))

connected = 0
connections = []
k = 0
while k != 1000:
    k += 1
    i,j = np.where(matrix == np.min(matrix))[0]
    print(k,"Valore: ", data[i],data[j],i,j)
    print(connections)
    found = False
    for conn in connections:
        if i in conn and j in conn:
            connected += 2
            found = True
            continue
        if i in conn:
            found = True
            connected += 1
            conn.append(int(j))
            continue
        if j in conn:
            found = True
            connected += 1
            conn.append(int(i))
            continue
    if not found:
        connected += 2
        connections.append([int(i),int(j)])
    conn_a_index = 0
    while conn_a_index < len(connections):
        conn_a = connections[conn_a_index]
        conn_b_index = conn_a_index + 1
        while conn_b_index < len(connections):
            conn_b = connections[conn_b_index]
            for item in conn_b:
                if item in conn_a:
                    conn_a.extend(conn_b)
                    connections[conn_a_index] = list(set(conn_a))
                    del connections[conn_b_index]
                    conn_b_index -= 1
                    break
            conn_b_index += 1
        conn_a_index += 1
                    
    matrix[i,j] = np.inf
    matrix[j,i] = np.inf

connections.sort(key=lambda x: len(x), reverse=True)
result = 1
for i in range(3):
    result *= len(connections[i])
print("Result: ", result)
print("Connections: ", connections)