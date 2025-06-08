from celery import Celery
import pandas as pd
import boto3
from datetime import datetime  # Import datetime module

app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//',  # Connects to RabbitMQ
    backend='rpc://'
)

payload_buffer = []

# S3 client for LocalStack
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

BUCKET_NAME = 'rabbitmq-reddit'

@app.task(name='tasks.consume_from_raw_queue')
def consume_from_raw_queue(payload):
    global payload_buffer

    # Check if it's the signal to finalize the batch
    if payload == "__END__":
        upload_buffer_to_s3()
        return

    payload_buffer.append(payload)

def upload_buffer_to_s3():
    global payload_buffer
    
    df = pd.DataFrame(payload_buffer)
    
    # Generate filename with current date and time in YYYYMMDDHHMMSS format
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    csv_filename = f"reddit_{timestamp}.csv"

    # Write CSV content to memory buffer instead of file system
    csv_buffer = df.to_csv(index=False).encode('utf-8')

    s3.put_object(Bucket=BUCKET_NAME, Key=csv_filename, Body=csv_buffer)

    print(f"✅ Uploaded {csv_filename} directly to s3://{BUCKET_NAME}")
    payload_buffer = []  # Clear buffer
