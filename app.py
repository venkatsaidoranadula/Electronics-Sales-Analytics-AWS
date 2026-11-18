from flask import Flask, jsonify, send_file
import boto3
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# ================= AWS S3 SETTINGS =================

BUCKET_NAME = "electronics-sales-datalake-2026"
REGION = "eu-north-1"

CLEANED_FILE = "processed/cleaned_sales.csv"
PREDICTION_FILE = "predictions/sales_predictions.csv"


# ================= CONNECT TO S3 =================

s3 = boto3.client(
    "s3",
    region_name=REGION
)


# ================= LOAD CSV FROM S3 =================

def load_csv_from_s3(file_key):

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=file_key
    )

    data = response["Body"].read()

    return pd.read_csv(BytesIO(data))


# ================= HOME PAGE =================

@app.route("/")
def home():

    return send_file("index.html")


# ================= DASHBOARD API =================

@app.route("/api/dashboard")
def dashboard():

    df = load_csv_from_s3(CLEANED_FILE)

    total_sales = df["line_total"].sum()
    total_profit = df["profit_amount"].sum()
    total_quantity = df["quantity"].sum()
    total_orders = df["order_id"].nunique()
    total_products = df["product_id"].nunique()

    average_order_value = (
        total_sales / total_orders
    )

    result = {

        "total_sales": float(total_sales),

        "total_profit": float(total_profit),

        "total_quantity": int(total_quantity),

        "total_orders": int(total_orders),

        "total_products": int(total_products),

        "average_order_value": float(
            average_order_value
        )
    }

    return jsonify(result)


# ================= ANALYTICS API =================

@app.route("/api/analytics")
def analytics():

    df = load_csv_from_s3(CLEANED_FILE)

    # ---------- TOP PRODUCTS ----------

    top_products = (
        df.groupby("product_name")["line_total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


    # ---------- CATEGORY SALES ----------

    category_sales = (
        df.groupby("category")["line_total"]
        .sum()
        .sort_values(ascending=False)
    )


    # ---------- BRAND SALES ----------

    brand_sales = (
        df.groupby("brand")["line_total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


    # ---------- MONTHLY SALES ----------

    df["full_date"] = pd.to_datetime(
        df["full_date"]
    )

    df["month"] = df["full_date"].dt.to_period("M").astype(str)

    monthly_sales = (
        df.groupby("month")["line_total"]
        .sum()
        .reset_index()
    )

    result = {

        "top_products": [

            {
                "product": name,
                "sales": float(value)
            }

            for name, value in top_products.items()
        ],


        "category_sales": [

            {
                "category": name,
                "sales": float(value)
            }

            for name, value in category_sales.items()
        ],


        "brand_sales": [

            {
                "brand": name,
                "sales": float(value)
            }

            for name, value in brand_sales.items()
        ],


        "monthly_sales": [

            {
                "month": row["month"],
                "sales": float(row["line_total"])
            }

            for _, row in monthly_sales.iterrows()
        ]
    }

    return jsonify(result)

@app.route("/api/predictions")
def predictions():

    df = load_csv_from_s3(
        PREDICTION_FILE
    )

    records = df.to_dict(
        orient="records"
    )

    return jsonify({

        "predictions": records

    })
if __name__ == "__main__":

    app.run(
        debug=True
    )