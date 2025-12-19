# UsingAWSSQS_crawl-data

# Tiki Product Crawler

A Python-based project to crawl product data from Tiki.vn using **asyncio** and **AWS services** (S3 + SQS). This project is designed for **data engineering practice**, including batch processing, asynchronous API calls, and cloud workflow.

---



## 🔹 Features

- Load product IDs from **CSV files** stored locally or in **S3 bucket**.
- Use **asyncio + aiohttp** to fetch product details concurrently from Tiki API.
- Batch processing using **SQS queues** to handle thousands of product IDs safely.
- Store raw product data into **JSON files** in local storage or S3.
- Designed to avoid IP blocking and rate-limit issues with:
  - Semaphore for concurrent requests
  - Retry mechanism for 429/403 HTTP responses
  - Random delays between requests
- Scalable: supports multiple worker processes for parallel crawling.
- Cloud-ready: designed to run on **AWS EC2** with SQS + S3 integration.

---

Batch Processing

Large CSV files are split into smaller batches for better processing:
Use batch.py to split a file into smaller CSVs:
python src/batch.py 
Each small batch is then uploaded to S3 and sent to SQS.
This ensures:
No worker gets overwhelmed
Rate limits are respected

Progress can resume easily if a batch fails
## 🔹 Requirements

- Python 3.9+
- AWS account with:
  - S3 bucket for storing CSV batches
  - SQS queue for batch processing
- Python packages:


```bash
pip install aiohttp boto3
```
🔹 Setup AWS
Create S3 bucket
Store CSV files in input/ folder.

Create SQS queue
Push product IDs from CSV to SQS.

Upload CSV batches using s3.py:

bash
Copy code
```python src/s3.py```
This script reads CSVs from local folder and sends IDs to the SQS queue.

🔹 Run the Worker
Set environment variables or configure ~/.aws/credentials with proper AWS keys.

Run async worker to fetch product data:

bash
Copy code
```python src/worker_sqs.py```
Worker polls messages from SQS, fetches product data asynchronously, and saves JSON output.

Supports multiple batches and parallel workers.

🔹 Running Locally Without AWS
You can test crawling locally using fetch_async.py:

bash
Copy code
```python src/fetch_async.py```
Reads product IDs from local CSV.

Fetches data using async requests without SQS.

🔹 Configuration Parameters
Variable	Description
MAX_CONCURRENT	Max concurrent API calls per worker
RETRIES	Number of retries for failed requests
TIMEOUT	Timeout for each HTTP request
SLEEP_TIME	Base sleep between retries to avoid blocking
BASE_DELAY	Delay between requests to prevent rate limiting

🔹 Notes
Designed to handle thousands of product IDs safely with retries and async batch processing.

Logs success/failure for each product.

Works within AWS free tier if used moderately:

S3 free storage: 5GB/month

SQS free requests: 1 million/month

🔹 Potential Improvements
Use multiple EC2 instances to scale beyond thousands of product IDs.

Store output directly to AWS S3 instead of local files.

Integrate AWS Lambda for serverless crawling.

Add data cleaning / normalization pipeline before storing JSON.
