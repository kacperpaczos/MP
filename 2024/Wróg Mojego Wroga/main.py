from collections import defaultdict, deque

class KingdomRelations:
    def __init__(self, n):
        self.graph = defaultdict(list)
        self.closed = set()
        self.friends = defaultdict(set)
        self.party_info = defaultdict(int)
        self.king_status = [0] * n
        self.n = n

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def update_friends(self):
        for node in self.graph:
            for enemy in self.graph[node]:
                for friend_of_enemy in self.graph[enemy]:
                    if friend_of_enemy != node:  # Unikamy dodawania samego siebie
                        self.friends[node].add(friend_of_enemy)
                        self.friends[friend_of_enemy].add(node)

    def bfs(self, start):
        visited = [False] * self.n
        visited[start] = True
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbour in self.graph[node]:
                if not visited[neighbour] and neighbour not in self.closed:
                    visited[neighbour] = True
                    queue.append(neighbour)
        return visited

    def process_event(self, action, king):
        king -= 1
        if action in [1, 2]:
            if action == 1:
                self.closed.add(king)
            elif action == 2:
                self.closed.remove(king)
        elif action == 3:
            accessible_kingdoms = self.bfs(king)
            self.party_info[king] += 1
            known_by = 0
            for k, is_accessible in enumerate(accessible_kingdoms):
                if is_accessible and k not in self.closed:
                    known_by += 1
                    if k in self.friends[king] or k == king:
                        self.king_status[k] += 1
                    else:
                        self.king_status[k] -= 1
            return known_by
        return None

    def process_events(self, events):
        parties_known = []
        for event in events:
            known_by = self.process_event(*event)
            if known_by is not None:
                parties_known.append(known_by)
        return parties_known, self.king_status

def main():
    n = int(input())
    relations = KingdomRelations(n)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        relations.add_edge(u - 1, v - 1)

    q = int(input())
    events = [list(map(int, input().split())) for _ in range(q)]

    relations.update_friends()
    parties_known, king_status = relations.process_events(events)

    print(' '.join(map(str, parties_known)))
    print(' '.join(map(str, king_status)))

if __name__ == "__main__":
    main()
