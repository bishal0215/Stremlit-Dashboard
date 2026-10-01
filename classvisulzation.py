#visulization and story telling 
# for explaining the outcomes / results for data analysis we use variours types of visulizatiioin ranging from charts, graphs , tables to map
# lets talk about what type of visulization to be used in what case:

#1. Bar chart 
# bar charts are best suits to visulie results while comaparing entities .
# for example - which product generate the highest sales?

#2 Line chart 
# line chart are best suits to visualize trends over time, 
# for ecammle : how did sales change over 12 months period ?

#3 Scatter Plot:
# Scatter plot best suits to visulize relationships among the entities. 
# for example : is advertising expending realtes to sales?

#4 Pie Chart:
# Pie chart best suits to visulize percentage composition of certain entities .
# for example: which product among the electronics has highest percentage of sales?

#5 Histogram :
# Histogram are best use to visulize distribution 
#for example: how many of our customers were of what age ? in other words distribution of age among our customers 


#stacked Bar:
# Stacked Bars are best use to visulize comparision over time. or category compositions 
#for example: saless : sales by region and category 


# maps
# maps are use t visulize geo locations
#for example Sales visulize sales by cities or regions. 



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


# 1. BAR CHART


products = ["Laptop", "Mobile", "Tablet", "Headphone", "Keyboard"]
sales = [120000, 180000, 90000, 50000, 30000]

plt.figure(figsize=(8, 5))

plt.bar(products, sales)

plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales")

plt.show()


# 2. LINE CHART


months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

monthly_sales = [
    50000, 60000, 55000, 70000,
    80000, 75000, 90000, 95000,
    85000, 100000, 110000, 120000
]

plt.figure(figsize=(10, 5))

plt.plot(months, monthly_sales, marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.show()



# 3. SCATTER PLOT


advertising = [10, 20, 30, 40, 50, 60, 70, 80]
sales_amount = [25, 35, 40, 50, 55, 65, 70, 85]

plt.figure(figsize=(8, 5))

plt.scatter(advertising, sales_amount)

plt.title("Advertising Expenditure vs Sales")
plt.xlabel("Advertising Expenditure")
plt.ylabel("Sales")

plt.show()



# 4. PIE CHART


products = ["Laptop", "Mobile", "Tablet", "Headphone"]
sales = [120000, 180000, 90000, 50000]

plt.figure(figsize=(7, 7))

plt.pie(
    sales,
    labels=products,
    autopct="%1.1f%%"
)

plt.title("Percentage of Sales by Product")

plt.show()



# 5. HISTOGRAM


ages = [
    18, 19, 20, 21, 21, 22, 22, 23,
    23, 23, 24, 24, 25, 25, 26, 27,
    28, 29, 30, 31, 32, 35, 36, 40
]

plt.figure(figsize=(8, 5))

plt.hist(
    ages,
    bins=6,
    edgecolor="black"
)

plt.title("Age Distribution of Customers")
plt.xlabel("Age")
plt.ylabel("Number of Customers")

plt.show()



# 6. STACKED BAR CHART


data = {
    "Region": ["East", "West", "North", "South"],
    "Electronics": [50000, 60000, 45000, 70000],
    "Clothing": [30000, 40000, 35000, 50000],
    "Food": [20000, 25000, 30000, 35000]
}

df = pd.DataFrame(data)

plt.figure(figsize=(9, 5))

df.set_index("Region").plot(
    kind="bar",
    stacked=True
)

plt.title("Sales by Region and Category")
plt.xlabel("Region")
plt.ylabel("Sales")

plt.show()



# 7. MAP


# Create map centered around Nepal
nepal_map = folium.Map(
    location=[28.3949, 84.1240],
    zoom_start=7
)

# Kathmandu
folium.Marker(
    [27.7172, 85.3240],
    popup="Kathmandu - Sales: Rs. 150,000"
).add_to(nepal_map)

# Pokhara
folium.Marker(
    [28.2096, 83.9856],
    popup="Pokhara - Sales: Rs. 100,000"
).add_to(nepal_map)

# Butwal
folium.Marker(
    [27.7000, 83.4500],
    popup="Butwal - Sales: Rs. 80,000"
).add_to(nepal_map)

# Display map
nepal_map.save("sales_map.html")

print("======================================")
print("All visualizations completed!")
print("Map saved as: sales_map.html")
print("======================================")
