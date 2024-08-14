import csv
import datetime

def load_products(filename):
    products = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products[row['id']] = {
                'name': row['product_name'],
                'price': float(row['price']),
                'category': row['category'],
                'stock': int(row['stock'])  # Load stock from CSV
            }
    return products

def load_discounts(filename):
    discounts = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            discounts[row['category']] = {
                'type': row['discount_type'],
                'value': float(row['discount_value'])
            }
    return discounts

def apply_discount(price, discount_type, discount_value):
    if discount_type == 'percentage':
        return price * (1 - discount_value / 100)
    elif discount_type == 'fixed':
        return price - discount_value
    return price

def print_and_log_bill(items, products, discounts, file_writer=None):
    header = f"{'ID':<10}{'Product':<40}{'Category':<15}{'Quantity':<10}{'Price':<10}{'Discount':<10}{'Total':>10}{'Savings':>10}"
    separator = '-' * len(header)

    print("\n" + separator)
    print(header)
    print(separator)

    total = 0
    total_savings = 0
    for item_id, quantity in items.items():
        if item_id in products:
            product = products[item_id]
            price = product['price']
            category = product['category']
            stock = product['stock']
            discount_info = discounts.get(category, {'type': 'fixed', 'value': 0})
            discount_type = discount_info['type']
            discount_value = discount_info['value']

            discounted_price = apply_discount(price, discount_type, discount_value)
            discount_total = (price - discounted_price) * quantity
            final_total = discounted_price * quantity
            total += final_total
            total_savings += discount_total

            # Print to console
            print(f"{item_id:<10}{product['name']:<40}{category:<15}{quantity:<10}{price:>10.2f}{discount_total:>10.2f}{final_total:>10.2f} INR{discount_total:>10.2f} INR")

            # Write to file
            if file_writer:
                file_writer.writerow([
                    item_id, product['name'], category, quantity,
                    f"{price:.2f}", f"{discount_total:.2f}", f"{final_total:.2f} INR"
                ])
        else:
            print(f"{item_id:<10}{'Unknown':<40}{'N/A':<15}{quantity:<10}{'N/A':>10}{'N/A':>10}{'N/A':>10}{'N/A':>10}")

    print(separator)
    print(f"{'Total Amount':<70}{total:>10.2f} INR")
    print(f"{'Total Savings':<70}{total_savings:>10.2f} INR")
    print(separator)

    # Write total to file
    if file_writer:
        file_writer.writerow([])
        file_writer.writerow([''] * 6 + ['Total Amount', f"{total:.2f} INR"])
        file_writer.writerow([''] * 6 + ['Total Savings', f"{total_savings:.2f} INR"])
        file_writer.writerow([''] * 7)  # Blank line after each bill

def update_stock_and_warn(items, products):
    for item_id, quantity in items.items():
        if item_id in products:
            product = products[item_id]
            # Update stock after the bill is printed
            products[item_id]['stock'] -= quantity
            new_stock = products[item_id]['stock']

            # Warning if stock is low
            if new_stock < 10:
                print(f"Warning: Stock for {product['name']} is low (only {new_stock} left).")

def update_stock_file(filename, products):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'product_name', 'price', 'category', 'origin_price', 'stock'])  # Header
        for item_id, details in products.items():
            writer.writerow([
                item_id, details['name'], details['price'], details['category'],
                details['price'], details['stock']
            ])

def main():
    products_file = 'products.csv'
    discounts_file = 'categories.csv'

    # Load products and discounts
    products = load_products(products_file)
    discounts = load_discounts(discounts_file)

    # Determine log filename based on current date
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_filename = f'bill_log_{today_date}.csv'

    with open(log_filename, mode='a', newline='') as log_file:
        file_writer = csv.writer(log_file)

        # Only write the header if the file is new
        log_file.seek(0, 2)
        if log_file.tell() == 0:
            file_writer.writerow(['ID', 'Product', 'Category', 'Quantity', 'Price', 'Discount', 'Total'])

        while True:
            items = {}
            while True:
                item_id = input("Enter product ID (or press Enter to finish): ").strip()
                if item_id == "":
                    break
                if item_id in products:
                    max_stock = products[item_id]['stock']
                    if max_stock <= 0:
                        print(f"Sorry, {products[item_id]['name']} is out of stock.")
                        continue

                    quantity_str = input(f"Enter quantity for {products[item_id]['name']} (Available: {max_stock}): ").strip()
                    try:
                        quantity = int(quantity_str)
                        if quantity > max_stock:
                            print(f"Insufficient stock! Only {max_stock} available.")
                            continue

                        if item_id in items:
                            items[item_id] += quantity
                        else:
                            items[item_id] = quantity
                    except ValueError:
                        print("Invalid quantity. Please enter a valid number.")
                else:
                    print("Product ID not found. Please try again.")

            if items:
                # Print the bill first
                print_and_log_bill(items, products, discounts, file_writer)
                # Update stock and show warnings after bill is shown
                update_stock_and_warn(items, products)
            else:
                print("No items added. Please enter product IDs and quantities.")

            # End input after processing one bill
            break

    # Update stock in the products.csv file
    update_stock_file(products_file, products)

if __name__ == "__main__":
    main()
