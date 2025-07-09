import pika 
from dotenv import load_dotenv
from os import getenv


load_dotenv()



connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="localhost",
    credentials=pika.PlainCredentials(username=getenv("RABBIT_USERNAME", ""), password=getenv("RABBIT_PASSWORD", ""))
))

channel = connection.channel()

try:
    # Проверяем существование exchange (НЕ создаём новый)
    channel.exchange_declare(exchange='my_exchange', passive=True)
    print("Exchange уже существует")
except pika.exceptions.ChannelClosedByBroker as e:
    if e.reply_code == 404:
        print("Exchange не существует")
        # Здесь можно создать exchange, если нужно:
        channel = connection.channel()  # Нужно открыть новый канал после ошибки!
        channel.exchange_declare(exchange='my_exchange', exchange_type='direct')
        print("Exchange создан")
    else:
        raise
    
connection.close()