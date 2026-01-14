import pandas as pd
import os

def process_tax_and_consolidation():
    """
    Project 5: Sovereign Engine - Layer 2
    Purpose: Read Layer 1 data, calculate corporate tax (27%), and consolidate.
    """
    input_path = 'data/ESFE_FACT_GL.csv'
    output_path = 'data/ESFE_CONSOLIDATED_FINANCIALS.csv'

    # 1. Check if Layer 1 data exists
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found. Please run Layer 1 first.")
        return

    # 2. Load the Ledger
    df = pd.read_csv(input_path)

    # 3. Apply Strategic Finance Logic
    # Filter for Revenue (Code 4000) to calculate tax liability
    revenue_total = df[df['account_code'] == 4000]['amount'].sum()
    tax_rate = 0.27  # 27% SA Corporate Tax
    tax_liability = revenue_total * tax_rate

    # 4. Create Consolidated Summary
    summary_data = [
        {'Metric': 'Total Revenue', 'Amount': round(revenue_total, 2)},
        {'Metric': 'Corporate Tax Liability (27%)', 'Amount': round(tax_liability, 2)},
        {'Metric': 'Net After-Tax Revenue', 'Amount': round(revenue_total - tax_liability, 2)}
    ]
    
    summary_df = pd.DataFrame(summary_data)

    # 5. Save the processed data
    summary_df.to_csv(output_path, index=False)
    
    print("-" * 30)
    print("LAYER 2: PROCESSING COMPLETE")
    print(f"Total Revenue Found: R{revenue_total:,.2f}")
    print(f"Tax Calculated: R{tax_liability:,.2f}")
    print(f"Consolidated file saved at: {output_path}")
    print("-" * 30)

if __name__ == "__main__":
    process_tax_and_consolidation()
    
    