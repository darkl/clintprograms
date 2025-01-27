from tabulate import tabulate
from math import isqrt, sqrt, ceil
from typing import List, Tuple

def get_primes_until(n: int) -> List[int]:
    numbers = [False] * (n + 1)
    square_root = isqrt(n)

    location = 0
    numbers[0] = True

    while location <= square_root:
        location = next(
            (x for x in range(location + 1, n + 1) if not numbers[x]),
            None
        )

        if location is None:
            break

        prime = location + 1

        for i in range(location + prime, n + 1, prime):
            numbers[i] = True

    result = [i + 1 for i, x in enumerate(numbers) if not x]
    return result

def generate_table(start: int, height: int) -> Tuple[List[str], List[List[str]]]:
    primes = get_primes_until(ceil(sqrt(10 * (start + height))))

    # Generate header row
    header = list(map(lambda x : '10n + '+ str(x), range(1, 10, 2)))

    value = start
    table_content = []

    # Generate table content
    for _ in range(height + 1):
        current_row = [value]
        for x in range(1, 10, 2):
            number = 10 * value + x
            result = prime_factor(number, primes)

            if number != result:
                current_row.append(str(result))
            else:
                current_row.append("prime")

        table_content.append(current_row)
        value += 1

    return header, table_content

def prime_factor(n: int, primes: List[int]) -> int:
    square_root = isqrt(n)
    for p in primes:
        if p > square_root:
            return n
        if n % p == 0:
            return p
    return n

def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    if b > a:
        a, b = b, a

    while True:
        if b == 0:
            return a
        a %= b
        if a == 0:
            return b
        b %= a


def main():
    start = int(input("Enter start: "))
    height = int(input("Enter height: "))

    headers, table = generate_table(start, height)
    print(tabulate(table, headers=headers, tablefmt="grid"))

main()