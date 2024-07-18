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
                'category': row['category']
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
    header = f"{'ID':<10}{'Product':<40}{'Category':<15}{'Quantity':<10}{'Price':<10}{'Discount':<10}{'Total':>10}"
    separator = '-' * len(header)

    print("\n" + separator)
    print(header)
    print(separator)

    total = 0
    for item_id, quantity in items.items():
        if item_id in products:
            product = products[item_id]
            price = product['price']
            category = product['category']
            discount_info = discounts.get(category, {'type': 'fixed', 'value': 0})
            discount_type = discount_info['type']
            discount_value = discount_info['value']

            discounted_price = apply_discount(price, discount_type, discount_value)
            discount_total = (price - discounted_price) * quantity
            final_total = discounted_price * quantity
            total += final_total

            # Print to console
            print(
                f"{item_id:<10}{product['name']:<40}{category:<15}{quantity:<10}{price:>10.2f}{discount_total:>10.2f}{final_total:>10.2f} INR")

            # Write to file
            if file_writer:
                file_writer.writerow([
                    item_id, product['name'], category, quantity,
                    f"{price:.2f}", f"{discount_total:.2f}", f"{final_total:.2f} INR"
                ])
        else:
            print(f"{item_id:<10}{'Unknown':<40}{'N/A':<15}{quantity:<10}{'N/A':>10}{'N/A':>10}{'N/A':>10}")

    print(separator)
    print(f"{'Total Amount':<70}{total:>10.2f} INR")
    print(separator)

    # Write total to file
    if file_writer:
        file_writer.writerow([])
        file_writer.writerow([''] * 6 + ['Total Amount', f"{total:.2f} INR"])

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

        # Write header for new day or continue with existing file
        file_writer.writerow(['ID', 'Product', 'Category', 'Quantity', 'Price', 'Discount', 'Total'])
        file_writer.writerow([''] * 7)

        while True:
            items = {}
            while True:
                item_id = input("Enter product ID (or press Enter to finish): ").strip()
                if item_id == "":
                    break
                if item_id in products:
                    quantity = int(input(f"Enter quantity for {products[item_id]['name']}: "))
                    if item_id in items:
                        items[item_id] += quantity
                    else:
                        items[item_id] = quantity
                else:
                    print("Product ID not found. Please try again.")

            if items:
                print_and_log_bill(items, products, discounts, file_writer)
            else:
                print("No items added. Please enter product IDs and quantities.")

            # End input after processing
            break

if __name__ == "__main__":
    main()
