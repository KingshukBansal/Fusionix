import pika
import os
import sys
import time
from pymongo import MongoClient
import gridfs
from utils import to_pdf
import json

def main():
    # MongoDB connection
    client = MongoClient("host.minikube.internal", 27017)
    db_docx = client.docx_files
    db_pdf = client.pdf_files
    db_pdf_conversions = client.pdf_conversions 

    fs_docx = gridfs.GridFS(db_docx)
    fs_pdf = gridfs.GridFS(db_pdf)

    # RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        try:
            # Parse RabbitMQ message
            message = json.loads(body.decode("utf-8"))

            # Extract docx_fid from the message
            docx_fid = message.get("docx_fid")
            if not docx_fid:
                print("docx_fid is missing in the message.")
                return

            # Check for password field in the message
            password = message.get("password")
            if password and password.strip():  # Non-empty password
                print("Password detected, using password-protected conversion.")
                pdf_fid, err = to_pdf.convert_with_password_protection(
                    body, fs_docx, fs_pdf, ch
                )
            else:  # No password provided
                print("No password provided, using simple conversion.")
                pdf_fid, err = to_pdf.convert(body, fs_docx, fs_pdf, ch)

            # Acknowledge or Nack the message based on error
            if not pdf_fid:
                print(f"Error: {err}")
                ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                # Insert docx_fid and pdf_id into MongoDB
                record = {
                    "docx_fid": docx_fid,
                    "pdf_fid": str(pdf_fid[0]),  # Convert ObjectId to string if needed
                    "timestamp": time.time()  # Optional: Add a timestamp
                }
                 # Use the appropriate database/collection
                db_pdf_conversions.records.insert_one(record)

                print(f"Inserted record into MongoDB: {record}")
                ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"Unexpected error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    # Set up RabbitMQ consumer
    channel.basic_consume(
        queue=os.environ.get("DOCX_QUEUE"),
        on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL + C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
