from tabulate import tabulate
from math import isqrt
from collections import defaultdict
from typing import List, Dict, Tuple

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def inverse(a: int, n: int) -> int:
    _, y = euclidean_algorithm(n, a % n)
    return y

def euclidean_algorithm(a: int, b: int) -> Tuple[int, int]:
    big, small = (a, b) if a > b else (b, a)
    prev_x, prev_y = 1, 0
    curr_x, curr_y = 0, 1
    
    while small > 0:
        q = big // small
        big, small = small, big % small
        prev_x, curr_x = curr_x, prev_x - q * curr_x
        prev_y, curr_y = curr_y, prev_y - q * curr_y
    
    return prev_x, prev_y

def chinese_value(a: int, b: int, r1: int, r2: int) -> int | None:
    d = gcd(a, b)
    
    if r1 % d != r2 % d:
        return None
    
    factorization_of_a: Dict[int, int] = factorization(a)
    factorization_of_b: Dict[int, int] = factorization(b)
    
    a_prime, b_prime = a, b
    
    for prime in factorization_of_a.keys():
        if prime in factorization_of_b:
            a_exponent = factorization_of_a[prime]
            b_exponent = factorization_of_b[prime]
            if a_exponent < b_exponent:
                a_prime //= prime ** a_exponent
            else:
                b_prime //= prime ** b_exponent
    
    first_coefficient = inverse(b_prime, a_prime)
    second_coefficient = inverse(a_prime, b_prime)
    
    solution = b_prime * first_coefficient * r1 + a_prime * second_coefficient * r2
    prime = a_prime * b_prime
    
    solution = (solution % prime + prime) % prime
    return solution

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



def generate_table(a: int, b: int, start_x: int, start_y: int, width: int, height: int):
    modulo_table = []
    
    header = [j for j in range(start_x, start_x + width)]
    
    for i in range(start_y, start_y + height):
        current_row = [i]
        
        for j in range(start_x, start_x + width):
            result = chinese_value(a, b, i, j)
            current_row.append(result)
        
        modulo_table.append(current_row)
    
    return header, modulo_table

def main():
    try:
        a = int(input("Enter number a: "))
        b = int(input("Enter number b: "))
    except ValueError:
        print("Please enter valid positive numbers for a and b.")
        return
    
    start_x, start_y = 0, 0
    width, height = b - start_x, a - start_y
    
    if a <= 0 or b <= 0:
        print("Please enter valid positive numbers for a and b.")
        return
    
    if start_x < 0 or start_x >= b or start_y < 0 or start_y >= a or \
       width <= 0 or height <= 0 or (start_x + width - 1) >= b or (start_y + height - 1) >= a:
        print("Invalid values for startX, startY, width, or height. Please check and try again.")
        return
    
    print(f"Intersection of arithmetic progressions (mod {a}) and (mod {b})")
    headers, table = generate_table(a, b, start_x, start_x, width, height)
    print(tabulate(table, headers=headers, tablefmt="grid"))

main()