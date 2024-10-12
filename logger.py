import pika
from config import BROKER_URI

BROKER_URI = "logs-rabbitmq-container"
QUEUE = 'tg-logging'

def logging_startup():
    """
    Initialize logger \n
    Connects to RabbitMQ and makes queue and exchange for it
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(BROKER_URI))
        channel = connection.channel()
        print("connected to brocker")

        channel.queue_declare(QUEUE)
        print("queue declared")
        channel.exchange_declare(exchange='logs', exchange_type='topic')
        print("exchange declared")
        channel.queue_bind(exchange='logs', queue=QUEUE, routing_key="test.*")
        print("queue binded")

    except Exception as e:
        print("Connection to broker failed")
        print(e)



def to_brocker(host:str, exchange:str, body:str, routing_key:str = ""):
    """
    Send data to RabbitMQ
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=body)

    print("log sended: \n")
    print(body)