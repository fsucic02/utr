import sys

input = []
for line in sys.stdin:
    input.append(line) # u ovu listu spremam sve linije

nizovi = [niz.strip().split(",") for niz in input[0].split("|")] # ulazni nizovi
stanja = input[1].strip().split(",")
funkcija = input[7:] # funkcija prijelaza
pocetno_stanje = input[5].strip() # pocetno stanje
pocetno_stanje_stoga = input[6].strip()
prihvatljiva_stanja = input[4].strip().split(",")

prijelazi = {} # prijelazi oblika (trenutno_stanje, ulazni_znak, znak_stoga): (novo_stanje, niz_znakova_stoga)

for prijelaz in funkcija: 
    prijelaz = prijelaz.strip()
    trenutno_stanje = prijelaz.split("->")[0].split(",")[0]
    ulazni_znak = prijelaz.split("->")[0].split(",")[1]
    znak_stoga = prijelaz.split("->")[0].split(",")[2]
    novo_stanje = prijelaz.split("->")[1].split(",")[0]
    niz_znakova_stoga = prijelaz.split("->")[1].split(",")[1]
    prijelazi[(trenutno_stanje, ulazni_znak, znak_stoga)] = (novo_stanje, niz_znakova_stoga)

for niz in nizovi:
    stog = [pocetno_stanje_stoga] # na vrh stoga stavljamo pocetno stanje
    trenutno_stanje = pocetno_stanje # trenutno smo u pocetnom stanju
    ispis = [f"{pocetno_stanje}#{stog[-1]}"]

    for znak in niz: # za znak niza
        # moramo epsilon prijelaze napraviti koliko god ih ima
        epsilon_prijelaz = prijelazi.get((trenutno_stanje, "$", stog[-1]), [])

        while epsilon_prijelaz:
            trenutno_stanje = epsilon_prijelaz[0]
            niz_znakova_stoga = epsilon_prijelaz[1]

            if niz_znakova_stoga == "$":
                stog.pop()
                if len(stog) == 0:
                    stog.append("$")
            else:
                if len(niz_znakova_stoga) == 1:
                    if niz_znakova_stoga == stog[-1]:
                        pass
                    else:
                        stog.pop()
                        stog.append(niz_znakova_stoga)
                else:
                    stog.pop()
                    for znak_stoga in niz_znakova_stoga[::-1]:
                        stog.append(znak_stoga)

            ispis_stoga = "".join(stog[::-1])
            ispis.append(f"{trenutno_stanje}#{ispis_stoga}")
            epsilon_prijelaz = prijelazi.get((trenutno_stanje, "$", stog[-1]), [])

        prijelaz = prijelazi.get((trenutno_stanje, znak, stog[-1]), [])

        if not prijelaz: # ne postoji prijelaz
            # moramo obaviti epsilon prijelaze

            ispis.append("fail")
            zavrsili_u_prihvatljivom = 0
            epsilon_prijelaz = prijelazi.get((trenutno_stanje, "$", stog[-1]), [])

            while epsilon_prijelaz and not zavrsili_u_prihvatljivom:
                trenutno_stanje = epsilon_prijelaz[0]
                niz_znakova_stoga = epsilon_prijelaz[1]

                if niz_znakova_stoga == "$":
                    stog.pop()
                    if len(stog) == 0:
                        stog.append("$")
                else:
                    if len(niz_znakova_stoga) == 1:
                        if niz_znakova_stoga == stog[-1]:
                            pass
                        else:
                            stog.pop()
                            stog.append(niz_znakova_stoga)
                    else:
                        stog.pop()
                        for znak_stoga in niz_znakova_stoga[::-1]:
                            stog.append(znak_stoga)

                ispis_stoga = "".join(stog[::-1])
                ispis.append(f"{trenutno_stanje}#{ispis_stoga}")

                if trenutno_stanje in prihvatljiva_stanja:
                    zavrsili_u_prihvatljivom = 1

                epsilon_prijelaz = prijelazi.get((trenutno_stanje, "$", stog[-1]), [])

            if not zavrsili_u_prihvatljivom:
                ispis.append("0")
            else:
                ispis.append("1")
            
            print("|".join(ispis))
            break
        else: # prijelaz postoji
            novo_stanje = prijelaz[0]
            niz_znakova_stoga = prijelaz[1]

            if niz_znakova_stoga == "$":
                stog.pop()
                if len(stog) == 0:
                    stog.append("$")
            else:
                if len(niz_znakova_stoga) == 1:
                    if niz_znakova_stoga == stog[-1]:
                        pass
                    else:
                        stog.pop()
                        stog.append(niz_znakova_stoga)
                else:
                    stog.pop()
                    for znak_stoga in niz_znakova_stoga[::-1]:
                        stog.append(znak_stoga)

            trenutno_stanje = novo_stanje
            ispis_stoga = "".join(stog[::-1])
            ispis.append(f"{trenutno_stanje}#{ispis_stoga}")
    else: # procitali smo cijeli niz
        if trenutno_stanje in prihvatljiva_stanja:
            ispis.append("1")
        else:
            zavrsili_u_prihvatljivom = 0
            epsilon_prijelaz = prijelazi.get((trenutno_stanje, "$", stog[-1]), [])

            while epsilon_prijelaz and not zavrsili_u_prihvatljivom:
                trenutno_stanje = epsilon_prijelaz[0]
                niz_znakova_stoga = epsilon_prijelaz[1]

                if niz_znakova_stoga == "$":
                    stog.pop()
                    if len(stog) == 0:
                        stog.append("$")
                else:
                    if len(niz_znakova_stoga) == 1:
                        if niz_znakova_stoga == stog[-1]:
                            pass
                        else:
                            stog.pop()
                            stog.append(niz_znakova_stoga)
                    else:
                        stog.pop()
                        for znak_stoga in niz_znakova_stoga[::-1]:
                            stog.append(znak_stoga)

                ispis_stoga = "".join(stog[::-1])
                ispis.append(f"{trenutno_stanje}#{ispis_stoga}")

                if trenutno_stanje in prihvatljiva_stanja:
                    zavrsili_u_prihvatljivom = 1

                epsilon_prijelaz = prijelazi.get((trenutno_stanje, "$", stog[-1]), [])

            if not zavrsili_u_prihvatljivom:
                ispis.append("0")
            else:
                ispis.append("1")
        
        print("|".join(ispis))