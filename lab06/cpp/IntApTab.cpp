#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <iomanip>

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

std::pair<std::vector<int>, std::vector<std::vector<int>>> generate_table(int a, int b, int start_x, int start_y, int width, int height) {
    std::vector<std::vector<int>> modulo_table;
    std::vector<int> header;

    for (int j = start_x; j < start_x + width; ++j) {
        header.push_back(j);
    }

    for (int i = start_y; i < start_y + height; ++i) {
        std::vector<int> current_row;
        current_row.push_back(i);

        for (int j = start_x; j < start_x + width; ++j) {
            int result = chinese_value(a, b, i, j);
            current_row.push_back(result);
        }

        modulo_table.push_back(current_row);
    }

    return {header, modulo_table};
}

void print_table(const std::vector<int>& headers, const std::vector<std::vector<int>>& table) {
    // Print the header
    std::cout << std::setw(5) << " ";
    for (int h : headers) {
        std::cout << std::setw(5) << h;
    }
    std::cout << std::endl;

    // Print the table
    for (const auto& row : table) {
        for (const auto& cell : row) {
            if (cell != -1) {
                std::cout << std::setw(5) << cell;
            } else {
                std::cout << std::setw(5) << "";
            }
        }
        std::cout << std::endl;
    }
}

int main() {
    int a, b;
    std::cout << "Enter number a: ";
    std::cin >> a;
    std::cout << "Enter number b: ";
    std::cin >> b;

    if (std::cin.fail() || a <= 0 || b <= 0) {
        std::cout << "Please enter valid positive numbers for a and b." << std::endl;
        return 1;
    }

    int start_x = 0, start_y = 0;
    int width = b - start_x;
    int height = a - start_y;

    if (start_x < 0 || start_x >= b || start_y < 0 || start_y >= a ||
        width <= 0 || height <= 0 || (start_x + width - 1) >= b || (start_y + height - 1) >= a) {
        std::cout << "Invalid values for startX, startY, width, or height. Please check and try again." << std::endl;
        return 1;
    }

    std::cout << "Intersection of arithmetic progressions (mod " << a << ") and (mod " << b << ")" << std::endl;

    auto [headers, table] = generate_table(a, b, start_x, start_y, width, height);
    print_table(headers, table);

    return 0;
}
