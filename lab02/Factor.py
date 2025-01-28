from math import isqrt
from collections import defaultdict
from typing import List, Dict

def factorization_string(n: int) -> str:
    factorization_result = factorization(n)

    result_string = " x ".join(
        f"{key}^{value}" if value > 1 else str(key)
        for key, value in factorization_result.items()
    )

    return result_string

def factorization(n: int) -> Dict[int, int]:
    factors = factor(n)

    grouped_factors = defaultdict(int)
    for currentFactor in factors:
        grouped_factors[currentFactor] += 1

    return dict(grouped_factors)

def factor(n: int) -> List[int]:
    result = []

    # Remove powers of 2, 3, 5
    for prime in [2, 3, 5]:
        n = remove_factors(n, result, prime)

    d = 0

    # Trial division with selected forms of d
    square_root = isqrt(n)
    while n > 1 and d <= square_root:
        forms_of_d = [1, 7, 11, 13, 17, 19, 23, 29]

        for current_residue in forms_of_d:
            current_divisor = d + current_residue

            if current_divisor != 1 and n % current_divisor == 0:
                n = remove_factors(n, result, current_divisor)

        d += 30  # Move to the next set of forms

    if n > 1:
        result.append(n)

    return result

def remove_factors(n: int, factors: List[int], prime: int) -> int:
    while n % prime == 0:
        factors.append(prime)
        n //= prime

    return n

def main():
    n = int(input("Enter n: "))
    factorizationString = factorization_string(n)
    print(factorizationString)

main()
