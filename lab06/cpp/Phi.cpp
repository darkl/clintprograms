#include <iostream>
#include <vector>
#include <map>
#include <cmath>

using namespace std;

map<int, int> factorization(int n);
vector<int> factor(int n);
int remove_factors(int &n, vector<int> &factors, int prime);


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

int phi(int n) {
    map<int, int> current_factorization = factorization(n);
    int result = 1;
    
    for (const auto &[prime, exponent] : current_factorization) {
        result *= (prime - 1);
        result *= pow(prime, exponent - 1);
    }
    
    return result;
}

int main() {
    int n;
    cout << "Enter number n: ";
    cin >> n;
    int result = phi(n);
    cout << "ϕ(" << n << ") = " << result << endl;
    return 0;
}
