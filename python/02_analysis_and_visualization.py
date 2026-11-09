# ============================================================
# 1. PROJECT SETUP
# ============================================================

from pathlib import Path

# Define the main project directory
project_dir = Path(__file__).resolve().parent.parent

# Define directories for raw and processed data
raw_data_dir = project_dir / "data" / "raw"
processed_data_dir = project_dir / "data" / "processed"

# Define directories for charts and analysis outputs
figures_dir = project_dir / "figures"
output_dir = project_dir / "output"

# Create output directories if they do not already exist
figures_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. IMPORT REQUIRED LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


# ============================================================
# 3. DATA IMPORT AND PREPARATION
# ============================================================

# Configure pandas display options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.expand_frame_repr", False)

# Import the previously cleaned dataset
a = pd.read_csv(processed_data_dir / "cleaned.csv")

# Convert invoice_date from string to datetime format
a["invoice_date"] = pd.to_datetime(a["invoice_date"])

# Extract year, month, and day into separate columns
# These columns will be used for grouping and time-based analysis
a["year"] = a["invoice_date"].dt.year
a["month"] = a["invoice_date"].dt.month
a["day"] = a["invoice_date"].dt.day

# Separate cancelled invoices from non-cancelled transactions
# Cancelled invoices are identified by an invoice number starting with "C"
cancelled_orders = a[
    a["invoice"].str.startswith("C", na=False)
].copy()

# Retain only non-cancelled transactions for the sales analysis
a = a[
    ~a["invoice"].str.startswith("C", na=False)
].copy()

# Create separate datasets for monthly and yearly analyses

# Monthly analysis:
# Include December 2009 but exclude incomplete December 2011
monthly_data = a[
    ~((a["year"] == 2011) & (a["month"] == 12))
].copy()

# Yearly analysis:
# Exclude December 2009 but retain December 2011
yearly_data = a[
    ~((a["year"] == 2009) & (a["month"] == 12))
].copy()


# ============================================================
# 4. OVERALL SALES ANALYSIS
# ============================================================

# Calculate total and average sales by year
# December 2009 is excluded, while December 2011 is retained
year_analysis_sum = yearly_data.groupby("year")["total_price"].sum()
year_analysis_mean = yearly_data.groupby("year")["total_price"].mean()

# Calculate total and average sales by year and month
# December 2009 is included, while December 2011 is excluded
month_year_group_sum = (
    monthly_data.groupby(["year", "month"])["total_price"].sum()
)

print(month_year_group_sum)

month_year_group_mean = (
    monthly_data.groupby(["year", "month"])["total_price"].mean()
)


# ============================================================
# 5. MONTHLY SALES LINE CHART
# ============================================================

# Convert year and month combinations into datetime values
# The first day of each month is used as the date
dates = pd.to_datetime([
    f"{year}-{month:02d}-01"
    for year, month in month_year_group_sum.index
])

# Create the line chart
fig, ax = plt.subplots(figsize=(16, 6))

ax.plot(
    dates,
    month_year_group_sum.values,
    marker="o"
)

# Add chart title and axis labels
ax.set_title("Monthly Sales Over Time (December 2009–November 2011)")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales")

# Display every month on the x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b, %Y"))

# Restrict the x-axis to the actual data range
ax.set_xlim(
    dates.min() - pd.Timedelta(days=10),
    dates.max() + pd.Timedelta(days=10)
)

# Format y-axis values with comma separators
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x:,.0f}")
)

# Improve chart readability
plt.xticks(rotation=45)
ax.grid(True)
fig.tight_layout()

# Save the figure in high resolution
fig.savefig(
    figures_dir / "01_monthly_sales_over_time.png",
    dpi=300,
    bbox_inches="tight"
)

# Display the chart
plt.show()


# ============================================================
# 6. YEARLY SALES BAR CHART
# ============================================================

# Create a vertical bar chart with one bar for each year
# December 2009 is excluded from the yearly analysis
# December 2011 is retained in the 2011 total
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(
    year_analysis_sum.index.astype(str),
    year_analysis_sum.values
)

# Add chart title and axis labels
ax.set_title("Total Sales by Year (2010–2011)")
ax.set_xlabel("Year")
ax.set_ylabel("Total Sales")

# Format y-axis values with comma separators
ax.yaxis.set_major_formatter(
    ticker.StrMethodFormatter("{x:,.0f}")
)

