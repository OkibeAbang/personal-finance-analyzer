# forecast.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def show_prediction(df):
    st.subheader("🔮 Forecast Future Monthly Spending")

    # Group transactions by month and calculate total spending
    monthly_data = df.groupby(df['Date '].dt.to_period("M"))['Amount'].sum()
    monthly_data.index = monthly_data.index.to_timestamp()
    monthly_data = monthly_data.reset_index()
    monthly_data.columns = ['Month', 'Total']
    monthly_data['MonthIndex'] = range(len(monthly_data))

    X = monthly_data[['MonthIndex']]
    y = monthly_data['Total']

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    n_months = st.slider("How many months ahead to forecast?", 1, 12, 3)
    future_indices = np.array([[i] for i in range(X['MonthIndex'].max() + 1, X['MonthIndex'].max() + 1 + n_months)])
    future_preds = model.predict(future_indices)

    residuals = y - y_pred
    std_error = residuals.std()
    lower_bound = future_preds - std_error
    upper_bound = future_preds + std_error

    forecast_df = pd.DataFrame({
        'Month': pd.date_range(start=monthly_data['Month'].max() + pd.offsets.MonthBegin(),
                               periods=n_months, freq='MS'),
        'Prediction': future_preds,
        'LowerBound': lower_bound,
        'UpperBound': upper_bound
    })

    st.subheader("📈 Forecast Chart")

    fig, ax = plt.subplots()
    ax.plot(monthly_data['Month'], y, label='Actual Spending', marker='o')
    ax.plot(monthly_data['Month'], y_pred, label='Trend Line (Fitted)', linestyle='--')
    ax.plot(forecast_df['Month'], forecast_df['Prediction'], label='Forecast', marker='x')
    ax.fill_between(forecast_df['Month'], forecast_df['LowerBound'], forecast_df['UpperBound'],
                    color='lightgray', alpha=0.4, label='Confidence Interval (±1σ)')

    ax.set_xlabel("Month")
    ax.set_ylabel("Spending ($)")
    ax.set_title("Monthly Spending Forecast")
    ax.legend()
    plt.xticks(rotation=45)

    st.pyplot(fig)
