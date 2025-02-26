#include <iostream>
#include <vector>
#include <map>
#include <stdexcept>
#include <iostream>
#include <map>
#include <vector>
#include <cmath>
#include <stdexcept>
#include <regex>

using namespace std;

map<int, int> parse_polynomial(const string& input_str) {
    map<int, int> poly;
    std::regex x_regex(R"(([+-]?\d*)(x)?(?:\^(\d+))?)");
    auto words_begin = sregex_iterator(input_str.begin(), input_str.end(), x_regex);
    auto words_end = sregex_iterator();

    for (auto it = words_begin; it != words_end; ++it) {
        smatch match = *it;
        string c = match[1].str();
        string x = match[2].str();
        string p = match[3].str();

        if (c.empty() && x.empty() && p.empty()) continue;

        int coeff = (c == "-" ? -1 : (c == "+" || c.empty() ? 1 : stoi(c)));
        int power = (p.empty() ? (x.empty() ? 0 : 1) : stoi(p));

        poly[power] += coeff;
    }
    
    return poly;
}

string polynomial_to_string(const map<int, int>& polynomial) {
    string result;
    bool is_first = true;
    for (auto it = polynomial.rbegin(); it != polynomial.rend(); ++it) {
        int power = it->first;
        int coefficient = it->second;

        if (coefficient != 0) {
            if (coefficient > 0 && !is_first) result += "+";
            if (power == 0) {
                result += to_string(coefficient);
            } else {
                string exponent = (power == 1) ? "x" : "x^" + to_string(power);
                if (coefficient == 1) result += exponent;
                else if (coefficient == -1) result += "-" + exponent;
                else result += to_string(coefficient) + exponent;
            }
            is_first = false;
        }
    }
    return result;
}

using bigint = long long;

bigint powerMod(bigint baseValue, int exponent, bigint modulo) {
    bigint result = 1;
    baseValue = baseValue % modulo;

    while (exponent > 0) {
        if (exponent % 2 == 1) {
            result = (result * baseValue) % modulo;
        }
        baseValue = (baseValue * baseValue) % modulo;
        exponent /= 2;
    }
    return result;
}

bigint EvaluatePolynomial(const map<int, int>& polynomial, bigint x, bigint n) {
    bigint result = 0;
    auto it = polynomial.rbegin();
    int lastPower = it->first;

    for (auto it = polynomial.rbegin(); it != polynomial.rend(); ++it) {
        int currentPower = it->first;
        int coefficient = it->second;
        bigint difference = lastPower - currentPower;
        bigint powerForDifference = powerMod(x, difference, n);
        result = (result * powerForDifference) % n;
        result = (result + coefficient) % n;
        lastPower = currentPower;
    }
    if (lastPower != 0) {
        bigint powerForLast = powerMod(x, lastPower, n);
        result = (result * powerForLast) % n;
    }
    return result;
}

vector<int> FindSolutions(const map<int, int>& polynomial, int n) {
    vector<int> result;
    for (int i = 0; i < n; i++) {
        if (EvaluatePolynomial(polynomial, i, n) == 0) {
            result.push_back(i);
        }
    }
    return result;
}

map<int, int> polynomialDerivative(const map<int, int>& polynomial) {
    map<int, int> result;
    for (const auto& [power, coefficient] : polynomial) {
        int newPower = power - 1;
        int newCoefficient = power * coefficient;
        if (newPower >= 0 && newCoefficient != 0) {
            result[newPower] = newCoefficient;
        }
    }
    return result;
}

vector<pair<int, string>> FindSolutionsWithType(const map<int, int>& polynomial, int n) {
    vector<pair<int, string>> result;
    map<int, int> derivative = polynomialDerivative(polynomial);
    vector<int> solutions = FindSolutions(polynomial, n);

    for (int solution : solutions) {
        bigint derivativeAtSolution = EvaluatePolynomial(derivative, solution, n);
        if (derivativeAtSolution == 0) {
            result.emplace_back(solution, "singular");
        } else {
            result.emplace_back(solution, "regular");
        }
    }
    return result;
}

pair<bigint, bigint> euclideanAlgorithm(bigint a, bigint b) {
    vector<tuple<bigint, bigint, bigint, bigint, bigint>> result;
    pair<bigint, bigint> previousLinear = {1, 0}, currentLinear = {0, 1};

    if (a < 0) {
        previousLinear = {-1, 0};
        a = -a;
    }
    if (b < 0) {
        currentLinear = {0, -1};
        b = -b;
    }
    if (a < b) swap(a, b), swap(previousLinear, currentLinear);

    bigint big = a, small = b;
    while (small > 0) {
        bigint r = big % small;
        bigint q = big / small;
        big = small;
        small = r;

        pair<bigint, bigint> newLinear = {previousLinear.first - q * currentLinear.first,
                                  previousLinear.second - q * currentLinear.second};
        previousLinear = currentLinear;
        currentLinear = newLinear;
    }

    return previousLinear;
}


