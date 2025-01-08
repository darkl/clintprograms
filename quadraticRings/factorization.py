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
    irreducible = HelperFunctions.find_irreducible_elements(n, ring)

    decompositions_list = []

    for j in range(2, n + 1):
        factors = HelperFunctions.find_factors_in_ring(ring, j, irreducible)
        decompositions = HelperFunctions.find_factorizations(ring, j, factors)
        decomposition_strings = [
            f"{HelperFunctions.compute_string(ring, decomposition)}" for decomposition in decompositions
        ]
        decompositions_list.append((j, decomposition_strings))

    for number, decompositions in decompositions_list:
        print(f"{number}:")
        for decomposition in decompositions:
            print(f"\t* {decomposition}")

main()