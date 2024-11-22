import os
import gridfs
import requests
from flask import Flask, request, send_file, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from utils.rabbitmq_helper import RabbitMQConnection

# Initialize Flask app
server = Flask(__name__)
CORS(server)

# MongoDB connections
mongo_docx_uri = os.environ.get("MONGO_DOCX_URI", "mongodb://host.minikube.internal:27017/docx_files")
mongo_pdf_uri = os.environ.get("MONGO_PDF_URI", "mongodb://host.minikube.internal:27017/pdf_files")
mongo_docx = PyMongo(server, uri=mongo_docx_uri)
mongo_pdf = PyMongo(server, uri=mongo_pdf_uri)

# GridFS setup
fs_docx = gridfs.GridFS(mongo_docx.db)
fs_pdf = gridfs.GridFS(mongo_pdf.db)

# Initialize RabbitMQ helper
rabbitmq = RabbitMQConnection()

# Routes
@server.route('/upload', methods=['POST'])
def upload():
    if len(request.files) != 1:
        return "Only 1 file required", 400

    for _, file in request.files.items():
        try:
            # Store the DOCX file in GridFS
            docx_file_id = fs_docx.put(file)

            # Prepare the message to publish
            docx_info = {
                "docx_fid": str(docx_file_id),
                "email": request.form.get('email'),
                "password": request.form.get('password', None),
                "pdf_fid": None
            }

            # Publish the message to RabbitMQ
            rabbitmq.publish_message(queue='docx', message=docx_info)

            return jsonify({"message": "file uploaded successfully", "docx_id": str(docx_file_id)}), 200

        except Exception as err:
            print(f"Error uploading file: {err}")
            return f"Error uploading file: {err}", 500


@server.route('/download', methods=['GET'])
def download():
    fid_string = request.args.get("fid")
    if not fid_string:
        return "fid is required", 400

    download_service_url = f"http://{os.environ.get('DOWNLOAD_SVC_ADDRESS', 'download-service')}/get_pdf"

    try:
        response = requests.get(download_service_url, params={'docx_fid': fid_string}, stream=True)
        if response.status_code == 200:
            return send_file(
                response.raw,
                download_name=f"{fid_string}.pdf",
                mimetype="application/pdf"
            )
        else:
            return f"Error from download service: {response.text}", response.status_code

    except requests.exceptions.RequestException as err:
        print(f"Error communicating with download service: {err}")
        return "Error communicating with the download service", 500


@server.route('/getMetadata', methods=['GET'])
def get_metadata():
    fid_string = request.args.get("fid")
    if not fid_string:
        return "fid is required", 400

    metadata_service_url = f"http://{os.environ.get('METADATA_SVC_ADDRESS', 'metadata-service')}/metadata"

    try:
        response = requests.get(metadata_service_url, params={'fid': fid_string})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return f"Error from metadata service: {response.text}", response.status_code

    except requests.exceptions.RequestException as err:
        print(f"Error calling metadata service: {err}")
        return "Error communicating with the metadata service", 500


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8081)
