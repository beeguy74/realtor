import pika 
from dotenv import load_dotenv
from os import getenv


load_dotenv()


EXCHANGE_NAME = getenv("RABBIT_MAIN_EXCHANGE_NAME", '')
ROUTING_KEY = getenv("RABBIT_MAIN_EXCHANGE_KEY")


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="localhost",
    credentials=pika.PlainCredentials(username=getenv("RABBITMQ_DEFAULT_USER", ""), password=getenv("RABBITMQ_DEFAULT_PASS", ""))
))

channel = connection.channel()

try:
    # Проверяем существование exchange (НЕ создаём новый)
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', passive=True)
    print("Exchange уже существует")
except pika.exceptions.ChannelClosedByBroker as e:
    if e.reply_code == 404:
        print("Exchange не существует")
        # Здесь можно создать exchange, если нужно:
        channel = connection.channel()  # Нужно открыть новый канал после ошибки!
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
        print("Exchange создан")
    else:
        raise
    
channel.queue_declare(
    queue='my_queue',
    durable=True,      # Сохраняется после перезапуска
    exclusive=False,   # Не эксклюзивная
    auto_delete=False  # Не удаляется автоматически
)

channel.queue_bind(
    queue='my_queue',
    exchange=EXCHANGE_NAME,
    routing_key=ROUTING_KEY
)

def callback(ch, method, properties, body):
    print(f"Получено: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='my_queue', on_message_callback=callback)
channel.start_consuming()

    
connection.close()