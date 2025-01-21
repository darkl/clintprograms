from tabulate import tabulate

# Function to generate the table
def generate_table(b, c, x_center, y_center, width, height):
    x_min = x_center - (width // 2)
    x_max = x_center + (width // 2)
    y_min = y_center - (height // 2)
    y_max = y_center + (height // 2)

    headers = []
    # Generate header row
    for x in range(x_min, x_max + 1):
        headers.append(x)

    table_content = []
    # Generate table content
    for y in range(y_min, y_max + 1):
        current_row = [y]
        for x in range(x_min, x_max + 1):
            result = x * b + y * c
            current_row.append(result)
        table_content.append(current_row)

    return headers, table_content

def main():
    b = int(input("Enter b: "))
    c = int(input("Enter c: "))
    x_center = int(input("Enter xCenter: "))
    y_center = int(input("Enter yCenter: "))
    width = int(input("Enter width: "))
    height = int(input("Enter height: "))

    headers, table = generate_table(b, c, x_center, y_center, width, height)
    print(tabulate(table, headers=headers, tablefmt="grid"))

main()