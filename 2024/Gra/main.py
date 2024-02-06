class Poczatek:
    def __init__(self, wspolrzedne):
        self.wspolrzedne = wspolrzedne

    def aktualizuj(self, nowe_wspolrzedne):
        self.wspolrzedne = nowe_wspolrzedne
        print(f"Nowe współrzędne początku: {self.wspolrzedne}")

class Koniec:
    def __init__(self, wspolrzedne):
        self.wspolrzedne = wspolrzedne

    def aktualizuj(self, nowe_wspolrzedne):
        self.wspolrzedne = nowe_wspolrzedne
        print(f"Nowe współrzędne końca: {self.wspolrzedne}")

class Plansza:
    def __init__(self, wysokosc, szerokosc, schemat):
        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.schemat = [list(wiersz) for wiersz in schemat]
        self.poczatek = Poczatek(self.znajdz_pozycje('P'))
        self.koniec = Koniec(self.znajdz_pozycje('K'))

    def znajdz_pozycje(self, symbol):
        for y, wiersz in enumerate(self.schemat):
            if symbol in wiersz:
                return (y, wiersz.index(symbol))
        return None

    def obroc_w_lewo(self):
        print("Mapa przed obróceniem w lewo:")
        self.wyswietl()
        self.schemat = [list(x) for x in zip(*self.schemat[::-1])]
        nowe_wspolrzedne_poczatku = self.znajdz_pozycje('P')
        nowe_wspolrzedne_konca = self.znajdz_pozycje('K')
        self.poczatek.aktualizuj(nowe_wspolrzedne_poczatku)
        self.koniec.aktualizuj(nowe_wspolrzedne_konca)
        self.symuluj_upadek()
        print("Mapa po obróceniu w lewo:")
        self.wyswietl()

    def obroc_w_prawo(self):
        print("Mapa przed obróceniem w prawo:")
        self.wyswietl()
        self.schemat = [list(reversed(x)) for x in zip(*self.schemat)]
        nowe_wspolrzedne_poczatku = self.znajdz_pozycje('P')
        nowe_wspolrzedne_konca = self.znajdz_pozycje('K')
        self.poczatek.aktualizuj(nowe_wspolrzedne_poczatku)
        self.koniec.aktualizuj(nowe_wspolrzedne_konca)
        self.symuluj_upadek()
        print("Mapa po obróceniu w prawo:")
        self.wyswietl()

    def symuluj_upadek(self):
        y, x = self.poczatek.wspolrzedne
        while y + 1 < self.wysokosc and self.schemat[y + 1][x] == '.':
            y += 1
        self.poczatek.aktualizuj((y, x))
        print(f"P spadł na pozycję: {self.poczatek.wspolrzedne}")

    def wyswietl(self):
        for wiersz in self.schemat:
            print(''.join(wiersz))

class Gra:
    def __init__(self, wymiary):
        wymiary = wymiary.split()
        wysokosc, szerokosc = int(wymiary[0]), int(wymiary[1])
        schemat = [
            "####",
            "#K.#",
            "#..#",
            "#P.#",
            "####"
        ]
        self.plansza = Plansza(wysokosc, szerokosc, schemat)

    def uruchom(self):
        while True:
            self.plansza.wyswietl()
            komenda = input("Obróć w lewo (l) czy w prawo (p)? ")
            if komenda == "l":
                self.plansza.obroc_w_lewo()
            elif komenda == "p":
                self.plansza.obroc_w_prawo()
            else:
                break

if __name__ == "__main__":
    wymiary = "5 4"
    gra = Gra(wymiary)
    gra.uruchom()