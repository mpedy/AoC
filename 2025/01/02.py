with open("data","r") as file:
    data = file.read().split("\n")


number_of_zeros = 0
starting_point = 50
n = starting_point

def mov(a,b,dir):
    if dir=="R":
        return a+b
    elif dir=="L":
        return a-b
    else:
        raise Exception("Dir not recognized! >> ", dir)

for moves in data:
    direction, distance = moves[0], int(moves[1:])
    while distance > 0:
        n = mov(n,1,direction)
        distance -= 1
        if n >= 100:
            n -= 100
        if n<0:
            n += 100
        if n==0:
            number_of_zeros += 1
    print(moves, "n: ", n, " number of zeros: ", number_of_zeros)
print("Number of zeros: ", number_of_zeros)
