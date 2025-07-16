import pika
import json
import random
import time
from dotenv import load_dotenv
from os import getenv


load_dotenv()

exchange_name = getenv("RABBIT_MAIN_EXCHANGE_NAME", '')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="localhost",
    credentials=pika.PlainCredentials(username=getenv("RABBIT_USERNAME", ""), password=getenv("RABBIT_PASSWORD", ""))
))
channel = connection.channel()
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

devices = [random.randint(0, 100) for _ in range(100)]
routing_keys = [getenv("RABBIT_MAIN_EXCHANGE_KEY", '')]

while True:
    measure = random.choice(routing_keys)
    data = {'device': random.choice(devices), 'measure': measure, 'value': random.randint(0,100)}
    message = json.dumps(data)
    channel.basic_publish(exchange=exchange_name, routing_key=measure, body=message)
    print(f'Sent: {message}')
    time.sleep(3)