# Improve chart readability
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)
fig.tight_layout()

# Save the figure in high resolution
fig.savefig(
    figures_dir / "02_yearly_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 7. GEOGRAPHICAL SALES ANALYSIS
# ============================================================

# Calculate total sales for each country across the monthly-analysis
# period: December 2009 through November 2011
country_analysis = monthly_data.groupby("country")["total_price"].sum()

# December 2009 is a one-month observation, so keep it separate
# from the full-year country analyses
dataset_december_2009 = monthly_data[
    (monthly_data["year"] == 2009) &
    (monthly_data["month"] == 12)
]

# Use yearly_data for 2010 and 2011:
# December 2009 is excluded and December 2011 is retained
dataset_2010 = yearly_data[yearly_data["year"] == 2010]
dataset_2011 = yearly_data[yearly_data["year"] == 2011]

# Calculate total sales by country for December 2009
country_analysis_december_2009 = (
    dataset_december_2009.groupby("country")["total_price"].sum()
)

# Calculate total sales by country for each year
country_analysis_2010 = (
    dataset_2010.groupby("country")["total_price"].sum()
)

country_analysis_2011 = (
    dataset_2011.groupby("country")["total_price"].sum()
)

# Identify the top 10 countries by sales for each period
top_10_countries_december_2009 = (
    country_analysis_december_2009.sort_values(ascending=False).head(10)
)

print(top_10_countries_december_2009)

top_10_countries_2010 = (
    country_analysis_2010.sort_values(ascending=False).head(10)
)

top_10_countries_2011 = (
    country_analysis_2011.sort_values(ascending=False).head(10)
)


# ============================================================
# 8. TOP 10 COUNTRIES BY SALES (DECEMBER 2009)
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(
    top_10_countries_december_2009.index,
    top_10_countries_december_2009.values
)

# Add chart title and axis labels
ax.set_title("Top 10 Countries by Total Sales (December 2009)")
ax.set_xlabel("Country")
ax.set_ylabel("Total Sales")

# Format y-axis values with comma separators
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x:,.0f}")
)

# Improve readability
plt.xticks(rotation=45, ha="right")
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()

# Save the figure in high resolution
fig.savefig(
    figures_dir / "03_top_10_countries_december_2009.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 9. TOP 10 COUNTRIES BY SALES (2010)
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(
    top_10_countries_2010.index,
    top_10_countries_2010.values
)

# Add chart title and axis labels
ax.set_title("Top 10 Countries by Total Sales (2010)")
ax.set_xlabel("Country")
ax.set_ylabel("Total Sales")

# Format y-axis values with comma separators
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x:,.0f}")
)

# Improve readability
plt.xticks(rotation=45, ha="right")
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()

# Save the figure in high resolution
fig.savefig(
    figures_dir / "04_top_10_countries_2010.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 10. TOP 10 COUNTRIES BY SALES (2011)
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(
    top_10_countries_2011.index,
    top_10_countries_2011.values
)

# Add chart title and axis labels
ax.set_title("Top 10 Countries by Total Sales (2011)")
ax.set_xlabel("Country")
ax.set_ylabel("Total Sales")

# Format y-axis values with comma separators
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, pos: f"{x:,.0f}")
)

# Improve readability
plt.xticks(rotation=45, ha="right")
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()

