FROM python:alpine3.20

WORKDIR /app

RUN pip3 install telebot --no-cache-dir
RUN pip3 install pika --no-cache-dir


COPY main.py ./

ENTRYPOINT [ "python", "main.py" ]
EXPOSE 80
