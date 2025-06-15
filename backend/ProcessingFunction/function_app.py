import logging
import os
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import azure.cognitiveservices.speech as speechsdk


container_name = os.environ["INPUT_CONTAINER_NAME"]
output_container = os.environ["OUTPUT_CONTAINER_NAME"]
account_name = os.environ["STORAGE_ACCOUNT_NAME"]
account_key = os.environ["STORAGE_ACCOUNT_KEY"]


connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={account_name};"
    f"AccountKey={account_key};"
    f"EndpointSuffix=core.windows.net"
)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

speech_key = os.environ["SPEECH_KEY"]
service_region = os.environ["SPEECH_REGION"]


app = func.FunctionApp()

@app.function_name(name="ProcessMessage")
@app.service_bus_queue_trigger(arg_name="msg", queue_name="%SERVICE_BUS_QUEUE_NAME%", connection="SERVICE_BUS_CONNECTION_STRING")
def process_message(msg: func.ServiceBusMessage):
    try:
        body = msg.get_body().decode("utf-8")
        data = json.loads(body)
        file_id = data["file_id"]

        logging.info(f"Processing file: {file_id}")

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_id)
        stream = blob_client.download_blob().readall()

        logging.info(f"File {file_id} size: {len(stream)} bytes")

        temp_file = f"/tmp/{file_id}"
        with open(temp_file, "wb") as f:
            f.write(stream)

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_config = speechsdk.audio.AudioConfig(filename=temp_file)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = recognizer.recognize_once()
        transcription = result.text

        logging.info(f"Transcription for {file_id}: {transcription}")

        output_blob_client = blob_service_client.get_blob_client(container=output_container, blob=file_id)
        output_blob_client.upload_blob(transcription, overwrite=True)

        logging.info(f"Saved transcription for {file_id}")

    except Exception as e:
        logging.exception(f"Processing failed: {str(e)}")
