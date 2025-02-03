#include <iostream>
#include <map>
#include <vector>
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

int power_mod(int base, int exponent, int mod) {
    int result = 1;
    base %= mod;
    while (exponent > 0) {
        if (exponent % 2 == 1) result = (1LL * result * base) % mod;
        base = (1LL * base * base) % mod;
        exponent /= 2;
    }
    return result;
}

int evaluate_polynomial(const map<int, int>& polynomial, int x, int n) {
    int result = 0;
    int last_power = polynomial.rbegin()->first;

    for (auto it = polynomial.rbegin(); it != polynomial.rend(); ++it) {
        int current_power = it->first;
        int coefficient = it->second;
        int difference = last_power - current_power;
        result = (result * power_mod(x, difference, n)) % n;
        result = (result + coefficient) % n;
        last_power = current_power;
    }
    if (last_power != 0) {
        result = (result * power_mod(x, last_power, n)) % n;
    }
    return result;
}

vector<int> find_solutions(const map<int, int>& polynomial, int n) {
    vector<int> solutions;
    for (int i = 0; i < n; i++) {
        if (evaluate_polynomial(polynomial, i, n) == 0) {
            solutions.push_back(i);
        }
    }
    return solutions;
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

int main() {
    string polynomial_input;
    int n;
    
    cout << "Enter polynomial: ";
    getline(cin, polynomial_input);
    cout << "Enter modulus n: ";
    cin >> n;
    
    map<int, int> parsed_polynomial = parse_polynomial(polynomial_input);
    vector<int> solutions = find_solutions(parsed_polynomial, n);
    string polynomial_str = polynomial_to_string(parsed_polynomial);
    
    if (!solutions.empty()) {
        cout << "The solutions to " << polynomial_str << " ≡ 0 (mod " << n << ") are x = ";
        for (size_t i = 0; i < solutions.size(); ++i) {
            cout << solutions[i] << (i + 1 < solutions.size() ? ", " : "");
        }
        cout << ".\n";
    } else {
        cout << "No solutions to " << polynomial_str << " ≡ 0 (mod " << n << ") exist.\n";
    }
    return 0;
}
