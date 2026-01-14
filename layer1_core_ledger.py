import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_ledger():
    # 1. Create Data Directory
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data' folder.")

    # 2. Setup Parameters
    rows = 1000
    start_date = datetime(2023, 1, 1)
    
    # Financial Structure
    accounts = {
        '1000': 'Cash',
        '4000': 'Revenue',
        '5000': 'Operating Expenses',
        '2000': 'Intercompany Payables'
    }

    # 3. Generate Data
    data = []
    for i in range(rows):
        acc_code = np.random.choice(list(accounts.keys()))
        amount = np.random.uniform(100, 5000)
        
        data.append({
            'txn_id': f'TXN-{1000+i}',
            'date': (start_date + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
            'account_code': acc_code,
            'account_name': accounts[acc_code],
            'amount': round(amount, 2),
            'currency': 'ZAR'
        })

    # 4. Save to CSV
    df = pd.DataFrame(data)
    output_path = 'data/ESFE_FACT_GL.csv'
    df.to_csv(output_path, index=False)
    print(f"SUCCESS: File created at {output_path}")

if __name__ == "__main__":
    generate_ledger()
    