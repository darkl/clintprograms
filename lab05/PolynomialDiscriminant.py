from fractions import Fraction
import re

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

def determinant(matrix):
    n = len(matrix)
    mat = [row[:] for row in matrix]
    det = Fraction(1)
    
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(mat[k][i]) > abs(mat[max_row][i]):
                max_row = k
        
        if mat[max_row][i] == 0:
            return 0
        
        mat[i], mat[max_row] = mat[max_row], mat[i]
        if i != max_row:
            det *= Fraction(-1)
        
        det *= mat[i][i]
        for k in range(i + 1, n):
            mat[i][k] /= mat[i][i]
        
        for k in range(i + 1, n):
            for j in range(i + 1, n):
                mat[k][j] -= mat[k][i] * mat[i][j]
    
    return float(det)

def sylvester_matrix(poly1, poly2):
    m = len(poly1) - 1
    n = len(poly2) - 1
    size = m + n
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    
    for i in range(n):
        for j in range(len(poly1)):
            matrix[i][i + j] = Fraction(poly1[j], 1)
    
    for i in range(m):
        for j in range(len(poly2)):
            matrix[n + i][i + j] = Fraction(poly2[j], 1)
    
    return matrix

def polynomial_derivative(coefficients):
    return [coefficients[i] * i for i in range(1, len(coefficients))]

def discriminant(polynomial_map):
    polynomial = map_to_polynomial_array(polynomial_map)
    derivative = polynomial_derivative(polynomial)
    sylvester = sylvester_matrix(polynomial, derivative)
    degree = len(polynomial) - 1
    return (-1) ** ((degree * (degree - 1)) // 2) * determinant(sylvester) / polynomial[degree]

def map_to_polynomial_array(poly_map):
    max_degree = max((k for k in poly_map.keys() if poly_map[k] != 0), default=0)
    coefficients = [0] * (max_degree + 1)
    
    for degree, coefficient in poly_map.items():
        coefficients[degree] = coefficient
    
    return coefficients


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
    parsed_polynomial = parse_polynomial(polynomial_input)
    polynomial_discriminant = discriminant(parsed_polynomial)
    polynomial_str = polynomial_to_string(parsed_polynomial)

    print(f"disc({polynomial_str}) = {polynomial_discriminant}.")

main()