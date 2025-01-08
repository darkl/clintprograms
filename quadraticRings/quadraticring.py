import math

class QuadraticRingElement:
    def __init__(self, ring, a, b):
        self.ring = ring
        self.a = a
        self.b = b
        self._norm = ring.norm(self)

    def add(self, other):
        return self.ring.add(self, other)

    def subtract(self, other):
        return self.ring.subtract(self, other)

    def multiply(self, other):
        return self.ring.multiply(self, other)

    def divide(self, other):
        return self.ring.divide(self, other)

    def inverse(self):
        return self.ring.inverse(self)

    def norm(self):
        return self._norm

    def is_integral(self):
        return self.ring.is_integral(self)

    def __str__(self):
        return self.ring.to_string(self)


class QuadraticRing:
    def __init__(self, alpha):
        self.mAlpha = alpha

    def add(self, z1, z2):
        return self.element(z1.a + z2.a, z1.b + z2.b)

    def subtract(self, z1, z2):
        return self.element(z1.a - z2.a, z1.b - z2.b)

    def multiply(self, z1, z2):
        return self.element(
            z1.a * z2.a + self.mAlpha * z1.b * z2.b,
            z1.a * z2.b + z1.b * z2.a
        )

    def inverse(self, z):
        norm = self.norm(z)
        return QuadraticRingElement(self, z.a / norm, -z.b / norm)

    def divide(self, z1, z2):
        result = self.multiply(z1, self.conjugate(z2))
        norm = z2.norm()
        return self.element(result.a / norm, result.b / norm)

    def is_integral(self, z):
        return z.a == math.floor(z.a) and z.b == math.floor(z.b)

    def norm(self, z):
        return z.a * z.a - self.mAlpha * z.b * z.b

    def element(self, a, b):
        return QuadraticRingElement(self, a, b)

    def conjugate(self, z):
        return self.element(z.a, -z.b)

    def to_string(self, z):
        real_part = ''
        imaginary_part = ''

        if z.a == 0 and z.b == 0:
            return '0'

        if z.a != 0:
            real_part = self.nice_string(z.a)
            if z.b > 0:
                imaginary_part = '+'

        if z.b != 0:
            symbol = f"\\sqrt{{{self.mAlpha}}}"

            if self.mAlpha == -1:
                symbol = 'i'

            if z.b == 1:
                imaginary_part += symbol if z.a == 0 else f"{symbol}"
            elif z.b == -1:
                imaginary_part += f"-{symbol}"
            else:
                imaginary_part += f"{self.nice_string(z.b)}{symbol}"

        return real_part + imaginary_part

    def nice_string(self, value):
        if value == math.floor(value):
            return str(math.floor(value))
        return str(value)

class HelperFunctions:

    @staticmethod
    def find_factorizations(ring, number, factors):
        result = []
        factors_left = factors[:]

        while factors_left:
            current = ring.element(number, 0)
            current_factor = factors_left[0]
            current = ring.divide(current, current_factor)

            initial_factors = [current_factor]

            current_conjugate = ring.conjugate(current_factor)

            if HelperFunctions.is_divisible(ring, current, current_conjugate):
                initial_factors.append(current_conjugate)
                current = ring.divide(current, current_conjugate)

            current_decomposition = (
                initial_factors + 
                HelperFunctions.find_decomposition(ring, factors, current, factors_left)
            )

            result.append(current_decomposition)
            factors_left = [x for x in factors_left if x not in current_decomposition]

        return result

    @staticmethod
    def find_decomposition(ring, factors, current, factors_left):
        current_decomposition = []

        while abs(current.norm()) != 1:
            for factor in factors + [ring.conjugate(x) for x in factors]:
                if HelperFunctions.is_divisible(ring, current, factor):
                    current_decomposition.append(factor)
                    current = ring.divide(current, factor)

                    conjugate = ring.conjugate(factor)

                    if HelperFunctions.is_divisible(ring, current, conjugate):
                        current_decomposition.append(conjugate)
                        current = ring.divide(current, conjugate)

                    break

        if not (current.a == 1 and current.b == 0):
            current_decomposition.append(current)

        return current_decomposition

    @staticmethod
    def find_factors_in_ring(ring, number, irreducible_elements):
        number_squared = number * number
        number_as_element = ring.element(number, 0)

        result = []

        for element in irreducible_elements:
            if element.norm() > number_squared:
                break

            if HelperFunctions.is_divisible(ring, number_as_element, element):
                result.append(element)

        return result

    @staticmethod
    def find_irreducible_elements(n, ring):
        elements = []

        initial_value = 0
        if ring.norm(ring.element(0, 1)) == 1:
            initial_value = 1

        for i in range(initial_value, n + 1):
            for j in range(n + 1):
                elements.append(ring.element(i, j))

        ordered_elements = sorted(
            [
                x for x in elements
                if abs(ring.norm(x)) > 1 and 
                   ((x.a == 0 or x.b == 0) or abs(HelperFunctions.gcd(x.a, x.b)) == 1)
            ],
            key=lambda x: abs(ring.norm(x))
        )

        last_index = 0
        irreducible_elements = ordered_elements[:]

        while last_index < len(irreducible_elements):
            last_element = irreducible_elements[last_index]
            last_element_conjugate = ring.conjugate(last_element)

            if last_element.norm() > n:
                break

            irreducible_elements = [
                x for i, x in enumerate(irreducible_elements)
                if not (
                    i > last_index and 
                    (HelperFunctions.is_divisible(ring, x, last_element) or
                     HelperFunctions.is_divisible(ring, x, last_element_conjugate))
                )
            ]

            last_index += 1

        return irreducible_elements

    @staticmethod
    def gcd(a, b):
        a, b = abs(a), abs(b)
        if b > a:
            a, b = b, a
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def is_divisible(ring, first, second):
        return (
            first.norm() % second.norm() == 0 and 
            ring.is_integral(ring.divide(first, second))
        )

    @staticmethod
    def is_prime(n):
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def find_factors(ring, p):
        p_element = ring.element(p, 0)

        initial_value = 0
        if ring.element(0, 1).norm() == 1:
            initial_value = 1

        for a in range(initial_value, int(math.sqrt(p)) + 1):
            loop_element = ring.element(a, 1)

            for b in range(1, int(math.sqrt(p)) + 1):
                loop_element = ring.element(a, b)
                if abs(ring.norm(loop_element)) > 1:
                    quotient = ring.divide(p_element, loop_element)

                    if quotient.is_integral():
                        return [loop_element, quotient]

        return [p_element]

    @staticmethod
    def compute_string(ring, elements):
        if len(elements) == 1:
            return str(ring.to_string(elements[0]))
        else:
            return ''.join(f'({ring.to_string(x)})' for x in elements)