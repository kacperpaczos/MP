debug = False  # Globalna flaga debug
verbose = False  # Flaga dla szczegółowych komunikatów

class Pracownik:
    def __init__(self, wydajnosc, data_zatrudnienia):
        if verbose: print(f"[DEBUG] Tworzenie pracownika: wydajność={wydajnosc}, zatrudniony={data_zatrudnienia}")
        self.wydajnosc = wydajnosc
        self.data_zatrudnienia = data_zatrudnienia

class Stanowisko:
    def __init__(self, numer):
        if verbose: print(f"[DEBUG] Tworzenie stanowiska nr {numer}")
        self.numer = numer
        self.pracownik = None
        self.zaplanowane_zmiany = []
        self.dzienna_produkcja = 0
        self.produkcja_po_dniach = [0]  # Lista produkcji po każdym dniu
        self.debug_rejestr = []  # Dodajemy rejestr debugowania

    def dodaj_zmiane(self, dzien, typ_zmiany, parametry):
        if verbose: print(f"[DEBUG] Stanowisko {self.numer}: Dodano zmianę na dzień {dzien}: {typ_zmiany} {parametry}")
        if verbose and typ_zmiany != 'Q': 
            print(f"Zaplanowano zmianę dla stanowiska {self.numer} na dzień {dzien}: {self._opisz_zmiane(typ_zmiany, parametry)}")
        self.zaplanowane_zmiany.append((dzien, typ_zmiany, parametry))
        print(self.zaplanowane_zmiany)
        #self.zaplanowane_zmiany.sort(key=lambda x: x[0])

    def _opisz_zmiane(self, typ_zmiany, parametry):
        if typ_zmiany == 'H':
            return f"zatrudnienie pracownika (wydajność: {parametry['wydajnosc']})"
        elif typ_zmiany == 'F':
            return "zwolnienie pracownika"
        elif typ_zmiany == 'V':
            return f"zmiana wydajności na {parametry['wydajnosc']}"
        return ""

    def aktualizuj_dzien(self, aktualny_dzien):
        zmiany_na_dzien = [z for z in self.zaplanowane_zmiany if z[0] == aktualny_dzien]
        
        # Oblicz produkcję przed zmianami
        self.dzienna_produkcja = 0
        if self.pracownik:
            if any(z[1] == 'F' for z in zmiany_na_dzien):
                self.dzienna_produkcja = self.pracownik.wydajnosc  # Produkcja w dniu zwolnienia
            elif not any(z[1] == 'H' for z in zmiany_na_dzien):
                self.dzienna_produkcja = self.pracownik.wydajnosc

        # Aktualizuj listę produkcji
        if aktualny_dzien >= len(self.produkcja_po_dniach):
            poprzednia_produkcja = self.produkcja_po_dniach[-1]
            self.produkcja_po_dniach.append(poprzednia_produkcja + self.dzienna_produkcja)

        # Wykonaj zmiany po obliczeniu produkcji
        for zmiana in zmiany_na_dzien:
            typ_zmiany = zmiana[1]
            parametry = zmiana[2]
            
            if typ_zmiany == 'H':
                self.pracownik = Pracownik(parametry['wydajnosc'], aktualny_dzien)
            elif typ_zmiany == 'F':
                self.pracownik = None
            elif typ_zmiany == 'V':
                if self.pracownik:
                    self.pracownik.wydajnosc = parametry['wydajnosc']

        if debug:
            self.debug_rejestr.append({
                'dzien': aktualny_dzien,
                'produkcja': self.dzienna_produkcja,
                'wydajnosc': self.pracownik.wydajnosc if self.pracownik else 0,
                'zmiany': [z for z in zmiany_na_dzien]
            })
        return self.dzienna_produkcja

    def get_produkcja(self, dzien=None):
        """Zwraca całkowitą produkcję stanowiska do podanego dnia"""
        if dzien is None:
            dzien = len(self.produkcja_po_dniach) - 1
        if dzien >= len(self.produkcja_po_dniach):
            # Jeśli pytamy o dzień w przyszłości, zwracamy ostatnią znaną wartość
            return self.produkcja_po_dniach[-1]
        return self.produkcja_po_dniach[dzien]

    def _oblicz_produkcje_dnia(self, aktualny_dzien, zmiany_na_dzien):
        if not self.pracownik:
            return 0
        
        # Jeśli pracownik jest zwalniany, produkuje w tym dniu
        if any(z[1] == 'F' for z in zmiany_na_dzien):
            return self.pracownik.wydajnosc
        
        # Jeśli pracownik jest zatrudniany, nie produkuje w tym dniu
        if any(z[1] == 'H' for z in zmiany_na_dzien):
            return 0
        
        # Przy zmianie wydajności używamy starej wartości
        if any(z[1] == 'V' for z in zmiany_na_dzien):
            return self.pracownik.wydajnosc
        
        return self.pracownik.wydajnosc

