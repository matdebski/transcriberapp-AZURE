import logging
import azure.functions as func
import uuid
from azure.storage.blob import BlobServiceClient
import os

connect_str = os.environ["AzureWebJobsStorage"]
blob_container = os.environ["UPLOAD_CONTAINER"]

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get("file")
        if not file:
            return func.HttpResponse("No file uploaded", status_code=400)

        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()

        if not ext or ext not in [".wav", ".mp3", ".mp4", ".m4a", ".webm", ".ogg"]:
            return func.HttpResponse("Invalid file type. Only audio/video formats are allowed.", status_code=400)

        file_id = str(uuid.uuid4()) + ext

        blob_client = blob_service_client.get_blob_client(container=blob_container, blob=file_id)
        blob_client.upload_blob(file.stream)

        return func.HttpResponse(f"Uploaded {file_id}", status_code=200)

    except Exception as e:
        logging.exception("Upload failed")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
