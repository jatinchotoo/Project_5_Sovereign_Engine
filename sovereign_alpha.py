import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Sovereign Alpha | Live FX Engine", layout="wide")

# --- 1. LIVE FX ENGINE (Real-Time API) ---
@st.cache_data(ttl=3600)  # Cache rates for 1 hour to stay efficient
def get_live_rates():
    """Fetches real-time FX rates from a public API."""
    try:
        # Using a free public API for demonstration
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data["result"] == "success":
            return data["rates"]
    except Exception:
        st.warning("⚠️ Live FX feed unavailable. Using fallback static rates.")
    
    # Fallback rates if API fails
    return {"USD": 1.0, "ZAR": 18.55, "EUR": 0.92, "GBP": 0.78, "JPY": 148.20}

rates = get_live_rates()

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    # Integrating your Project 2 transaction style
    data = {
        'date': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-02-10', '2024-02-25', '2024-03-05', '2024-03-15']),
        'account': ['Revenue', 'OpEx', 'Revenue', 'OpEx', 'Revenue', 'Cash'],
        'amount_usd': [12500, 4200, 18000, 6100, 22000, 45000],
    }
    return pd.DataFrame(data)

df = load_data()

# --- 3. DYNAMIC INTERFACE ---
st.sidebar.title("🏛️ Sovereign Control")
st.sidebar.info("The engine is currently using live exchange rates fetched via API.")

# User selects currency
target_curr = st.sidebar.selectbox("Reporting Currency", options=sorted(rates.keys()), index=list(sorted(rates.keys())).index("ZAR") if "ZAR" in rates else 0)

# Display the live rate in the sidebar
current_rate = rates[target_curr]
st.sidebar.metric(f"Live USD/{target_curr}", f"{current_rate:.4f}")

# Filter by date
date_range = st.sidebar.date_input("Analysis Period", [df['date'].min(), df['date'].max()])

# --- 4. CALCULATION ENGINE ---
df['reported_amount'] = df['amount_usd'] * current_rate
mask = (df['date'] >= pd.Timestamp(date_range[0])) & (df['date'] <= pd.Timestamp(date_range[1]))
f_df = df.loc[mask]

# --- 5. DASHBOARD ---
st.title("Sovereign Alpha Engine")
st.markdown(f"### Global Consolidated View ({target_curr})")

# KPI Metrics
c1, c2, c3 = st.columns(3)
with c1:
    total = f_df[f_df['account'] == 'Revenue']['reported_amount'].sum()
    st.metric("Total Revenue", f"{target_curr} {total:,.2f}")
with c2:
    exp = f_df[f_df['account'] == 'OpEx']['reported_amount'].sum()
    st.metric("Total Expenses", f"{target_curr} {exp:,.2f}")
with c3:
    cash = f_df[f_df['account'] == 'Cash']['reported_amount'].sum()
    st.metric("Cash Position", f"{target_curr} {cash:,.2f}")

st.divider()

# Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_line = px.line(f_df.sort_values('date'), x='date', y='reported_amount', color='account', title="Trend Analysis", markers=True)
    st.plotly_chart(fig_line, width="stretch")

with chart_col2:
    fig_bar = px.bar(f_df.groupby('account')['reported_amount'].sum().reset_index(), x='account', y='reported_amount', title="Account Totals", color='account')
    st.plotly_chart(fig_bar, width="stretch")

# Data Table
st.markdown("#### 🔍 Source Ledger (Live Conversion)")
st.dataframe(f_df, width="stretch")
