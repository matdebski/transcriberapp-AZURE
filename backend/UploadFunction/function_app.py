import azure.functions as func
import json
import logging
import uuid
import os
from azure.storage.blob import BlobServiceClient
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
import asyncio

async def send_message(file_id):
    conn_str = os.environ["SERVICE_BUS_CONNECTION_STRING"]
    queue_name = os.environ["SERVICE_BUS_QUEUE_NAME"]

    servicebus_client = ServiceBusClient.from_connection_string(conn_str)
    async with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=queue_name)
        async with sender:
            msg = ServiceBusMessage(json.dumps({
                "file_id": file_id,
            }))
            await sender.send_messages(msg)




app = func.FunctionApp()

container_name = os.environ["INPUT_CONTAINER_NAME"]
account_name = os.environ["STORAGE_ACCOUNT_NAME"]
account_key = os.environ["STORAGE_ACCOUNT_KEY"]

connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={account_name};"
    f"AccountKey={account_key};"
    f"EndpointSuffix=core.windows.net"
)

#connection_string="AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

@app.function_name('UploadFunction')
@app.route(route="upload", auth_level=func.AuthLevel.ANONYMOUS)
def upload(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get("file")
        
        if not file:
            return func.HttpResponse(
                json.dumps({"error": "No file uploaded"}),
                status_code=400,
                mimetype="application/json"
            )

        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        allowed_extensions = [".wav", ".mp3", ".mp4", ".m4a", ".webm", ".ogg"]

        if ext not in allowed_extensions:
            return func.HttpResponse(
                json.dumps({"error": "Unsupported file type"}),
                status_code=400,
                mimetype="application/json"
            )

        file_id = str(uuid.uuid4()) + ext
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_id)
        blob_client.upload_blob(file.stream, metadata={"original_filename": filename})

        asyncio.run(send_message(file_id))
        
        return func.HttpResponse(
            json.dumps({"message": "Upload successful", "file_id": file_id}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception("Upload failed")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
