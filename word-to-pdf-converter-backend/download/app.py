from flask import Flask, request, send_file, jsonify
from pymongo import MongoClient
import gridfs
from io import BytesIO
from bson import ObjectId


app = Flask(__name__)

# MongoDB connection
client = MongoClient("host.minikube.internal", 27017)
db_pdf = client.pdf_files
db_conversions = client.pdf_conversions
fs_pdf = gridfs.GridFS(db_pdf)

@app.route('/get_pdf', methods=['GET'])
def get_pdf():
    try:
        # Get docx_fid from request arguments
        docx_fid = request.args.get('docx_fid')
        if not docx_fid:
            return jsonify({"error": "docx_fid is required"}), 400

        # Find corresponding pdf_id in pdf_conversions collection
        conversion_record = db_conversions.records.find_one({"docx_fid": docx_fid})
        if not conversion_record:
            return jsonify({"error": "No PDF found for the given docx_fid"}), 404

        pdf_id = conversion_record.get("pdf_fid")
        if not pdf_id:
            return jsonify({"error": "Invalid record: pdf_id missing"}), 500

        # Fetch the PDF from GridFS using pdf_id
        pdf_file = fs_pdf.get(ObjectId(pdf_id))
        if not pdf_file:
            return jsonify({"error": "PDF file not found in GridFS"}), 404

        # Send the file as a response
        pdf_stream = BytesIO(pdf_file.read())
        pdf_stream.seek(0)
        return send_file(
            pdf_stream,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{docx_fid}.pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
