# from colorama import *

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
        self.enlarge_matrix()
        self.search_starting_pos()
        self._matrix = self.matrix.copy()

    def enlarge_matrix(self):
        m = self.matrix.copy()
        self.old_matrix = m
        self.matrix = []
        for y in range(self.dimy):
            line = []
            for x in range(self.dimx):
                if m[y][x] == -1:
                    line.append(-1)
                    line.append(-1)
                elif m[y][x] == 0:
                    line.append(0)
                    line.append(0)
                elif m[y][x] == 2:
                    line.append(2)
                    line.append(3)
                elif m[y][x] == 1:
                    line.append(1)
                    line.append(0)
            self.matrix.append(line)
        self.dimx *= 2
        self.dim = [self.dimy, self.dimx]

    def print(self, literal=False):
        print("\n\n")
        res = []

        def convert(c):
            if c == -1:
                return "#"
            if c == 1:
                return "@"
            elif c == -2:
                return "#"
            elif c == 2:
                return "["
            elif c == 3:
                return "]"
            else:
                return chr(c)
        for j in range(len(self.matrix)):
            res.append(" ".join([convert(i) if literal else (str(i) if i != 1 else str(i))
                       for i in self.matrix[j]]))
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
            print("Going ... ", move, "\nSTEP = ", self.steps)
            if self.steps>=18937:
                asdasd = 1
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
            if self.get((self.pos[0]-1, self.pos[1])) in [0, 2, 3]:
                self.moveRobot((self.pos[0]-1, self.pos[1]))

    def goRight(self):
        if not self.cond_right(self.pos):
            if self.get((self.pos[0]+1, self.pos[1])) in [0, 2, 3]:
                self.moveRobot((self.pos[0]+1, self.pos[1]))

    def goUp(self):
        if not self.cond_up(self.pos):
            if self.get((self.pos[0], self.pos[1]-1)) in [0, 2, 3]:
                self.moveRobot((self.pos[0], self.pos[1]-1))

    def goDown(self):
        if not self.cond_down(self.pos):
            if self.get((self.pos[0], self.pos[1]+1)) in [0, 2, 3]:
                self.moveRobot((self.pos[0], self.pos[1]+1))

    def moveRobot(self, newpos):
        if self.get(newpos) in [2, 3]:
            self.moveObjects(newpos)
        else:
            self.assign(self.pos, 0)
            self.pos = newpos
            self.assign(newpos, 1)
    
    def getArea(self,pos,area=[]):
        n_area = []
        n_area.append(pos)
        if self.direction == "left":
            for i in range(pos[0]-1,0,-1):
                if self.get((i,pos[1])) in [2,3]:
                    n_area.append((i,pos[1]))
                elif self.get((i,pos[1])) == -1:
                    return False, n_area
                elif self.get((i,pos[1]))==0:
                    return True, n_area
            return True, n_area
        if self.direction == "right":
            for i in range(pos[0],self.dimx):
                if self.get((i,pos[1])) in [2,3]:
                    n_area.append((i,pos[1]))
                elif self.get((i,pos[1])) == -1:
                    return False, n_area
                elif self.get((i,pos[1]))==0:
                    return True, n_area
            return True, n_area
        if self.get(pos)==2:
            n_area.append((pos[0]+1,pos[1]))
        elif self.get(pos)==3:
            n_area.append((pos[0]-1,pos[1]))
        elif self.get(pos)==-1:
            return False, area
        elif self.get(pos)==0:
            return True, area
        for i in n_area:
            area.append(i)
            if self.direction == "up":
                can_continue, n_area_1 = self.getArea((i[0],i[1]-1),[i])
                if not can_continue:
                    return False, area
                for x in n_area_1:
                    if x not in area:
                        area.append(x)
            elif self.direction == "down":
                can_continue, n_area_1 = self.getArea((i[0],i[1]+1),[i])
                if not can_continue:
                    return False, area
                for x in n_area_1:
                    if x not in area:
                        area.append(x)
            elif self.direction == "left":
                can_continue, n_area_1 = self.getArea((pos[0]-1,pos[1]),[i])
                if not can_continue:
                    return False, area
                for x in n_area_1:
                    if x not in area:
                        area.append(x)
            elif self.direction == "right":
                can_continue, n_area_1 = self.getArea((pos[0]+1,pos[1]),[i])
                if not can_continue:
                    return False, area
                for x in n_area_1:
                    if x not in area:
                        area.append(x)
        return True, area
        


    def getLastSpaces(self,newpos, lastspaces = []): # newpos è la nuova posizione wannabe
        result = False
        positions = [newpos]
        # non cambia a seconda della direzione, le scatole sono aperte<>chiuse nella stessa riga sempre, con apertura a sx e chiusura a dx
        if self.get(newpos)==2:
            positions.append((newpos[0]+1,newpos[1]))
        elif self.get(newpos)==3:
            positions.append((newpos[0]-1,newpos[1]))
        elif self.get(newpos)==0:
            return True, [newpos], [newpos]
        oldp = []
        area = []

        if self.direction == "up":
            for block in area:
                if self.get((block[0],block[1]-1))=="#":
                    return False, area
            return True,area


        if self.direction == "up":
            while len(oldp)!=len(positions):
                oldp = positions.copy()
                for p in positions:
                    if self.get((p[0],p[1]-1)) in [2,3]:
                        result, positionsa, lastspaces = self.getLastSpaces((p[0],p[1]-1), lastspaces=lastspaces)
                        if result:
                            for x in positionsa:
                                positions.append(x)
                            positions = list(set(positions))
                        else:
                            return result, positions, lastspaces
                    elif self.get((p[0],p[1]-1)) == 0:
                        lastspaces.append((p[0],p[1]-1))
                        result = True
                    elif self.get((p[0],p[1]-1))==-1:
                        return False, [], lastspaces

        if self.direction == "down":
            while len(oldp)!=len(positions):
                oldp = positions.copy()
                for p in positions:
                    if self.get((p[0],p[1]+1)) in [2,3]:
                        result, positions, lastspaces = self.getLastSpaces((p[0],p[1]+1), lastspaces=[])
                        if result:
                            #for x in positionsa:
                            #    positions.append(x)
                            positions = list(set(positions))
                        else:
                            return result, positions, lastspaces
                    elif self.get((p[0],p[1]+1)) == 0:
                        if (p[0],p[1]+1) not in lastspaces:
                            lastspaces.append((p[0],p[1]+1))
                        result = True
                    elif self.get((p[0],p[1]+1))==-1:
                        return False, [], lastspaces
        
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
                return
        
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

        return result, positions, lastspaces
                                                       

    def moveObjects(self, newpos):
        found_area, area = self.getArea(newpos,[])
        area = list(set(area))
        if found_area:
            if self.direction == "left":
                x_min, x_max = min([a[0] for a in area]), max([a[0] for a in area])
                y = area[0][1]
                for x in range(x_min,x_max+1):
                    self.assign((x-1,y),self.get((x,y)))
                self.assign((x_max,y),1)
                self.assign(self.pos,0)
                self.pos = (x_max,y)
            if self.direction == "right":
                x_min, x_max = min([a[0] for a in area]), max([a[0] for a in area])
                y = area[0][1]
                for x in range(x_max+1,x_min,-1):
                    self.assign((x,y),self.get((x-1,y)))
                self.assign((x_min,y),1)
                self.assign(self.pos,0)
                self.pos = (x_min,y)
            if self.direction == "up":
                x_min, x_max, y_min, y_max = min([a[0] for a in area]), max([a[0] for a in area]), min([a[1] for a in area]), max([a[1] for a in area])
                for x in range(x_min,x_max+1):
                    for y in range(y_min,y_max+1):
                        if (x,y) in area:
                            self.assign((x,y-1), self.get((x,y)))
                            self.assign((x,y),0)
                for x in range(x_min,x_max+1):
                    if (x,y_max) in area:
                        self.assign((x,y_max),0)
                self.assign(newpos,1)
                self.assign(self.pos,0)
                self.pos = newpos
            if self.direction == "down":
                x_min, x_max, y_min, y_max = min([a[0] for a in area]), max([a[0] for a in area]), min([a[1] for a in area]), max([a[1] for a in area])
                for x in range(x_min,x_max+1):
                    for y in range(y_max,y_min-1,-1):
                        if (x,y) in area:
                            self.assign((x,y+1), self.get((x,y)))
                            self.assign((x,y),0)
                for x in range(x_min,x_max+1):
                    if (x,y_min) in area:
                        self.assign((x,y_min),0)
                self.assign(newpos,1)
                self.assign(self.pos,0)
                self.pos = newpos
        return

    def calculate_GPS_coordinates(self):
        result = 0
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x, y)) == 2:
                    result = result + y*100 + x
        return result


w = Warehouse(mappa, moves)
w.start()
w.print(literal=False)

result = w.calculate_GPS_coordinates()

print("\n\nResult: ", result)