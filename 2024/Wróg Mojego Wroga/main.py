import numpy as np
from collections import defaultdict

def bfs(graph, start, closed):
    visited = np.zeros(len(graph), dtype=bool)
    visited[start] = True
    queue = [start]
    while queue:
        node = queue.pop(0)
        for neighbour in graph[node]:
            if not visited[neighbour] and neighbour not in closed:
                visited[neighbour] = True
                queue.append(neighbour)
    return visited

def process_events(n, events, graph):
    closed = set()
    party_info = defaultdict(int)
    king_status = np.zeros(n, dtype=int)
    parties_known = []

    for event in events:
        action, king = event
        king -= 1

        if action in [1, 2]:  # Król wyjeżdża lub wraca
            if action == 1:
                closed.add(king)
            else:
                closed.remove(king)

        elif action == 3:  # Organizacja imprezy
            accessible_kingdoms = bfs(graph, king, closed)
            party_info[king] += 1
            known_by = 0  # Zmiana: inicjalizacja liczby królów znających imprezę
            for k in range(len(accessible_kingdoms)):
                if accessible_kingdoms[k]:  # Usunięcie warunku sprawdzającego, czy król nie jest organizatorem
                    known_by += 1
                    if k != king and k not in closed:  # Dodanie warunku sprawdzającego, czy król nie jest organizatorem
                        king_status[k] -= 1  # Królowie wiedzący o imprezie, ale nie organizujący, tracą 1 punkt
            if king not in closed:  # Jeśli król organizator nie jest zamknięty, to zyskuje punkty za każdego gościa
                king_status[king] += known_by - 1  # Aktualizacja statusu króla - uwzględnienie organizatora imprezy
            parties_known.append(known_by)

    return parties_known, king_status

def main():
    n = int(input())
    graph = defaultdict(list)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    q = int(input())
    events = [list(map(int, input().split())) for _ in range(q)]

    parties_known, king_status = process_events(n, events, graph)

    print(' '.join(map(str, parties_known)))
    print(' '.join(map(str, king_status)))

if __name__ == "__main__":
    main()
