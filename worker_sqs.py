import asyncio
import aiohttp
import boto3
import time
import json

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/511039171643/tiki-product-queue"
API_URL = "https://api.tiki.vn/product-detail/api/v1/products/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

MAX_CONCURRENT = 5
MAX_SQS_MESSAGES = 10
TIMEOUT = 5
RETRIES = 3

sqs = boto3.client("sqs", region_name="us-east-1")


async def fetch_product(session, pid):
    for attempt in range(RETRIES):
        try:
            async with session.get(API_URL.format(pid), timeout=TIMEOUT) as r:
                if r.status == 200:
                    data = await r.json()
                    print(f"{pid}")
                    return {
                        "id": data.get("id"),
                        "name": data.get("name"),
                        "price": data.get("price")
                    }
                elif r.status in (429, 403):
                    await asyncio.sleep(2 ** attempt)
        except Exception:
            await asyncio.sleep(1)
    return None


async def process_batch(pids):
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT)
    async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
        tasks = [fetch_product(session, pid) for pid in pids]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]


def main():
    start = time.time()
    all_results = []

    print("Worker started...")

    while True:
        resp = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=MAX_SQS_MESSAGES,
            WaitTimeSeconds=20,
            VisibilityTimeout=60
        )

        messages = resp.get("Messages", [])
        if not messages:
            print("No more messages")
            break

        pids = [msg["Body"] for msg in messages]

        results = asyncio.run(process_batch(pids))
        all_results.extend(results)

        for msg in messages:
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

    with open(f"output_{int(time.time())}.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"Worker done: {len(all_results)} items")
    print(f"Time: {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()
