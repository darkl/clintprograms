import re
from collections import defaultdict

def parse_polynomial(input_str: str) -> dict:
    poly = {}
    signs = {"+": 1, "-": -1}
    x_regex = re.compile(r'([-+]?\d*)(x?)\^?(\d*)')
    
    input_str = input_str.replace(" ", "").replace("**", "^")
    
    for match in x_regex.finditer(input_str):
        c, x, p = match.groups()
        
        if not c and not x and not p:
            continue
        
        coeff = signs.get(c)
        if not coeff:
            coeff = int(c) if c else 1
        power = int(p) if p else (1 if x else 0)
        
        if power in poly:
            poly[power] += coeff
        else:
            poly[power] = coeff
    
    return poly

def power_mod(base_value: int, exponent: int, modulo: int) -> int:
    result = 1
    base_value %= modulo
    
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base_value) % modulo
        base_value = (base_value * base_value) % modulo
        exponent //= 2
    
    return result

def evaluate_polynomial(polynomial: dict, x: int, n: int) -> int:
    result = 0
    powers = sorted(polynomial.keys(), reverse=True)
    last_power = max(powers, default=0)
    
    for current_power in powers:
        difference = last_power - current_power
        result = (result * power_mod(x, difference, n)) % n
        result = (result + polynomial[current_power]) % n
        last_power = current_power
    
    if last_power != 0:
        result = (result * power_mod(x, last_power, n)) % n
    
    return result

def find_solutions(polynomial: dict, n: int) -> list:
    return [i for i in range(n) if evaluate_polynomial(polynomial, i, n) == 0]

def polynomial_to_string(polynomial: dict) -> str:
    to_concat = []
    is_first = True

    for power in sorted(polynomial.keys(), reverse=True):
        coefficient = polynomial.get(power, 0)

        if coefficient != 0:
            if coefficient > 0 and not is_first:
                to_concat.append("+")

            if power == 0:
                to_concat.append(f"{coefficient}")
            else:
                exponent = f"x^{power}" if power != 1 else "x"
                if coefficient == 1:
                    to_concat.append(exponent)
                elif coefficient == -1:
                    to_concat.append(f"-{exponent}")
                else:
                    to_concat.append(f"{coefficient}{exponent}")

            is_first = False

    result = "".join(to_concat)
    return result

def main():
    polynomial_input = input("Enter polynomial: ")
    n = int(input("Enter modulus n: "))
    parsed_polynomial = parse_polynomial(polynomial_input)
    solutions = find_solutions(parsed_polynomial, n)
    polynomial_str = polynomial_to_string(parsed_polynomial)
    
    if solutions:
        print(f"The solutions to {polynomial_str} ≡ 0 (mod {n}) are x = {', '.join(map(str, solutions))}.")
    else:
        print(f"No solutions to {polynomial_str} ≡ 0 (mod {n}) exist.")

main()