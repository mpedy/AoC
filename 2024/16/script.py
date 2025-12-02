from enum import Enum
import numpy
import heapq

try:
    with open("2024/16/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()


class DIR(Enum):
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

    @classmethod
    def cost_change(self, From, To):
        if From == To:
            return 0
        if From in [self.UP, self.DOWN]:
            if To in [self.RIGHT, self.LEFT]:
                return 1
            else:
                return 2
        if From in [self.RIGHT, self.LEFT]:
            if To in [self.UP, self.DOWN]:
                return 1
            else:
                return 2


class Casella:
    def __init__(self, x=None, y=None, dir=None, dist = float("inf")):
        self.x = x
        self.y = y
        self.dir = dir
        self.dist = dist
        self.prev = None

    def __repr__(self):
        return f"{(self.x,self.y)} {self.dir} {self.dist}"

    def __str__(self):
        return f"{(self.x,self.y)} {self.dir} {self.dist}"
    
    def __lt__(self, other):
        return self.dist < other.dist


class Path:
    def __init__(self, casella=None, dimx=None, dimy=None):
        self.caselle = []
        self.caselle.copy()
        if casella is not None:
            self.caselle.append(casella)
    
    def extract_min(self):
        min_dist_index = numpy.argmin([c.dist for c in self.caselle], axis=0)
        casella = self.caselle.pop(min_dist_index)
        #for dir in [DIR.UP, DIR.DOWN, DIR.LEFT, DIR.RIGHT]:
        #    for c in self.caselle:
        #        if (c.x,c.y,c.dir) == (casella.x,casella.y,dir):
        #            self.caselle.remove(c)
        #            break
        return casella

    def getLast(self):
        return self.caselle[len(self.caselle)-1]

    def getLastPosDir(self):
        last = self.caselle[len(self.caselle)-1]
        return (last.x, last.y), last.dir

    def __repr__(self):
        return ", ".join([str(i) for i in self.caselle])

    def contains(self, casella: Casella, _no_dir=True):
        for c in self.caselle:
            if not _no_dir:
                if (c.x, c.y, c.dir) == (casella.x, casella.y, casella.dir):
                    return True, c
            else:
                if (c.x, c.y) == (casella.x, casella.y):
                    return True, c
        return False, None

    def fromPath(self, p):
        self.caselle = p.caselle.copy()

    def add(self, casella):
        self.caselle.append(casella)
    
    def cost(self):
        change_dirs = 0
        steps = -1 #la prima è casa
        last_dir = self.caselle[0].dir
        for i in self.caselle:
            if last_dir != i.dir:
                change_dirs += DIR.cost_change(last_dir,i.dir)
                last_dir = i.dir
            steps += 1
        return steps+change_dirs*1000, change_dirs, steps



class Maze:
    def __init__(self, mappa):
        self.data = mappa
        self.matrix = mappa.split("\n")
        self.dim = (len(self.matrix), len(self.matrix[0]))
        self.dimx = self.dim[1]
        self.dimy = self.dim[0]
        self.pos = (0, 0)
        self.end_pos = (-1, -1)
        self.steps = 0
        self.direction = None
        self.VUOTO = 0
        self.OSTACOLO = 1
        self.ME = 2
        self.END = 3
        self.convert_matrix()
        self.search_starting_pos()
        self.search_ending_pos()
        self._matrix = self.matrix.copy()
        self.points = 0
        self.paths = [Path(Casella(self.pos[0], self.pos[1], DIR.RIGHT))]

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

    def search_starting_pos(self):
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x, y)) == self.ME:
                    self.pos = (x, y)
                    return

    def search_ending_pos(self):
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x, y)) == self.END:
                    self.end_pos = (x, y)
                    return

    def get(self, pos=None):
        if pos == None:
            return self.matrix[self.pos[1]][self.pos[0]]
        else:
            return self.matrix[pos[1]][pos[0]]

    def convert_matrix(self):
        def convert(symb):
            if symb == "#":
                return self.OSTACOLO
            if symb == ".":
                return self.VUOTO
            if symb == "S":
                return self.ME
            if symb == "E":
                return self.END
            else:
                return -2
        for i in range(len(self.matrix)):
            self.matrix[i] = [convert(s) for s in self.matrix[i]]

    def assign(self, pos, elem):
        t = list(self.matrix[pos[1]])
        t[pos[0]] = elem
        self.matrix[pos[1]] = t
        self.assigned = pos

    def cond_up(self, pos):
        return pos[1] == 0 or self.get((pos[0], pos[1]-1)) == self.OSTACOLO

    def cond_down(self, pos):
        return pos[1] == self.dim[0]-1 or self.get((pos[0], pos[1]+1)) == self.OSTACOLO

    def cond_right(self, pos):
        return pos[0] == self.dim[1]-1 or self.get((pos[0]+1, pos[1])) == self.OSTACOLO

    def cond_left(self, pos):
        return pos[0] == 0 or self.get((pos[0]-1, pos[1])) == self.OSTACOLO

    def lookAround(self, pos, path: Path):
        result = []
        if not self.cond_up(pos) and self.get((pos[0], pos[1]-1)) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0], pos[1]-1, DIR.UP))
        if not self.cond_down(pos) and self.get((pos[0], pos[1]+1)) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0], pos[1]+1, DIR.DOWN))
        if not self.cond_right(pos) and self.get((pos[0]+1, pos[1])) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0]+1, pos[1], DIR.RIGHT))
        if not self.cond_left(pos) and self.get((pos[0]-1, pos[1])) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0]-1, pos[1], DIR.LEFT))
        res = []
        for i in result:
            if not path.contains(i)[0]:
                res.append(i)
        return res

    def start(self, path: Path = None):
        #print("Arrivato il path: ", path)
        if path is None:
            path = self.paths[0]
        if path.contains(Casella(10, 7, DIR.RIGHT))[0]:
            asd = 1
        while self.get(self.pos) != self.END:
            possible_moves = self.lookAround(path.getLastPosDir()[0], path)
            if len(possible_moves) == 1:
                path.add(possible_moves[0])
                if path.contains(Casella(self.end_pos[0],self.end_pos[1],None))[0]:
                    self.paths.append(path)
                    print("Percorsi trovati: ", len(self.paths))
                    return
            elif len(possible_moves) > 1:
                for i in possible_moves:
                    p = Path()
                    p.fromPath(path)
                    p.add(i)
                    self.start(p)
                break
            elif len(possible_moves) == 0:
                break
        last_casella = path.getLast()
        if self.get((last_casella.x, last_casella.y)) == self.END:
            self.paths.append(path)
            print("Percorsi trovati: ", len(self.paths))
    
    def printPath(self, path : Path, literal=False):
        m = self.matrix.copy()
        def getdir(dir):
            if dir == DIR.UP:
                return "^"
            if dir == DIR.LEFT:
                return "<"
            if dir == DIR.RIGHT:
                return ">"
            if dir == DIR.DOWN:
                return "v"
        for c in path.caselle:
            self.assign((c.x,c.y), getdir(c.dir))
        self.print(literal=literal)
        self.matrix = m.copy()
    
    def getMinimumPathCost(self):
        minimum_cost = self.paths[0].cost()
        minimum_path = self.paths[0]
        for p in self.paths:
            minimum_cost_new = min(minimum_cost,p.cost())
            if minimum_cost_new != minimum_cost:
                minimum_path = p
                minimum_cost = minimum_cost_new
        return minimum_path, minimum_cost

    def lookAround_v2(self, pos, path):
        result = []
        if not self.cond_up(pos) and self.get((pos[0], pos[1]-1)) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0], pos[1]-1, DIR.UP))
        if not self.cond_down(pos) and self.get((pos[0], pos[1]+1)) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0], pos[1]+1, DIR.DOWN))
        if not self.cond_right(pos) and self.get((pos[0]+1, pos[1])) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0]+1, pos[1], DIR.RIGHT))
        if not self.cond_left(pos) and self.get((pos[0]-1, pos[1])) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0]-1, pos[1], DIR.LEFT))
        res = []
        for i in result:
            found, c = path.contains(i)
            if found:
                if c.dir is None or True:
                    c.dir = i.dir
                res.append(c)
        return res
    

    def lookAround_v3(self, pos, path):
        result = []
        if not self.cond_up(pos) and self.get((pos[0], pos[1]-1)) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0], pos[1]-1, DIR.UP))
        if not self.cond_down(pos) and self.get((pos[0], pos[1]+1)) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0], pos[1]+1, DIR.DOWN))
        if not self.cond_right(pos) and self.get((pos[0]+1, pos[1])) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0]+1, pos[1], DIR.RIGHT))
        if not self.cond_left(pos) and self.get((pos[0]-1, pos[1])) in [self.VUOTO,self.END]:
            result.append(Casella(pos[0]-1, pos[1], DIR.LEFT))
        return result
    
    def lookAround_v4(self, pos, path: Path):
        result = []
        if not self.cond_up(pos) and self.get((pos[0], pos[1]-1)) in [self.VUOTO,self.END]:
            #for dir in [DIR.UP, DIR.DOWN, DIR.LEFT, DIR.RIGHT]:
            result.append(Casella(pos[0], pos[1]-1, dir=DIR.UP))
        if not self.cond_down(pos) and self.get((pos[0], pos[1]+1)) in [self.VUOTO,self.END]:
            #for dir in [DIR.UP, DIR.DOWN, DIR.LEFT, DIR.RIGHT]:
            result.append(Casella(pos[0], pos[1]+1, dir=DIR.DOWN))
        if not self.cond_right(pos) and self.get((pos[0]+1, pos[1])) in [self.VUOTO,self.END]:
            #for dir in [DIR.UP, DIR.DOWN, DIR.LEFT, DIR.RIGHT]:
            result.append(Casella(pos[0]+1, pos[1], dir=DIR.RIGHT))
        if not self.cond_left(pos) and self.get((pos[0]-1, pos[1])) in [self.VUOTO,self.END]:
            #for dir in [DIR.UP, DIR.DOWN, DIR.LEFT, DIR.RIGHT]:
            result.append(Casella(pos[0]-1, pos[1], dir=DIR.LEFT))
        res = []
        for i in result:
            found, c = path.contains(i,_no_dir=False)
            if found:
                res.append(c)
        return res
        #return filter(lambda i: path.contains(i, _no_dir=False), result)
    
    def dijkstra_v2(self):
        Q = []
        for x in range(self.dimx):
            for y in range(self.dimy):
                elem = self.get((x,y))
                if elem in [self.VUOTO, self.END, self.ME]:
                    if elem == self.ME:
                        heapq.heappush(Q, (float("inf"),Casella(x,y,dir=DIR.RIGHT)))
                    else:
                        for dir in [DIR.UP, DIR.LEFT, DIR.RIGHT, DIR.DOWN]:
                            heapq.heappush(Q, (float("inf"), Casella(x,y,dir=dir)))
        while len(Q)>0:
            dist_u, u = heapq.heappop(Q)

            possible_moves = self.lookAround_v2((u.x,u.y))
            for move in possible_moves:
                try:
                    if Q.index(move)>=0:
                        alt = 1000*DIR.cost_change(u.dir, move.dir)+1
                        if alt < move.dist:
                            move.dist = alt
                            move.prev = u
                            heapq.heappush(Q,(alt, move))
                except Exception:
                    continue
        sh = Path()


    def dijkstra(self):
        Q = Path()
        p = {}
        queue = []
        shortest_path = Path()
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x,y)) in [self.VUOTO, self.END]:
                    Q.add(Casella(x,y))
                    p[(x,y)] = [float("inf"), None]
                if self.get((x,y)) in [self.ME]:
                    Q.add(Casella(x,y,dir=DIR.RIGHT,dist=0))
                    p[(x,y)] = [0,None]

        iter = 0
        while len(Q.caselle)>0:
            iter += 1
            print("\n\nIter: ",iter)
            #for q1 in Q.caselle:
            #    print(q1)
            for k in p.keys():
                print(k, p[k])
            u = Q.extract_min()
            if (u.x,u.y) == (3,0):
                asd = 1
            #if (u.x,u.y) == self.end_pos:
            #    break
            
            possible_moves = self.lookAround_v2((u.x,u.y),Q)
            for v in possible_moves:
                alt = u.dist + 1000*DIR.cost_change(u.dir, v.dir)+1
                if alt < v.dist:
                    v.dist = alt
                    v.prev = u
                    p[(v.x,v.y)] = [alt,u]
        for u in shortest_path.caselle:
            if (u.x,u.y) == self.end_pos:
                if u.prev is not None or (u.x,u.y) == self.pos:
                    while u is not None:
                        shortest_path.add(u)
                        u = u.prev
        u = p[self.end_pos]
        if u[1].prev is not None or (u[1].x,u[1].y) == self.pos:
            while u[1] is not None:
                shortest_path.add(u[1])
                u = p[(u[1].x,u[1].y)]
        return shortest_path, p
    
    def dijkstra_v3(self):
        Q = Path()
        shortest_path = Path()
        queue = []
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x,y)) in [self.VUOTO, self.END]:
                    for dir in [DIR.UP, DIR.DOWN, DIR.LEFT, DIR.RIGHT]:
                        c = Casella(x,y,dir=dir)
                        Q.add(c)
                        heapq.heappush(queue, (float("inf"), c))
                if self.get((x,y)) in [self.ME]:
                    c = Casella(x,y,dir=DIR.RIGHT,dist=0)
                    Q.add()
                    heapq.heappush(queue, (float("inf"), c))

        while len(Q.caselle)>0:
            u = Q.extract_min()
            print(len(Q.caselle))
            if (u.x,u.y) == self.end_pos:
                break
            
            possible_moves = self.lookAround_v4((u.x,u.y),Q)
            #print(u)
            #print(possible_moves)
            #print("\n\n")
            for v in possible_moves:
                alt = u.dist + 1000*DIR.cost_change(u.dir, v.dir)+1
                if alt < v.dist:
                    v.dist = alt
                    v.prev = u
        if u.prev is not None or (u.x,u.y) == self.pos:
            while u is not None:
                shortest_path.add(u)
                u = u.prev
        return shortest_path

    def dijkstra_v4(self):
        Q = Path()
        shortest_path = Path()
        queue = []
        for x in range(self.dimx):
            for y in range(self.dimy):
                if self.get((x,y)) in [self.VUOTO, self.END]:
                    for dir in [DIR.UP, DIR.DOWN, DIR.LEFT, DIR.RIGHT]:
                        c = Casella(x,y,dir=dir)
                        Q.add(c)
                if self.get((x,y)) in [self.ME]:
                    c = Casella(x,y,dir=DIR.RIGHT,dist=0)
                    Q.add(c)
                    heapq.heappush(queue, (0, c))
        iter= 0
        distances = {}
        distances[(self.pos[0],self.pos[1],DIR.RIGHT)] = 0
        while len(queue)>0:
            #print(len(queue))
            iter += 1
            score, u = heapq.heappop(queue)
            if (u.x,u.y) == self.end_pos:
                break
            
            possible_moves = self.lookAround_v4((u.x,u.y),Q)
            for v in possible_moves:
                alt = score + 1000*DIR.cost_change(u.dir, v.dir)+1
                if alt < v.dist or (v.x,v.y,v.dir) not in distances:
                    v.dist = alt
                    v.prev = u
                    distances[(v.x,v.y,v.dir)]=alt
                    heapq.heappush(queue,(alt,v))
        if u.prev is not None or (u.x,u.y) == self.pos:
            while u is not None:
                shortest_path.add(u)
                u = u.prev
        return shortest_path



m = Maze(data)
sh_path = m.dijkstra_v4()
m.printPath(sh_path, literal=False)
print(sh_path.cost())
#m.start()
#m.paths = m.paths[1:]
#for i in m.paths:
#    m.printPath(i)
#    print("Costo: ", i.cost())
#    a = 1

#path_min, path_min_cost = m.getMinimumPathCost()
#print(m.printPath(path_min), path_min_cost[0])
