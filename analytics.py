import boto3
import pandas as pd
import io

# ==========================================
# AWS S3 SETTINGS
# ==========================================

BUCKET_NAME = "electronics-sales-datalake-2026"
INPUT_KEY = "processed/cleaned_sales.csv"

s3 = boto3.client(
    "s3",
    region_name="eu-north-1"
)

# ==========================================
# READ CLEANED DATA FROM S3
# ==========================================

print("Reading cleaned data from S3...")

response = s3.get_object(
    Bucket=BUCKET_NAME,
    Key=INPUT_KEY
)

df = pd.read_csv(response["Body"])

print("Data loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# BASIC ANALYTICS
# ==========================================

total_sales = df["line_total"].sum()
total_profit = df["profit_amount"].sum()
total_quantity = df["quantity"].sum()

total_orders = df["order_id"].nunique()
total_products = df["product_name"].nunique()

average_order_value = total_sales / total_orders


print("\n========================================")
print("        ELECTRONICS SALES ANALYTICS")
print("========================================")

print(f"\nTotal Sales       : ₹{total_sales:,.2f}")
print(f"Total Profit      : ₹{total_profit:,.2f}")
print(f"Total Quantity    : {total_quantity:,.0f}")
print(f"Total Orders      : {total_orders:,}")
print(f"Total Products    : {total_products:,}")
print(f"Average Order     : ₹{average_order_value:,.2f}")


# ==========================================
# TOP PRODUCTS
# ==========================================

print("\n========================================")
print("           TOP 10 PRODUCTS")
print("========================================")

top_products = (
    df.groupby("product_name")
      .agg(
          sales=("line_total", "sum"),
          quantity=("quantity", "sum")
      )
      .sort_values("sales", ascending=False)
      .head(10)
)

print(top_products.to_string())


# ==========================================
# CATEGORY ANALYSIS
# ==========================================

print("\n========================================")
print("          CATEGORY PERFORMANCE")
print("========================================")

category_sales = (
    df.groupby("category")
      .agg(
          sales=("line_total", "sum"),
          profit=("profit_amount", "sum"),
          quantity=("quantity", "sum")
      )
      .sort_values("sales", ascending=False)
)

print(category_sales.to_string())


# ==========================================
# BRAND ANALYSIS
# ==========================================

print("\n========================================")
print("             BRAND PERFORMANCE")
print("========================================")

brand_sales = (
    df.groupby("brand")
      .agg(
          sales=("line_total", "sum"),
          quantity=("quantity", "sum")
      )
      .sort_values("sales", ascending=False)
      .head(10)
)

print(brand_sales.to_string())


# ==========================================
# STORE ANALYSIS
# ==========================================

print("\n========================================")
print("             STORE PERFORMANCE")
print("========================================")

store_sales = (
    df.groupby("store_name")
      .agg(
          sales=("line_total", "sum"),
          profit=("profit_amount", "sum")
      )
      .sort_values("sales", ascending=False)
)

print(store_sales.to_string())


# ==========================================
# MONTHLY SALES
# ==========================================

print("\n========================================")
print("             MONTHLY SALES")
print("========================================")

df["full_date"] = pd.to_datetime(df["full_date"])

monthly_sales = (
    df.groupby(df["full_date"].dt.to_period("M"))
      .agg(
          sales=("line_total", "sum"),
          profit=("profit_amount", "sum"),
          quantity=("quantity", "sum")
      )
      .sort_index()
)

print(monthly_sales.to_string())


# ==========================================
# SALES BY CHANNEL
# ==========================================

print("\n========================================")
print("             SALES BY CHANNEL")
print("========================================")

channel_sales = (
    df.groupby("channel")
      .agg(
          sales=("line_total", "sum"),
          quantity=("quantity", "sum")
      )
      .sort_values("sales", ascending=False)
)

print(channel_sales.to_string())


# ==========================================
# RETURNS
# ==========================================

print("\n========================================")
print("             RETURN ANALYSIS")
print("========================================")

returned_sales = df[df["is_returned"] == True]

print("Returned Transactions:", len(returned_sales))

if len(returned_sales) > 0:
    print(
        "Returned Sales: ₹"
        + f"{returned_sales['line_total'].sum():,.2f}"
    )

return_rate = (
    len(returned_sales) / len(df)
) * 100

print(f"Return Rate: {return_rate:.2f}%")


# ==========================================
# BEST PRODUCT
# ==========================================

best_product = top_products.index[0]

print("\n========================================")
print("             BEST PRODUCT")
print("========================================")

print("Best-selling product:", best_product)


# ==========================================
# BEST CATEGORY
# ==========================================

best_category = category_sales.index[0]

print("Best-selling category:", best_category)


# ==========================================
# BEST BRAND
# ==========================================

best_brand = brand_sales.index[0]

print("Top brand:", best_brand)


print("\n========================================")
print("        ANALYTICS COMPLETED")
print("========================================")