import boto3
import pandas as pd
import io

# -----------------------------
# AWS S3 SETTINGS
# -----------------------------
BUCKET_NAME = "electronics-sales-datalake-2026"
INPUT_KEY = "raw/electrical_goods_sales_dataset.csv"
OUTPUT_KEY = "processed/cleaned_sales.csv"

# -----------------------------
# CONNECT TO S3
# -----------------------------
s3 = boto3.client("s3", region_name="eu-north-1")

print("Reading sales data from S3...")

# Download CSV from S3
response = s3.get_object(
    Bucket=BUCKET_NAME,
    Key=INPUT_KEY
)

df = pd.read_csv(response["Body"])

print("Original shape:", df.shape)

# -----------------------------
# DATA CLEANING
# -----------------------------

# Convert date column
df["full_date"] = pd.to_datetime(
    df["full_date"],
    errors="coerce"
)

# Convert important numeric columns
numeric_columns = [
    "quantity",
    "unit_price",
    "discount_amount",
    "discount_rate",
    "tax_amount",
    "tax_rate",
    "line_total",
    "cost_amount",
    "profit_amount",
    "commission_amount",
    "commission_rate"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Convert returned field
df["is_returned"] = (
    df["is_returned"]
    .astype(str)
    .str.lower()
    .map({
        "t": True,
        "f": False,
        "true": True,
        "false": False
    })
)

# Remove duplicate sales records
df = df.drop_duplicates()

# Remove rows missing important information
df = df.dropna(
    subset=[
        "sales_id",
        "full_date",
        "product_name",
        "category",
        "quantity",
        "line_total"
    ]
)

# Fill optional text fields
text_columns = [
    "brand",
    "subcategory",
    "store_name",
    "channel",
    "platform",
    "device_type",
    "shipping_method"
]

for column in text_columns:
    df[column] = df[column].fillna("Unknown")

# Fill optional numeric fields
df["salesperson_id"] = df["salesperson_id"].fillna(0)

# -----------------------------
# SORT DATA
# -----------------------------
df = df.sort_values("full_date")

# -----------------------------
# SAVE CLEANED DATA
# -----------------------------
csv_buffer = io.StringIO()

df.to_csv(
    csv_buffer,
    index=False
)

s3.put_object(
    Bucket=BUCKET_NAME,
    Key=OUTPUT_KEY,
    Body=csv_buffer.getvalue(),
    ContentType="text/csv"
)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
print("\nCleaning completed!")
print("Cleaned shape:", df.shape)

print("\nColumns:", len(df.columns))

print("\nTotal Sales:",
      round(df["line_total"].sum(), 2))

print("Total Profit:",
      round(df["profit_amount"].sum(), 2))

print("Total Quantity:",
      round(df["quantity"].sum(), 2))

print("\nCleaned file uploaded to:")
print("s3://" + BUCKET_NAME + "/" + OUTPUT_KEY)

print("\nSUCCESS! Data processing completed.")