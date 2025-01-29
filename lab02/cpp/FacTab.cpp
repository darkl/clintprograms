#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <boost/multiprecision/cpp_int.hpp>

using namespace std;

int prime_factor(int n, const vector<int>& primes) {
    int square_root = sqrt(n);
    for (int p : primes) {
        if (p > square_root) return n;
        if (n % p == 0) return p;
    }
    return n;
}

int gcd(int a, int b) {
    a = abs(a);
    b = abs(b);
    if (b > a) swap(a, b);
    
    while (true) {
        if (b == 0) return a;
        a %= b;
        if (a == 0) return b;
        b %= a;
    }
}

vector<int> get_primes_until(int n) {
    vector<bool> numbers(n + 1, false);
    int square_root = sqrt(n);
    int location = 0;
    numbers[0] = true;

    while (location <= square_root) {
        auto it = find(numbers.begin() + location + 1, numbers.end(), false);
        if (it == numbers.end()) break;
        location = distance(numbers.begin(), it);
        int prime = location + 1;

        for (int i = location + prime; i <= n; i += prime) {
            numbers[i] = true;
        }
    }

    vector<int> result;
    for (int i = 0; i <= n; ++i) {
        if (!numbers[i]) result.push_back(i + 1);
    }
    return result;
}

vector<vector<string>> generate_table(int start, int height) {
    int limit = ceil(sqrt(10 * (start + height)));
    vector<int> primes = get_primes_until(limit);

    vector<string> header;
    for (int i = 1; i < 10; i += 2) {
        header.push_back("10n + " + to_string(i));
    }

    vector<vector<string>> table_content;
    int value = start;

    for (int i = 0; i <= height; ++i) {
        vector<string> current_row;
        current_row.push_back(to_string(value));
        
        for (int x = 1; x < 10; x += 2) {
            int number = 10 * value + x;
            int result = prime_factor(number, primes);
            
            if (number != result) {
                current_row.push_back(to_string(result));
            } else {
                current_row.push_back("prime");
            }
        }

        table_content.push_back(current_row);
        ++value;
    }

    return table_content;
}


int main() {
    int start, height;
    cout << "Enter start: ";
    cin >> start;
    cout << "Enter height: ";
    cin >> height;

    vector<vector<string>> table = generate_table(start, height);

    cout << left << setw(10) << "n";
    for (const auto& col : {"10n+1", "10n+3", "10n+5", "10n+7", "10n+9"}) {
        cout << setw(10) << col;
    }
    cout << endl;

    for (const auto& row : table) {
        for (const auto& cell : row) {
            cout << setw(10) << cell;
        }
        cout << endl;
    }

    return 0;
}