import random

def miller_rabin_test(n: int, k: int) -> bool:
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    s = 0
    d = n - 1

    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = mod_exp(a, d, n)

        if x == 1 or x == n - 1:
            continue

        is_composite = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                is_composite = False
                break

        if is_composite:
            return False

    return True

def mod_exp(base: int, exp: int, mod: int) -> int:
    result = 1
    base = base % mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod

    return result

def find_next_prime_big(a: int) -> int:
    if a < 2:
        return 2
    candidate = a + 1

    while True:
        if miller_rabin_test(candidate, 10):
            return candidate
        candidate += 1

def find_next_prime(a: int) -> int:
    if a >= 10**9:
        return find_next_prime_big(a)
    
    n = int(a)
    if n <= 1:
        return 2

    sieve_size = 2 * n
    sieve = [True] * sieve_size

    for p in range(2, int(sieve_size**0.5) + 1):
        if sieve[p]:
            for i in range(p * p, sieve_size, p):
                sieve[i] = False

    for i in range(n + 1, sieve_size):
        if sieve[i]:
            return i

    return -1  # This should not happen given a reasonable input.

def main():
    a = int(input("Enter a: "))
    p = find_next_prime(a)
    print(p)

main()