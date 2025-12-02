try:
    with open("2024/25/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()


class DoorORKey:
    def __init__(self, data):
        self.data = data
        self.matrix = data.split("\n")
        self.dim = (len(self.matrix), len(self.matrix[0]))
        self.dimx = self.dim[1]
        self.dimy = self.dim[0]
        self.is_door = False
        self.is_key = False
        self.pins = []
        self.checkDoorORKey()
        self.convert_pins()
        self.idx = "".join([str(i) for i in self.pins])
    
    def checkDoorORKey(self):
        for x in range(self.dimx):
            if self.get((x,0)) != "#":
                self.is_key = True
                return
        self.is_door = True
        return

    def convert_pins(self):
        if not self.is_door:
            asd = 1
        for x in range(self.dimx):
            pin = 0
            for y in ( range(1,self.dimy) if self.is_door else range(self.dimy-2,-1,-1)):
                if self.get((x,y)) == "#":
                    pin += 1
                else:
                    self.pins.append(pin)
                    break


    def print(self, literal=False):
        print("\n\n")
        res = []

        def convert(c):
            if c == self.OSTACOLO:
                return "#"
            elif c == self.VUOTO:
                return "."
            elif c == self.ME:
                return "S"
            elif c == self.END:
                return "E"
            else:
                return chr(c)
        for j in range(len(self.matrix)):
            if literal:
                res.append(" ".join([convert(i)]))
            else:
                res.append(
                    " ".join([(str(i) if i != 1 else str(i)) for i in self.matrix[j]]))
        for row in res:
            row = row.split(" ")
            print(" ".join(f"{str(item):<{2}}" for item in row))

    def get(self, pos=None):
        if pos == None:
            return self.matrix[self.pos[1]][self.pos[0]]
        else:
            return self.matrix[pos[1]][pos[0]]

    def assign(self, pos, elem):
        t = list(self.matrix[pos[1]])
        t[pos[0]] = elem
        self.matrix[pos[1]] = t
        self.assigned = pos

data = data.split("\n\n")

doors = []
keys = []

for i in range(len(data)):
    obj = DoorORKey(data[i])
    if obj.is_door:
        doors.append(obj)
    else:
        keys.append(obj)

result = []

for k in keys:
    for d in doors:
        found = True
        for i in range(len(k.pins)):
            if (k.pins[i] + d.pins[i] >= k.dimy-1):
                found=False
                break
        if found:
            print(d.pins, k.pins)
            result.append((k.idx,d.idx))

print(list(set(result)))