bigint inverse(bigint a, bigint n) {
    if (n == 1) return 1;
    auto result = euclideanAlgorithm(n, a % n);
    return result.second;
}

vector<pair<bigint, bigint>> henselLiftRegular(map<int, int>& polynomial, int solution, bigint p, int maxPower) {
    if (EvaluatePolynomial(polynomial, solution, p) != 0) {
        throw runtime_error("Expected solution to be a root of the polynomial modulo p.");
    }

    map<int, int> derivative = polynomialDerivative(polynomial);
    bigint derivativeValue = EvaluatePolynomial(derivative, solution, p);

    if (derivativeValue == 0) {
        throw runtime_error("Expected solution not to be a root of the derivative of the polynomial modulo p.");
    }

    bigint inverseDerivativeValueModp = inverse(derivativeValue, p);

    vector<pair<bigint, bigint>> result;
    bigint currentLifted = solution;
    bigint previousPower = 1;

    for (int i = 1; i < maxPower; i++) {
        bigint currentPower = previousPower * p;
        bigint currentValue = EvaluatePolynomial(polynomial, currentLifted, currentPower);
        bigint multiple = currentValue / previousPower;

        bigint currentC = ((-inverseDerivativeValueModp * multiple) % p + p) % p;
        currentLifted = currentLifted + currentC * previousPower;
        result.emplace_back(currentC, currentLifted);
        previousPower = currentPower;
    }

    return result;
}

vector<pair<bigint, bigint>> allHenselSingularLifts(map<int, int>& polynomial, int solution, bigint p, int currentPower) {
    if (EvaluatePolynomial(polynomial, solution, p) != 0) {
        throw runtime_error("Expected solution to be a root of the polynomial modulo p.");
    }

    map<int, int> derivative = polynomialDerivative(polynomial);
    bigint derivativeValue = EvaluatePolynomial(derivative, solution, p);

    if (derivativeValue != 0) {
        throw runtime_error("Expected solution to be a root of the derivative of the polynomial modulo p.");
    }

    vector<pair<bigint, bigint>> result;
    bigint previousPower = 1;
    for (int i = 1; i < currentPower; i++) {
        previousPower *= p;
    }
    bigint powerValue = previousPower * p;
    bigint evaluation = EvaluatePolynomial(polynomial, solution, powerValue);

    if (evaluation == 0) {
        for (int i = 0; i < p; i++) {
            bigint currentSolution = solution + previousPower * i;
            result.emplace_back(i, currentSolution);
        }
    }

    return result;
}

bool isRegular(map<int, int>& polynomial, int solution, bigint p) {
    map<int, int> derivative = polynomialDerivative(polynomial);
    return EvaluatePolynomial(derivative, solution, p) != 0;
}


int main() {
    string polynomial_input;
    int n;
    
    cout << "Enter polynomial: ";
    getline(cin, polynomial_input);
    cout << "Enter modulus n: ";
    cin >> n;
    
    map<int, int> parsed_polynomial = parse_polynomial(polynomial_input);
    vector<pair<int, string>> solutions = FindSolutionsWithType(parsed_polynomial, n);
    string polynomial_str = polynomial_to_string(parsed_polynomial);
    
    if (!solutions.empty()) {
        std::cout << "The solutions to " << polynomial_str << " ≡ 0 (mod " << n << ") are x = ";
        for (size_t i = 0; i < solutions.size(); ++i) {
            std::cout << solutions[i].first;
            if (i < solutions.size() - 1) std::cout << ", ";
        }
        std::cout << ".\n";
    } else {
        std::cout << "No solutions to " << polynomial_str << " ≡ 0 (mod " << n << ") exist." << std::endl;
    }
    
    int solution_to_lift;
    std::cout << "Enter solution to lift: ";
    std::cin >> solution_to_lift;
    
    std::vector<std::pair<int, std::string>> relevant_tuple;
    for (const auto &sol : solutions) {
        if (sol.first == solution_to_lift) {
            relevant_tuple.push_back(sol);
        }
    }
    
    while (relevant_tuple.empty()) {
        std::cout << "Not a solution! Enter solution to lift: ";
        std::cin >> solution_to_lift;
        
        relevant_tuple.clear();
        for (const auto &sol : solutions) {
            if (sol.first == solution_to_lift) {
                relevant_tuple.push_back(sol);
            }
        }
    }
    
    if (relevant_tuple[0].second == "regular") {
        int power_to_lift;
        std::cout << "Enter maximal power to lift: ";
        std::cin >> power_to_lift;
        
        std::vector<std::pair<bigint, bigint>> lifted = henselLiftRegular(parsed_polynomial, solution_to_lift, n, power_to_lift + 1);
        
        for (size_t i = 1; i < lifted.size(); ++i) {
            std::cout << "The lifted solution is x ≡ " << lifted[i].second << " (mod " << n << "^" << (i+1) << ").\n";
        }
    }
    
    return 0;
}