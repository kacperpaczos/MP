import subprocess

# Przygotowanie danych wejściowych
input_data = """4
2 4
1 2
3 2
9
3 2
1 2
3 4
3 1
3 3
2 2
1 1
3 3
1 2
"""

# Wywołanie main.py z podanymi danymi wejściowymi
process = subprocess.Popen(['python3', 'Wróg Mojego Wroga/main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = process.communicate(input=input_data)

# Wyświetlenie wyników
print(stdout)
if stderr:
    print("Wystąpiły błędy:\n", stderr)
