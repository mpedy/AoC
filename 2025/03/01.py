with open("data","r") as file:
    battery = file.read().split("\n")

result = 0

for packs in battery:
    packs = [int(i) for i in list(packs)]
    n_max = max(packs[:-1])
    n_max_2 = max(packs[packs.index(n_max)+1:])
    result = result + (int("".join([str(n_max),str(n_max_2)])))

print(result)
