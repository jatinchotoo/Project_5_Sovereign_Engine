import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- SETTINGS ---
# Updated for 2026 Streamlit standards to avoid deprecation warnings
st.set_page_config(page_title="Sovereign Alpha | Capital & Treasury", layout="wide")

# --- 1. THE ARCHITECTURAL DATA ENGINE ---
# Simulating a live feed of Assets, Liabilities, and Equity for the Group
def get_live_balance_sheet():
    data = {
        'Category': ['Current Asset', 'Fixed Asset', 'Investment', 'Current Liability', 'Long-term Liability', 'Equity', 'Equity'],
        'Account': ['Cash & Equivalents', 'Property (Leasehold)', 'Equities Portfolio', 'VAT/PAYE Payable', 'IFRS 16 Lease Liab', 'Share Capital', 'Retained Earnings'],
        'Amount_ZAR': [4500000, 12000000, 2800000, -850000, -9500000, -5000000, -3950000]
    }
    return pd.DataFrame(data)

df_bs = get_live_balance_sheet()

# --- 2. CALCULATIONS (THE CFO LOGIC) ---
total_assets = df_bs[df_bs['Category'].str.contains('Asset|Investment')]['Amount_ZAR'].sum()
total_liabilities = abs(df_bs[df_bs['Category'].str.contains('Liability')]['Amount_ZAR'].sum())
total_equity = abs(df_bs[df_bs['Category'] == 'Equity']['Amount_ZAR'].sum())

# Key Metrics for Executive Reporting
cash_on_hand = df_bs[df_bs['Account'] == 'Cash & Equivalents']['Amount_ZAR'].values[0]
investment_value = df_bs[df_bs['Account'] == 'Equities Portfolio']['Amount_ZAR'].values[0]
current_ratio = cash_on_hand / 850000 # Cash / Current Liab
debt_to_equity = total_liabilities / total_equity

# --- 3. INVESTMENT SIGNAL LOGIC ---
def get_investment_signal(cash, equity):
    """Determines capital allocation strategy based on liquidity weight."""
    cash_weight = cash / equity
    if cash_weight > 0.50:
        return "🔥 STRONG BUY / INVEST", "Excess Liquidity detected. Capital is idling. Deploy into high-yield assets.", "success"
    elif cash_weight < 0.15:
        return "⚠️ SELL / LIQUIDATE", "Liquidity Crisis Risk. Current cash is below 15% of Equity. Sell non-core investments.", "error"
    else:
        return "✅ HOLD / STABLE", "Cash reserves are optimized relative to Equity position.", "info"

signal, advice, status = get_investment_signal(cash_on_hand, total_equity)

# --- 4. DASHBOARD UI ---
st.title("Sovereign Alpha: Capital & Treasury Command")
st.markdown(f"**Group Consolidation View** | Last Pulse: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

# ROW 1: THE STRATEGIC SIGNAL BAR
st.divider()
sig_col1, sig_col2 = st.columns([1, 2])
with sig_col1:
    st.markdown(f"### Investment Signal")
    st.subheader(signal)
with sig_col2:
    if status == "success":
        st.success(f"**CFO Strategy:** {advice}")
    elif status == "error":
        st.error(f"**CFO Strategy:** {advice}")
    else:
        st.info(f"**CFO Strategy:** {advice}")

st.divider()

# ROW 2: KPI TILES
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Assets", f"R {total_assets:,.0f}")
kpi2.metric("Total Liabilities", f"R {total_liabilities:,.0f}", delta="-2.1% (Lease Amort)")
kpi3.metric("Total Equity", f"R {total_equity:,.0f}")
kpi4.metric("Current Ratio", f"{current_ratio:.2f}x", delta="Healthy" if current_ratio > 1.5 else "Low")

# ROW 3: VISUALIZATIONS
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Asset Composition")
    fig_assets = px.sunburst(df_bs[df_bs['Amount_ZAR'] > 0], path=['Category', 'Account'], values='Amount_ZAR',
                             color_discrete_sequence=px.colors.qualitative.Pastel)
    # Using 'stretch' to comply with 2026 Streamlit UI standards
    st.plotly_chart(fig_assets, width='stretch')

with col_chart2:
    st.subheader("Capital Structure (Debt vs Equity)")
    fig_cap = go.Figure(data=[go.Pie(labels=['Liabilities', 'Equity'], 
                                   values=[total_liabilities, total_equity], 
                                   hole=.6,
                                   marker_colors=['#E74C3C', '#2ECC71'])])
    st.plotly_chart(fig_cap, width='stretch')

# ROW 4: THE LIVE LEDGER
st.subheader("Integrated Statement of Financial Position")
# Formatting the dataframe for board-ready presentation
display_df = df_bs.copy()
display_df['Amount_ZAR_Formatted'] = display_df['Amount_ZAR'].apply(lambda x: f"R {x:,.2f}")

st.dataframe(display_df[['Category', 'Account', 'Amount_ZAR_Formatted']], width='stretch')

# ROW 5: SIMULATION TOOLS (The "What-If" for Management)
st.sidebar.title("🛠️ Treasury Simulator")
st.sidebar.markdown("Test the impact of a large purchase or investment.")
sim_spend = st.sidebar.slider("Simulate Cash Spend (ZAR)", 0, 4000000, 0, step=500000)

if sim_spend > 0:
    new_cash = cash_on_hand - sim_spend
    new_signal, new_advice, _ = get_investment_signal(new_cash, total_equity)
    st.sidebar.warning(f"**New Signal:** {new_signal}")
    st.sidebar.write(new_advice)

st.sidebar.divider()
st.sidebar.markdown("**Equity Controls**")
st.sidebar.checkbox("Consolidate Subsidiaries", value=True)
st.sidebar.checkbox("Apply IFRS 16 Revaluations", value=True)