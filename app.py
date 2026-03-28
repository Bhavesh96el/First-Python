import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portfolio Architect", layout="wide")

# --- INTERNAL MATH FUNCTION ---
def calc_repayment(loan, rate, years):
    if loan <= 0 or years <= 0: return 0
    m_rate = (rate / 100) / 12
    n = years * 12
    return loan * (m_rate * (1 + m_rate)**n) / ((1 + m_rate)**n - 1)

# --- SIDEBAR: INCOME & SETUP ---
st.sidebar.header("💰 Monthly Income")
user_income = st.sidebar.number_input("Your Take-home Pay ($)", value=5000)
spouse_income = st.sidebar.number_input("Spouse Take-home Pay ($)", value=0)
total_salary = user_income + spouse_income

# --- MAIN INTERFACE ---
st.title("🏠 Property Portfolio Analyzer")
st.info("Add your properties below to see your total financial standing.")

# Using 'columns' to organize the input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Primary Residence")
    h_loan = st.number_input("Home Loan Balance ($)", value=0)
    h_rate = st.number_input("Home Interest Rate (%)", value=6.0, step=0.1)
    h_years = st.number_input("Home Loan Years Left", value=30)
    h_out = st.number_input("Home Monthly Outgoings ($)", value=400)

with col2:
    st.subheader("Investment Property")
    i_loan = st.number_input("Inv. Loan Balance ($)", value=0)
    i_rate = st.number_input("Inv. Interest Rate (%)", value=6.5, step=0.1)
    i_years = st.number_input("Inv. Loan Years Left", value=30)
    i_rent = st.number_input("Monthly Rent Income ($)", value=0)
    i_out = st.number_input("Inv. Monthly Outgoings ($)", value=500)

# --- THE CALCULATIONS ---
h_repay = calc_repayment(h_loan, h_rate, h_years)
i_repay = calc_repayment(i_loan, i_rate, i_years)

total_repayments = h_repay + i_repay
total_outgoings = h_out + i_out
total_revenue = total_salary + i_rent
net_position = total_revenue - total_repayments - total_outgoings
debt_ratio = (total_repayments / total_revenue) * 100 if total_revenue > 0 else 0

# --- DASHBOARD RESULTS ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Total Monthly Repayments", f"${total_repayments:,.2f}")
m2.metric("Net Monthly Cashflow", f"${net_position:,.2f}", delta=net_position, delta_color="normal")
m3.metric("Debt-to-Income Ratio", f"{debt_ratio:.1f}%")

if debt_ratio > 40:
    st.error("⚠️ HIGH LEVERAGE: Your repayments exceed 40% of your total gross income.")
elif net_position < 0:
    st.warning("⚠️ NEGATIVE CASHFLOW: Your outgoings exceed your income.")
else:
    st.success("✅ STABLE: Your portfolio is currently self-sustaining.")