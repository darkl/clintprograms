a = int(input("Enter a: "))
b = int(input("Enter b: "))

print(f"({a}, {b})", end="")

while True:
    # Break the loop if a > 0 and b == 0
    if a > 0 and b == 0:
        break

    # Ensure both a and b are non-negative
    if a < 0 or b < 0:
        a = abs(a)
        b = abs(b)
    # Swap if a < b
    elif a < b:
        a, b = b, a
    # Perform modulo operation if b is not zero
    elif b != 0:
        a = a % b

    input("")
    print(f" = ({a}, {b})", end="")
