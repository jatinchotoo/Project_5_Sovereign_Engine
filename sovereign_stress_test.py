import pandas as pd
import numpy as np
import time
import os
# We import the visualization logic from your existing script
try:
    from sovereign_visualizer import generate_strategic_dashboard
except ImportError:
    print("Note: sovereign_visualizer.py not found. Only data processing will be tested.")

def run_stress_test(row_count=100000):
    """
    Simulates high-volume data ingestion and triggers the visualization engine.
    This proves the engine can handle 100k rows in seconds.
    """
    print(f"--- STARTING SOVEREIGN ENGINE STRESS TEST: {row_count:,} ROWS ---")
    start_time = time.time()

    # 1. GENERATE MASSIVE DATASET (SIMULATING 100k TRANSACTIONS)
    # This mimics a massive export from an ERP like SAP or Oracle
    data = {
        'txn_id': [f'TXN-{i}' for i in range(row_count)],
        'account_name': np.random.choice(['Revenue', 'Operating Expenses', 'Cash', 'Intercompany'], row_count),
        'amount': np.random.uniform(100, 5000, row_count),
        'currency': 'ZAR'
    }
    df_huge = pd.DataFrame(data)
    
    gen_time = time.time() - start_time
    print(f"Successfully generated {row_count:,} rows in {gen_time:.2f} seconds.")

    # 2. ENGINE LOGIC (CONSOLIDATION)
    # We group the 100k rows into the 4 strategic categories the dashboard needs
    summary = df_huge.groupby('account_name')['amount'].sum().reset_index()
    
    # Save this huge result as our primary data source for the visualizer
    os.makedirs('data', exist_ok=True)
    df_huge.to_csv('data/ESFE_FACT_GL.csv', index=False)
    
    print("\n[Engine Logic] Data Consolidated for Dashboarding:")
    print(summary)

    # 3. TRIGGER DASHBOARD
    # This runs your Project 5 visualization logic on the massive dataset
    print("\n[Visualizer] Generating Dashboard from High-Volume Data...")
    try:
        generate_strategic_dashboard()
        print("SUCCESS: sovereign_dashboard.png updated with stress-test data.")
    except NameError:
        print("Skipping dashboard generation (visualizer logic not imported).")
    
    total_time = time.time() - start_time
    print(f"\n--- TEST COMPLETE ---")
    print(f"Total time to process {row_count:,} rows and update visuals: {total_time:.2f} seconds.")

if __name__ == "__main__":
    run_stress_test()
    