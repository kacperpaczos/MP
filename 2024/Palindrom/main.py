def generate_palindrome(n, k):
    if (k == 2 and n % 2 == 0 or k >= 3) and n >= 2:
        return "NIE" 
    else:
        # middle = []
        # if n % 2 == 1:
        #     middle = ['9']
        #     n -= 1
        half = [str(9 - i % k) for i in range(n // 2 + 1)]
        if n % 2 == 1:
            return ''.join(half[:-1] + half[::-1])
        else:
            return ''.join(half[1:-1] + half[-1::-1])   # ???
# Generowanie palindromów dla różnych wartości k i n
# wartosci_nie = []
# with open('output.txt', 'w') as output_file, open('NIE.txt', 'w') as nie_file:
#     for k in range(1, 101):
#         output_file.write(f"Wartości palindromów dla k={k}:\n")
#         for n in range(1, 101):  # Iterujemy przez n dla każdego k
#             palindrome = generate_palindrome(n, k)
#             if palindrome != "NIE":
#                 output_file.write(f"  n={n}: {palindrome}\n")
#             else:
#                 wartosci_nie.append((k, n))
#         output_file.write("\n")  # Dodajemy pustą linię dla lepszej czytelności

#     # Wypisywanie wartości dla których funkcja zwróciła "NIE"
#     nie_file.write("Wartości dla których palindrom zwrócił 'NIE':\n")
#     for k, n in wartosci_nie:
#         nie_file.write(f"k={k}, n={n}\n")

n, k = map(int, input().split())
print(generate_palindrome(n, k))