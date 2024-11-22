from flask import jsonify, send_file
import os
import tempfile
import json
from bson import ObjectId
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
import subprocess
import pika
from PyPDF2 import PdfReader, PdfWriter


def convert_docx_to_pdf(input_path):
    """
    Converts a DOCX file to PDF using LibreOffice in headless mode.
    """
    try:
        output_path = os.path.splitext(input_path)[0] + ".pdf"
        command = [
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", os.path.dirname(input_path),
            input_path
        ]
        print("process running")
        subprocess.run(command, check=True)
        print("process khtm")
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Conversion failed: {e}")


def convert(message, fs_docx, fs_pdf, channel):
    """
    Handles the DOCX to PDF conversion process.
    
    - Retrieves the DOCX file from GridFS.
    - Converts it to PDF using `libreoffice`.
    - Stores the PDF back in GridFS.
    - Sends a confirmation message via RabbitMQ.

    Args:
        message (str): The RabbitMQ message in JSON format.
        fs_docx (GridFS): The GridFS instance for DOCX files.
        fs_pdf (GridFS): The GridFS instance for PDF files.
        channel (BlockingChannel): The RabbitMQ channel.

    Returns:
        Response: JSON response or an error message.
    """
    try:
        # Parse the message from RabbitMQ
        message = json.loads(message.decode('utf-8'))
        print("message",message)

        # Fetch the DOCX file from GridFS using the provided file ID
        docx_fid = message.get("docx_fid")
        print(f"docx_fid:{docx_fid}")
        if not docx_fid:
            return jsonify({"error": "DOCX file ID is missing in the message"}), 400

        # Retrieve the file from GridFS
        docx_file = fs_docx.get(ObjectId(docx_fid))

        print(f"docx_fid2:{docx_fid}")

        # Create a temporary file for the DOCX file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx_file:
            temp_docx_file.write(docx_file.read())
            temp_docx_path = temp_docx_file.name
        print(f"docx_fid3:{docx_fid}")

        # Convert the DOCX file to PDF
        with ThreadPoolExecutor() as executor:
            temp_pdf_path = executor.submit(convert_docx_to_pdf, temp_docx_path).result()
        print(f"docx_fid4:{docx_fid}")

        # Store the converted PDF back into GridFS
        with open(temp_pdf_path, 'rb') as pdf_file:
            pdf_fid = fs_pdf.put(pdf_file, filename=os.path.basename(temp_pdf_path))
        print(f"docx_fid5:{docx_fid}")

        # Send confirmation via RabbitMQ
        confirmation_message = json.dumps({
            "status": "success",
            "docx_fid": docx_fid,
            "pdf_fid": str(pdf_fid),
            "username":message.get("email")
        })
        print(f"docx_fid6:{docx_fid}")

        channel.basic_publish(
            exchange='', 
            routing_key=os.environ.get("PDF_QUEUE"), 
            body=confirmation_message, 
            properties = pika.BasicProperties(
            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            ))

        # Clean up temporary files
        print(f"docx_fid7:{docx_fid}")

        os.remove(temp_docx_path)
        os.remove(temp_pdf_path)

        # return jsonify({"message": "Conversion successful", "pdf_fid": str(pdf_fid)}), 200
        print(f"Convert pdf_fid:{pdf_fid}")
        return (pdf_fid,None),200

    except Exception as err:
        # Return an error message for any exceptions
        print(f"Convert Exception:{err}")
        return (None,err), 500


def protect_pdf(input_pdf_path, password):
    """
    Protects the given PDF file with a password.
    """
    try:
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Add password protection
        writer.encrypt(password)

        # Save the password-protected PDF
        protected_pdf_path = os.path.splitext(input_pdf_path)[0] + "_protected.pdf"
        with open(protected_pdf_path, "wb") as protected_pdf_file:
            writer.write(protected_pdf_file)

        return protected_pdf_path
    except Exception as e:
        raise Exception(f"Failed to protect PDF: {e}")


def convert_with_password_protection(message, fs_docx, fs_pdf, channel):
    """
    Handles the DOCX to password-protected PDF conversion process.

    - Retrieves the DOCX file from GridFS.
    - Converts it to PDF using `libreoffice`.
    - Protects the PDF with a password.
    - Stores the protected PDF back in GridFS.
    - Sends a confirmation message via RabbitMQ.

    Args:
        message (str): The RabbitMQ message in JSON format.
        fs_docx (GridFS): The GridFS instance for DOCX files.
        fs_pdf (GridFS): The GridFS instance for PDF files.
        channel (BlockingChannel): The RabbitMQ channel.

    Returns:
        Response: JSON response or an error message.
    """
    try:
        # Parse the message from RabbitMQ
        message = json.loads(message.decode('utf-8'))

        # Fetch the DOCX file ID and password
        docx_fid = message.get("docx_fid")
        password = message.get("password")

        if not docx_fid:
            return jsonify({"error": "DOCX file ID is missing in the message"}), 400
        if not password:
            return jsonify({"error": "Password is missing in the message"}), 400

        # Retrieve the file from GridFS
        docx_file = fs_docx.get(ObjectId(docx_fid))

        # Create a temporary file for the DOCX file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx_file:
            temp_docx_file.write(docx_file.read())
            temp_docx_path = temp_docx_file.name

        # Convert the DOCX file to PDF
        with ThreadPoolExecutor() as executor:
            temp_pdf_path = executor.submit(convert_docx_to_pdf, temp_docx_path).result()

        # Protect the PDF with a password
        protected_pdf_path = protect_pdf(temp_pdf_path, password)

        # Store the password-protected PDF back into GridFS
        with open(protected_pdf_path, 'rb') as protected_pdf_file:
            pdf_fid = fs_pdf.put(protected_pdf_file, filename=os.path.basename(protected_pdf_path))

        # Send confirmation via RabbitMQ
        confirmation_message = json.dumps({
            "status": "success",
            "docx_fid": docx_fid,
            "pdf_fid": str(pdf_fid),
            "username":message.get("email")

        })
        channel.basic_publish(
            exchange='', 
            routing_key=os.environ.get("PDF_QUEUE"), 
            body=confirmation_message, 
            properties = pika.BasicProperties(
            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            ))

        # Clean up temporary files
        os.remove(temp_docx_path)
        os.remove(temp_pdf_path)
        os.remove(protected_pdf_path)

        return (pdf_fid,None),200

    except Exception as e:
        # Return an error message for any exceptions
        return (None,e), 500
