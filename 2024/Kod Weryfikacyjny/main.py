class KodWeryfikacyjny:
    def __init__(self, slowo):
        self.slowo = slowo
        self.mapowanie_liter_na_cyfry = {
            'zero': '0', 'jeden': '1', 'dwa': '2', 'trzy': '3', 'cztery': '4',
            'piec': '5', 'szesc': '6', 'siedem': '7', 'osiem': '8', 'dziewiec': '9'
        }

    def zlicz_litery(self):
        zliczenie_liter = {}
        for litera in self.slowo:
            if litera in zliczenie_liter:
                zliczenie_liter[litera] += 1
            else:
                zliczenie_liter[litera] = 1
        return zliczenie_liter

    def odtworz_cyfry(self, zliczenie_liter):
        cyfry = ''
        for cyfra_slownie, cyfra in self.mapowanie_liter_na_cyfry.items():
            while cyfra_slownie in self.slowo:
                cyfry += cyfra
                self.slowo = self.slowo.replace(cyfra_slownie, '', 1)
        if len(cyfry) < len(self.slowo):
            for cyfra_slownie, cyfra in self.mapowanie_liter_na_cyfry.items():
                liczba_wystapien = min(zliczenie_liter.get(litera, 0) for litera in cyfra_slownie)
                if liczba_wystapien > 0:
                    cyfry += cyfra * liczba_wystapien
                    for litera in cyfra_slownie:
                        zliczenie_liter[litera] -= liczba_wystapien
                        if zliczenie_liter[litera] <= 0:
                            del zliczenie_liter[litera]
        return cyfry

    def generuj_kod(self):
        zliczenie_liter = self.zlicz_litery()
        cyfry = self.odtworz_cyfry(zliczenie_liter)
        kod = ''.join(sorted(cyfry, reverse=True))
        return int(kod)

if __name__ == "__main__":
    debug = False

    if debug:
        testy = {
            'r5c0a': (7, 'pawiecd', 52),
            'r5c0b': (16, 'dwazerodwacztery', 4220),
            'r5c0c': (10, 'trzypiec', 53),
            'r5c0d': (14, 'czterycztery', 44),
        }

        for nazwa_testu, (dlugosc, wejscie, oczekiwane_wyjscie) in testy.items():
            kod_weryfikacyjny = KodWeryfikacyjny(wejscie)
            wynik = kod_weryfikacyjny.generuj_kod()
            assert wynik == oczekiwane_wyjscie, f"Błąd w teście {nazwa_testu}: oczekiwano {oczekiwane_wyjscie}, otrzymano {wynik}"
    else:
        n = int(input())
        slowo = input().strip()
        kod_weryfikacyjny = KodWeryfikacyjny(slowo)
        wynik = kod_weryfikacyjny.generuj_kod()
        print(f"{wynik}.")
