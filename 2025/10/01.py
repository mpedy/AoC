import itertools

with open("data","r") as file:
    data = file.read().split("\n")

def createButtons(buttons, l):
    buttonList = []
    for b in buttons:
        action = [0 for _ in range(l)] 
        b = b.replace("(","").replace(")","")
        i=0
        while i < len(b):
            if b[i] != ",":
                action[int(b[i])] = 1
            i+=1
        #print("Action prima: ", list(reversed(action)))
        action = int("".join([str(x) for x in list(reversed(action))]), 2)
        #print("Action dopo: ", action)
        buttonList.append(action)
    return buttonList

def createDiagram(diagram):
    d = diagram[1:-1]
    return [0 if x =="." else 1 for x in d]

results = 0
for i in range(len(data)):
    d = data[i].split(" ")
    diagram = createDiagram(d[0])
    state = int("".join([str(x) for x in reversed(diagram)]), 2)
    buttons = createButtons(d[1:-1], len(diagram))
    joltage = d[-1]
    print("STATE: ", state, " -- Diagram ", diagram, " Buttons: ", buttons, " Joltage: ", joltage)
    found = False
    len_combinations = 0
    final_comb = []
    while not found:
        len_combinations += 1
        #print("")
        for comb in itertools.combinations_with_replacement(buttons, len_combinations):
            result = None
            #print("Trying combination: ", comb)
            final_comb = []
            for c in comb:
                if result is None:
                    result = c
                else:
                    result ^= c
                #print("result in progress: ", result)
                final_comb.append(c)
                if result == state:
                    #print("RESULT FOUND: ", result)
                    found = True
                    break
            if found:
                results += len(final_comb)
                break
    print("Found with comb: ", final_comb, [buttons.index(x) for x in final_comb])
    

print("Final Result: ", results)