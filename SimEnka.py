import sys

input = []
for line in sys.stdin:
    input.append(line) # u ovu listu spremam sve linije

nizovi = [niz.strip().split(",") for niz in input[0].split("|")] # ulazni nizovi
funkcija = input[5:] # funkcija prijelaza
pocetno_stanje = input[4].strip() # pocetno stanje
prijelazi = {} # prijelazi u obliku tuple (stanje, znak) -> stanje (stanje je potencijalno skup stanja)

# nesto slicno dfs-u za trazenje epsilon okolina stanja
# vracam listu stanja koja su u epsilon okolini stanja stanje
def epsilon_okolina(stanje, posjeceni):
    rez = []
    posjeceni.append(stanje)
    eps = prijelazi.get((stanje, "$"), []) # izbjegavam key error
    if len(eps) == 0: # ako nema epsilon prijelaza,
        return rez # vracam praznu listu
    else:
        for el in eps:
            rez.append(el)
            if el not in posjeceni: # za sva neposjecena stanja vrtim rekurziju
                rez += epsilon_okolina(el, posjeceni) # rezultat tih poziva dodajem u rez
    
    return rez

for prijelaz in funkcija: # za svaki prijelaz radim par u dictu prijelazi
    prijelaz = prijelaz.strip()
    p1 = prijelaz.split("->") # splitam po "->", p1[0] ce bit (stanje, znak), p1[1] ce bit stanje u koje prelazimo (ili skup stanja u koja prelazimo)
    [stanje1, znak] = p1[0].split(",")
    stanje2 = p1[1].split(",") # u slucaju da je skup stanja, ak nije nikom nis
    if stanje2 != ["#"]: # nepotreban prijelaz u prazan skup
        prijelazi[(stanje1, znak)] = stanje2

for niz in nizovi:
    q0 = epsilon_okolina(pocetno_stanje, [])
    q0.append(pocetno_stanje) # lista pocetnih stanja (nije dovoljno uzeti samo pocetno stanje, nego i stanja koja su u njegovoj epsilon okolini)

    #lista u koju spremam ispise za pojedini znak niza
    ispis = [q0]
    for znak in niz:
        # za svako stanje iz liste ispis prvo gledamo prijelaz za znak, onda gledamo epsilon okoline tih stanja
        sljedeca_stanja = []
        for stanje in q0:
            eps = [] # lista u koju cu spremiti sva stanja u epsilon okolini svih stanja koje dobijem ucitavanjem znaka
            sljedece_stanje = prijelazi.get((stanje, znak), []) # efektivno ucitavamo znak

            for sstanje in sljedece_stanje:
                eps_okolina = epsilon_okolina(sstanje, []) # za svako od sljedecih stanja gledamo epsilon prijelaze
                for el in eps_okolina: # ne zelim duplikate, usporava izvodenje programa
                    eps.append(el)

            for el in eps:
                if el not in sljedece_stanje: # izbjegavam duplikate, inace dobivam timeout za test 33
                    sljedece_stanje.append(el)

            for el in sljedece_stanje:
                if el not in sljedeca_stanja: # izbjegavam duplikate, inace dobivam timeout za test 33
                    sljedeca_stanja.append(el)

        ispis.append(sljedeca_stanja) # dodamo rezultat u listu ispis
        q0 = sljedeca_stanja # pocetna stanja su sad rezultat svog ucitavanja i episilon prijelaza

    for i in range(len(ispis)):
        skup = list(set(ispis[i])) # makivam potencijalne duplikate
        skup.sort() # leksikografski poredak
        # formatiranje printanja
        if i != 0:
            print("|", end = "")
        if len(skup) == 0:
            print("#", end = "")
        else:
            print(",".join(skup), end = "")
    else:
        print() # \n