import pandas as pd
import matplotlib.pyplot as plt


def parse_bill_log(filename):
    # Read the CSV file
    df = pd.read_csv(filename, skip_blank_lines=False)

    # Filter out the empty lines and the lines containing 'Total Amount'
    df = df.dropna(how='all')  # Drop completely empty rows
    df = df[~df.iloc[:, -1].str.contains('Total Amount', na=False)]  # Drop rows with 'Total Amount'

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
    log_filename = 'bill_log_2024-07-14.csv'  # Change this to your log file name
    df = parse_bill_log(log_filename)
    category_revenue = calculate_category_revenue(df)
    plot_pie_chart(category_revenue)


if __name__ == "__main__":
    main()
