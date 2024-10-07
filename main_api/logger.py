import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


def to_brocker(host:str, exchange:str, body:str, routing_key:str = ""):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=body)

