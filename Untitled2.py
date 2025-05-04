import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

revenue_df = pd.read_csv("teladoc_annual_revenue.csv")
stock_df = pd.read_csv("teladoc_stock.csv")
stock_df['Date'] = pd.to_datetime(stock_df['Date'], utc=True)
stock_df['Year'] = stock_df['Date'].dt.year

st.title("📊 Teladoc Health Dashboard")
st.write("Explore annual revenue trends and stock performance of Teladoc Health (TDOC).")

st.subheader("📊 Annual Revenue (in Millions USD)")
selected_years = st.multiselect(
    "Select Year(s):",
    options=revenue_df['Year'].astype(str).tolist(),
    default=revenue_df['Year'].astype(str).tolist()
)
filtered_revenue = revenue_df[revenue_df['Year'].astype(str).isin(selected_years)]

fig1, ax1 = plt.subplots()
ax1.bar(filtered_revenue['Year'].astype(str), filtered_revenue['Revenue'], color='lightgreen')
ax1.set_xlabel("Year")
ax1.set_ylabel("Revenue (in Millions USD)")
st.pyplot(fig1)

st.subheader("📈 Stock Price Over Time")
start_date, end_date = st.date_input(
    "Select Date Range:",
    [stock_df['Date'].min().date(), stock_df['Date'].max().date()]
)
filtered_stock = stock_df[
    (stock_df['Date'].dt.date >= start_date) & (stock_df['Date'].dt.date <= end_date)
]

fig2, ax2 = plt.subplots()
ax2.plot(filtered_stock['Date'], filtered_stock['Close'], color='skyblue', alpha=0.7)
ax2.set_xlabel("Date")
ax2.set_ylabel("Closing Price")
st.pyplot(fig2)

st.subheader("📉 Revenue vs. Average Stock Price")

avg_close_per_year = stock_df.groupby('Year')['Close'].mean().reset_index()
combined_df = pd.merge(revenue_df, avg_close_per_year, on='Year', how='inner')

sort_order = st.radio("Sort by Year:", ['Ascending', 'Descending'])
combined_df_sorted = combined_df.sort_values('Year', ascending=(sort_order == 'Ascending'))

fig3, ax3 = plt.subplots()
ax4 = ax3.twinx()

ax3.bar(combined_df_sorted['Year'].astype(str), combined_df_sorted['Revenue'], color='lightblue', label='Revenue')
ax4.plot(combined_df_sorted['Year'].astype(str), combined_df_sorted['Close'], color='orange', marker='o', label='Avg Close')

ax3.set_xlabel("Year")
ax3.set_ylabel("Revenue", color='lightblue')
ax4.set_ylabel("Avg Close Price", color='orange')
st.pyplot(fig3)

