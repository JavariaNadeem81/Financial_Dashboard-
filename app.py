import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# -------------------- Load Environment --------------------
load_dotenv()
user_name = os.getenv("USER_NAME", "User")

# -------------------- Load CSV Data --------------------
DATA_PATH = os.path.join(os.getcwd(), 'Cleaned_Personal_Finance.csv')
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()
df['Date'] = pd.to_datetime(df['Date'])
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df.dropna(subset=['Amount'], inplace=True)
df_sorted = df.sort_values('Date')

# -------------------- Streamlit Page Setup --------------------
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title(f"Welcome, {user_name}! 💸")
st.subheader("📊 Your Personal Finance Overview")

# -------------------- Summary Metrics --------------------
total_income = df[df['Type'] == 'Income']['Amount'].sum()
total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
total_savings = df['Net'].sum() if 'Net' in df.columns else total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Income", f"Rs. {total_income:,.2f}")
col2.metric("💸 Total Expenses", f"Rs. {total_expense:,.2f}")
col3.metric("📈 Net Savings", f"Rs. {total_savings:,.2f}")

# -------------------- Bar Chart: Expenses by Category --------------------
st.subheader("📌 Expenses by Category")
expense_by_category = df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum()

fig1, ax1 = plt.subplots()
expense_by_category.sort_values().plot(kind='barh', ax=ax1, color='salmon')
ax1.set_xlabel("Amount (Rs.)")
ax1.set_title("Expenses by Category")
st.pyplot(fig1)

# -------------------- Line Chart: Cumulative Savings Over Time --------------------
if 'Cumulative_Savings' in df_sorted.columns:
    st.subheader("📉 Cumulative Savings Over Time")
    fig2, ax2 = plt.subplots()
    ax2.plot(df_sorted['Date'], df_sorted['Cumulative_Savings'], marker='o', linestyle='-')
    ax2.set_ylabel("Savings (Rs.)")
    ax2.set_xlabel("Date")
    ax2.set_title("Cumulative Savings Over Time")
    ax2.grid(True)
    st.pyplot(fig2)

# -------------------- Sidebar Filter + Data Table --------------------
st.sidebar.header("🔍 Filter")
selected_type = st.sidebar.selectbox("Select Transaction Type", options=df['Type'].unique())
filtered_df = df[df['Type'] == selected_type]

st.subheader(f"📄 Transactions - {selected_type}")
st.dataframe(filtered_df)
