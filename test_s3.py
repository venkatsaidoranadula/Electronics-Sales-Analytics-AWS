import boto3

BUCKET_NAME = "electronics-sales-datalake-2026"
REGION = "eu-north-1"

s3 = boto3.client("s3", region_name=REGION)

try:
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    print("SUCCESS!")
    print("Connected to S3 bucket:", BUCKET_NAME)

    if "Contents" in response:
        print("\nFiles/Folders:")
        for item in response["Contents"]:
            print(item["Key"])
    else:
        print("Bucket is empty.")

except Exception as e:
    print("ERROR:")
    print(e)