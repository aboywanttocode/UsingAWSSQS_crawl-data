import boto3
import csv
import io

# ===============================
BUCKET = "tiki-data-raw"
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/511039171643/tiki-product-queue"
BATCH_FILES = [f"input/batch_{i:03}.csv" for i in range(1, 10)]

sqs = boto3.client("sqs", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")

# ===============================
for batch_file in BATCH_FILES:
    print(f"Pushing batch {batch_file} to SQS...")
    obj = s3.get_object(Bucket=BUCKET, Key=batch_file)
    body = obj["Body"].read().decode("utf-8")

    reader = csv.reader(io.StringIO(body))
    next(reader) 

    for row in reader:
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=row[0])

print("All batches pushed to SQS successfully.")
