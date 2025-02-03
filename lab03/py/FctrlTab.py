from tabulate import tabulate
from typing import List, Tuple

def generate_table(n, start_y, given_height=None):
    height = given_height if given_height is not None else n

    header = ["10j"] + [f"10j + {k}" for k in range(1, 10)]

    current_number = 10 * start_y
    table = []
    result = factorial_modulo(current_number, n)
    
    a = start_y
    while a <= start_y + height - 1 and not (given_height is None and result == 0 and a - start_y >= 10):
        current_row = [a]
        for k in range(10):
            current_row.append(result)
            result = (result * (current_number + 1)) % n
            current_number += 1
        table.append(current_row)
        a += 1
    
    return [header, table]

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def factorial_modulo(a, n):
    result = 1
    for i in range(1, a + 1):
        result = (result * i) % n
    return result


def main():
    start = int(input("Enter start: "))
    height = int(input("Enter height: "))
    n = int(input("Enter n: "))

    headers, table = generate_table(n, start, height)
    print(tabulate(table, headers=headers, tablefmt="grid"))

main()