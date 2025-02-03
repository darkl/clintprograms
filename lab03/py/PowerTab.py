from tabulate import tabulate

def generate_table(n, start_x, start_y, width, height, toggle):
    header = [k for k in range(start_x, start_x + width)]
    
    power_table = []
    
    for a in range(start_y, start_y + height):
        common_factor = gcd(a, n)
        current_row = [a]
        result = power_mod(a, start_x, n)
        
        for k in range(start_x, start_x + width):
            if not toggle or (common_factor == 1 or k == 0):
                current_row.append(result)
            else:
                current_row.append('')
            
            result = (result * a) % n
        
        power_table.append(current_row)
    
    return [header, power_table]

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def power_mod(a, b, n):
    result = 1
    a = a % n
    
    while b > 0:
        # If b is odd, multiply result with a
        if b % 2 == 1:
            result = (result * a) % n
        
        # b must be even now
        b //= 2
        a = (a * a) % n
    
    return result



def main():
    start_x = int(input("Enter start x: "))
    start_y = int(input("Enter start y: "))
    width = int(input("Enter width: "))
    height = int(input("Enter height: "))
    n = int(input("Enter n: "))

    headers, table = generate_table(n, start_x, start_x, width, height, False)
    print(tabulate(table, headers=headers, tablefmt="grid"))

main()