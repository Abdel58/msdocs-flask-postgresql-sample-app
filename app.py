from flask import Flask, request, send_file
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file, overwrite=True)
        return f"File '{file.filename}' uploaded successfully!"
    return "No file selected", 400
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        blob_client = container_client.get_blob_client(filename)
        blob_data = blob_client.download_blob()
        return send_file(
            blob_data.readall(),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return f"Error downloading the file: {str(e)}", 404
