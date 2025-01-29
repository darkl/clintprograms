#include <iostream>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
#include <random>

using BigInteger = boost::multiprecision::cpp_int;

BigInteger mod_exp(BigInteger base, BigInteger exp, BigInteger mod) {
    BigInteger result = 1;
    base = base % mod;

    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }
        exp /= 2;
        base = (base * base) % mod;
    }

    return result;
}

BigInteger random_bigint(BigInteger low, BigInteger high) {
    std::random_device rd;
    std::mt19937 gen(rd());
    
    BigInteger range = high - low + 1;
    BigInteger random_number = 0;
    BigInteger base = 1;
    while (range > 0) {
        // Generate random 32-bit chunks
        std::uniform_int_distribution<uint32_t> dist(0, std::numeric_limits<uint32_t>::max());
        uint32_t chunk = dist(gen);
        random_number += base * chunk;
        base *= (static_cast<BigInteger>(std::numeric_limits<uint32_t>::max()) + 1);
        range /= (static_cast<BigInteger>(std::numeric_limits<uint32_t>::max()) + 1);
    }
    return low + (random_number % (high - low + 1));
}


bool miller_rabin_test(BigInteger n, int k) {
    if (n == 2 || n == 3) {
        return true;
    }
    if (n < 2 || n % 2 == 0) {
        return false;
    }

    BigInteger s = 0;
    BigInteger d = n - 1;

    while (d % 2 == 0) {
        d /= 2;
        ++s;
    }

    std::random_device rd;
    std::mt19937 gen(rd());

    for (int i = 0; i < k; ++i) {
        BigInteger a = random_bigint(2, n - 2);
        BigInteger x = mod_exp(a, d, n);

        if (x == 1 || x == n - 1) {
            continue;
        }

        bool is_composite = true;
        for (BigInteger r = 0; r < s - 1; ++r) {
            x = (x * x) % n;
            if (x == n - 1) {
                is_composite = false;
                break;
            }
        }

        if (is_composite) {
            return false;
        }
    }

    return true;
}

BigInteger find_next_prime_big(BigInteger a) {
    if (a < 2) {
        return 2;
    }

    BigInteger candidate = a + 1;
    while (true) {
        if (miller_rabin_test(candidate, 10)) {
            return candidate;
        }
        ++candidate;
    }
}

BigInteger find_next_prime(BigInteger a) {
    if (a >= 1000000000) {
        return find_next_prime_big(a).convert_to<int>();
    }

    if (a <= 1) {
        return 2;
    }

    int n = a.convert_to<int>();
    int sieve_size = 2 * n;
    std::vector<bool> sieve(sieve_size, true);

    for (int p = 2; p * p < sieve_size; ++p) {
        if (sieve[p]) {
            for (int i = p * p; i < sieve_size; i += p) {
                sieve[i] = false;
            }
        }
    }

    for (int i = n + 1; i < sieve_size; ++i) {
        if (sieve[i]) {
            return i;
        }
    }

    return -1; // This should not happen given a reasonable input.
}

int main() {
    std::cout << "Enter a: ";
    BigInteger a;
    std::cin >> a;

    BigInteger p;
    if (a >= 1000000000) {
        p = find_next_prime_big(a);
    } else {
        p = find_next_prime(a);
    }

    std::cout << p << std::endl;
    return 0;
}