from enum import Enum, auto

# Stwórz wyliczenie dla statusu piłki
class StatusPilki(Enum):
    PORUSZA_SIE = auto()
    ZATRZYMALA_SIE = auto()

# Klasa reprezentująca piłkę
class Pilka:
    def __init__(self):
        self.status = StatusPilki.ZATRZYMALA_SIE
        self.pozycja_x = 0
        self.pozycja_y = 0

    def zmien_status(self, nowy_status):
        self.status = nowy_status

    def ustaw_pozycje(self, x, y):
        self.pozycja_x = x
        self.pozycja_y = y

# Klasa reprezentująca planszę
class Plansza:
    def __init__(self, n, m):
        self.plansza = [["#" for i in range(m)] for j in range(n)]
        self.n = n
        self.m = m
        self.pilka = Pilka()

    def wczytaj_plansze(self):
        with open("plansza.txt", "r") as f:
            n, m = map(int, f.readline().split())
            self.plansza = [list(line.strip()) for line in f]
            self.n = n
            self.m = m

        print("Plansza została wczytana.")

    def obroc_plansze(self, kierunek):
        if self.pilka.status == StatusPilki.ZATRZYMALA_SIE:
            if kierunek == "w lewo":
                self.obroc_plansze_w_lewo()
            elif kierunek == "w prawo":
                self.obroc_plansze_w_prawo()
        else:
            print("Nie można obrócić planszy, gdy piłka się porusza.")

    def obroc_plansze_w_lewo(self):
        nowa_plansza = [[self.plansza[j][self.m - 1 - i] for j in range(self.n)] for i in range(self.m)]
        self.plansza, self.n, self.m = nowa_plansza, self.m, self.n

    def obroc_plansze_w_prawo(self):
        nowa_plansza = [[self.plansza[self.n - 1 - j][i] for j in range(self.n)] for i in range(self.m)]
        self.plansza, self.n, self.m = nowa_plansza, self.m, self.n

    def znajdz_pozycje_poczatkowa_i_koncowa(self):
        pozycja_P = None
        pozycja_K = None
        for i in range(self.n):
            for j in range(self.m):
                if self.plansza[i][j] == "P":
                    pozycja_P = (i, j)
                elif self.plansza[i][j] == "K":
                    pozycja_K = (i, j)
        if pozycja_P is None or pozycja_K is None:
            raise ValueError("Plansza musi zawierać zarówno P jak i K")
        return pozycja_P, pozycja_K

    def symulacja_ruchu(self):
        pozycja_P, pozycja_K = self.znajdz_pozycje_poczatkowa_i_koncowa()
        self.pilka.ustaw_pozycje(*pozycja_P)
        ruchy = 0
        while self.pilka.pozycja_x != pozycja_K[0] or self.pilka.pozycja_y != pozycja_K[1]:
            self.pilka.zmien_status(StatusPilki.PORUSZA_SIE)
            if self.pilka.pozycja_y < pozycja_K[1]:
                self.obroc_plansze("w prawo")
                self.pilka.pozycja_y = self.n - 1 - self.pilka.pozycja_x
                self.pilka.pozycja_x = self.m - 1 - self.pilka.pozycja_y
            else:
                self.obroc_plansze("w lewo")
                self.pilka.pozycja_x = self.m - 1 - self.pilka.pozycja_y
                self.pilka.pozycja_y = self.n - 1 - self.pilka.pozycja_x
            
def main():
    # Ustaw parametry gry
    n = 5  # Wysokość planszy
    m = 5  # Szerokość planszy
    tryb_testowy = True

    # Utwórz planszę
    plansza = Plansza(n, m)

    # Wczytaj planszę (z pliku lub użytkownika)
    if tryb_testowy:
        plansza.plansza = [
            ["#", "#", "#", "#", "#"],
            ["#", "P", ".", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", "K", ".", ".", "#"],
            ["#", "#", "#", "#", "#"],
        ]
    else:
        plansza.wczytaj_plansze()

    # Symulacja gry
    try:
        liczba_ruchow = plansza.symulacja_ruchu()
        if liczba_ruchow == 0:
            print("-1")  # Nie można przejść z P do K
        else:
            print(liczba_ruchow)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()