class Produkcja:
    def __init__(self, n, poczatkowe_wydajnosci):
        if verbose: print(f"[DEBUG] Inicjalizacja produkcji: {n} stanowisk")
        if verbose: print(f"Inicjalizacja {n} stanowisk produkcyjnych")
        self.liczba_stanowisk = n
        self.stanowiska = [Stanowisko(i) for i in range(1, n + 1)]
        self.aktualny_dzien = 0
        self.max_dzien = 0
        self.zapytania = []
        
        # Inicjalizacja początkowych pracowników
        for i, wydajnosc in enumerate(poczatkowe_wydajnosci):
            self.stanowiska[i].dodaj_zmiane(0, 'H', {'wydajnosc': wydajnosc})

    def dodaj_zapytanie(self, typ, parametry):
        if verbose: print(f"[DEBUG] Dodano zapytanie: {typ} {parametry}")
        
        # Walidacja parametrów
        waliduj_parametry(typ, parametry, self.liczba_stanowisk)
        
        dzien = parametry.get('t', 0)
        self.max_dzien = max(self.max_dzien, dzien)

        if typ == 'Q':
            if verbose: print(f"Zaplanowano zapytanie o sumę produkcji stanowisk {parametry['i']}-{parametry['j']} na dzień {dzien}")
            self.zapytania.append((dzien, typ, parametry))
        else:
            stanowisko = self.stanowiska[parametry['i'] - 1]
            stanowisko.dodaj_zmiane(dzien, typ, parametry)

    def przelicz_dzien(self, dzien):
        """Przelicza jeden dzień produkcji"""
        if verbose: print(f"\n[DEBUG] === Rozpoczęcie dnia {dzien} ===")
        if verbose: print(f"\n=== Dzień {dzien} ===")
        
        # Aktualizuj każde stanowisko i zbierz produkcję
        dzienna_produkcja = 0
        for stanowisko in self.stanowiska:
            dzienna_produkcja += stanowisko.aktualizuj_dzien(dzien)
        
        if verbose: print(f"Łączna produkcja: {dzienna_produkcja} litrów soku")
        return dzienna_produkcja

    def symuluj(self):
        if verbose: print(f"[DEBUG] Rozpoczęcie symulacji na {self.max_dzien + 1} dni")
        if verbose: print(f"\nRozpoczęcie symulacji na {self.max_dzien + 1} dni\n")
        
        wyniki = []
        
        for dzien in range(self.max_dzien + 1):
            self.aktualny_dzien = dzien
            dzienna_produkcja = self.przelicz_dzien(dzien)
            
            # Sprawdź zapytania dla tego dnia
            for zap_dzien, typ, params in self.zapytania:
                if zap_dzien == dzien:
                    if typ == 'Q':
                        suma = 0
                        if debug: print(f"\n[DEBUG] Szczegóły zapytania Q dla dnia {dzien}:")
                        
                        for i in range(params['i'], params['j'] + 1):
                            stanowisko = self.stanowiska[i-1]
                            produkcja_stanowiska = stanowisko.get_produkcja(dzien)
                            if debug:
                                print(f"[DEBUG] Stanowisko {i}:")
                                for wpis in stanowisko.debug_rejestr:
                                    if wpis['dzien'] <= dzien:
                                        zmiany_opis = ", ".join([self._opisz_zmiane_debug(z) for z in wpis['zmiany']])
                                        print(f"  Dzień {wpis['dzien']}: produkcja={wpis['produkcja']} " +
                                              f"(wydajność={wpis['wydajnosc']}) " +
                                              f"{f'Zmiany: {zmiany_opis}' if zmiany_opis else ''}")
                                print(f"  Suma do dnia {dzien}: {produkcja_stanowiska}")
                            suma += produkcja_stanowiska
                        
                        if debug: print(f"[DEBUG] Łączna suma dla zapytania: {suma}")
                        wyniki.append(suma)
        
        return wyniki

    def _opisz_zmiane_debug(self, zmiana):
        typ = zmiana[1]
        params = zmiana[2]
        if typ == 'H':
            return f"zatrudnienie (wydajność={params['wydajnosc']})"
        elif typ == 'F':
            return "zwolnienie"
        elif typ == 'V':
            return f"zmiana wydajności na {params['wydajnosc']}"
        return ""

