import pandas as pd
import os
import re

def run_kpi_engine():
    """
    Step 3 of the Sovereign Engine:
    Transforms validated ledger entries into financial intelligence (KPIs).
    Localized for the South African (ZAR) reporting environment.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Prioritize the Consolidated ZAR file for the South African reporting entity
    consolidated_path = os.path.join(base_dir, 'data', 'ESFE_GROUP_CONSOLIDATED_ZAR.csv')
    validated_path = os.path.join(base_dir, 'data', 'ESFE_VALIDATED_GL.csv')
    
    input_path = consolidated_path if os.path.exists(consolidated_path) else validated_path
    output_path = os.path.join(base_dir, 'data', 'ESFE_KPIS.csv')

    print(f"--- KPI Engine Execution (South African Edition) ---")
    print(f"Source Data: {os.path.basename(input_path)}")
    
    if not os.path.exists(input_path):
        print(f"ERROR: Data not found. Please run Layer 2 or Layer 5 first.")
        return

    # 1. Load data
    df = pd.read_csv(input_path)

    # 2. Filter for valid records
    if 'control_status' in df.columns:
        clean_df = df[df['control_status'] == 'PASS'].copy()
    else:
        # If coming from Layer 5, we assume consolidated data is ready for analysis
        clean_df = df.copy()
    
    if clean_df.empty:
        print("ERROR: No records found to process.")
        return

    # 3. Dynamic Column Detection
    cols = clean_df.columns.tolist()
    is_single_col = 'amount' in cols or 'amount_zar' in cols
    
    def clean_val(val):
        if pd.isna(val): return 0.0
        if isinstance(val, (int, float)): return float(val)
        clean_str = re.sub(r'[^\d.-]', '', str(val))
        return float(clean_str) if clean_str else 0.0

    # 4. Normalize Data into standard Debit/Credit for aggregation
    if is_single_col:
        amt_col = 'amount_zar' if 'amount_zar' in cols else 'amount'
        clean_df['norm_debit'] = clean_df[amt_col].apply(lambda x: clean_val(x) if clean_val(x) > 0 else 0.0)
        clean_df['norm_credit'] = clean_df[amt_col].apply(lambda x: abs(clean_val(x)) if clean_val(x) < 0 else 0.0)
    else:
        # Priority mapping for SA Reporting: rep_zar -> zar -> standard
        d_col = next((c for c in ['rep_debit_zar', 'debit_zar', 'debit'] if c in cols), None)
        c_col = next((c for c in ['rep_credit_zar', 'credit_zar', 'credit'] if c in cols), None)
        
        if not d_col or not c_col:
            print(f"ERROR: Financial columns not detected.")
            return
            
        clean_df['norm_debit'] = clean_df[d_col].apply(clean_val)
        clean_df['norm_credit'] = clean_df[c_col].apply(clean_val)

    # 5. Aggregation Logic
    summary = clean_df.groupby('account_name').agg({
        'norm_debit': 'sum',
        'norm_credit': 'sum'
    }).reset_index()

    summary.columns = ['account_name', 'debit', 'credit']
    summary['total_volume_zar'] = summary['debit'] + summary['credit']
    
    # 6. Export KPI Summary
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    summary.to_csv(output_path, index=False)

    # 7. Advanced Financial Intelligence (ZAR Focused)
    rev_mask = summary['account_name'].str.contains('Revenue|Sales|Subscription', case=False, na=False)
    exp_mask = summary['account_name'].str.contains('Cost|Expense|Salary|Operating|Infrastructure', case=False, na=False)
    tax_mask = summary['account_name'].str.contains('Tax|VAT|Sars', case=False, na=False)
    
    total_rev = summary[rev_mask]['credit'].sum()
    total_opex = summary[exp_mask]['debit'].sum()
    
    # EBITDA Calculation
    ebitda = total_rev - total_opex
    
    # Check for actual tax entries
    actual_tax = summary[tax_mask]['debit'].sum() + summary[tax_mask]['credit'].sum()
    
    # Profit before Tax
    pbt = ebitda 
    
    # Tax Provision (27% of PBT for SA)
    sa_tax_rate = 0.27
    projected_tax = max(0, pbt * sa_tax_rate) if actual_tax == 0 else actual_tax
    
    net_profit = pbt - projected_tax
    
    # Margin Analysis
    margin_pct = (net_profit / total_rev * 100) if total_rev > 0 else 0

    print(f"\n--- SOVEREIGN ENGINE: SOUTH AFRICA SNAPSHOT ---")
    print(f"Total Group Revenue:      R {total_rev:,.2f}")
    print(f"Total Operating Costs:    R {total_opex:,.2f}")
    print(f"-----------------------------------------------")
    print(f"EBITDA:                   R {ebitda:,.2f}")
    
    if actual_tax > 0:
        print(f"Tax/VAT (Actual):         R {actual_tax:,.2f}")
    elif pbt > 0:
        print(f"Tax Provision (27%):      R {projected_tax:,.2f} (Projected)")
    else:
        print(f"Tax Provision:            R 0.00 (Loss Position)")
        
    print(f"-----------------------------------------------")
    print(f"Net Operational Result:   R {net_profit:,.2f}")
    print(f"Net Profit Margin:        {margin_pct:.2f}%")
    print(f"-----------------------------------------------")
    
    # Strategic Insights for Portfolio
    if pbt < 0:
        print(f"ADVISORY: Net loss detected. Assessing potential Deferred Tax Asset.")
    elif actual_tax == 0 and total_rev > 0:
        print(f"ADVISORY: Using South African statutory rate (27%) for projection.")
        
    print(f"SUCCESS: ZAR KPIs exported to data/ESFE_KPIS.csv")

if __name__ == "__main__":
    run_kpi_engine()