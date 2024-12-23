class Pracownik:
    def __init__(self, id, wydajnosc):
        if debug: print(f"[DEBUG] Tworzenie nowego pracownika: id={id}, wydajnosc={wydajnosc}")
        self.id = id
        self.wydajnosc = wydajnosc
        self.data_zatrudnienia = 0

    def zmien_wydajnosc(self, nowa_wydajnosc):
        if debug: print(f"[DEBUG] Zmiana wydajności pracownika {self.id}: {self.wydajnosc} -> {nowa_wydajnosc}")
        self.wydajnosc = nowa_wydajnosc

class Stanowisko:
    def __init__(self, numer):
        if debug: print(f"[DEBUG] Tworzenie nowego stanowiska nr {numer}")
        self.numer = numer
        self.pracownik = None
        self.historia = []  # [(pracownik, dzien_start, dzien_koniec)]

    def zatrudnij(self, pracownik, dzien):
        if debug: print(f"[DEBUG] Próba zatrudnienia pracownika {pracownik.id} na stanowisku {self.numer} w dniu {dzien}")
        if self.pracownik is None:
            self.pracownik = pracownik
            self.historia.append((pracownik, dzien, None))
            if debug: print(f"[DEBUG] Zatrudnienie udane")
            return True
        if debug: print(f"[DEBUG] Zatrudnienie nieudane - stanowisko zajęte")
        return False

    def zwolnij(self, dzien):
        if debug: print(f"[DEBUG] Próba zwolnienia pracownika ze stanowiska {self.numer} w dniu {dzien}")
        if self.pracownik is not None:
            self.historia[-1] = (self.historia[-1][0], self.historia[-1][1], dzien)
            self.pracownik = None
            if debug: print(f"[DEBUG] Zwolnienie udane")
            return True
        if debug: print(f"[DEBUG] Zwolnienie nieudane - brak pracownika")
        return False

class Produkcja:
    def __init__(self, n, poczatkowe_wydajnosci):
        if debug: print(f"[DEBUG] Inicjalizacja produkcji: {n} stanowisk, wydajności: {poczatkowe_wydajnosci}")
        self.liczba_stanowisk = n
        self.stanowiska = [Stanowisko(i) for i in range(1, n + 1)]
        self.dzienna_produkcja = {}  # słownik przechowujący produkcję dzienną
        
        # Inicjalizacja początkowych pracowników
        for i in range(n):
            pracownik = Pracownik(i+1, poczatkowe_wydajnosci[i])
            self.stanowiska[i].zatrudnij(pracownik, 0)
            
    def oblicz_produkcje(self, start_stanowisko, koniec_stanowisko, dzien):
        if debug: print(f"[DEBUG] Obliczanie produkcji dla stanowisk {start_stanowisko}-{koniec_stanowisko} za dni 0-{dzien}")
        suma = 0

        # Dla każdego stanowiska w zakresie
        for nr_stanowiska in range(start_stanowisko - 1, koniec_stanowisko):
            stanowisko = self.stanowiska[nr_stanowiska]
            
            # Sprawdź pracownika na tym stanowisku
            for wpis in stanowisko.historia:
                pracownik, start, koniec = wpis
                
                # Jeśli pracownik pracował w tym okresie
                if (koniec is None or koniec >= 0) and start <= dzien:
                    # Oblicz ile dni pracował w zadanym okresie
                    efektywny_start = max(start, 0)
                    efektywny_koniec = min(koniec if koniec is not None else dzien, dzien)
                    dni_pracy = efektywny_koniec - efektywny_start + 1
                    
                    # Dodaj jego produkcję
                    suma += dni_pracy * pracownik.wydajnosc

        if debug: print(f"[DEBUG] Całkowita produkcja: {suma}")
        return suma

    def zmien_wydajnosc(self, nr_stanowiska, nowa_wydajnosc):
        if debug: print(f"[DEBUG] Próba zmiany wydajności na stanowisku {nr_stanowiska} na {nowa_wydajnosc}")
        stanowisko = self.stanowiska[nr_stanowiska - 1]
        if stanowisko.pracownik:
            stanowisko.pracownik.zmien_wydajnosc(nowa_wydajnosc)
            if debug: print(f"[DEBUG] Zmiana wydajności udana")
            return True
        if debug: print(f"[DEBUG] Zmiana wydajności nieudana - brak pracownika")
        return False

    def zwolnij_pracownika(self, nr_stanowiska, czas):
        if debug: print(f"[DEBUG] Próba zwolnienia pracownika ze stanowiska {nr_stanowiska} w czasie {czas}")
        return self.stanowiska[nr_stanowiska - 1].zwolnij(czas)

    def zatrudnij_pracownika(self, nr_stanowiska, wydajnosc, czas):
        if debug: print(f"[DEBUG] Próba zatrudnienia pracownika na stanowisku {nr_stanowiska} z wydajnością {wydajnosc} w czasie {czas}")
        stanowisko = self.stanowiska[nr_stanowiska - 1]
        if stanowisko.pracownik is None:
            nowy_pracownik = Pracownik(nr_stanowiska, wydajnosc)
            return stanowisko.zatrudnij(nowy_pracownik, czas)
        return False

