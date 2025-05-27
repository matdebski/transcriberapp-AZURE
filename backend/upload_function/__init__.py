import os
import datetime
import azure.functions as func
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

connection_string = os.getenv("AzureWebJobsStorage")
storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME")

container_name = "input"


def main(req: func.HttpRequest) -> func.HttpResponse:
    filename = req.params.get('filename')
    if not filename:
        return func.HttpResponse("Missing filename", status_code=400)

    sas_token = generate_blob_sas(
        account_name=storage_account_name,
        container_name=container_name,
        blob_name=filename,
        account_key=os.getenv("STORAGE_ACCOUNT_KEY"),
        permission=BlobSasPermissions(write=True),
        expiry=datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    )

    url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{filename}?{sas_token}"
    return func.HttpResponse(url)