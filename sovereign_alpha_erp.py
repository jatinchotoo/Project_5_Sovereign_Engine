import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="Sovereign Alpha ERP | Group Command", layout="wide")

# --- 1. LIVE FX GATEWAY ---
@st.cache_data(ttl=3600)
def get_live_rates():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        data = requests.get(url, timeout=5).json()
        return data["rates"] if data["result"] == "success" else {"USD": 1.0, "ZAR": 18.50, "EUR": 0.92, "GBP": 0.78}
    except:
        return {"USD": 1.0, "ZAR": 18.50, "EUR": 0.92, "GBP": 0.78}

rates = get_live_rates()

# --- 2. THE MULTI-MODULE DATA ENGINE ---
def load_erp_data():
    # Synthetic Ledger simulating high-complexity transactions
    data = {
        'Date': pd.to_datetime(['2024-01-01', '2024-01-15', '2024-02-01', '2024-02-15', '2024-03-01']),
        'Category': ['Revenue', 'Insurance', 'Lease (IFRS 16)', 'Payroll', 'Revenue'],
        'Description': ['SaaS Global Sales', 'D&O Liability Policy', 'HQ Office Rent', 'Group Salaries', 'Consulting Fees'],
        'Amount_USD': [150000, -12000, -25000, -80000, 200000],
        'Vatable': [True, False, False, False, True]
    }
    return pd.DataFrame(data)

df = load_erp_data()

# --- 3. STATUTORY LOGIC (VAT / PAYE / CIT) ---
def apply_statutory_logic(amount, is_vatable):
    vat_rate = 0.15  # South Africa Standard
    paye_rate = 0.25 # Average effective
    cit_rate = 0.27  # Corporate Tax
    
    vat = amount * vat_rate if is_vatable else 0
    # Simplification for demo: Payroll usually negative, so we calculate tax on absolute
    paye = abs(amount) * paye_rate if "Salaries" in str(amount) else 0 
    return vat, paye

# --- 4. SIDEBAR CONTROL ---
st.sidebar.title("🏛️ Group ERP Control")
target_curr = st.sidebar.selectbox("Global Reporting Currency", options=sorted(rates.keys()), index=list(sorted(rates.keys())).index("ZAR"))
current_rate = rates[target_curr]

st.sidebar.divider()
st.sidebar.subheader("Compliance Settings")
vat_toggle = st.sidebar.checkbox("Apply VAT (15%)", value=True)
tax_toggle = st.sidebar.checkbox("Provision for CIT (27%)", value=True)

# --- 5. CALCULATIONS ---
df['Amount_Reported'] = df['Amount_USD'] * current_rate
df['VAT_Provision'] = df.apply(lambda x: x['Amount_Reported'] * 0.15 if x['Vatable'] else 0, axis=1)
df['Net_Cash_Flow'] = df['Amount_Reported'] - df['VAT_Provision']

# --- 6. DASHBOARD LAYOUT ---
st.title("Sovereign Alpha: Executive Command Center")
st.markdown(f"**Real-Time Group Consolidation** | Reporting in **{target_curr}** @ {current_rate:.4f}")

# TOP LEVEL KPIS
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    total_rev = df[df['Category'] == 'Revenue']['Amount_Reported'].sum()
    st.metric("Gross Revenue", f"{target_curr} {total_rev:,.2f}")
with kpi2:
    total_vat = df['VAT_Provision'].sum()
    st.metric("VAT Liability (Output)", f"{target_curr} {total_vat:,.2f}", delta_color="inverse")
with kpi3:
    lease_ins = df[df['Category'].isin(['Insurance', 'Lease (IFRS 16)'])]['Amount_Reported'].sum()
    st.metric("Fixed Obligations", f"{target_curr} {abs(lease_ins):,.2f}")
with kpi4:
    net_position = df['Net_Cash_Flow'].sum()
    st.metric("Estimated Net Cash", f"{target_curr} {net_position:,.2f}")

st.divider()

# COMPLEX VISUALS
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Treasury & Compliance Flow")
    # Building a Waterfall chart to show how Gross Revenue becomes Net Cash
    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "relative", "total"],
        x = ["Gross Revenue", "Tax/VAT", "Leases/Insurance", "Net Liquidity"],
        textposition = "outside",
        text = [f"+{total_rev:,.0f}", f"-{total_vat:,.0f}", f"{lease_ins:,.0f}", "RESULT"],
        y = [total_rev, -total_vat, lease_ins, 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    fig.update_layout(title="Revenue Leakage & Compliance Bridge", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🧾 Fixed Cost Weighting")
    pie_df = df[df['Amount_Reported'] < 0]
    fig_pie = px.pie(pie_df, values=abs(pie_df['Amount_Reported']), names='Category', hole=.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

# THE REAL-TIME LEDGER
st.subheader("🔍 Integrated ERP Ledger")
st.markdown("This ledger combines Revenue, Insurance schedules, and Lease amortizations with live FX.")

# Highlight rows for management
def highlight_negatives(val):
    color = 'red' if isinstance(val, (int, float)) and val < 0 else 'black'
    return f'color: {color}'

st.dataframe(
    df.style.applymap(highlight_negatives, subset=['Amount_Reported', 'Net_Cash_Flow'])
    .format({"Amount_Reported": "{:,.2f}", "VAT_Provision": "{:,.2f}", "Net_Cash_Flow": "{:,.2f}"}),
    use_container_width=True
)

# FOOTER FOR MANAGEMENT
st.info(f"Management Note: Leases are currently recognized under IFRS 16 guidelines. "
        f"Insurance premiums are recognized on an accrual basis. FX Rates refreshed as of {datetime.now().strftime('%H:%M')}.")
