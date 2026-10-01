import pandas as pd
import seaborn as sns
import plotly.express as px

data = { "Category":["Electronics", "Clothing", "Home & Kitchen", "Books", "Toys"],
         "Sales":[50000, 40000, 30000, 20000, 10000] }

df = pd.DataFrame(data)
fig = px.pie(df, values='Sales', names='Category', title='Percentage of Sales by Category')
fig.show()