def debug_test(test_name, input_data):
    """Uruchamia test z podanymi danymi wejściowymi"""
    print(f"\n[DEBUG] Uruchamianie testu: {test_name}")
    print("[DEBUG] Wejście:")
    for line in input_data.strip().split('\n'):
        print(f"[DEBUG] {line}")

    import sys
    from io import StringIO
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO(input_data)
    test_output = StringIO()
    sys.stdout = test_output

    # Uruchomienie testu
    main()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    # Wyświetlenie wyników
    print("\n[DEBUG] Otrzymane wyjście:")
    print(test_output.getvalue().strip())

def run_debug_tests():
    print("\n[DEBUG] ========= ROZPOCZECIE TESTOW DEBUGOWYCH =========")
    
    testy = {
        "r2d0a": """5 7
1 2 3 2 4
Q 1 5 2
Q 2 3 2
F 2 3
V 3 5 3
Q 2 4 4
H 2 5 6
Q 1 5 8""",
        "r2d0b": """1 7
2
Q 1 1 1
F 1 1
H 1 6 2
Q 1 1 3
Q 1 1 4
Q 1 1 7
Q 1 1 8"""
    }

    for nazwa, test in testy.items():
        print(f"\n[DEBUG] ========= TEST {nazwa} =========")
        debug_test(nazwa, test)
    
    print("[DEBUG] ========= ZAKONCZENIE TESTOW DEBUGOWYCH =========\n")

def waliduj_parametry(typ, params, n):
    """Sprawdza poprawność parametrów operacji"""
    t = params.get('t', 0)
    if not (0 <= t <= 10**9):
        raise ValueError(f"Nieprawidłowy czas: {t}")

    if typ in ['V', 'F', 'H']:
        i = params.get('i', 0)
        if not (1 <= i <= n):
            raise ValueError(f"Nieprawidłowy numer stanowiska: {i}")
        
        if typ in ['V', 'H']:
            v = params.get('wydajnosc', 0)
            if not (0 <= v <= 10**3):
                raise ValueError(f"Nieprawidłowa wydajność: {v}")

    elif typ == 'Q':
        i, j = params.get('i', 0), params.get('j', 0)
        if not (1 <= i <= j <= n):
            raise ValueError(f"Nieprawidłowy przedział stanowisk: {i}-{j}")

def main():
    try:
        n, q = map(int, input().split())
        wydajnosci = list(map(int, input().split()))
        
        produkcja = Produkcja(n, wydajnosci)
        
        for _ in range(q):
            zapytanie = input().split()
            typ = zapytanie[0]
            
            if typ == 'V':
                i, v, t = map(int, zapytanie[1:])
                produkcja.dodaj_zapytanie('V', {'i': i, 'wydajnosc': v, 't': t})
            elif typ == 'F':
                i, t = map(int, zapytanie[1:])
                produkcja.dodaj_zapytanie('F', {'i': i, 't': t})
            elif typ == 'H':
                i, v, t = map(int, zapytanie[1:])
                produkcja.dodaj_zapytanie('H', {'i': i, 'wydajnosc': v, 't': t})
            elif typ == 'Q':
                i, j, t = map(int, zapytanie[1:])
                produkcja.dodaj_zapytanie('Q', {'i': i, 'j': j, 't': t})
        
        wyniki = produkcja.symuluj()
        
        for wynik in wyniki:
            print(wynik)

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    debug = True  # Włączamy tryb debug
    verbose = True  # Włączamy tryb verbose
    
    if debug:
        try:
            run_debug_tests()
        except Exception as e:
            print(f"[DEBUG] Błąd podczas wykonywania testów: {str(e)}")
    else:
        main()  # Uruchom w trybie interaktywnym
