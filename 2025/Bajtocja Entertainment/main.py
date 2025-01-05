from typing import List, Optional, Tuple
import logging

# Konfiguracja loggera
DEBUG = False  # Dodaj zmienną kontrolującą debugowanie

if DEBUG:
    logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def czy_mozliwy_podzial(arr: List[int], target_sum: int) -> Tuple[bool, List[int]]:
    if target_sum == 0:
        if DEBUG: logger.debug(f"Target sum jest zero, zwracam False")
        return False, []
        
    current_sum = 0
    pozycje = []
    
    if DEBUG: logger.debug(f"Sprawdzam podział dla target_sum={target_sum}")
    
    for i in range(len(arr)):
        current_sum += arr[i]
        if DEBUG: logger.debug(f"Pozycja {i}: arr[i]={arr[i]}, current_sum={current_sum}")
        
        if current_sum == target_sum:
            pozycje.append(i + 1)
            current_sum = 0
            if DEBUG: logger.debug(f"Znaleziono odcinek kończący się na pozycji {i+1}, pozycje={pozycje}")
    
    wynik = len(pozycje) >= 2 and current_sum == 0 and pozycje[-1] == len(arr)
    if DEBUG: logger.debug(f"Końcowy wynik: {wynik}, pozycje={pozycje}, current_sum={current_sum}")
    return wynik, pozycje if wynik else []

def znajdz_podzial(n: int, arr: List[int]) -> Optional[List[int]]:
    suma_total = sum(arr)
    if DEBUG: logger.debug(f"Suma całkowita: {suma_total}")
    
    najlepszy_wynik = None
    
    # Znajdujemy wszystkie możliwe dzielniki sumy całkowitej
    for i in range(1, abs(suma_total) + 1):
        if suma_total % i == 0:
            # Sprawdzamy zarówno dodatni jak i ujemny dzielnik
            for znak in [-1, 1]:
                if suma_total < 0 and znak > 0:
                    continue
                if suma_total > 0 and znak < 0:
                    continue
                    
                current_target = i * znak
                logger.debug(f"Sprawdzam target={current_target}")
                
                mozliwe, pozycje = czy_mozliwy_podzial(arr, current_target)
                if mozliwe:
                    if najlepszy_wynik is None or len(pozycje) > len(najlepszy_wynik):
                        najlepszy_wynik = pozycje
                        logger.debug(f"Znaleziono lepsze rozwiązanie: {pozycje}")
    
    logger.debug(f"Końcowy wynik: {najlepszy_wynik}")
    return najlepszy_wynik

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    
    wynik = znajdz_podzial(n, arr)
    
    if wynik is None:
        print("Nie")
    else:
        print("Tak")
        print(len(wynik))
        print(" ".join(map(str, wynik)))

if __name__ == "__main__":
    main()