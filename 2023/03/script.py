from numpy import prod
try:
    with open("2023/03/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()

class Engine:
    def __init__(self, mappa):
        self.data = mappa
        self.matrix = mappa.split("\n")
        self.dim = (len(self.matrix), len(self.matrix[0]))
        self.dimx = self.dim[1]
        self.dimy = self.dim[0]
        self.points = 0
    
    def get(self, pos=None):
        if pos[0]<0 or pos[0]>=self.dimx or pos[1]<0 or pos[1]>=self.dimy:
            return None
        else:
            return self.matrix[pos[1]][pos[0]]

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

    def start_part1(self):
        found = False
        found_number = []
        result = 0
        for y in range(self.dimy):
            for x in range(self.dimx):
                if self.get((x,y)) in ["0","1","2","3","4","5","6","7","8","9"]:
                    found = True
                    found_number.append((x,y))
                else:
                    if len(found_number)>0:
                        number = int("".join([str(i) for n in found_number for i in self.get((n[0],n[1]))]))
                        can_calculate = False
                        for n in found_number:
                            if self.get((n[0]-1,n[1])) != None and self.get((n[0]-1,n[1])) != "." and self.get((n[0]-1,n[1])) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                            if self.get((n[0]+1,n[1])) != None and self.get((n[0]+1,n[1])) != "." and self.get((n[0]+1,n[1])) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                            if self.get((n[0],n[1]-1)) != None and self.get((n[0],n[1]-1)) != "." and self.get((n[0],n[1]-1)) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                            if self.get((n[0],n[1]+1)) != None and self.get((n[0],n[1]+1)) != "." and self.get((n[0],n[1]+1)) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                            
                            if self.get((n[0]-1,n[1]-1)) != None and self.get((n[0]-1,n[1]-1)) != "." and self.get((n[0]-1,n[1]-1)) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                            if self.get((n[0]-1,n[1]+1)) != None and self.get((n[0]-1,n[1]+1)) != "." and self.get((n[0]-1,n[1]+1)) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                            if self.get((n[0]+1,n[1]-1)) != None and self.get((n[0]+1,n[1]-1)) != "." and self.get((n[0]+1,n[1]-1)) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                            if self.get((n[0]+1,n[1]+1)) != None and self.get((n[0]+1,n[1]+1)) != "." and self.get((n[0]+1,n[1]+1)) not in ["0","1","2","3","4","5","6","7","8","9"]:
                                can_calculate = True
                        if can_calculate:
                            print("Trovato numero: ", number)
                            result += number
                    found_number = []
        return result

    def start_part2(self):
        found_gear = []
        result = 0
        for y in range(self.dimy):
            for x in range(self.dimx):
                if self.get((x,y)) == "*":
                    found_gear.append((x,y))
        for gear in found_gear:
            found_number = 0
            found_number_position = []
            n = gear
            if self.get((n[0]-1,n[1])) != None and self.get((n[0]-1,n[1])) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0]-1,n[1]))
            if self.get((n[0]+1,n[1])) != None and self.get((n[0]+1,n[1])) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0]+1,n[1]))
            if self.get((n[0],n[1]-1)) != None and self.get((n[0],n[1]-1)) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0],n[1]-1))
            if self.get((n[0],n[1]+1)) != None and self.get((n[0],n[1]+1)) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0],n[1]+1))
            if self.get((n[0]-1,n[1]-1)) != None and self.get((n[0]-1,n[1]-1)) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0]-1,n[1]-1))
            if self.get((n[0]-1,n[1]+1)) != None and self.get((n[0]-1,n[1]+1)) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0]-1,n[1]+1))
            if self.get((n[0]+1,n[1]-1)) != None and self.get((n[0]+1,n[1]-1)) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0]+1,n[1]-1))
            if self.get((n[0]+1,n[1]+1)) != None and self.get((n[0]+1,n[1]+1)) in ["0","1","2","3","4","5","6","7","8","9"]:
                found_number += 1
                found_number_position.append((n[0]+1,n[1]+1))
            
            if found_number > 1:
                number_str = []
                for position in found_number_position:
                    _x, x = position[0], position[0]
                    y = position[1]
                    n_found = [self.get((x,y))]
                    x = x+1
                    while self.get((x,y)) in ["0","1","2","3","4","5","6","7","8","9"]:
                        n_found.append(self.get((x,y)))
                        x+=1
                    x = _x-1
                    while self.get((x,y)) in ["0","1","2","3","4","5","6","7","8","9"]:
                        n_found.insert(0,self.get((x,y)))
                        x -= 1
                    number_str.append(int("".join(n_found)))
                number_str = list(set(number_str))
                result += prod(list(set(number_str))) if found_number>1 else list(set(number_str))[0]**2
        return result
e = Engine(data)
print(e.start_part1())
print(e.start_part2())