with open("data","r") as file:
    data = file.read().split(",")

def check_if_doubled(x):
    results = {}
    for s in range(1,len(x)//2+1):
        results[s] = {"piece": None, "matches": []}
        piece = x[:s]
        for i in range(s,len(x),s):
            if x[i:i+s] != piece:
                results[s]["piece"] = piece
                results[s]["matches"].append(False)
                break
            else:
                results[s]["piece"] = piece
                results[s]["matches"].append(True)
    for i in results:
        if all(p is True for p in results[i]["matches"]):
            if len(results[i]["matches"])>=1:
                print(x, "is invalid")
                return True
    return False
    #return results

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