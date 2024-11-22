import pika, os, sys
from send import email

def main():
    print("Notification Service Running ............")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    def callback(ch,method, properties,body):
        err = email.notification(body)
        print(f"body:{body}")
        if err:
            print(f"Error:{err}")
            ch.basic_nack(delivery_tag = method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag = method.delivery_tag)
    

    channel.basic_consume(
        queue = os.environ.get("PDF_QUEUE"),on_message_callback=callback
    )

    print("waiting for messages. To exit press CTRL + C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        print("Consumer.py file running..............")
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(1)
        except:
            os._exit(1)

