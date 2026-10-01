"""
Project: Housing Price Analysis
Business Problem

A real-estate company wants to understand what factors influence house 
prices and identify patterns in its property portfolio.

Students prepare:

housing.csv

with columns:

Id
Area
Bedrooms
Bathrooms
Stories
Parking
Location
Furnishing
Age
Price

Now prepare an EDA as we practice for sales.csv in the class.

Students must answer questions such as:

What is the average house price?
Which location has the highest average price?
Does house area appear related to price?
What is the average price by number of bedrooms?
Do houses with parking have higher prices?
Which variables have the strongest relationship with price?
Are there potential outliers?
What percentage of houses have missing values?
Which property characteristics appear most important?
What recommendations can be made to the real-estate company? """

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no display needed, just save files
import matplotlib.pyplot as plt
import seaborn as sns
 
sns.set_style("whitegrid")
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)
 
OUT_DIR = "."  # charts save alongside this script
 
 
def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

section("1. LOAD & INSPECT THE DATA")
 
df = pd.read_csv("housing.csv")
 
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
print("Column types:")
print(df.dtypes)
print("\nFirst 5 rows:")
print(df.head())
 
print("\nSummary statistics (numeric columns):")
print(df.describe().round(2))

#Data quality checks
section("2. WHAT PERCENTAGE OF HOUSES HAVE MISSING VALUES?")
 
missing_count = df.isnull().sum()
missing_pct = (df.isnull().mean() * 100).round(2)
missing_summary = pd.DataFrame({"missing_count": missing_count, "missing_pct": missing_pct})
missing_summary = missing_summary[missing_summary["missing_count"] > 0].sort_values(
    "missing_pct", ascending=False
)
print(missing_summary if not missing_summary.empty else "No missing values found.")
 
rows_with_any_missing = df.isnull().any(axis=1).sum()
pct_rows_missing = round(rows_with_any_missing / len(df) * 100, 2)
print(f"\n{rows_with_any_missing} of {len(df)} rows ({pct_rows_missing}%) have at least one missing value.")

#handling missing values
df_clean = df.copy()
for col in ["Bathrooms", "Age"]:
    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
for col in ["Location", "Furnishing"]:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
 
print("\nMissing values after cleaning:", df_clean.isnull().sum().sum())
 
#3.average house price
section("3. WHAT IS THE AVERAGE HOUSE PRICE?")

 
avg_price = df_clean["Price"].mean()
median_price = df_clean["Price"].median()
std_price = df_clean["Price"].std()
print(f"Average price : {avg_price:,.2f}")
print(f"Median price  : {median_price:,.2f}")
print(f"Std deviation : {std_price:,.2f}")
print(f"Min / Max     : {df_clean['Price'].min():,.0f} / {df_clean['Price'].max():,.0f}")
 
plt.figure(figsize=(8, 5))
sns.histplot(df_clean["Price"], bins=30, kde=True, color="steelblue")
plt.axvline(avg_price, color="red", linestyle="--", label=f"Mean = {avg_price:,.0f}")
plt.axvline(median_price, color="green", linestyle="--", label=f"Median = {median_price:,.0f}")
plt.title("Distribution of House Prices")
plt.xlabel("Price")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/01_price_distribution.png", dpi=120)
plt.close()

#4. Which location has the highest average price?
section("4. WHICH LOCATION HAS THE HIGHEST AVERAGE PRICE?")
 
price_by_location = (
    df_clean.groupby("Location")["Price"]
    .agg(["mean", "median", "count"])
    .sort_values("mean", ascending=False)
    .round(2)
)
print(price_by_location)
top_location = price_by_location.index[0]
print(f"\nHighest average price: {top_location}")
 
plt.figure(figsize=(8, 5))
order = price_by_location.index
sns.barplot(x="Location", y="Price", data=df_clean, order=order, estimator=np.mean, errorbar=None, palette="viridis")
plt.title("Average Price by Location")
plt.ylabel("Average Price")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/02_price_by_location.png", dpi=120)
plt.close()

