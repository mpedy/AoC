#from colorama import *

try:
    with open("2024/15/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()

data = data.split("\n\n")
mappa = data[0]
moves = data[1]


class Warehouse:
    def __init__(self, mappa, moves):
        self.data = mappa
        self.matrix = mappa.split("\n")
        self.moves = moves
        self.dim = (len(self.matrix), len(self.matrix[0]))
        self.dimx = self.dim[1]
        self.dimy = self.dim[0]
        self.pos = (0, 0)
        self.steps = 0
        self.direction = None
        self.convert_matrix()
        self.search_starting_pos()
        self._matrix = self.matrix.copy()
    
    def print(self, literal=False):
        print("\n\n")
        res = []
        def convert(c):
            if c == -1:
                return "."
            elif c == -2:
                return "#"
            else:
                return chr(c)
        for j in range(len(self.matrix)):
            res.append(" ".join([convert(i) if literal else (str(i) if i != 1 else str(i))
                       for i in self.matrix[j]]))
        # print("\n".join(res))
        for row in res:
            row = row.split(" ")
            print(" ".join(f"{str(item):<{2}}" for item in row))

    def search_starting_pos(self):
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x, y)) == 1:
                    self.pos = (x, y)
                    return

    def get(self, pos=None):
        if pos == None:
            return self.matrix[self.pos[1]][self.pos[0]]
        else:
            return self.matrix[pos[1]][pos[0]]

    def convert_matrix(self):
        def convert(symb):
            """
            -1 = ostacolo
            0  = vuoto
            1  = robot
            2  = cassa
            """
            if symb == "#":
                return -1
            if symb == ".":
                return 0
            if symb == "O":
                return 2
            else:
                return 1
        for i in range(len(self.matrix)):
            self.matrix[i] = [convert(s) for s in self.matrix[i]]

    def assign(self, pos, elem):
        t = list(self.matrix[pos[1]])
        t[pos[0]] = elem
        self.matrix[pos[1]] = t
        self.assigned = pos

    def cond_up(self, pos):
        return pos[1] == 0 or self.get((pos[0], pos[1]-1)) == -1

    def cond_down(self, pos):
        return pos[1] == self.dim[0]-1 or self.get((pos[0], pos[1]+1)) == -1

    def cond_right(self, pos):
        return pos[0] == self.dim[1]-1 or self.get((pos[0]+1, pos[1])) == -1

    def cond_left(self, pos):
        return pos[0] == 0 or self.get((pos[0]-1, pos[1])) == -1

    def start(self):
        for move in moves:
            self.steps += 1
            #self.print()
            print("Going ... ",move, "\nSTEP = ",self.steps)
            if move == ">":
                self.direction = "right"
                self.goRight()
            elif move == "<":
                self.direction = "left"
                self.goLeft()
            elif move == "^":
                self.direction = "up"
                self.goUp()
            elif move == "v":
                self.direction = "down"
                self.goDown()

    def goLeft(self):
        if not self.cond_left(self.pos):
            if self.get((self.pos[0]-1, self.pos[1])) in [0, 2]:
                self.moveRobot((self.pos[0]-1, self.pos[1]))

    def goRight(self):
        if not self.cond_right(self.pos):
            if self.get((self.pos[0]+1, self.pos[1])) in [0, 2]:
                self.moveRobot((self.pos[0]+1, self.pos[1]))

    def goUp(self):
        if not self.cond_up(self.pos):
            if self.get((self.pos[0], self.pos[1]-1)) in [0, 2]:
                self.moveRobot((self.pos[0], self.pos[1]-1))

    def goDown(self):
        if not self.cond_down(self.pos):
            if self.get((self.pos[0], self.pos[1]+1)) in [0, 2]:
                self.moveRobot((self.pos[0], self.pos[1]+1))

    def moveRobot(self, newpos):
        if self.get(newpos) == 2:
            self.moveObjects(newpos)
        else:
            self.assign(self.pos,0)
            self.pos = newpos
            self.assign(newpos,1)
    
    def moveObjects(self,newpos):
        is_movable = False
        if self.direction == "up":
            ymin = -1
            for y in range(newpos[1],0,-1):
                if self.get((newpos[0],y))==0:
                    is_movable = True
                    ymin = y
                    break
                if self.get((newpos[0],y))==-1:
                    return
            if is_movable:
                newarr = [*[1], *[self.get((newpos[0],y)) for y in range(newpos[1],ymin,-1)]]
                for y in range(len(newarr)):
                    self.assign((newpos[0],newpos[1]-y),newarr[y])
                self.assign(self.pos,0)
                self.pos = newpos

        if self.direction == "down":
            ymax = -1
            for y in range(newpos[1],self.dimy):
                if self.get((newpos[0],y))==0:
                    is_movable = True
                    ymax = y
                    break
                if self.get((newpos[0],y))==-1:
                    return
            if is_movable:
                newarr = [*[1], *[self.get((newpos[0],y)) for y in range(newpos[1],ymax)]]
                for y in range(len(newarr)):
                    self.assign((newpos[0],newpos[1]+y),newarr[y])
                self.assign(self.pos,0)
                self.pos = newpos
        
        if self.direction == "right":
            xmax = -1
            for x in range(newpos[0],self.dimx):
                if self.get((x,newpos[1]))==0:
                    is_movable = True
                    xmax = x
                    break
                if self.get((x,newpos[1]))==-1:
                    return
            if is_movable:
                newarr = [*[1], *[self.get((x,newpos[1])) for x in range(newpos[0],xmax)]]
                for x in range(len(newarr)):
                    self.assign((newpos[0]+x,newpos[1]),newarr[x])
                self.assign(self.pos,0)
                self.pos = newpos
        
        if self.direction == "left":
            xmin = -1
            for x in range(newpos[0],0,-1):
                if self.get((x,newpos[1]))==0:
                    is_movable = True
                    xmin = x
                    break
                if self.get((x,newpos[1]))==-1:
                    return
            if is_movable:
                newarr = [*[1], *[self.get((x,newpos[1])) for x in range(newpos[0],xmin,-1)]]
                for x in range(len(newarr)):
                    self.assign((newpos[0]-x,newpos[1]),newarr[x])
                self.assign(self.pos,0)
                self.pos = newpos

    def calculate_GPS_coordinates(self):
        result = 0
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x,y))==2:
                    result = result + y*100 + x
        return result
                    



w = Warehouse(mappa,moves)
w.start()
result = w.calculate_GPS_coordinates()
print("\nResult: ", result)