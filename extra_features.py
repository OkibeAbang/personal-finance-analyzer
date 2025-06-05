# extra_features.py

import streamlit as st
import pandas as pd

# -----------------------------
# Filter by Category
# -----------------------------
def filter_by_category(df):
    st.subheader("🔍 Filter by Categroy")
    categories = df['Categroy'].unique()
    selected_category = st.selectbox("Select a category:", categories)
    filtered_df = df[df['Categroy'] == selected_category]
    st.write(f"Transactions in **{selected_category}**:")
    st.dataframe(filtered_df)


# -----------------------------
# Filter by Date Range
# -----------------------------
def filter_by_date_range(df):
    st.subheader("🗓️ Filter by Date Range")
    start_date = st.date_input("Start date", value=df['Date '].min().date())
    end_date = st.date_input("End date", value=df['Date '].max().date())
    
    # Ensure filtering only occurs when dates are valid
    if start_date and end_date and start_date <= end_date:
        mask = (df['Date '] >= pd.to_datetime(start_date)) & (df['Date '] <= pd.to_datetime(end_date))
        df = df[mask]
    else:
        st.warning("Invalid date range selected.")
    return df


# -----------------------------
# Toggle Views (Checkbox-based controls)
# -----------------------------
def toggle_visuals(df):
    if st.checkbox("Show Total Spending"):
        st.write(f"Total: **${df['Amount'].sum():.2f}**")

    if st.checkbox("Show Spending by Category"):
        st.bar_chart(df.groupby("Category")["Amount"].sum())

    if st.checkbox("Show Daily Spending Line Chart"):
        daily = df.groupby(df['Date '])['Amount'].sum()
        st.line_chart(daily)


# -----------------------------
# User-Defined Budget Checker
# -----------------------------
def budget_checker(df):
    st.subheader("💵 Set Your Monthly Budget")

    # Ask user for their budget
    budget = st.number_input("Enter your monthly budget ($):", min_value=0.0, value=500.0)

    # Group by month
    monthly_total = df.groupby(df['Date '].dt.to_period("M"))['Amount'].sum()
    last_month_spend = monthly_total.iloc[-1] if not monthly_total.empty else 0

    # Compare and give feedback
    if last_month_spend > budget:
        st.error(f"🚨 You overspent! You spent ${last_month_spend:.2f}, which is ${last_month_spend - budget:.2f} over your budget.")
    else:
        st.success(f"✅ Good job! You spent ${last_month_spend:.2f}, which is within your budget of ${budget:.2f}.")
