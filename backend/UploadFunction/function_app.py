import azure.functions as func
import datetime
import json
import logging

import uuid
import os
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

container_name = os.environ["INPUT_CONTAINER_NAME"] #"input-transcriber"
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
        body = req.get_body()
        content_type = req.headers.get('content-type', '')

        if not content_type.startswith("multipart/form-data"):
            return func.HttpResponse("Invalid content-type", status_code=400)

        file_id = str(uuid.uuid4()) + ".bin"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_id)
        blob_client.upload_blob(body)

        return func.HttpResponse(f"Uploaded as {file_id}", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"Upload error: {str(e)}", status_code=500)
