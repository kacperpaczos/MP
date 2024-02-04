n, m, k = map(int, input().split())  # Wczytanie liczby robotów, zależności i maksymalnej grupy
skills = [(i + 1, skill) for i, skill in enumerate(map(int, input().split()))]  # Przypisanie umiejętności do robotów
dependencies = [tuple(map(int, input().split())) for _ in range(m)]  # Wczytanie zależności między robotami

all_components = []  # Lista wszystkich komponentów

# Tworzenie grafu zależności
dependency_graph = {i: [] for i in range(1, n + 1)}
for dep in dependencies:
    dependency_graph[dep[1]].append(dep[0])
    dependency_graph[dep[0]].append(dep[1])

visited = {i: False for i in range(1, n + 1)}  # Słownik odwiedzonych wierzchołków

def dfs_iterative(start_node):
    """Funkcja przeszukująca graf w głąb iteracyjnie."""
    stack = [start_node]
    component = []
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            component.append(node)
            stack.extend(neighbour for neighbour in dependency_graph[node] if not visited[neighbour])
    return component

# Przeszukiwanie grafu w celu znalezienia wszystkich komponentów
for i in range(1, n + 1):
    if not visited[i]:
        component = dfs_iterative(i)
        all_components.append(component)


# Obliczanie sumy umiejętności, liczebności dla każdej grupy oraz obliczanie ilorazu wartości do liczby elementów w grupie
group_values_counts_and_ratios = []
for group in all_components:
    sum_skills = sum(skills[node-1][1] for node in group)
    group_len = len(group)
    group_values_counts_and_ratios.append((sum_skills, group_len, sum_skills/group_len))

# Sortowanie grup według ilorazu wartości do liczby elementów w grupie od największego
sorted_group_values_counts_and_ratios = sorted(group_values_counts_and_ratios, key=lambda x: x[2], reverse=True)

#print(sorted_group_values_counts_and_ratios)

# Zakładając, że masz już 'sorted_group_values_counts_and_ratios' z poprzedniego kodu

# Dynamiczne programowanie do obliczenia maksymalnej wartości umiejętności
# z uwzględnieniem liczebności grupy dla k robotów, ale z dodatkowym warunkiem ilościowym
dp = [[0] * (k+1) for _ in range(len(sorted_group_values_counts_and_ratios)+1)]

for i in range(1, len(sorted_group_values_counts_and_ratios)+1):
    for w in range(1, k+1):
        value, count, _ = sorted_group_values_counts_and_ratios[i-1]
        if count <= w:
            dp[i][w] = max(dp[i-1][w], dp[i-1][w-count] + value)
        else:
            dp[i][w] = dp[i-1][w]

print(dp[-1][-1])  # Wyświetlenie maksymalnej wartości umiejętności, która może być zapakowana