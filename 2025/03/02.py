with open("data","r") as file:
    battery = file.read().split("\n")

result = 0

for packs in battery:
    number = []
    packs = [int(i) for i in list(packs)]
    offset = 0
    while len(number) != 11:
        n_max = max(packs[:-12+len(number)+1])
        offset = packs.index(n_max)+1
        packs[offset-1] = -1
        packs = packs[offset:]
        number.append(n_max)
    n_max = max(packs)
    number.append(n_max)
    result = result + (int("".join([str(i) for i in number])))

print(result)