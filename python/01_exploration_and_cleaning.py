
# ============================================================
# 1. PROJECT SETUP
# ============================================================

from pathlib import Path

# Define the main project directory
project_dir = Path(__file__).resolve().parent.parent

# Define data directories
raw_data_dir = project_dir / "data" / "raw"
processed_data_dir = project_dir / "data" / "processed"

# Define output directories
figures_dir = project_dir / "figures"
output_dir = project_dir / "output"


# ============================================================
# 2. IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import janitor


# ============================================================
# 3. DISPLAY SETTINGS
# ============================================================

# Display all columns and avoid truncating the DataFrame
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.expand_frame_repr", False)


# ============================================================
# 4. IMPORT RAW DATA
# ============================================================

# Import all sheets from the Excel file
retail_sheets = pd.read_excel(
    raw_data_dir / "online_retail.xlsx",
    sheet_name=None
)

# Combine all sheets into one DataFrame
a = pd.concat(retail_sheets.values(), ignore_index=True)


# ============================================================
# 5. DATA EXPLORATION AND QUALITY CHECKS
# ============================================================

# Check the number of rows and columns
print(a.shape)

# Check for duplicate rows
print(r"Duplicated rows : ")
print(a.duplicated().sum())
print(a[a.duplicated()])

# Calculate the percentage of duplicate rows
duplicated = a[a.duplicated()]
print(r"percentage of duplicated rows =", (len(duplicated) / len(a)) * 100)

# Check for missing values in each column
print(a.isna().sum())

# Inspect rows with missing descriptions
print(a[a["Description"].isna()])


# ============================================================
# 6. DATA CLEANING
# ============================================================

# Remove34,335 duplicate rows
a = a.drop_duplicates().copy()

# Verify that no duplicate rows remain
print(a.duplicated().sum())

# Fill missing descriptions using StockCode as a lookup key
# Only use StockCodes associated with one unique description
description_lookup = (
    a.groupby("StockCode")["Description"]
    .agg(["nunique", "first"])
    .reset_index()
)

description_lookup = description_lookup[
    description_lookup["nunique"] == 1
]

description_map = description_lookup.set_index("StockCode")["first"]

a["Description"] = a["Description"].fillna(
    a["StockCode"].map(description_map)
)

# Check missing values after filling descriptions
print(a.isna().sum())


# ============================================================
# 7. DATA TYPE CONVERSION
# ============================================================

# Check original data types
print(a.dtypes)

# Convert columns to appropriate data types
a = a.astype({
    "Invoice": "string",
    "StockCode": "string",
    "Description": "string",
    "Customer ID": "string"
})

# Verify data type conversion
print(a.dtypes)


# ============================================================
# 8. COLUMN NAME STANDARDIZATION
# ============================================================

# Convert all column names to snake_case
a = a.clean_names(case_type="snake")

# Inspect the cleaned column names and first five rows
print(a.head())


# ============================================================
# 9. FEATURE ENGINEERING
# ============================================================

# Calculate total price for each transaction row
# (Quantity multiplied by Price)
a["total_price"] = a["price"] * a["quantity"]

# Inspect the updated DataFrame
print(a.head())


# ============================================================
# 10. EXPORT CLEANED DATA
# ============================================================

# Save the cleaned DataFrame as a CSV file
a.to_csv(processed_data_dir / "cleaned.csv", index=False)
