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

// Function to generate the addition table
vector<vector<string>> generate_table(int n, int start_x, int start_y, int width, int height, bool toggle) {
    vector<string> header;
    
    header.push_back("");
    for (int k = start_x; k < start_x + width; k++) {
        header.push_back(to_string(k));
    }

    vector<vector<string>> power_table;

    for (int a = start_y; a < start_y + height; a++) {
        vector<string> current_row;
        current_row.push_back(to_string(a));

        for (int k = start_x; k < start_x + width; k++) {
            int result = (a + k) % n;
            int common_factor = gcd(result, n);

            if (!toggle || (common_factor == 1)) {
                current_row.push_back(to_string(result));
            } else {
                current_row.push_back("");
            }
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

    cout << "Enter n: ";
    cin >> n;

    vector<vector<string>> table = generate_table(n, 0, 0, n, n, false);
    print_table(table);

    return 0;
}
