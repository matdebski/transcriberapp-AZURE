import logging
import os
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient

container_name = os.environ["INPUT_CONTAINER_NAME"]
account_name = os.environ["STORAGE_ACCOUNT_NAME"]
account_key = os.environ["STORAGE_ACCOUNT_KEY"]


connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={account_name};"
    f"AccountKey={account_key};"
    f"EndpointSuffix=core.windows.net"
)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

app = func.FunctionApp()

@app.function_name(name="ProcessMessage")
@app.service_bus_queue_trigger(arg_name="msg", queue_name="%SERVICE_BUS_QUEUE_NAME%", connection="SERVICE_BUS_CONNECTION_STRING")
def process_message(msg: func.ServiceBusMessage):
    try:
        body = msg.get_body().decode("utf-8")
        data = json.loads(body)
        file_id = data["file_id"]

        logging.info(f"Processing file: {file_id}")

        # Pobieranie pliku z blob storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_id)
        stream = blob_client.download_blob().readall()

        logging.info(f"File {file_id} size: {len(stream)} bytes")

    except Exception as e:
        logging.exception("Processing failed")
