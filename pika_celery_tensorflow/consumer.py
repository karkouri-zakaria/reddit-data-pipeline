import pika
import json

# Establish connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the same queue
channel.queue_declare(queue='task_queue', durable=True)

# Define callback function
def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Received message {message['sequence']}: {message['data']} (sent at {message['timestamp']})")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up consumer
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
