import pandas as pd
import numpy as np
import os

def run_monte_carlo_simulation():
    """
    Advanced Layer 4: Decision Intelligence Framework.
    Runs 1,000 simulations to model financial risk and probability.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    kpi_path = os.path.join(base_dir, 'data', 'ESFE_KPIS.csv')
    output_path = os.path.join(base_dir, 'reports', 'Strategic_Risk_Simulation.xlsx')

    print(f"--- Strategic Simulation Engine Execution ---")
    
    if not os.path.exists(kpi_path):
        print("ERROR: KPI data missing. Run Layer 3 first.")
        return

    # 1. Load the "Static" Reality from Layer 3
    df_kpi = pd.read_csv(kpi_path)
    
    # Extract baseline figures
    # We use the credit (Revenue) and debit (Expenses) totals
    baseline_rev = df_kpi[df_kpi['account_name'].str.contains('Revenue', case=False, na=False)]['credit'].sum()
    baseline_exp = df_kpi[df_kpi['account_name'].str.contains('Operating', case=False, na=False)]['debit'].sum()
    
    # 2. Define Risk Parameters (Simulating Volatility)
    simulations = 1000
    rev_volatility = 0.15  # 15% standard deviation in revenue
    exp_volatility = 0.05  # 5% standard deviation in costs
    
    print(f"Running {simulations} iterations for Monte Carlo Analysis...")

    # 3. Generate Random Scenarios
    # Using a normal distribution to simulate "Real World" fluctuations
    simulated_revs = np.random.normal(baseline_rev, baseline_rev * rev_volatility, simulations)
    simulated_exps = np.random.normal(baseline_exp, baseline_exp * exp_volatility, simulations)
    
    # 4. Calculate Simulated Net Results
    results = simulated_revs - simulated_exps
    
    # 5. Build Simulation Dataframe
    sim_df = pd.DataFrame({
        'Scenario': range(1, simulations + 1),
        'Simulated_Revenue_ZAR': simulated_revs,
        'Simulated_Expense_ZAR': simulated_exps,
        'Net_Result_ZAR': results
    })

    # 6. Statistical Summaries (Decision Intelligence)
    prob_profit = (len(sim_df[sim_df['Net_Result_ZAR'] > 0]) / simulations) * 100
    var_95 = np.percentile(results, 5) # Value at Risk (5th percentile)
    
    # 7. Export to Advanced Excel Report
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        sim_df.to_excel(writer, sheet_name='Simulation_Data', index=False)
        
        # Summary Sheet
        summary_stats = pd.DataFrame({
            'Metric': ['Baseline Net Result', 'Mean Simulated Result', 'Probability of Profit (%)', '95% Confidence Value at Risk (VaR)'],
            'Value_ZAR': [baseline_rev - baseline_exp, np.mean(results), prob_profit, var_95]
        })
        summary_stats.to_excel(writer, sheet_name='Executive_Summary', index=False)

    print(f"\n--- SIMULATION COMPLETE ---")
    print(f"Probability of turning a profit: {prob_profit:.2f}%")
    print(f"95% Confidence Value at Risk: R {abs(var_95):,.2f}")
    print(f"Strategic Report Saved: {output_path}")

if __name__ == "__main__":
    run_monte_carlo_simulation()