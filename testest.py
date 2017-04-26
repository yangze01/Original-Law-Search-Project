

def count_primes(n):
    count = 0
    for i in range(2, n+1):
        s = 0
        while n % i == 0:
            n = n/i
            s += 1
        if s > 0:
            for k in range(s):
                print(1)

if __name__ == "__main__":
    print(range(2))