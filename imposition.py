from rich import print
import matplotlib.pyplot as plt
import pandas as pd
import os

# Define tax brackets
current_tax_brackets = {
    "default_rate": 0.50,
    "description": "Current tax brackets (2024 income, 2025 taxes)",
    "instalments": [
        {"amount": 15820, "rate": 0.25},
        {"amount": 12100, "rate": 0.40},
        {"amount": 20400, "rate": 0.45}
    ]
}

new_tax_brackets = {
    "default_rate": 0.45,
    "description": "New tax brackets based on Bart De Wever's proposal (N-VA)",
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

def generate_tax_report(revenues, systems) -> pd.DataFrame:
    """
    Generate tax data for given revenues and taxation systems.
    """
    data = []
    for revenue in revenues:
        row = {'revenue': revenue}
        for system_name, system in systems.items():
            tax = calculate_total_tax(revenue, system)
            row[f'{system_name}_tax'] = tax
        data.append(row)
    return pd.DataFrame(data)

def enrich_data(df) -> pd.DataFrame:
    """
    Enrich data from a DataFrame.
    """
    df['rate_super_nota_bart_de_wever_102024'] = df['super_nota_bart_de_wever_102024_tax'] / df['revenue']
    df['rate_current_system'] = df['current_system_tax'] / df['revenue']
    df['diff'] = ((df['rate_current_system'] - df['rate_super_nota_bart_de_wever_102024']) / df['rate_current_system']).abs() * 100
    df.to_csv("./imposition.csv", index=False)
    return df

def plot_tax_report(df, output_image) -> None:
    """
    Plot tax data from a DataFrame and save as an image.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df['revenue'], df['rate_current_system'], label='Current System')
    plt.plot(df['revenue'], df['rate_super_nota_bart_de_wever_102024'], label='Super Nota Bart De Wever 102024')
    plt.xlabel('Revenue')
    plt.ylabel('Tax Rate')
    plt.title('Comparison of Tax Bracket Systems in Belgium')
    plt.legend(loc='lower right')

    # Plot difference on secondary y-axis
    ax2 = plt.gca().twinx()
    ax2.plot(df['revenue'], df['diff'], label='Difference (%)', color='purple', linestyle=':')
    ax2.set_ylabel('Difference (%)')

    # Add a line for median revenue at 4,076 euros per month (2022 data statbel)
    plt.axvline(x=4076 * 12, color='green', linestyle='--', label='Median Revenue')

    # Add legend
    plt.legend()
    plt.savefig(output_image)

# Main execution
if __name__ == "__main__":
    revenue_range = range(5000, 200000, 500)
    systems = {
        "current_system": current_tax_brackets,
        "super_nota_bart_de_wever_102024": new_tax_brackets
    }

    df = generate_tax_report(revenue_range, systems)
    df = enrich_data(df)
    plot_tax_report(df, 'imposition.png')
