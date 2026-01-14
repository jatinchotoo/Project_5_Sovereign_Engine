import pandas as pd
import os
import re

def process_tax_and_consolidation():
    """
    Project 5: Sovereign Engine - Layer 2 (Enhanced)
    Purpose: Read Layer 1 data, calculate corporate tax (27%), 
    and generate high-level KPIs for the South African reporting environment.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'data', 'ESFE_FACT_GL.csv')
    output_path = os.path.join(base_dir, 'data', 'ESFE_CONSOLIDATED_FINANCIALS.csv')

    print(f"--- Sovereign Engine: Layer 2 Execution ---")
    
    # 1. Check if Layer 1 data exists
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found. Please run Layer 1 first.")
        return

    # 2. Load the Ledger
    df = pd.read_csv(input_path)

    # 3. Dynamic Column Detection & Cleaning
    cols = df.columns.tolist()
    is_single_col = 'amount' in cols or 'amount_zar' in cols
    
    def clean_val(val):
        if pd.isna(val): return 0.0
        if isinstance(val, (int, float)): return float(val)
        clean_str = re.sub(r'[^\d.-]', '', str(val))
        return float(clean_str) if clean_str else 0.0

    # Normalize Data
    if is_single_col:
        amt_col = 'amount_zar' if 'amount_zar' in cols else 'amount'
        df['norm_debit'] = df[amt_col].apply(lambda x: clean_val(x) if clean_val(x) > 0 else 0.0)
        df['norm_credit'] = df[amt_col].apply(lambda x: abs(clean_val(x)) if clean_val(x) < 0 else 0.0)
    else:
        d_col = 'debit' if 'debit' in cols else 'debit_zar'
        c_col = 'credit' if 'credit' in cols else 'credit_zar'
        df['norm_debit'] = df[d_col].apply(clean_val)
        df['norm_credit'] = df[c_col].apply(clean_val)

    # 4. Advanced Financial Intelligence (ZAR Focused)
    # Masks help identify specific account types for high-level reporting
    rev_mask = df['account_name'].str.contains('Revenue|Sales|Subscription', case=False, na=False)
    exp_mask = df['account_name'].str.contains('Cost|Expense|Salary|Operating|Infrastructure', case=False, na=False)
    tax_mask = df['account_name'].str.contains('Tax|VAT|Sars', case=False, na=False)
    
    total_rev = df[rev_mask]['norm_credit'].sum()
    total_opex = df[exp_mask]['norm_debit'].sum()
    
    # EBITDA Calculation
    ebitda = total_rev - total_opex
    
    # Tax Calculation Logic
    actual_tax = df[tax_mask]['norm_debit'].sum() + df[tax_mask]['norm_credit'].sum()
    sa_tax_rate = 0.27
    projected_tax = max(0, ebitda * sa_tax_rate) if actual_tax == 0 else actual_tax
    
    net_profit = ebitda - projected_tax
    margin_pct = (net_profit / total_rev * 100) if total_rev > 0 else 0

    # 5. Create Consolidated Summary Output
    summary_data = [
        {'Metric': 'Total Group Revenue', 'Amount': round(total_rev, 2)},
        {'Metric': 'Total Operating Costs', 'Amount': round(total_opex, 2)},
        {'Metric': 'EBITDA', 'Amount': round(ebitda, 2)},
        {'Metric': 'Tax Provision (27%)', 'Amount': round(projected_tax, 2)},
        {'Metric': 'Net Operational Result', 'Amount': round(net_profit, 2)},
        {'Metric': 'Net Profit Margin (%)', 'Amount': round(margin_pct, 2)}
    ]
    
    summary_df = pd.DataFrame(summary_data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    summary_df.to_csv(output_path, index=False)

    # 6. Terminal Reporting
    print(f"\n--- SOVEREIGN ENGINE: SOUTH AFRICA SNAPSHOT ---")
    print(f"Total Group Revenue:      R {total_rev:,.2f}")
    print(f"Total Operating Costs:    R {total_opex:,.2f}")
    print(f"-----------------------------------------------")
    print(f"EBITDA:                   R {ebitda:,.2f}")
    print(f"Tax Provision (27%):      R {projected_tax:,.2f}")
    print(f"-----------------------------------------------")
    print(f"Net Operational Result:   R {net_profit:,.2f}")
    print(f"Net Profit Margin:        {margin_pct:.2f}%")
    print(f"-----------------------------------------------")
    print(f"SUCCESS: Consolidated financials saved to {output_path}")

if __name__ == "__main__":
    process_tax_and_consolidation()
    