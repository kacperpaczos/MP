def count_lukry(n):
  """
  Funkcja zlicza lukry, które Staszek otrzyma po przeczytaniu do strony n.

  Args:
      n: Numer strony, do której Staszek zamierza czytać.

  Returns:
      Liczba lukrów, które Staszek otrzyma.
  """
  lukry = 0
  strona = 1
  while strona <= n:
    lukry += 1
    strona += lukry
  return lukry

# Pobranie numeru strony od użytkownika
n = int(input())

# Wyliczenie liczby lukrów
liczba_lukrow = count_lukry(n)

# Wypisanie wyniku
print(liczba_lukrow)
