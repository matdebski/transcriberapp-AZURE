import logging
import azure.functions as func
import uuid
import os
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage

connect_str = os.environ["AzureWebJobsStorage"]
queue_name = os.environ["QUEUE_NAME"]
blob_container = os.environ["UPLOAD_CONTAINER"]

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
servicebus_client = ServiceBusClient.from_connection_string(connect_str)

app = func.FunctionApp()

@app.route(route="upload", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def upload(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get("file")
        if not file:
            return func.HttpResponse("No file uploaded", status_code=400)

        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()

        if ext not in {".wav", ".mp3", ".mp4", ".m4a", ".webm", ".ogg"}:
            return func.HttpResponse("Invalid file extension", status_code=400)

        file_id = str(uuid.uuid4()) + ext

        blob_client = blob_service_client.get_blob_client(container=blob_container, blob=file_id)
        blob_client.upload_blob(file.stream)

        with servicebus_client:
            sender = servicebus_client.get_queue_sender(queue_name=queue_name)
            with sender:
                sender.send_messages(ServiceBusMessage(file_id))

        return func.HttpResponse(f"Uploaded and queued: {file_id}", status_code=200)

    except Exception as e:
        logging.exception("Upload failed")
        return func.HttpResponse("Internal server error", status_code=500)
