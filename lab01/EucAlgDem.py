from typing import List, Tuple

def euclidean_algorithm(a: int, b: int, optimization: bool) -> List[Tuple[int, int, int, int, int]]:
    result: List[Tuple[int, int, int, int, int]] = []

    previous_linear: Tuple[int, int] = (1, 0)
    current_linear: Tuple[int, int] = (0, 1)

    if a < 0:
        previous_linear = (-1, 0)
        a = -a
    if b < 0:
        current_linear = (0, -1)
        b = -b

    if a < b:
        a, b = b, a  # Swap `a` and `b`
        previous_linear, current_linear = current_linear, previous_linear

    big = a
    small = b

    while small > 0:
        r = big % small
        q = big // small

        modified_integer = False
        if optimization and r > small // 2:
            q += 1
            r -= small
            modified_integer = True

        big = small
        small = r

        result.append((big, q, r, current_linear[0], current_linear[1]))

        new_linear = (
            previous_linear[0] - q * current_linear[0],
            previous_linear[1] - q * current_linear[1]
        )

        if modified_integer:
            small = -r
            new_linear = (-new_linear[0], -new_linear[1])

        previous_linear = current_linear
        current_linear = new_linear

    return result

def main():
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))

    sign = ""
    if b > 0:
        sign = "+"

    description = f"At every stage we have {a} x_i {sign} {b} y_i = r_i."
    print(description)

    # Call the Euclidean algorithm function
    table_values = euclidean_algorithm(a, b, False)
    index = 1

    for value in table_values:
        formatted_string = f"r_{index - 1} = {value[0]}, q_{index} = {value[1]}, r_{index} = {value[2]}, x_{index - 1} = {value[3]}, y_{index - 1} = {value[4]}"
        index += 1

        print(formatted_string)

main()