#5. Does house area appear related to price?
section("5. DOES HOUSE AREA APPEAR RELATED TO PRICE?")
 
corr_area_price = df_clean["Area"].corr(df_clean["Price"])
print(f"Correlation (Area, Price): {corr_area_price:.3f}")
if abs(corr_area_price) > 0.6:
    strength = "strong"
elif abs(corr_area_price) > 0.3:
    strength = "moderate"
else:
    strength = "weak"
print(f"-> This is a {strength} {'positive' if corr_area_price > 0 else 'negative'} relationship.")
 
plt.figure(figsize=(8, 5))
sns.regplot(x="Area", y="Price", data=df_clean, scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
plt.title(f"Area vs Price (correlation = {corr_area_price:.2f})")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/03_area_vs_price.png", dpi=120)
plt.close()


# 6. AVERAGE PRICE BY NUMBER OF BEDROOMS

section("6. WHAT IS THE AVERAGE PRICE BY NUMBER OF BEDROOMS?")
 
price_by_bedrooms = df_clean.groupby("Bedrooms")["Price"].agg(["mean", "count"]).round(2)
print(price_by_bedrooms)
 
plt.figure(figsize=(8, 5))
sns.barplot(x="Bedrooms", y="Price", data=df_clean, estimator=np.mean, errorbar=None, palette="crest")
plt.title("Average Price by Number of Bedrooms")
plt.ylabel("Average Price")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/04_price_by_bedrooms.png", dpi=120)
plt.close()
 
 

# 7. DO HOUSES WITH PARKING HAVE HIGHER PRICES?

section("7. DO HOUSES WITH PARKING HAVE HIGHER PRICES?")
 
df_clean["HasParking"] = np.where(df_clean["Parking"] > 0, "Has Parking", "No Parking")
price_by_parking = df_clean.groupby("HasParking")["Price"].agg(["mean", "median", "count"]).round(2)
print(price_by_parking)
 
diff = price_by_parking.loc["Has Parking", "mean"] - price_by_parking.loc["No Parking", "mean"]
pct_diff = diff / price_by_parking.loc["No Parking", "mean"] * 100
print(f"\nHouses with parking average {diff:,.0f} more ({pct_diff:.1f}%) than houses without.")
 
plt.figure(figsize=(6, 5))
sns.boxplot(x="HasParking", y="Price", data=df_clean, palette="Set2")
plt.title("Price by Parking Availability")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/05_price_by_parking.png", dpi=120)
plt.close()
 
 

# 8. WHICH VARIABLES HAVE THE STRONGEST RELATIONSHIP WITH PRICE?

section("8. WHICH VARIABLES HAVE THE STRONGEST RELATIONSHIP WITH PRICE?")
 
numeric_cols = ["Area", "Bedrooms", "Bathrooms", "Stories", "Parking", "Age", "Price"]
corr_matrix = df_clean[numeric_cols].corr()
price_corr = corr_matrix["Price"].drop("Price").sort_values(key=abs, ascending=False)
print("Correlation with Price (sorted by strength):")
print(price_corr.round(3))
 
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/06_correlation_heatmap.png", dpi=120)
plt.close()
 
 

# 9. ARE THERE POTENTIAL OUTLIERS?

section("9. ARE THERE POTENTIAL OUTLIERS?")
 
 
def iqr_outliers(series):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return series[(series < lower) | (series > upper)], lower, upper
 
 
price_outliers, p_low, p_high = iqr_outliers(df_clean["Price"])
area_outliers, a_low, a_high = iqr_outliers(df_clean["Area"])
 
print(f"Price: {len(price_outliers)} outlier(s) outside [{p_low:,.0f}, {p_high:,.0f}]")
if len(price_outliers):
    print(df_clean.loc[price_outliers.index, ["Id", "Area", "Location", "Price"]])
 
print(f"\nArea: {len(area_outliers)} outlier(s) outside [{a_low:,.0f}, {a_high:,.0f}]")
if len(area_outliers):
    print(df_clean.loc[area_outliers.index, ["Id", "Area", "Location", "Price"]])
 
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
sns.boxplot(y=df_clean["Price"], ax=axes[0], color="salmon")
axes[0].set_title("Price — Outlier Check")
sns.boxplot(y=df_clean["Area"], ax=axes[1], color="lightblue")
axes[1].set_title("Area — Outlier Check")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/07_outlier_boxplots.png", dpi=120)
plt.close()
 
 


# 10. WHICH PROPERTY CHARACTERISTICS APPEAR MOST IMPORTANT?

section("10. WHICH PROPERTY CHARACTERISTICS APPEAR MOST IMPORTANT?")
 
# Simple, interpretable approach: standardized linear regression coefficients.
# Standardizing puts all variables on the same scale so coefficients are comparable.
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
 
feature_cols = ["Area", "Bedrooms", "Bathrooms", "Stories", "Parking", "Age"]
X = df_clean[feature_cols]
y = df_clean["Price"]
 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
 
model = LinearRegression()
model.fit(X_scaled, y)
 
importance = pd.Series(model.coef_, index=feature_cols).sort_values(key=abs, ascending=False)
print("Standardized coefficients (larger |value| = bigger effect on price):")
print(importance.round(2))
print(f"\nModel R^2 (how well these features explain price): {model.score(X_scaled, y):.3f}")
 
plt.figure(figsize=(8, 5))
importance.plot(kind="barh", color=["green" if v > 0 else "red" for v in importance])
plt.title("Feature Importance (Standardized Regression Coefficients)")
plt.xlabel("Effect on Price (standardized)")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/08_feature_importance.png", dpi=120)
plt.close()
 
 

# 11. RECOMMENDATIONS

section("11. RECOMMENDATIONS FOR THE REAL-ESTATE COMPANY")
 
top_feature = importance.abs().idxmax()
recommendations = f"""
Based on this EDA:
 
1. Pricing benchmark: the portfolio averages {avg_price:,.0f}, but the median
   ({median_price:,.0f}) is a more reliable "typical price" reference since
   the mean is pulled up by a small number of high-value outliers.
 
2. Location strategy: "{top_location}" commands the highest average price
   ({price_by_location.loc[top_location, 'mean']:,.0f}). Marketing and pricing
   strategy should treat location as a primary price tier, not an afterthought.
 
3. Area is the strongest lever: Area correlates {corr_area_price:.2f} with price,
   a {strength} relationship — every additional unit of floor area is one of the
   most reliable ways to justify a higher asking price.
 
4. Parking adds measurable value: listings with parking sell for about
   {pct_diff:.1f}% more on average. Low-cost parking additions could be a
   worthwhile upsell for lower-tier listings.
 
5. Data quality: {pct_rows_missing}% of rows have missing data, concentrated
   in {', '.join(missing_summary.index) if not missing_summary.empty else 'no columns'}.
   The intake form/process for new listings should make these fields mandatory
   to avoid degrading future analysis.
 
6. Outlier review: {len(price_outliers)} price outlier(s) and {len(area_outliers)}
   area outlier(s) were flagged. These should be manually verified — they may be
   luxury/commercial properties that should be modeled separately rather than
   averaged in with standard residential listings.
 
7. Most influential feature overall: "{top_feature}" has the largest standardized
   effect on price among the modeled features, so it should be the primary factor
   sales staff highlight when justifying valuations to clients.
"""
print(recommendations)
 
print("\nAll charts saved to the current directory:")
for f in [
    "01_price_distribution.png", "02_price_by_location.png", "03_area_vs_price.png",
    "04_price_by_bedrooms.png", "05_price_by_parking.png", "06_correlation_heatmap.png",
    "07_outlier_boxplots.png", "08_feature_importance.png",
]:
    print(f" - {f}")

 

 
 