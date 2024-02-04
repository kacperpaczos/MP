n, k = map(int, input().split())

def generate_palindrome(n, k):
    if k > n // 2:  
        return "NIE"
    else:
        middle = []
        if n % 2 == 1:
            middle = ['9']
            n -= 1
        half = [str(9 - i % k) for i in range(n // 2)]
        return ''.join(half + middle + half[::-1])

palindrome = generate_palindrome(n, k)
print(palindrome)
