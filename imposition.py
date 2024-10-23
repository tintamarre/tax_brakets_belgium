from rich import print
import matplotlib.pyplot as plt
import pandas as pd

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
    data = "system,revenue,tax\n"
    for revenue in revenues:
        for system_name, system in systems.items():
            tax = calculate_total_tax(revenue, system)
            data += f"{system_name},{revenue},{tax}\n"
            print(f"Revenue: {revenue} - Tax ({system_name}): {tax}")
    return data

def save_report_to_csv(data, file_path) -> None:
    """
    Save data to a CSV file.
    """
    with open(file_path, 'w') as f:
        f.write(data)

def plot_tax_report(file_path, output_image) -> None:
    """
    Plot tax data from a CSV file and save as an image.
    """
    df = pd.read_csv(file_path)
    df['rate'] = df['tax'] / df['revenue']
    df = df.groupby(['system', 'revenue']).sum().reset_index()

    fig, ax = plt.subplots()
    for key, grp in df.groupby(['system']):
        grp.plot(ax=ax, kind='line', x='revenue', y='rate', label=key)
    
    plt.savefig(output_image)

# Main execution
revenue_range = range(5000, 200000, 100)
systems = {
    "current_system": current_tax_brackets,
    "super-nota-bart-de-wever": new_tax_brackets
}

data = generate_tax_report(revenue_range, systems)
csv_file = "./imposition.csv"
save_report_to_csv(data, csv_file)
plot_tax_report(csv_file, 'imposition.png')
