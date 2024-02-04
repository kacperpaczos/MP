n, m, k = map(int, input().split())
skills = [(i+1, skill) for i, skill in enumerate(map(int, input().split()))]
dependencies = [list(map(int, input().split())) for _ in range(m)]

dependency_graph = {i: [] for i in range(1, n+1)}
for dep in dependencies:
    dependency_graph[dep[1]].append(dep[0])

groups = []
visited = set()
for node in range(1, n+1):
    if node not in visited:
        group = set()
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                group.add(current)
                stack.extend(dependency_graph[current])
        groups.append(group)

group_values = [sum(skills[node-1][1] for node in group) for group in groups]

dp = [0] * (k+1)
for i in range(len(groups)):
    for w in range(k, len(groups[i])-1, -1):
        dp[w] = max(dp[w], dp[w-len(groups[i])] + group_values[i])

print(dp[k])

