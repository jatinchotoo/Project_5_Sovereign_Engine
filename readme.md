Project 5: Sovereign Alpha – Treasury & Capital Engine 🇿🇦

📌 Executive Summary

The Sovereign Engine is a high-performance financial intelligence tool designed for CFOs and Global Treasury Management. It bridges the gap between raw General Ledger data and executive decision-making by synthesizing multi-currency ledgers, statutory tax obligations (SARS 27%), and risk-adjusted capital allocation models.

🛠 Strategic Finance Logic (Niche Specialization)

This project focuses on high-stakes treasury "niches" often overlooked by standard ERP exports:

Treasury Command Dashboard: A real-time interface using Streamlit and React (Lucide-ready) to monitor capital health across global entities.

Multi-Currency Consolidation: Automated FX translation (USD/GBP/EUR to ZAR) with Intercompany (Account 2000) elimination logic to prevent consolidated revenue inflation.

Investment Signal Heuristics: Logic-driven alerts (Strong Buy / Liquidate) based on real-time cash-to-equity weighting.

Monte Carlo Risk Modeling: 1,000-iteration stress testing to calculate the "Probability of Profit" and 95% Confidence Value-at-Risk (VaR).

South African Statutory Alignment: Hardcoded provisioning for the 27% SARS Corporate Tax rate and ZAR-base reporting.

🏗 Modular Data Pipeline (5-Layer Architecture)

Layer 1 (Ledger): Deterministic synthetic data generation following IFRS standards (ZAR/USD).

Layer 2 (Governance): Automated audit controls to prevent double-entry violations and ensure 4-digit CoA mapping.

Layer 3 (KPIs & Tax): Real-time calculation of EBITDA, Current Ratio, and 27% South African Corporate Tax provisioning.

Layer 4 (Simulation): Strategic risk forecasting using NumPy-based volatility modeling.

Layer 5 (Reporting): Board-ready Excel exports with automated charting and executive summaries.

🚀 Technical Stack

Backend: Python 3.12 (Pandas, NumPy)

Frontend/Visuals: Streamlit, Plotly, React (Tailwind CSS)

APIs: Real-time FX Engine integration

Version Control: Git/GitHub

📊 How to Execute

To run the full suite and generate the Strategic Advisory Report, execute the layers in sequence:

# 1. Generate and Validate Ledger
python layer1_ledger.py
python layer2_controls_validation.py

# 2. Run Analytics & Simulation
python layer3_kpis_engine.py
python layer4_simulation_engine.py

# 3. Launch Visual Command Center
streamlit run sovereign_alpha.py


Developed by Jatin - Finance & Tech Integration Specialistgit add .