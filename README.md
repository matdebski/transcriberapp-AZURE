# Transcriber - Azure-Based Audio/Video Transcription App

A full-stack serverless application for transcribing audio/video files, using Azure Static Web Apps, Azure Functions, and Blob Storage.

## How the App Works

1. Users upload an audio/video file (e.g., `.wav`, `.mp3`, `.mp4`).
2. The file is sent to an Azure Function (`upload_function`) and stored in Azure Blob Storage.
3. An Azure Service Bus queue is notified about the new file.
4. A background Function picks up the message and triggers transcription using Azure Cognitive Services (Speech-to-Text).
5. The transcribed text is saved in Blob Storage.
6. Users can view/download the transcript through the frontend.


## Architecture Overview

![image](https://github.com/user-attachments/assets/b90cbb1c-c4ea-422f-ac47-7296a9de265c)

## Tech Stack

| Layer        | Technology                           |
|--------------|---------------------------------------|
| Frontend     | React HTML/CSS                        |
| Backend      | Azure Functions (Python)              |
| Transcription| Azure Cognitive Services – Speech API |
| Messaging    | Azure Service Bus                     |
| Storage      | Azure Blob Storage                    |
| Deployment   | Terraform + GitHub Actions            |
| Auth         | Azure OIDC via `azure/login@v1`       |

##  Project Progress Tracker

| Feature / Task                         | Status       | Comment                                                                |
|----------------------------------------|--------------|----------------------------------------------------------------------|
| Infrastructure via Terraform         | ✅ Completed  | Frontend, Azure Functions, Storage, Service Bus all provisioned     |
| Frontend build & deploy (React)      | ✅ Completed  | Hosted on Azure Static Web Apps                                     |
| Upload endpoint                      | ✅ Completed  | Working with real files, checks extensions                          |
| Blob Storage integration             | ✅ Completed  | Files stored successfully                                           |
| GitHub Actions automation            | ✅ Completed  | Full CI/CD including function publish and env injection             |
| Processing function (transcription) | 🟡 In progress| Function exists, needs reliable cognitive integration                |
| Transcript preview in UI            | ⏳ Planned    | Not yet displayed to user                                             |
| Authentication layer                | ⏳ Planned    | Current endpoints are public                                          |
