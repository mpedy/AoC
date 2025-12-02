with open("data","r") as file:
    data = file.read().split("\n")


number_of_zeros = 0
starting_point = 50
n = starting_point

for moves in data:
    direction, distance = moves[0], int(moves[1:]) % 100
    n = (n+distance) if direction == "R" else (n-distance)
    while n>=100:
        n -= 100
    while n<0:
        n+=100
    if n==0:
        number_of_zeros+=1
    print("n: ", n, " number of zeros: ", number_of_zeros)
print("Number of zeros: ", number_of_zeros)
