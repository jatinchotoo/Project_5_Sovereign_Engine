import pandas as pd
import os
import re

def run_controls_engine():
    print("Executing financial control checks...")
    
    # Paths are defined relative to the project root
    input_file = 'data/ESFE_FACT_GL.csv'
    output_file = 'data/ESFE_VALIDATED_GL.csv'
    
    if not os.path.exists(input_file):
        print(f"ERROR: Could not find {input_file}. Run Layer 1 first.")
        return

    # Load the synthetic ledger generated in Layer 1
    df = pd.read_csv(input_file)
    cols = df.columns.tolist()

    # --- ADVANCED COLUMN DETECTION ---
    # Logic: Detect if data is 'Split' (Debit/Credit) or 'Single Column' (Amount)
    is_single_col = 'amount' in cols or 'amount_zar' in cols
    
    if is_single_col:
        amt_col = 'amount_zar' if 'amount_zar' in cols else 'amount'
        d_col, c_col = None, None # Using logic below for single col
        print(f"Mode: Single Column Validation ({amt_col})")
    else:
        d_col = 'debit_zar' if 'debit_zar' in cols else 'debit'
        c_col = 'credit_zar' if 'credit_zar' in cols else 'credit'
        print(f"Mode: Dual Column Validation ({d_col}/{c_col})")

    # Final safety check
    if not is_single_col and (d_col not in cols or c_col not in cols):
        print(f"ERROR: Column mismatch. Available columns: {cols}")
        return

    def clean_currency(value):
        """Helper to convert currency strings to floats."""
        if pd.isna(value):
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        clean_str = re.sub(r'[^\d.-]', '', str(value)) # Keep negative sign if present
        return float(clean_str) if clean_str else 0.0

    def validate_row(row):
        """
        Governance Logic:
        1. Single Column: Check for non-zero transactions.
        2. Dual Column: Ensure no double-entry on a single row (IFRS).
        3. Account codes must be 4-digit format.
        """
        try:
            # Step 1: Calculate Debit/Credit equivalents for logic check
            if is_single_col:
                val = clean_currency(row[amt_col])
                row_debit = val if val > 0 else 0.0
                row_credit = abs(val) if val < 0 else 0.0
            else:
                row_debit = clean_currency(row[d_col])
                row_credit = clean_currency(row[c_col])

            # Rule 1: Dual-entry prevention (only applicable for split columns)
            if not is_single_col and row_debit > 0 and row_credit > 0:
                return "FAIL: Double Entry Violation"
            
            # Rule 2: Validation of account code (4-digit check)
            acc_code = str(row['account_code']).strip()
            if not (acc_code.isdigit() and len(acc_code) == 4):
                return "FAIL: Invalid CoA Mapping"
                
            # Rule 3: Null Transaction Check
            if row_debit == 0 and row_credit == 0:
                return "FAIL: Null Transaction"
                
            return "PASS"
        except Exception as e:
            return f"FAIL: Processing Error ({str(e)})"

    # Apply the governance rules
    df['control_status'] = df.apply(validate_row, axis=1)
    
    # Save the validated dataset
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_file, index=False)
    
    # Audit trail statistics
    passed = len(df[df['control_status'] == "PASS"])
    failed_df = df[df['control_status'] != "PASS"]
    
    print(f"SUCCESS: Layer 2 Validation Complete.")
    print(f"Audit Summary: {len(df)} processed | {passed} PASSED | {len(failed_df)} FAILED")
    
    if len(failed_df) > 0:
        print("\n--- FAILURE ANALYSIS (First 5 errors) ---")
        print(failed_df[['account_code', 'control_status']].head())

if __name__ == "__main__":
    run_controls_engine()
    