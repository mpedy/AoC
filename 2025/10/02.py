import pulp as pl

with open("data","r") as file:
    data = file.read().split("\n")

def createButtons(buttons, l):
    buttonList = []
    for b in buttons:
        action = []
        b = b[1:-1]
        i=0
        while i < len(b):
            if b[i] != ",":
                action.append(int(b[i]))
            i+=1
        buttonList.append(action)
    return buttonList

def createDiagram(diagram):
    d = diagram[1:-1]
    return [0 if x =="." else 1 for x in d]

def createJoltage(joltage):
    joltage = joltage[1:-1].split(",")
    return [int(x) for x in joltage]

result = 0
for i in range(len(data)):
    d = data[i].split(" ")
    diagram = createDiagram(d[0])
    o_buttons = d[1:-1]
    buttons = createButtons(d[1:-1], len(diagram))
    joltage = createJoltage(d[-1])
    #print("Buttons: ", buttons, " Joltage: ", joltage)
    model = pl.LpProblem("Test_Problem", pl.LpMinimize)
    k = pl.LpVariable.dicts("ki", range(len(buttons)), lowBound=0, cat="Integer")
    for i in range(len(joltage)):
        model += pl.lpSum([k[b] for b in range(len(buttons)) if i in buttons[b]]) == joltage[i]
    for i in range(len(k)):
        model += k[i] >= 0
    model += pl.lpSum([k[i] for i in range(len(buttons))])
    #model.solve()
    pl.PULP_CBC_CMD(msg=0).solve(model)
    print("Status:", pl.LpStatus[model.status])
    result += sum([k[i].value() for i in range(len(buttons))])
    #print("Total buttons pressed: ", result)
    #print("\n".join([f"{v.name}: {int(v.value())}" for v in model.variables()]))
print("Final result: ", result)