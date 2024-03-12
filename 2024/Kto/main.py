def porownaj_wyniki(algosia, bajtek):
    suma_algosia = sum(algosia)
    suma_bajtek = sum(bajtek)
    if suma_algosia == suma_bajtek:
        for punkty in range(10, 0, -1):
            konkursy_algosia = algosia.count(punkty)
            konkursy_bajtek = bajtek.count(punkty)
            if konkursy_algosia > konkursy_bajtek:
                return "Algosia"
            elif konkursy_bajtek > konkursy_algosia:
                return "Bajtek"
        return "Remis"
    elif suma_algosia > suma_bajtek:
        return "Algosia"
    else:
        return "Bajtek"

debug = True

if debug:
    algosia_wyniki = [10, 10, 7, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 4, 10, 10, 10]
    bajtek_wyniki = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 4, 3, 4, 10, 10, 10]
else:
    # Dane wejściowe
    algosia_wyniki = list(map(int, input().split()))
    bajtek_wyniki = list(map(int, input().split()))

# Wywołanie funkcji i wyświetlenie wyniku
print(porownaj_wyniki(algosia_wyniki, bajtek_wyniki))
