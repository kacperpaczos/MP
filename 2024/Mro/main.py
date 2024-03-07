def liczba_odbic(kierunki):
    n = len(kierunki)
    odbicia = [0] * n  # Tablica na liczbę odbić dla każdej mrówki

    # Obliczamy odbicia dla mrówek patrzących w lewo i prawo jednocześnie
    licznik_prawo = 0  # Licznik mrówek patrzących w prawo
    licznik_lewo = 0  # Licznik mrówek patrzących w lewo
    for i in range(n):
        if kierunki[i] == 'P':
            licznik_prawo += 1
        odbicia[i] += licznik_lewo  # Dodajemy odbicia dla mrówek patrzących w lewo do tej pory

    for i in range(n-1, -1, -1):
        if kierunki[i] == 'L':
            licznik_lewo += 1
        odbicia[i] += licznik_prawo  # Dodajemy odbicia dla mrówek patrzących w prawo do tej pory

    # Aby uzyskać poprawną liczbę odbić, należy odjąć od każdego elementu liczbę mrówek patrzących w przeciwną stronę
    for i in range(n):
        if kierunki[i] == 'P':
            odbicia[i] -= licznik_lewo
        else:
            odbicia[i] -= licznik_prawo

    return odbicia

# Przykład użycia
kierunki = "LPPLPL"
print(liczba_odbic(kierunki))