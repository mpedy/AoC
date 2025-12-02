from numpy import sum
try:
    with open("2023/02/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()

data = data.split("\n")

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

game_okay = []

for game in data:
    id = int(game.split(":")[0].split(" ")[1])
    gamesets = game.split(": ")[1].split("; ")
    found = True
    for gameset in gamesets:
        red = 0
        green = 0
        blue = 0
        gameset = gameset.split(", ")
        for colour in gameset:
            if "red" in colour:
                red = int(colour.split(" ")[0])
            if "green" in colour:
                green = int(colour.split(" ")[0])
            if "blue" in colour:
                blue = int(colour.split(" ")[0])
        if not(red <= MAX_RED and green <= MAX_GREEN and blue <= MAX_BLUE):
            found = False
            break
    if found:
        game_okay.append(id)

print(sum(game_okay))



result = []
for game in data:
    id = int(game.split(":")[0].split(" ")[1])
    gamesets = game.split(": ")[1].split("; ")
    red = None
    green = None
    blue = None
    for gameset in gamesets:
        gameset = gameset.split(", ")
        for colour in gameset:
            if "red" in colour:
                red = int(colour.split(" ")[0]) if red is None else max(red,int(colour.split(" ")[0]))
            if "green" in colour:
                green = int(colour.split(" ")[0]) if green is None else max(green,int(colour.split(" ")[0]))
            if "blue" in colour:
                blue = int(colour.split(" ")[0]) if blue is None else max(blue,int(colour.split(" ")[0]))
    #print(f"Game {id} = {red},{green},{blue} = {red*green*blue}")
    result.append(red*green*blue)
print(sum(result))