def waliduj_dane(n, q, wydajnosci):
    if debug: print(f"[DEBUG] Walidacja danych: n={n}, q={q}, wydajności={wydajnosci}")
    if not (1 <= n <= 10**6 and 1 <= q <= 10**6):
        raise ValueError("Nieprawidłowa liczba stanowisk lub zapytań")
    
    if len(wydajnosci) != n:
        raise ValueError("Nieprawidłowa liczba wydajności początkowych")
    
    if not all(0 <= v <= 10**3 for v in wydajnosci):
        raise ValueError("Nieprawidłowa wartość wydajności")

def debug_test(test_name, input_data):
    print(f"\n[DEBUG] Uruchamianie testu: {test_name}")
    print("[DEBUG] Wejście:")
    for line in input_data.strip().split('\n'):
        print(f"[DEBUG] {line}")
    
    # Zapisz obecne stdin
    import sys
    from io import StringIO
    old_stdin = sys.stdin
    sys.stdin = StringIO(input_data)
    
    print("\n[DEBUG] Wyjście:")
    main()
    
    # Przywróć stdin
    sys.stdin = old_stdin

def run_debug_tests():
    # Test r2d0a
    test_r2d0a = """5 7
1 2 3 2 4
Q 1 5 2
Q 2 3 2
F 2 3
V 3 5 3
Q 2 4 4
H 2 5 6
Q 1 5 8"""

    # Test r2d0b
    test_r2d0b = """1 7
2
Q 1 1 1
F 1 1
H 1 6 2
Q 1 1 3
Q 1 1 4
Q 1 1 7
Q 1 1 8"""

    debug_test("r2d0a", test_r2d0a)
    debug_test("r2d0b", test_r2d0b)

def main():
    try:
        if debug: print("[DEBUG] Rozpoczęcie programu")
        # Wczytanie pierwszej linii
        n, q = map(int, input().split())
        
        # Wczytanie wydajności pracowników
        wydajnosci = list(map(int, input().split()))
        
        # Dodane wyświetlanie metadanych
        print(f"Liczba stanowisk: {n}")
        print(f"Liczba zapytań: {q}")
        print(f"Początkowe wydajności: {wydajnosci}")
        print("---")  # separator
        
        # Pozostała część kodu...
        if debug: print(f"[DEBUG] Wczytano n={n}, q={q}")
        if debug: print(f"[DEBUG] Wczytano wydajności: {wydajnosci}")
        
        # Walidacja danych wejściowych
        waliduj_dane(n, q, wydajnosci)
        
        # Utworzenie systemu produkcji
        produkcja = Produkcja(n, wydajnosci)
        
        # Lista do przechowywania wszystkich zapytań i ich wyników
        zapytania = []
        
        # Najpierw zbieramy wszystkie zapytania
        for _ in range(q):
            zapytanie = input().split()
            zapytania.append(zapytanie)
        
        # Teraz wykonujemy operacje i wyświetlamy wyniki
        for zapytanie in zapytania:
            typ_operacji = zapytanie[0]
            
            if typ_operacji == 'V':
                i, v, t = map(int, zapytanie[1:])
                if not (1 <= i <= n and 0 <= v <= 10**3 and 0 <= t <= 10**9):
                    raise ValueError("Nieprawidłowe parametry dla operacji V")
                produkcja.zmien_wydajnosc(i, v)
                
            elif typ_operacji == 'F':
                i, t = map(int, zapytanie[1:])
                if not (1 <= i <= n and 0 <= t <= 10**9):
                    raise ValueError("Nieprawidłowe parametry dla operacji F")
                produkcja.zwolnij_pracownika(i, t)
                
            elif typ_operacji == 'H':
                i, v, t = map(int, zapytanie[1:])
                if not (1 <= i <= n and 0 <= v <= 10**3 and 0 <= t <= 10**9):
                    raise ValueError("Nieprawidłowe parametry dla operacji H")
                produkcja.zatrudnij_pracownika(i, v, t)
                
            elif typ_operacji == 'Q':
                i, j, t = map(int, zapytanie[1:])
                if not (1 <= i <= j <= n and 0 <= t <= 10**9):
                    raise ValueError("Nieprawidłowe parametry dla operacji Q")
                wynik = produkcja.oblicz_produkcje(i, j, t)
                print(wynik)

    except ValueError as e:
        if debug: print(f"[DEBUG] Błąd walidacji: {e}")
        print(f"Błąd: {e}")
    except Exception as e:
        if debug: print(f"[DEBUG] Nieoczekiwany błąd: {e}")
        print(f"Wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    debug = False  # Zmienna kontrolująca wyświetlanie debugów
    if debug:
        run_debug_tests()
    else:
        main()
