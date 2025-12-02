with open("data","r") as file:
    data = file.read().split(",")

def check_if_doubled(x):
    for i in range(len(x)):
        if x[:i] == x[i:]:
            return True
    return False

results = []
result = 0

for d in data:
    d = d.split("-")
    d[0] = int(d[0])
    d[1] = int(d[1])
    for i in range(d[0], d[1]+1):
        if check_if_doubled(str(i)):
            results.append(i)
            result += i

print(result)