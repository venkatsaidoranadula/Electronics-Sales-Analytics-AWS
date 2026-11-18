import boto3
import pandas as pd
import io
from sklearn.linear_model import LinearRegression

BUCKET_NAME = "electronics-sales-datalake-2026"
INPUT_KEY = "processed/cleaned_sales.csv"
OUTPUT_KEY = "predictions/sales_predictions.csv"

s3 = boto3.client(
    "s3",
    region_name="eu-north-1"
)

print("Reading cleaned data from S3...")

response = s3.get_object(
    Bucket=BUCKET_NAME,
    Key=INPUT_KEY
)

df = pd.read_csv(response["Body"])

print("Data loaded successfully!")
print("Rows:", len(df))

df["full_date"] = pd.to_datetime(df["full_date"])

df["month"] = df["full_date"].dt.to_period("M")

monthly = (
    df.groupby("month")
    .agg(
        sales=("line_total", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)

monthly["month_number"] = range(
    1,
    len(monthly) + 1
)

X = monthly[["month_number"]]

sales_model = LinearRegression()

sales_model.fit(
    X,
    monthly["sales"]
)

next_month_number = len(monthly) + 1

next_month_data = pd.DataFrame({
    "month_number": [next_month_number]
})

predicted_sales = sales_model.predict(
    next_month_data
)[0]

predicted_sales = max(
    0,
    predicted_sales
)

quantity_model = LinearRegression()

quantity_model.fit(
    X,
    monthly["quantity"]
)

predicted_quantity = quantity_model.predict(
    next_month_data
)[0]

predicted_quantity = max(
    0,
    round(predicted_quantity)
)

last_month = monthly["month"].iloc[-1]

next_month = last_month + 1

print("\n========================================")
print("          ML SALES PREDICTION")
print("========================================")

print("Latest month:", last_month)

print("Predicted month:", next_month)

print(
    f"Predicted Sales: ₹{predicted_sales:,.2f}"
)

print(
    f"Predicted Quantity: {predicted_quantity:,.0f}"
)

print("\n========================================")
print("       PRODUCT DEMAND PREDICTION")
print("========================================")

all_months = pd.period_range(
    start=df["month"].min(),
    end=df["month"].max(),
    freq="M"
)

products = (
    df["product_name"]
    .dropna()
    .unique()
)

product_predictions = []

for product in products:

    product_data = (
        df[df["product_name"] == product]
        .groupby("month")["quantity"]
        .sum()
        .reindex(
            all_months,
            fill_value=0
        )
        .reset_index()
    )

    product_data.columns = [
        "month",
        "quantity"
    ]

    product_data["month_number"] = range(
        1,
        len(product_data) + 1
    )

    if len(product_data) >= 3:

        X_product = product_data[
            ["month_number"]
        ]

        y_product = product_data[
            "quantity"
        ]

        product_model = LinearRegression()

        product_model.fit(
            X_product,
            y_product
        )

        next_product_month = pd.DataFrame({
            "month_number": [
                len(product_data) + 1
            ]
        })

        predicted_demand = product_model.predict(
            next_product_month
        )[0]

        predicted_demand = max(
            0,
            round(predicted_demand)
        )

        current_quantity = int(
            product_data["quantity"].iloc[-1]
        )

        product_predictions.append({
            "product_name": product,
            "current_month_quantity": current_quantity,
            "predicted_quantity": int(
                predicted_demand
            )
        })

prediction_df = pd.DataFrame(
    product_predictions
)

prediction_df = prediction_df.sort_values(
    "predicted_quantity",
    ascending=False
)

prediction_df["rank"] = range(
    1,
    len(prediction_df) + 1
)

output = prediction_df[
    [
        "rank",
        "product_name",
        "current_month_quantity",
        "predicted_quantity"
    ]
]

print(
    output.head(10).to_string(
        index=False
    )
)

csv_buffer = io.StringIO()

output.to_csv(
    csv_buffer,
    index=False
)

s3.put_object(
    Bucket=BUCKET_NAME,
    Key=OUTPUT_KEY,
    Body=csv_buffer.getvalue(),
    ContentType="text/csv"
)

print("\n========================================")
print("       PREDICTION COMPLETED")
print("========================================")

print(
    "\nPrediction file uploaded to:"
)

print(
    "s3://"
    + BUCKET_NAME
    + "/"
    + OUTPUT_KEY
)

if len(output) > 0:

    print("\nTop predicted product:")

    print(
        output.iloc[0]["product_name"]
    )

print("\nSUCCESS! ML prediction completed.")