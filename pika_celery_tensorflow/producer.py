import pika
import json
import uuid
import pandas as pd
import glob
import os

# Set up RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

# Process each Excel file in the ./Sources directory
excel_files = glob.glob("./Sources/*.xlsx")
total_rows_sent = 0

for file_path in excel_files:
    print(f"📄 Processing {file_path}...")
    df = pd.read_excel(file_path)

    for count, row in enumerate(df.to_dict(orient='records')):
        task_id = str(uuid.uuid4())

        message = {
            'task': 'tasks.consume_from_raw_queue',
            'id': task_id,
            'args': [row],  # Send row as first argument
            'kwargs': {},
            'retries': 0,
            'eta': None,
        }

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                content_type='application/json',
                content_encoding='utf-8',
                delivery_mode=2,
            )
        )
        total_rows_sent += 1

# ✅ Send a single "__END__" message at the end
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=json.dumps({
        'task': 'tasks.consume_from_raw_queue',
        'id': str(uuid.uuid4()),
        'args': ["__END__"],
        'kwargs': {},
        'retries': 0,
        'eta': None,
    }),
    properties=pika.BasicProperties(
        content_type='application/json',
        content_encoding='utf-8',
        delivery_mode=2,
    )
)

print(f"✅ Done! Sent {total_rows_sent} rows from {len(excel_files)} files.")
connection.close()
