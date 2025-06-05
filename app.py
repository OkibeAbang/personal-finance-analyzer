# Import necessary libraries
import streamlit as st  # Streamlit is used to build the web interface
import pandas as pd     # Pandas is used for data handling and manipulation
from predict import show_prediction
from extra_features import filter_by_category, filter_by_date_range, toggle_visuals, budget_checker
# Set the title of the Streamlit web app
st.title("📊 Personal Finance Tracker + Analyzer")

# Create a file uploader widget that accepts CSV files
uploaded_file = st.file_uploader("Upload your expense CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Show the uploaded raw data in an interactive table
    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # Display total spending calculated from the 'Amount' column
    st.subheader("💰 Total Spending")
    total_spent = df['Amount'].sum()  # Add up all values in the 'Amount' column
    st.write(f"Total: **${total_spent:.2f}**")

    # Show a bar chart of total amount spent in each category
    st.subheader("📊 Spending by Category")
    # Group by the 'Category' column and sum up the 'Amount' values
    category_totals = df.groupby('Categroy')['Amount'].sum()
    # Display the result as a bar chart
    st.bar_chart(category_totals)

    # Optional: Display a line chart of spending over time if 'Date' column exists
    if 'Date ' in df.columns:
        st.subheader("📈 Spending Over Time")
        # Convert the 'Date' column to datetime format
        df['Date '] = pd.to_datetime(df['Date '])
        # Group data by date and sum the amounts for each day
        daily_totals = df.groupby('Date ')['Amount'].sum()
        # Display the result as a line chart
        st.line_chart(daily_totals)

    # Ensure the essential columns exist
    required_columns = ['Date ', 'Description', 'Amount', 'Categroy']
    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        st.error(f"Missing columns in CSV: {', '.join(missing_cols)}")
    else:
        # Clean/convert data
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')  # Convert to numeric, force invalid to NaN
        df['Date '] = pd.to_datetime(df['Date '], errors='coerce')     # Convert to datetime

        # Drop rows with missing critical data
        df.dropna(subset=['Amount', 'Date ', 'Categroy'], inplace=True)


    # Average Monthly Spending
    st.subheader("📅 Average Monthly Spending")
    monthly = df.groupby(df['Date '].dt.to_period("M"))['Amount'].sum()
    st.write(f"Average: **${monthly.mean():.2f}**")

    # Top Spending Category
    st.subheader("🏆 Top Spending Category")
    top_category = category_totals.idxmax()
    st.write(f"Top category: **{top_category}** with **${category_totals.max():.2f}** spent")
    
    # Step 2: Filters
    df = filter_by_date_range(df)
    filter_by_category(df)

    # Step 3: Toggle visualizations
    toggle_visuals(df)

    # Step 4: Budget logic
    budget_checker(df)

    show_prediction(df)
else:
    # If no file is uploaded, show a small instruction
    st.info("Please upload a CSV file to begin.")



