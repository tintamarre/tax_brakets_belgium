from rich import print
import matplotlib.pyplot as plt
import pandas as pd
import os

# Define tax brackets
current_tax_brackets = {
    "default_rate": 0.50,
    "description": "Tranches d'imposition actuelles (revenus 2024 impots 2025)",
    "instalments": [
        {"amount": 15820, "rate": 0.25},
        {"amount": 12100, "rate": 0.40},
        {"amount": 20400, "rate": 0.45}
    ]
}

new_tax_brackets = {
    "default_rate": 0.45,
    "description": "Nouvelles tranches d'imposition basées sur la proposition de Bart De Wever (N-VA)",
    "instalments": [
        {"amount": 16000, "rate": 0.25},
        {"amount": 5000, "rate": 0.35},
        {"amount": 9000, "rate": 0.40}
    ]
}

def calculate_total_tax(revenue, tax_brackets) -> float:
    """
    Calculate the tax to be paid based on revenue and tax brackets.
    """
    total_tax = 0
    remaining_revenue = revenue

    for bracket in tax_brackets['instalments']:
        if remaining_revenue >= bracket['amount']:
            tax = bracket['amount'] * bracket['rate']
            remaining_revenue -= bracket['amount']
        else:
            tax = remaining_revenue * bracket['rate']
            remaining_revenue = 0

        total_tax += tax

    total_tax += remaining_revenue * tax_brackets['default_rate']
    return total_tax

def generate_tax_report(revenues, systems) -> str:
    """
    Generate tax data for given revenues and taxation systems.
    """
    data = "system_name1,tax1,system_name2,tax2,revenue\n"
    for revenue in revenues:
        for system_name, system in systems.items():
            tax = calculate_total_tax(revenue, system)
            data += f"{system_name},{tax},"
        data += f"{revenue}\n"
    return data

def save_report_to_csv(data, file_path) -> None:
    """
    Save data to a CSV file.
    """
    # delete file if it already exists
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'w') as f:
        f.write(data)
        
def enrich_data(file_path) -> None:
    """
    Enrich data from a CSV file.
    """
    df = pd.read_csv(file_path)
    df['rate1'] = df['tax1'] / df['revenue']
    df['rate2'] = df['tax2'] / df['revenue']
    df['diff'] = ((df['tax1'] - df['tax2']) / df['revenue']).abs() * 100
    df.to_csv(file_path, index=False)

    return df

def plot_tax_report(df, output_image) -> None:
    """
    Plot tax data from a CSV file and save as an image.
    """

    plt.figure(figsize=(10, 6))
    plt.plot(df['revenue'], df['rate1'], label='current_system')
    plt.plot(df['revenue'], df['rate2'], label='super-nota-bart-de-wever')
    plt.xlabel('Revenue')
    plt.ylabel('Tax rate')
    plt.title('Tax rate as a function of revenue')
    plt.legend(loc='lower right')
    # on other axis plot difference between the two systems
    plt.twinx()
    
    plt.plot(df['revenue'], df['diff'], label='difference', color='orange', linestyle='--')
    plt.ylabel('Difference (%)')
    
    # add a line for median revenue at 4,076 euros per month (2022 data statbel)
    plt.axvline(x=4076 * 12, color='grey', linestyle='--', label='Median revenue')
    
    # add legend
    plt.legend()
    
    plt.savefig(output_image)

# Main execution
revenue_range = range(5000, 200000, 500)
systems = {
    "current_system": current_tax_brackets,
    "super-nota-bart-de-wever": new_tax_brackets
}

data = generate_tax_report(revenue_range, systems)
csv_file = "./imposition.csv"
save_report_to_csv(data, csv_file)
df = enrich_data(csv_file)
plot_tax_report(df, 'imposition.png')
