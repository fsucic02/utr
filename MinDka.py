import sys

input = []
for line in sys.stdin:
    input.append(line) # u ovu listu spremam sve linije

stanja = input[0].strip().split(",")
abeceda = input[1].strip().split(",")
prihvatljiva_stanja = input[2].strip().split(",")
pocetno_stanje = input[3].strip()
funkcija = input[4:]
prijelazi = {} # dict prijelazi u obliku (trenutno_stanje, simbol_abecede)->iduce_stanje

for prijelaz in funkcija: # svaki prijelaz stavljamo u dict prijelazi
    prijelaz = prijelaz.strip() # makivamo \n
    trenutno_stanje = prijelaz.split("->")[0].split(",")[0]
    simbol_abecede = prijelaz.split("->")[0].split(",")[1]
    iduce_stanje = prijelaz.split("->")[1].split(",")[0]
    prijelazi[(trenutno_stanje, simbol_abecede)] = iduce_stanje

# minimizacija dka: prvo izbacimo nedohvatljiva stanja
# prvo cemo pronaci sva dohvatljiva tako sto cemo runnati jednostavan dfs
dohvatljiva_stanja = []
def dfs(stanje):
    dohvatljiva_stanja.append(stanje) # prvo dodamo stanje u listu dohvatljivih
    for simbol in abeceda: # za svaki simbol abecede
        iduce_stanje = prijelazi.get((stanje, simbol), []) # gledamo postoji li prijelaz
        if iduce_stanje and iduce_stanje not in dohvatljiva_stanja: # ako prijelaz postoji iduce stanje nije vec u dohvatljivim
            dfs(iduce_stanje) # runnamo dfs iz iduceg stanja

dfs(pocetno_stanje) # nakon ovoga su nam dohvatljiva stanja u listi dohvatljiva_stanja

for stanje in stanja.copy():
    if stanje not in dohvatljiva_stanja:
        stanja.remove(stanje) # brisemo nedohvatljiva stanja iz skupa stanja
        if stanje in prihvatljiva_stanja:
            prihvatljiva_stanja.remove(stanje) # brisemo ga i iz skupa prihvatljivih

for prijelaz in list(prijelazi):
    if prijelaz[0] not in dohvatljiva_stanja:
        del prijelazi[(prijelaz[0], prijelaz[1])]
    elif prijelazi[prijelaz] not in dohvatljiva_stanja:
        del prijelazi[prijelaz]

# za pronalazenje istovjetnih stanja koristit cu 3. algoritam
# koristim dvodimenzionalnu matricu, sve je postavljeno na 1
# pretpostavljamo da su sva istovjetna pa korak po korak
# izbacujemo parove koji nisu
matrica = [[0 for _ in range(len(dohvatljiva_stanja))] for _ in range(len(dohvatljiva_stanja))] # probaj stavit 1 for _ in range pa vidi
dohvatljiva_stanja.sort()
for i in range(len(dohvatljiva_stanja)):
    for j in range(len(dohvatljiva_stanja)):
        matrica[i][j] = 1

for i in range(1, len(dohvatljiva_stanja)):
    for j in range(0, i):
        if (dohvatljiva_stanja[i] in prihvatljiva_stanja and dohvatljiva_stanja[j] not in prihvatljiva_stanja) or (dohvatljiva_stanja[i] not in prihvatljiva_stanja and dohvatljiva_stanja[j] in prihvatljiva_stanja):
            matrica[i][j] = 0  # oznacavamo parove stanja (p, q) za koje vrijedi p∈F i q∉F


liste = {} # dict oblika (stanje1, stanje2): lista parova oblika (stanje3, stanje4)
posjeceni = []

def oznaci(i, j):
    i, j = max(i, j), min(i, j)
    matrica[i][j] = 0
    posjeceni.append((i, j))
    temp = liste.get((dohvatljiva_stanja[i], dohvatljiva_stanja[j]), []) 

    if temp:
        for par_stanja in temp:
            idx1 = dohvatljiva_stanja.index(par_stanja[0])
            idx2 = dohvatljiva_stanja.index(par_stanja[1])
            idx1, idx2 = max(idx1, idx2), min(idx1, idx2)
            if (idx1, idx2) not in posjeceni:
                oznaci(idx1, idx2)

for i in range(1, len(dohvatljiva_stanja)):
    for j in range(0, i):
        p = dohvatljiva_stanja[i]
        q = dohvatljiva_stanja[j]
        for simbol in abeceda:
            delta_p = prijelazi.get((p, simbol), []) # stanje δ(p, simbol)
            delta_q = prijelazi.get((q, simbol), []) # stanje δ(q, simbol)
            delta_p, delta_q = max(delta_p, delta_q, min(delta_p, delta_q))
            idx1 = dohvatljiva_stanja.index(delta_p) # index za matricu stanja δ(p, simbol)
            idx2 = dohvatljiva_stanja.index(delta_q) # index za matricu stanja δ(q, simbol)
            idx1, idx2 = max(idx1, idx2), min(idx1, idx2)
            if matrica[idx1][idx2] == 0: # ako su stanja δ(p, simbol) i δ(q, simbol) oznacena, onda oznacavamo i (p, q)
                oznaci(i, j)
            else:
                if delta_p != delta_q:
                    temp = liste.get((delta_p, delta_q), []) # dohvacamo listu koja je uz par stanja (delta_p, delta_q)
                    temp.append((p, q)) # appendamo stanja p, q
                    liste[(delta_p, delta_q)] = temp # stavljamo tu novu listu kao vrijednost uz kljuc delta_p, delta_q

# nakon ovog su parovi stanja (dohvatljiva_stanja[i], dohvatljiva_stanja[j]) u matrici matrica na mjestima gdje je
# matrica[i][j] = 1 istovjetni

for i in range(1, len(dohvatljiva_stanja)):
    for j in range(0, i):

        if matrica[i][j] == 1:
            # par stanja je istovjetan, moramo ostaviti samo ono leksikografski manje
            for prijelaz in list(prijelazi):
                if prijelaz[0] == dohvatljiva_stanja[i]: # brisemo prijelaze za leksikografski vece stanje
                    del prijelazi[(prijelaz[0], prijelaz[1])]
                    if dohvatljiva_stanja[i] in prihvatljiva_stanja:
                        prihvatljiva_stanja.remove(dohvatljiva_stanja[i]) # brisemo to stanje iz prihvatljivih
                    if dohvatljiva_stanja[i] in stanja:
                        stanja.remove(dohvatljiva_stanja[i]) # brisemo to stanje iz skupa svih stanja
                    if pocetno_stanje == dohvatljiva_stanja[i]:
                        pocetno_stanje = dohvatljiva_stanja[j]
                elif prijelazi[prijelaz] == dohvatljiva_stanja[i]: # ako prelazimo u to stanje
                    prijelazi[prijelaz] = dohvatljiva_stanja[j] # overwriteamo taj prijelaz tako da stavimo leksikografski manje, ali istovjetno stane


print(",".join(stanja))
print(",".join(abeceda))
print(",".join(prihvatljiva_stanja))
print(pocetno_stanje)
for prijelaz in prijelazi:
    print(f"{prijelaz[0]},{prijelaz[1]}->{prijelazi[prijelaz]}")