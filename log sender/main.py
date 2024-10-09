import telebot

import threading
import pika
from time import sleep


HOST_NAME = 'logs-rabbitmq-container'


##TELEGRAM BOT CONF
bot = telebot.TeleBot('7522751462:AAHc6eex2FDhtPqIf-ZfFSMPVqsOvoctmqw')
##

users = {"1014822113"}
QUEUE = 'tg-logging'



try:
    connection = pika.BlockingConnection(pika.ConnectionParameters("HOST_NAME"))
    channel = connection.channel()
    print("connection succesc")
except Exception as e:
    print("connection failed")
    print(e)








# def run_bot():
#     print("* Bot started")
#     bot.polling(none_stop=True, interval=0)




# def consume():
#     print("consume called")
#     def callback(ch, method, properties, body):

#         print("get: ", body)
#         # for user in users:
#         #     bot.send_message(user, body)
#     print("callback declared")

#     try:
#         channel.queue_declare(queue=QUEUE, durable=True)
#     except:
#         print("queue declaration")

#     channel.basic_consume(queue='',auto_ack=True,on_message_callback=callback)

#     print('* Consumer started')
#     channel.start_consuming()

# ##




# thread = threading.Thread(target=run_bot)
# thread2 = threading.Thread(target=consume)



# if __name__ == "__main__":

    



#     # try:
#     #     thread2.start()
#     # except:
#     #     print("Cannot start consumer")

#     # try:
#     #     thread.start()
#     #     pass
#     # except:
#     #     print("Cannot start bot")
