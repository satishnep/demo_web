
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_csv("cleaned_data.csv", parse_dates=["Date"])
    return data

data = load_data()

data['Revenue'] = data['Quantity'] * data['UnitPrice']
data['IsReturn'] = data['Revenue'] < 0

st.sidebar.header("📌 Filters")

min_date = data['Date'].min()
max_date = data['Date'].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

products = st.sidebar.multiselect("Select Products", options=data['Description'].dropna().unique())

countries = st.sidebar.multiselect("Select Country", options=data['Country'].dropna().unique())

filtered = data[
    (data['Date'] >= pd.to_datetime(date_range[0])) &
    (data['Date'] <= pd.to_datetime(date_range[1]))
]

if products:
    filtered = filtered[filtered['Description'].isin(products)]

if countries:
    filtered = filtered[filtered['Country'].isin(countries)]

st.title("📊 Business Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${filtered['Revenue'].sum():,.2f}")
col2.metric("🧾 Total Orders", filtered['InvoiceNo'].nunique())
col3.metric("👥 Unique Customers", filtered['CustomerID'].nunique())

st.subheader("📈 Revenue Over Time")
revenue_by_date = filtered.groupby('Date')['Revenue'].sum().reset_index()
fig_line = px.line(revenue_by_date, x='Date', y='Revenue', title='Revenue Over Time')
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("🥧 Top Products by Revenue")
top_products = filtered.groupby('Description')['Revenue'].sum().nlargest(5).reset_index()
fig_pie = px.pie(top_products, values='Revenue', names='Description', title='Top 5 Products by Revenue')
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("🌍 Revenue by Country")
country_revenue = filtered.groupby('Country')['Revenue'].sum().reset_index()
fig_map = px.choropleth(
    country_revenue,
    locations='Country',
    locationmode='country names',
    color='Revenue',
    title='Revenue by Country',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig_map, use_container_width=True)

st.subheader("↩️ Returns by Country")
returns = filtered[filtered['Revenue'] < 0]
returns_by_country = returns.groupby('Country')['Revenue'].sum().reset_index()
fig_returns = px.bar(returns_by_country, x='Country', y='Revenue', color='Revenue', title='Returns by Country')
st.plotly_chart(fig_returns, use_container_width=True)

st.markdown("---")
st.caption("Dashboard built with ❤️ using Streamlit")
