#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <boost/multiprecision/cpp_int.hpp>

using BigInteger = boost::multiprecision::cpp_int;

BigInteger removeFactors(BigInteger n, std::vector<BigInteger>& factors, const BigInteger& prime) {
    while (n % prime == 0) {
        factors.push_back(prime);
        n /= prime;
    }

    return n;
}

std::vector<BigInteger> factor(BigInteger n) {
    std::vector<BigInteger> result;

    // Remove powers of 2, 3, 5
    for (const BigInteger& prime : {2, 3, 5}) {
        n = removeFactors(n, result, prime);
    }

    BigInteger d = 0;

    // Trial division with selected forms of d
    BigInteger squareRoot = sqrt(n);
    while (n > 1 && d <= squareRoot) {
        const std::vector<BigInteger> formsOfD = {1, 7, 11, 13, 17, 19, 23, 29};

        for (const BigInteger& currentResidue : formsOfD) {
            BigInteger currentDivisor = d + currentResidue;

            if (currentDivisor != 1 && n % currentDivisor == 0) {
                n = removeFactors(n, result, currentDivisor);
            }
        }

        d += 30;
    }

    if (n > 1) {
        result.push_back(n);
    }

    return result;
}

std::map<BigInteger, int> factorization(BigInteger n) {
    std::vector<BigInteger> factors = factor(n);
    std::map<BigInteger, int> groupedFactors;

    for (const BigInteger& factor : factors) {
        groupedFactors[factor]++;
    }

    return groupedFactors;
}

std::string factorizationString(const BigInteger& n) {
    std::map<BigInteger, int> factorizationResult = factorization(n);

    std::ostringstream resultStream;
    bool first = true;

    for (const auto& [key, value] : factorizationResult) {
        if (!first) {
            resultStream << " x ";
        }
        first = false;
        if (value > 1) {
            resultStream << key << "^" << value;
        } else {
            resultStream << key;
        }
    }

    return resultStream.str();
}



int main() {
    BigInteger n;
    std::cout << "Enter a number: ";
    std::cin >> n;

    std::string result = factorizationString(n);
    std::cout << "Factorization: " << result << std::endl;

    return 0;
}