# Save the figure in high resolution
fig.savefig(
    figures_dir / "05_top_10_countries_2011.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 11. UNITED KINGDOM SALES ANALYSIS
# ============================================================

# Filter transactions to include only the United Kingdom
# Use monthly_data to include December 2009 and exclude December 2011
UK_analysis = monthly_data[
    monthly_data["country"] == "United Kingdom"
]

# Stock codes that are fees, adjustments, or test entries (not real products)
non_product_codes = [
    "POST", "DOT", "M", "C2", "AMAZONFEE",
    "ADJUST", "ADJUST2", "B", "D", "S",
    "BANK CHARGES", "TEST001", "TEST002",
]

# Keep real products only (upper() also catches the lowercase "m" code)
UK_products_only = UK_analysis[
    ~UK_analysis["stock_code"].astype(str).str.upper().isin(non_product_codes)
].copy()

# ------------------------------------------------------------
# 11.1 PRODUCT-LEVEL SALES ANALYSIS
# ------------------------------------------------------------

# Group products by product description
UK_product_analysis = (
    UK_products_only.groupby("description", as_index=False)
    .agg(
        total_sales=("total_price", "sum")
    )
)

# Identify the 10 products with the highest total sales
top_10_UK_products = UK_product_analysis.nlargest(10, "total_sales")

# Identify the 10 products with the lowest positive total sales
lowest_10_UK_products = (
    UK_product_analysis[UK_product_analysis["total_sales"] > 0]
    .nsmallest(10, "total_sales")
)

print(lowest_10_UK_products)


# ------------------------------------------------------------
# 11.2 TOP 10 PRODUCTS BY SALES
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

top_10_UK_products.sort_values(
    by="total_sales"
)["total_sales"].plot(
    kind="barh",
    color="seagreen"
)

# Replace stock codes with product descriptions on the y-axis
plt.yticks(
    range(len(top_10_UK_products)),
    top_10_UK_products.sort_values(
        by="total_sales"
    )["description"]
)

plt.title("Top 10 Products by Total Sales in the UK (Dec 2009–Nov 2011)")
plt.xlabel("Total Sales Price")
plt.ylabel("Product")
plt.tight_layout()

# Save the figure in high resolution
plt.gcf().savefig(
    figures_dir / "06_top_10_products_uk.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# 11.3 LOWEST 10 PRODUCTS BY POSITIVE SALES
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

lowest_10_UK_products.sort_values(
    by="total_sales",
    ascending=False
)["total_sales"].plot(
    kind="barh",
    color="indianred"
)

# Replace stock codes with product descriptions on the y-axis
plt.yticks(
    range(len(lowest_10_UK_products)),
    lowest_10_UK_products.sort_values(
        by="total_sales",
        ascending=False
    )["description"]
)

plt.title("Least 10 Products by Total Sales in the UK (Dec 2009–Nov 2011)")
plt.xlabel("Total Sales Price")
plt.ylabel("Product")
plt.tight_layout()

# Save the figure in high resolution
fig = plt.gcf()

fig.savefig(
    figures_dir / "07_lowest_10_products_uk.png",
    dpi=150
)

plt.show()


# ------------------------------------------------------------
# 11.4 UNITED KINGDOM VS REST OF THE WORLD
# ------------------------------------------------------------

# Calculate total sales for the United Kingdom
UK_total_sales = UK_analysis["total_price"].sum()

# Calculate total sales for all countries except the UK
total_sales_excl_uk = monthly_data[
    monthly_data["country"] != "United Kingdom"
]["total_price"].sum()

# Calculate total sales across all countries
total_sales_all_countries = monthly_data["total_price"].sum()

# Prepare data for the pie chart
sales = [UK_total_sales, total_sales_excl_uk]
labels = ["United Kingdom", "Rest of the World"]

# Create legend labels displaying sales values and percentages
legend_labels = [
    f"{label}: {value:,.0f} ({value / total_sales_all_countries:.1%})"
    for label, value in zip(labels, sales)
]

# Create the pie chart
plt.figure(figsize=(9, 7))

plt.pie(
    sales,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#3498DB", "#E67E22"],
    wedgeprops={"edgecolor": "white"}
)

plt.legend(
    legend_labels,
    title="Total Sales",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.12)
)

plt.title("United Kingdom vs Rest of the World - Total Sales (Dec 2009–Nov 2011)")
plt.tight_layout()

# Save the figure in high resolution
plt.gcf().savefig(
    figures_dir / "08_uk_vs_rest_of_world_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# 11.5 MONTHLY SALES IN THE UNITED KINGDOM
# ------------------------------------------------------------

# Calculate monthly sales in the UK across the monthly-analysis period
uk_yearly_analysis = (
    UK_analysis.groupby(["year", "month"])["total_price"].sum()
)

# Convert year and month combinations into datetime values
uk_yearly_analysis.index = pd.to_datetime(
    [
        f"{year}-{month:02d}-01"
        for year, month in uk_yearly_analysis.index
    ]
)

# Create the monthly sales line chart
plt.figure(figsize=(14, 7))

plt.plot(
    uk_yearly_analysis.index,
    uk_yearly_analysis.values,
    marker="o",
    color="steelblue",
    linewidth=2
)

plt.title("Monthly Total Sales in the United Kingdom")
plt.xlabel("Month")
plt.ylabel("Total Sales")

# Format the x-axis to display month and year
plt.gca().xaxis.set_major_formatter(
    mdates.DateFormatter("%b, %Y")
)

plt.gca().xaxis.set_major_locator(
    mdates.MonthLocator(interval=1)
)

# Format sales values with commas and zero decimal places
plt.gca().yaxis.set_major_formatter(
    ticker.StrMethodFormatter("{x:,.0f}")
)

plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the figure in high resolution
plt.gcf().savefig(
    figures_dir / "09_monthly_uk_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 12. MONTH-OVER-MONTH (MoM) SALES ANALYSIS
# ============================================================

# Convert the monthly sales series into a DataFrame
# and arrange the records chronologically
mom_analysis = (
    month_year_group_sum.reset_index()
    .sort_values(
        by=["year", "month"],
        ascending=True
    )
)

# Rename the sales column to identify the current month's value
mom_analysis = mom_analysis.rename(
    columns={"total_price": "current_month_sales"}
)

# Retrieve the previous month's sales using shift()
mom_analysis["last_month_sales"] = (
    mom_analysis["current_month_sales"].shift(1)
)

# Calculate the percentage change compared with the previous month
mom_analysis["mom"] = (
    round(
        (
            (
                mom_analysis["current_month_sales"]
                - mom_analysis["last_month_sales"]
            )
            / mom_analysis["last_month_sales"]
        ) * 100,
        2
    ).astype(str) + "%"
)

# Export the month-over-month analysis table
mom_analysis.to_csv(
    output_dir / "month_over_month_analysis.csv",
    index=False
)

print(mom_analysis)


# ============================================================
# 13. YEAR-OVER-YEAR (YoY) SALES ANALYSIS
# ============================================================

# Convert yearly sales into a DataFrame and arrange chronologically
yoy_analysis = (
    year_analysis_sum.reset_index()
    .sort_values(
        by="year",
        ascending=True
    )
)

# 2009 is already excluded from year_analysis_sum because
# December 2009 was excluded from yearly_data
# Therefore, the yearly analysis contains 2010 and 2011 only

# Rename the sales column to identify the current year's value
yoy_analysis = yoy_analysis.rename(
    columns={"total_price": "current_year_sales"}
)

# Retrieve the previous year's sales using shift()
yoy_analysis["last_year_sales"] = (
    yoy_analysis["current_year_sales"].shift(1)
)

# Calculate the percentage change compared with the previous year
yoy_analysis["yoy_change"] = (
    round(
        (
            (
                yoy_analysis["current_year_sales"]
                - yoy_analysis["last_year_sales"]
            )
            / yoy_analysis["last_year_sales"]
        ) * 100,
        2
    ).astype(str) + "%"
)

# Export the year-over-year analysis table
yoy_analysis.to_csv(
    output_dir / "year_over_year_analysis.csv",
    index=False
)

print(yoy_analysis)


# ============================================================
# 14. CUSTOMER AND ORDER METRICS
# ============================================================

# Use monthly_data so that incomplete December 2011 is excluded
# from the customer and order metrics

# Count the number of unique customers
unique_customers = monthly_data["customer_id"].nunique()
print(unique_customers)

# Count the number of unique non-cancelled invoices
total_orders = monthly_data["invoice"].nunique()
print(total_orders)

# Calculate average order value:
# First calculate the total value of each invoice,
# then calculate the average across all invoices
average_order_value = (
    monthly_data.groupby("invoice")["total_price"].sum().mean()
)
print(average_order_value)

# ============================================================
# 15. ANALYSIS NOTES AND LIMITATIONS
# ============================================================

# Note 1:
# This analysis calculates net sales by excluding cancelled invoices
# while retaining returns and other negative transaction values.

# Note 2:
# Monthly analyses include December 2009 but exclude December 2011
# because the available data for December 2011 ends on December 9.

# Note 3:
# Yearly analyses exclude December 2009 because the dataset begins
# in December 2009, providing no other months for that calendar year.
# December 2011 is retained in yearly analyses.

# Note 4:
# December 2009 is a partial observation period. This should be
# considered when interpreting monthly trends and MoM changes,
# particularly the comparison between December 2009 and January 2010.

# Note 5:
# The 2011 yearly total includes data only through December 9.
# Therefore, the comparison between 2010 and 2011 is not a
# like-for-like full-year comparison.

# Note 6:
# The December 2009 country analysis represents one month only
# and should not be interpreted as a full-year country comparison.
