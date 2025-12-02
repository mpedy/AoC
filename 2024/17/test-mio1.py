from z3 import *

def f(x):
    xi = ((x % 8) ^ 2)
    return (((x % 8) ^ 2) ^ 3 ^ (x >> ((x % 8) ^ 2)) ) % 8

def fw(x):
    output = []
    while x != 0:
        output.append(f(x))
        x= x >> 3
    return output

N_BITS = 64

output = [2,4,1,2,7,5,4,5,1,3,5,5,0,3,3,0]

s = Solver()

x = BitVec("x",N_BITS)

r = 16
for i in range(r):
    xi = (((x>>(i*3)) & 7) ^ 2)
    s.add( (xi ^ 3 ^ ((x>>(i*3)) >> xi)) & 7 == output[i])
s.add( (x>>(i+1)*3) == 0)
if s.check() == sat:
    print(s.model())
else:
    print("No solution")




# Definizione della variabile x come BitVec (32 bit, per gestire numeri interi grandi)
x = BitVec("x", 64)

# Creazione del solver
opt = Solver()

r = 8
for i in range(r):
    # Espressione f(x)
    mod_8 = (x>>(i*3)) & 7  # x % 8 equivale a x & 7 nei BitVec
    shift_amount = mod_8 ^ 2  # XOR tra mod_8 e 2
    expr = (((mod_8 ^ 2) ^ 3 ^ ( (x>>(i*3)) >> shift_amount)) & 7)  # f(x) modulo 8 equivale a & 7

    # Creazione dei vincoli
    opt.add(expr == output[i])  # f(x) deve essere uguale a 2
opt.add(x >> ((i+1)*3) == 0)
# Minimizzare x
#opt.minimize(x)

# Risolvere il problema
if opt.check() == sat:
    model = opt.model()
    print("Soluzione trovata:")
    print(f"x = {model[x]}")
    print(fw(model[x].as_long())[:r], " -- ", output[:r])
else:
    print("Nessuna soluzione trovata.")