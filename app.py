import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# Load data
# -----------------------------------

df = pd.read_csv("sales.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------------
# Dashboard title
# -----------------------------------

st.title("📊 Retail Sales Dashboard")

st.write(
    "Interactive analysis of retail sales performance."
)

# -----------------------------------
# Sidebar filters
# -----------------------------------

st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

products = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# -----------------------------------
# Apply filters
# -----------------------------------

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Product"].isin(products))
]

# -----------------------------------
# KPIs
# -----------------------------------

total_sales = filtered_df["Sales"].sum()

total_quantity = filtered_df["Quantity"].sum()

total_orders = len(filtered_df)

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"Rs. {total_sales:,.0f}"
)

col2.metric(
    "Total Quantity",
    f"{total_quantity:,}"
)

col3.metric(
    "Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Average Order Value",
    f"Rs. {average_order_value:,.0f}"
)

st.divider()

# -----------------------------------
# Sales by Product
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    product_sales = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .reset_index()
    )

    fig_product = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        title="Sales by Product",
        text="Sales"
    )

    fig_product.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )

# -----------------------------------
# Sales by Region
# -----------------------------------

with col2:

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig_region = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

# -----------------------------------
# Monthly Sales Trend
# -----------------------------------

filtered_df["Month"] = (
    filtered_df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    filtered_df
    .groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# -----------------------------------
# Category Analysis
# -----------------------------------

category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)

# -----------------------------------
# Raw Data
# -----------------------------------

with st.expander("View Raw Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )