import sys

ulaz = []
for linija in sys.stdin:
    ulaz.append(linija) # u ovu listu spremam sve linije

""" gramatika
S -> aAB 
S -> bBA
A -> bC
A -> a
B -> ccSbc
B -> ε
C -> AA
"""

niz = ulaz[0].strip()
duljina = len(niz)
idx = 0
izlaz = []

def prekid():
    print(''.join(izlaz))
    print("NE")
    quit()

def S():
    izlaz.append('S')

    global idx 
    if idx >= duljina:
        prekid()
    else:
        if niz[idx] == 'a':
            idx += 1
            A()
            B()
        elif niz[idx] == 'b':
            idx += 1
            B()
            A()
        else:
            prekid()

def A():
    izlaz.append('A')

    global idx 
    if idx >= duljina:
        prekid()
    else:
        if niz[idx] == 'b':
            idx += 1
            C()
        elif niz[idx] == 'a':
            idx += 1
        else:
            prekid()

def B():
    izlaz.append('B')

    global idx 
    if idx + 1 < duljina and niz[idx] == 'c' and niz[idx + 1] == 'c':
        idx += 2
        S()
    
    if idx + 1 < duljina and niz[idx] == 'b' and niz[idx + 1] == 'c':
        idx += 2
        
def C():
    izlaz.append('C')

    A()
    A()

S()
print(''.join(izlaz))
print("DA") if idx == duljina else print("NE")