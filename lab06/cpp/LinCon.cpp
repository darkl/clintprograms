#include <iostream>
#include <vector>
#include <map>
#include <cmath>

using namespace std;

int gcd(int a, int b) {
    while (b) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

pair<int, int> euclidean_algorithm(int a, int b) {
    int big = max(a, b), small = min(a, b);
    int prev_x = 1, prev_y = 0;
    int curr_x = 0, curr_y = 1;

    while (small > 0) {
        int q = big / small;
        int temp = big % small;
        big = small;
        small = temp;
        
        int temp_x = prev_x - q * curr_x;
        prev_x = curr_x;
        curr_x = temp_x;
        
        int temp_y = prev_y - q * curr_y;
        prev_y = curr_y;
        curr_y = temp_y;
    }
    return {prev_x, prev_y};
}

int inverse(int a, int n) {
    auto [_, y] = euclidean_algorithm(n, a % n);
    return y;
}

map<int, int> factorization(int n);
vector<int> factor(int n);
int remove_factors(int &n, vector<int> &factors, int prime);

int chinese_value(int a, int b, int r1, int r2) {
    int d = gcd(a, b);
    if (r1 % d != r2 % d) {
        return -1; // No solution
    }
    
    map<int, int> factorization_of_a = factorization(a);
    map<int, int> factorization_of_b = factorization(b);
    
    int a_prime = a, b_prime = b;
    
    for (auto &[prime, a_exponent] : factorization_of_a) {
        if (factorization_of_b.count(prime)) {
            int b_exponent = factorization_of_b[prime];
            if (a_exponent < b_exponent) {
                a_prime /= pow(prime, a_exponent);
            } else {
                b_prime /= pow(prime, b_exponent);
            }
        }
    }
    
    int first_coefficient = inverse(b_prime, a_prime);
    int second_coefficient = inverse(a_prime, b_prime);
    
    int solution = b_prime * first_coefficient * r1 + a_prime * second_coefficient * r2;
    int prime = a_prime * b_prime;
    
    solution = (solution % prime + prime) % prime;
    return solution;
}

map<int, int> factorization(int n) {
    vector<int> factors = factor(n);
    map<int, int> grouped_factors;
    for (int f : factors) {
        grouped_factors[f]++;
    }
    return grouped_factors;
}

vector<int> factor(int n) {
    vector<int> result;
    for (int prime : {2, 3, 5}) {
        remove_factors(n, result, prime);
    }
    int d = 0;
    int square_root = sqrt(n);
    while (n > 1 && d <= square_root) {
        for (int current_residue : {1, 7, 11, 13, 17, 19, 23, 29}) {
            int current_divisor = d + current_residue;
            if (current_divisor != 1 && n % current_divisor == 0) {
                remove_factors(n, result, current_divisor);
            }
        }
        d += 30;
    }
    if (n > 1) {
        result.push_back(n);
    }
    return result;
}

int remove_factors(int &n, vector<int> &factors, int prime) {
    while (n % prime == 0) {
        factors.push_back(prime);
        n /= prime;
    }
    return n;
}

int main() {
    int a, b, n;
    cout << "Enter number a: ";
    cin >> a;
    cout << "Enter number b: ";
    cin >> b;
    cout << "Enter number n: ";
    cin >> n;
    
    int d = gcd(a, n);
    if (b % d != 0) {
        cout << "No solutions." << endl;
    } else {
        int a_prime = a / d;
        int b_prime = b / d;
        int n_prime = n / d;
        
        int a_inverse = inverse(a_prime, n_prime);
        int result = ((a_inverse * b_prime % n_prime) + n_prime) % n_prime;
        
        cout << "x ≡ " << result << " (mod " << n_prime << ")" << endl;
    }
    
    return 0;
}
