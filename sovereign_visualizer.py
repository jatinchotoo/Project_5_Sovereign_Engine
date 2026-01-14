import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def generate_strategic_dashboard():
    """
    Generates an advanced Strategic Finance Dashboard for Project 5.
    Output: sovereign_dashboard.png
    """
    # 1. Setup Data based on the Sovereign Engine Output
    allocation_data = {
        'Category': ['Growth Investment', 'Defensive Capital', 'Liquidity Reserve'],
        'Amount_USD': [163800000, 175000000, 161200000]
    }
    
    risk_signals = {
        'Signal': ['Macro Tightening', 'Core Resilience', 'Tech Leverage', 'Geopolitical'],
        'Impact Score': [-0.18, 0.22, 0.15, -0.10],
        'Risk Level': [3, 1, 2, 2]
    }
    
    df_alloc = pd.DataFrame(allocation_data)
    df_risk = pd.DataFrame(risk_signals)
    
    # 2. Initialize the visual style
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 2)
    
    fig.suptitle('SOVEREIGN ENGINE: STRATEGIC FINANCE INTELLIGENCE DASHBOARD', fontsize=22, fontweight='bold', y=0.98)

    # --- CHART 1: PIE CHART (Capital Composition) ---
    ax1 = fig.add_subplot(gs[0, 0])
    colors = ['#2E86C1', '#28B463', '#D35400']
    # FIX: changed 'fontWeight' (CamelCase) to 'fontweight' (lowercase)
    ax1.pie(df_alloc['Amount_USD'], labels=df_alloc['Category'], autopct='%1.1f%%', 
            startangle=140, colors=colors, explode=(0.05, 0, 0), shadow=True, textprops={'fontweight': 'bold'})
    ax1.set_title('Strategic Capital Weighting', fontsize=14, pad=20)

    # --- CHART 2: BAR CHART (Allocation Totals) ---
    ax2 = fig.add_subplot(gs[0, 1])
    sns.barplot(x='Category', y='Amount_USD', data=df_alloc, palette=colors, ax=ax2)
    ax2.set_title('Allocation Value ($ USD)', fontsize=14)
    ax2.set_ylabel('Amount (Millions)')
    
    from matplotlib.ticker import FuncFormatter
    ax2.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: f'${x*1e-6:,.0f}M'))

    # --- CHART 3: HORIZONTAL BAR (Risk Signal Impact) ---
    ax3 = fig.add_subplot(gs[1, 0])
    signal_colors = ['red' if x < 0 else 'green' for x in df_risk['Impact Score']]
    sns.barplot(x='Impact Score', y='Signal', data=df_risk, palette=signal_colors, ax=ax3)
    ax3.axvline(0, color='black', linewidth=1)
    ax3.set_title('Strategic Signal Impact Analysis', fontsize=14)
    ax3.set_xlabel('Weighted Score Impact')

    # --- CHART 4: RISK HEATMAP ---
    ax4 = fig.add_subplot(gs[1, 1])
    heatmap_data = df_risk.pivot_table(index='Signal', values='Risk Level')
    sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn_r', cbar=False, ax=ax4)
    ax4.set_title('Risk Concentration Heatmap (1=Low, 3=High)', fontsize=14)

    # 3. Final Branding and Save
    plt.figtext(0.5, 0.02, "Sovereign Engine v1.0 | Developed by Jatin Chotoo | Strategic Finance Division", 
                ha="center", fontsize=12, fontweight='bold', bbox={"facecolor":"#2E86C1", "alpha":0.1, "pad":8})
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig('sovereign_dashboard.png', dpi=300)
    print("\nSUCCESS: Dashboard generated as 'sovereign_dashboard.png'")

if __name__ == "__main__":
    generate_strategic_dashboard()