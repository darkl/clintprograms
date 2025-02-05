from tabulate import tabulate

def generate_table(n, start_x, start_y, width, height, toggle):
    header = [k for k in range(start_x, start_x + width)]
    
    add_table = []
    
    for a in range(start_y, start_y + height):
        common_factor = gcd(a, n)
        current_row = [a]
        
        for k in range(start_x, start_x + width):
            result = (a+k) % n
            if not toggle or (common_factor == 1):
                current_row.append(result)
            else:
                current_row.append('')
        
        add_table.append(current_row)
    
    return [header, add_table]

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def main():
    n = int(input("Enter n: "))

    headers, table = generate_table(n, 0, 0, n, n, False)
    print(tabulate(table, headers=headers, tablefmt="grid"))

main()