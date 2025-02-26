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

def power_mod(base_value: int, exponent: int, modulo: int) -> int:
    result = 1
    base_value %= modulo

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base_value) % modulo
        base_value = (base_value * base_value) % modulo
        exponent //= 2
    
    return result

def evaluate_polynomial(polynomial: dict[int, int], x: int, n: int) -> int:
    result = 0
    last_power = max(polynomial.keys(), default=0)
    
    for current_power in sorted(polynomial.keys(), reverse=True):
        difference = last_power - current_power
        power_for_difference = power_mod(x, difference, n)
        result = (result * power_for_difference) % n

        current_coefficient = polynomial.get(current_power, 0)
        result = (result + current_coefficient) % n
        last_power = current_power
    
    if last_power != 0:
        power_for_last = power_mod(x, last_power, n)
        result = (result * power_for_last) % n
    
    return result

def polynomial_derivative(polynomial: dict[int, int]) -> dict[int, int]:
    result = {}
    for power, coefficient in polynomial.items():
        new_power = power - 1
        new_coefficient = power * coefficient
        if new_power >= 0 and new_coefficient != 0:
            result[new_power] = new_coefficient
    return result

def inverse(a: int, n: int) -> int:
    if n == 1:
        return 1
    _, y = euclidean_algorithm(n, a % n)
    return y % n

def euclidean_algorithm(a: int, b: int) -> tuple[int, int]:
    prev_x, prev_y = 1, 0
    curr_x, curr_y = 0, 1
    
    if a < 0:
        prev_x, prev_y = -1, 0
        a = -a
    if b < 0:
        curr_x, curr_y = 0, -1
        b = -b
    
    if a < b:
        a, b = b, a
        prev_x, prev_y, curr_x, curr_y = curr_x, curr_y, prev_x, prev_y
    
    while b > 0:
        q = a // b
        a, b = b, a % b
        prev_x, curr_x = curr_x, prev_x - q * curr_x
        prev_y, curr_y = curr_y, prev_y - q * curr_y
    
    return prev_x, prev_y

def hensel_lift_regular(polynomial: dict[int, int], solution: int, p: int, max_power: int) -> list[tuple[int, int]]:
    if evaluate_polynomial(polynomial, solution, p) != 0:
        raise ValueError("Expected solution to be a root of the polynomial modulo p.")
    
    derivative = polynomial_derivative(polynomial)
    derivative_value = evaluate_polynomial(derivative, solution, p)
    
    if derivative_value == 0:
        raise ValueError("Expected solution not to be a root of the derivative of the polynomial modulo p.")
    
    inverse_derivative_value_modp = inverse(derivative_value, p)
    result = []
    
    current_lifted = solution
    previous_power = 1
    
    for _ in range(1, max_power):
        current_power = previous_power * p
        current_value = evaluate_polynomial(polynomial, current_lifted, current_power)
        multiple = current_value // previous_power
        current_c = (-inverse_derivative_value_modp * multiple) % p
        current_lifted += current_c * previous_power
        result.append((current_c, current_lifted))
        previous_power = current_power
    
    return result

def all_hensel_singular_lifts(polynomial: dict[int, int], solution: int, p: int, current_power: int) -> list[tuple[int, int]]:
    if evaluate_polynomial(polynomial, solution, p) != 0:
        raise ValueError("Expected solution to be a root of the polynomial modulo p.")
    
    derivative = polynomial_derivative(polynomial)
    derivative_value = evaluate_polynomial(derivative, solution, p)
    
    if derivative_value != 0:
        raise ValueError("Expected solution to be a root of the derivative of the polynomial modulo p.")
    
    result = []
    previous_power = p ** (current_power - 1)
    power_value = previous_power * p
    evaluation = evaluate_polynomial(polynomial, solution, power_value)
    
    if evaluation == 0:
        for i in range(p):
            current_solution = solution + previous_power * i
            result.append((i, current_solution))
    
    return result

def is_regular(polynomial: dict[int, int], solution: int, p: int) -> bool:
    derivative = polynomial_derivative(polynomial)
    return evaluate_polynomial(derivative, solution, p) != 0

def find_solutions(polynomial: dict[int, int], n: int) -> list[int]:
    result = []
    
    for i in range(n):
        current_evaluation = evaluate_polynomial(polynomial, i, n)
        if current_evaluation == 0:
            result.append(i)
    
    return result

def find_solutions_with_type(polynomial: dict[int, int], n: int) -> list[tuple[int, str]]:
    derivative = polynomial_derivative(polynomial)
    solutions = find_solutions(polynomial, n)
    result = []
    
    for solution in solutions:
        derivative_at_solution = evaluate_polynomial(derivative, solution, n)
        if derivative_at_solution == 0:
            result.append((solution, "singular"))
        else:
            result.append((solution, "regular"))
    
    return result

def main():
    polynomial_input = input("Enter polynomial: ")
    n = int(input("Enter modulus n: "))
    parsed_polynomial = parse_polynomial(polynomial_input)
    solutions = find_solutions_with_type(parsed_polynomial, n)
    polynomial_str = polynomial_to_string(parsed_polynomial)

    if solutions:
        print(f"The solutions to {polynomial_str} ≡ 0 (mod {n}) are x = {', '.join(map(str, solutions))}.")
    else:
        print(f"No solutions to {polynomial_str} ≡ 0 (mod {n}) exist.")

    solution_to_lift = int(input("Enter solution to lift: "))
    
    relevant_tuple = [x for x in solutions if x[0] == solution_to_lift]
    
    while not relevant_tuple:
        print("Not a solution! Enter solution to lift: ")
        solution_to_lift = int(input())
        relevant_tuple = [x for x in solutions if x[0] == solution_to_lift]
    
    if relevant_tuple[0][1] == "regular":
        power_to_lift = int(input("Enter maximal power to lift: "))
        lifted = solution_to_lift
        
        lifted = hensel_lift_regular(parsed_polynomial, lifted, n, power_to_lift)
        for i,lift in enumerate(lifted[1:]):
            print(f"The lifted solution is x ≡ {lift[1]} (mod {n}^{i+2}).")

main()