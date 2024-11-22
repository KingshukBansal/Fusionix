# app/rabbitmq_helper.py

import pika
import json
import time
import os


class RabbitMQConnection:
    def __init__(self):
        self.host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
        self.retry_interval = int(os.environ.get("RABBITMQ_RETRY_INTERVAL", 5))
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        """Establish a connection to RabbitMQ."""
        while not self.connection or self.connection.is_closed:
            try:
                print("Trying to connect to RabbitMQ...")
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, heartbeat=600, blocked_connection_timeout=300)
                )
                self.channel = self.connection.channel()
                print("Successfully connected to RabbitMQ")
            except pika.exceptions.AMQPConnectionError as err:
                print(f"RabbitMQ connection failed: {err}. Retrying in {self.retry_interval} seconds...")
                time.sleep(self.retry_interval)

    def _ensure_channel(self):
        """Ensure the channel is open and valid."""
        if not self.channel or self.channel.is_closed:
            print("Channel is closed. Reconnecting...")
            self._connect()

    def publish_message(self, queue, message):
        """Publish a message to a queue."""
        while True:
            try:
                self._ensure_channel()
                self.channel.queue_declare(queue=queue, durable=True)
                self.channel.basic_publish(
                    exchange='',
                    routing_key=queue,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                    ),
                )
                print(f"Message successfully published to {queue}")
                break  # Exit loop after successful publish
            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed) as err:
                print(f"Error publishing message: {err}. Reconnecting...")
                self._connect()
            except Exception as e:
                print(f"Unexpected error: {e}")
                break  # Avoid infinite loop for unexpected errors
