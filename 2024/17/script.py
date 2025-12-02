try:
    with open("2024/17/test_input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("test_input.txt", "r") as file:
        data = file.read()

class PC:
    def __init__(self,a=0,b=0,c=0,opcodes=[], part2 = False):
        self.a = a
        self.b = b
        self.c = c
        self.opcodes = opcodes
        self.ip = 0
        self.instruction = None
        self.operand = None
        self.halted = False
        self.output = []

        self.part2 = part2
        self.correct_output = [2,4,1,2,7,5,4,5,1,3,5,5,0,3,3,0]
    
    def read(self):
        if self.halted:
            print(self)
            raise Exception("**** HALTED STATE!! ****\n\n")
        self.instruction = self.opcodes[self.ip]
        if self.instruction == 0:
            self.adv()
        elif self.instruction == 1:
            self.bxl()
        elif self.instruction == 2:
            self.bst()
        elif self.instruction == 3:
            if self.a != 0:
                self.operand = self.opcodes[self.ip+1]
                self.ip = self.operand
                return
        elif self.instruction == 4:
            self.bxc()
        elif self.instruction == 5:
            self.out()
        elif self.instruction == 6:
            self.bdv()
        elif self.instruction == 7:
            self.cdv()
        self.ip += 2
        print(self)

    def comboOperand(self):
        if self.operand in [0,1,2,3]:
            return self.operand
        elif self.operand == 4:
            return self.a
        elif self.operand == 5:
            return self.b
        elif self.operand == 6:
            return self.c
    
    def adv(self):
        self.operand = self.opcodes[self.ip + 1]
        operand = self.comboOperand()
        self.a = int(self.a / (2**operand))
    
    def bxl(self):
        self.operand = self.opcodes[self.ip + 1]
        self.b = (self.b ^ self.operand)

    def bst(self):
        self.operand = self.opcodes[self.ip+1]
        operand = self.comboOperand()
        self.b = ((operand % 8) & 7)
    
    def bxc(self):
        self.operand = self.opcodes[self.ip+1]
        self.b = (self.c ^ self.b)
    
    def out(self):
        self.operand = self.opcodes[self.ip+1]
        operand = self.comboOperand()
        self.output.append(operand % 8)
        if self.part2:
            m = min(len(self.output),len(self.correct_output))
            if self.output[:m] != self.correct_output[:m]:
                self.halted = True
                raise Exception("NO BUENO")
    
    def bdv(self):
        self.operand = self.opcodes[self.ip + 1]
        operand = self.comboOperand()
        self.b = int(self.a / (2**operand))
    
    def cdv(self):
        self.operand = self.opcodes[self.ip + 1]
        operand = self.comboOperand()
        self.c = int(self.a / (2**operand))

    def start(self):
        try:
            while True:
                self.read()
        except Exception as e:
            print("****** HALTED STATE!!! *******")
            print(self)
            print("ERROR: ", e)

    def __repr__(self):
        return f"A := {self.a}\nB := {self.b}\nC := {self.c}\nIP := {self.ip}\n\nOUTPUT = {','.join([str(i) for i in self.output])}\n\n{self.opcodes}"

data = data.split("\n\n")
data[0] = data[0].split("\n")
a = int(data[0][0].split("Register A: ")[1])
b = int(data[0][1].split("Register B: ")[1])
c = int(data[0][2].split("Register C: ")[1])
opcodes = [int(i) for i in data[1].split("Program: ")[1].split(",")]

pc = PC(a,b,c,opcodes)
print(pc)

pc.start()

# seconda parte

#_print = print
#def new_print(*args, **kwargs):
#    return
#print = new_print

output_giusto = [2,4, 1,2, 7,5, 4,5, 1,3, 5,5, 0,3, 3,0 ]
""" operazioni:
2 4 bst 4 -> B = (A % 8)  ... & 7
1 2 bxl 2 -> B = (B ^ 2)
7 5 cdv 5 -> C = |_ (A / 2^B) _|
4 5 bxc 5 -> B = (B ^ C)
1 3 bxl 3 -> B = (B ^ 3)
5 5 out 5 -> out.append( B )
0 3 adv 3 -> A = (A / 2^3)
3 0 jnz 0 -> ripete


A = 17
B=1 -> B=3 -> C=0, B=3, B=0,

"""
def f(x):
    output = []
    while x != 0:
        xm = (x % 8)^2
        output.append( ( xm ^ (int(x/2**xm)) ^ 3) % 8)
        x = int(x / 2**3)
    return output

# cerco a gruppi di 4
k1,k2,k3,k4 = 8**3,8**3,8**3,8**3
while f(k1) != output_giusto[0:4] and k1 <= 8**4:
    k1 +=1
while f(k2) != output_giusto[4:8] and k2 <= 8**4:
    k2 +=1
while f(k3) != output_giusto[8:12] and k3 <= 8**4:
    k3 +=1
while f(k4) != output_giusto[12:16] and k4 <= 8**4:
    k4 +=1
print(k1,k2,k3,k4)

_x = 8**15-1
# 35184401840000
while _x <= 8**16:
    _x = _x+1
    x = _x
    output = f(x)
    #pc = PC(_x,0,0,[2,4,1,2,7,5,4,5,1,3,5,5,0,3,3,0])
    #pc.start()
    #print("mio output: ", output)
    if _x % 10000 == 0:
        print("Trying: ",_x, (_x-(8**15-1))/(8**16-8**15)*100,"%", output)
    if output_giusto == output:
        print("Trovato con x: ",_x)
        break

pc.a = 815892000
a = -1
code = [2]
while True:
    a += 1
    pc = PC(a,b,c,opcodes,True)
    pc.start()
    if pc.output[:len(code)] == code:
        print(a, " -> ",pc.output)
        asd=1

while pc.a<=2**32-1:
    pc.a += 1
    pc.start()
    if pc.a % 1000 == 0:
        _print("Trying: ",pc.a, pc.a/(2**32-1)*100,"%", pc.output)
    if pc.output == output_giusto:
        _print("\nTROVATO: ",pc.a)
        break