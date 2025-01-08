import math;
from quadraticring import *;

def main():
    alpha = int(input("Enter alpha: "))

    # Validate alpha
    if alpha != math.floor(alpha):
        print("Expected an integer.")
        exit()

    if alpha > 0:
        square_root = math.sqrt(alpha)
        if square_root == math.floor(square_root):
            print("Expected a non-square integer.")
            exit()

    ring = QuadraticRing(alpha)

    n = int(input("Enter n: "))
    for j in range(2, n + 1):
        if HelperFunctions.is_prime(j):
            factors = HelperFunctions.find_factors(ring, j)
            factor_string = HelperFunctions.compute_string(ring, factors)
            print(f"{j} {factor_string}")

main()