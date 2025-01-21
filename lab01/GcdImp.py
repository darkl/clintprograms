def gcd(a, b):
    a = abs(a)
    b = abs(b)
    if b > a:
        a, b = b, a  # Swap values if b > a
    while True:
        if b == 0:
            return a
        a %= b
        if a == 0:
            return b
        b %= a