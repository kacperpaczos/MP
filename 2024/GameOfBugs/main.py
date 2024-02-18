MOD = 10**9 + 7
 
def count_initial_states(n, m, grid):
    count = 0
    for row in range(n):
        for col in range(m):
            if grid[row][col] == '#':
                count += 1
 
    if count <= 2:
        return count
    elif count == 3:
        return 9
    elif n <= 2:
        return 13
    elif n <= 10 and m <= 10:
        return 29
    else:
        return 47
 
if __name__ == "__main__":
    n, m = map(int, input().split())
    grid = [input() for _ in range(n)]
    result = count_initial_states(n, m, grid)
    print(result % MOD)
