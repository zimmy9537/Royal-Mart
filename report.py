import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_bill_log(filename):
    # Read the CSV file while ignoring problematic lines
    with open(filename, mode='r') as file:
        lines = file.readlines()

    # Filter out lines that don't have exactly 7 fields
    valid_lines = [line for line in lines if len(line.split(',')) == 7]

    # Create a DataFrame from the valid lines
    from io import StringIO
    df = pd.read_csv(StringIO(''.join(valid_lines)), skip_blank_lines=True)

    return df

def calculate_category_revenue(df):
    # Calculate total revenue by category
    df['Total'] = df['Total'].replace({' INR': ''}, regex=True).astype(float)  # Remove ' INR' and convert to float
    category_revenue = df.groupby('Category')['Total'].sum()
    return category_revenue

def plot_pie_chart(category_revenue):
    # Plot a pie chart for category-wise revenue
    plt.figure(figsize=(10, 7))
    plt.pie(category_revenue, labels=category_revenue.index, autopct='%1.1f%%', startangle=140)
    plt.title('Category-wise Revenue Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Generate a category-wise revenue pie chart from a bill log file.")
    parser.add_argument('log_filename', type=str, help="Path to the bill log CSV file")
    args = parser.parse_args()

    df = parse_bill_log(args.log_filename)
    category_revenue = calculate_category_revenue(df)
    plot_pie_chart(category_revenue)

if __name__ == "__main__":
    main()
