import pika, os, sys, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    client = MongoClient("host.minikube.internal",27017)
    db_vidoes = client.videos
    db_mp3s= client.mp3s

    fs_videos = gridfs.GridFS(db_vidoes)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    def callback(ch,method, properties,body):
        err = to_mp3.start(body,fs_videos,fs_mp3s,ch)

        if err:
            print(f"Error:{err}")
            ch.basic_nack(delivery_tag = method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag = method.delivery_tag)
    

    channel.basic_consume(
        queue = os.environ.get("VIDEOS_QUEUE"),on_message_callback=callback
    )

    print("waiting for messages. To exit press CTRL + C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(1)
        except:
            os._exit(1)

