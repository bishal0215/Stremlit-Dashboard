import streamlit as st
import pandas as pd
import plotly.express as px

 
# PAGE CONFIGURATION
 

st.set_page_config(
    page_title="Sales Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)

 
# TITLE
 

st.title("📊 Sales Visualization Dashboard")
st.write("Interactive dashboard showing different types of data visualizations.")

 
# SAMPLE DATA
 

# Product sales data
product_data = pd.DataFrame({
    "Product": ["Laptop", "Mobile", "Tablet", "Headphone", "Keyboard"],
    "Sales": [120000, 180000, 90000, 50000, 30000]
})

# Monthly sales data
monthly_data = pd.DataFrame({
    "Month": [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ],
    "Sales": [
        50000, 60000, 55000, 70000,
        80000, 75000, 90000, 95000,
        85000, 100000, 110000, 120000
    ]
})

# Advertising and sales data
advertising_data = pd.DataFrame({
    "Advertising": [10, 20, 30, 40, 50, 60, 70, 80],
    "Sales": [25, 35, 40, 50, 55, 65, 70, 85]
})

# Customer age data
age_data = pd.DataFrame({
    "Age": [
        18, 19, 20, 21, 21, 22, 22, 23,
        23, 23, 24, 24, 25, 25, 26, 27,
        28, 29, 30, 31, 32, 35, 36, 40
    ]
})

# Region and category data
region_data = pd.DataFrame({
    "Region": ["East", "West", "North", "South"],
    "Electronics": [50000, 60000, 45000, 70000],
    "Clothing": [30000, 40000, 35000, 50000],
    "Food": [20000, 25000, 30000, 35000]
})

 
# KPI CARDS
 

total_sales = product_data["Sales"].sum()
highest_product = product_data.loc[
    product_data["Sales"].idxmax(), "Product"
]

average_sales = product_data["Sales"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Sales",
    f"Rs. {total_sales:,.0f}"
)

col2.metric(
    "🏆 Highest Selling Product",
    highest_product
)

col3.metric(
    "📈 Average Sales",
    f"Rs. {average_sales:,.0f}"
)

st.divider()

 
# ROW 1 - BAR CHART + LINE CHART
 

col1, col2 = st.columns(2)

# BAR CHART
with col1:

    st.subheader("📊 Sales by Product")

    fig_bar = px.bar(
        product_data,
        x="Product",
        y="Sales",
        title="Product Sales Comparison",
        text="Sales"
    )

    fig_bar.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )


# LINE CHART
with col2:

    st.subheader("📈 Monthly Sales Trend")

    fig_line = px.line(
        monthly_data,
        x="Month",
        y="Sales",
        title="Sales Trend Over 12 Months",
        markers=True
    )

    st.plotly_chart(
        fig_line,
        use_container_width=True
    )


 
# ROW 2 - SCATTER + PIE CHART
 

col1, col2 = st.columns(2)

# SCATTER PLOT
with col1:

    st.subheader("🔵 Advertising vs Sales")

    fig_scatter = px.scatter(
        advertising_data,
        x="Advertising",
        y="Sales",
        title="Advertising Expenditure vs Sales",
        size="Sales"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# PIE CHART
with col2:

    st.subheader("🥧 Sales Composition")

    fig_pie = px.pie(
        product_data,
        names="Product",
        values="Sales",
        title="Percentage of Total Sales"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


 
# ROW 3 - HISTOGRAM + STACKED BAR
 

col1, col2 = st.columns(2)

# HISTOGRAM
with col1:

    st.subheader("📊 Customer Age Distribution")

    fig_hist = px.histogram(
        age_data,
        x="Age",
        nbins=8,
        title="Distribution of Customer Ages"
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )


# STACKED BAR
with col2:

    st.subheader("📚 Sales by Region and Category")

    # Convert data into long format
    region_long = region_data.melt(
        id_vars="Region",
        var_name="Category",
        value_name="Sales"
    )

    fig_stacked = px.bar(
        region_long,
        x="Region",
        y="Sales",
        color="Category",
        title="Regional Sales by Category"
    )

    st.plotly_chart(
        fig_stacked,
        use_container_width=True
    )


 
# DATA TABLE
 

st.divider()

st.subheader("📋 Product Sales Data")

st.dataframe(
    product_data,
    use_container_width=True
)

 
# FOOTER
 

st.divider()

st.write(
    "Dashboard created using Python, Pandas, Plotly and Streamlit."
)
