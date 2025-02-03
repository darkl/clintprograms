#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

// Function to compute GCD of two numbers
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

// Function for modular exponentiation
int power_mod(int a, int b, int n) {
    int result = 1;
    a = a % n;

    while (b > 0) {
        // If b is odd, multiply result with a
        if (b % 2 == 1) {
            result = (result * a) % n;
        }
        // b must be even now
        b /= 2;
        a = (a * a) % n;
    }
    return result;
}

// Function to generate the power table
vector<vector<string>> generate_table(int n, int start_x, int start_y, int width, int height, bool toggle) {
    vector<string> header;
    
    header.push_back("");
    for (int k = start_x; k < start_x + width; k++) {
        header.push_back(to_string(k));
    }

    vector<vector<string>> power_table;

    for (int a = start_y; a < start_y + height; a++) {
        int common_factor = gcd(a, n);
        vector<string> current_row;
        current_row.push_back(to_string(a));
        int result = power_mod(a, start_x, n);

        for (int k = start_x; k < start_x + width; k++) {
            if (!toggle || (common_factor == 1 || k == 0)) {
                current_row.push_back(to_string(result));
            } else {
                current_row.push_back("");
            }
            result = (result * a) % n;
        }
        power_table.push_back(current_row);
    }

    // Add header as the first row of the table
    power_table.insert(power_table.begin(), vector<string>(header.size()));
    for (size_t i = 0; i < header.size(); ++i) {
        power_table[0][i] = header[i];
    }

    return power_table;
}

// Function to print the table
void print_table(const vector<vector<string>>& table) {
    for (const auto& row : table) {
        for (const auto& item : row) {
            cout << setw(10) << item << " "; // Adjust the width as needed
        }
        cout << endl;
    }
}

int main() {
    int start_x, start_y, width, height, n;

    cout << "Enter start x: ";
    cin >> start_x;
    cout << "Enter start y: ";
    cin >> start_y;
    cout << "Enter width: ";
    cin >> width;
    cout << "Enter height: ";
    cin >> height;
    cout << "Enter n: ";
    cin >> n;

    vector<vector<string>> table = generate_table(n, start_x, start_y, width, height, false);
    print_table(table);

    return 0;
}
