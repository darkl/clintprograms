#include <iostream>
#include <vector>
#include <string>
#include <iomanip>

using namespace std;

vector<string> generate_header() {
    vector<string> header = {"10j"};
    for (int k = 1; k < 10; ++k) {
        header.push_back("10j + " + to_string(k));
    }
    return header;
}

int gcd(int a, int b) {
    a = abs(a);
    b = abs(b);
    while (b) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int factorial_modulo(int a, int n) {
    int result = 1;
    for (int i = 1; i <= a; ++i) {
        result = (1LL * result * i) % n;
    }
    return result;
}

vector<vector<int>> generate_table(int n, int start_y, int given_height = -1) {
    int height = (given_height != -1) ? given_height : n;
    vector<vector<int>> table;
    int current_number = 10 * start_y;
    int result = factorial_modulo(current_number, n);

    int a = start_y;
    while (a <= start_y + height - 1 && !(given_height == -1 && result == 0 && a - start_y >= 10)) {
        vector<int> current_row = {a};
        for (int k = 0; k < 10; ++k) {
            current_row.push_back(result);
            result = (1LL * result * (current_number + 1)) % n;
            current_number += 1;
        }
        table.push_back(current_row);
        a += 1;
    }
    return table;
}

void print_table(const vector<string>& headers, const vector<vector<int>>& table) {
    cout << left << setw(8) << headers[0];
    for (size_t i = 1; i < headers.size(); ++i) {
        cout << setw(12) << headers[i];
    }
    cout << "\n";

    for (const auto& row : table) {
        for (const auto& val : row) {
            cout << setw(12) << val;
        }
        cout << "\n";
    }
}

int main() {
    int start, height, n;
    cout << "Enter start: ";
    cin >> start;
    cout << "Enter height: ";
    cin >> height;
    cout << "Enter n: ";
    cin >> n;

    vector<string> headers = generate_header();
    vector<vector<int>> table = generate_table(n, start, height);
    print_table(headers, table);

    return 0;
}
