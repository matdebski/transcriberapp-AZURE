# Transcriber - Azure-Based Audio/Video Transcription App

A full-stack serverless application for transcribing audio files, using Azure Static Web Apps, Azure Functions, Azure Service Bus and Blob Storage.

## How the App Works

1. Users upload an audio file (e.g., `.wav`, `.mp3`).
2. The file is sent to an Azure Function (UploadFunction) and stored in Azure Blob Storage. 
The file is stored in Azure Blob Storage in the input container with file_id (UUID + file extension) as filename.
3. After successful upload, UploadFunction sends a message to Azure Service Bus Queue. The message contains file_id.
4. ProcessingFunction picks up the message, downloads the file from Blob Storage using file_id and triggers transcription using Azure Cognitive Services (Speech-to-Text).
5. The transcription result is stored as a text file {file_id}.txt in the output container of Azure Blob Storage.
6. Frontend checks Blob Storage if {file_id}.txt file exists, its content (transcription) is displayed to the user.


## Architecture Overview
![Architecture Diragram](https://github.com/user-attachments/assets/d431b60e-527a-431d-a9b2-710659258d20)



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
| Service Bus integration              | ✅ Completed| Messaging between functions works                                     |
| Processing function (transcription) | ✅ Completed| Speech-to-Text integrated                                              |
| Application Insights integration	✅ | Completed	| Logging for monitoring/debugging Azure Functions |
| GitHub Actions automation            | ✅ Completed  | Full CI/CD including function publish and env injection             |
| Github workflow Improvements  | ⏳ Planned    |   Workflow layout, Artifacts usage, Caching |
| Authentication and security layer                | ⏳ Planned    | For now endpoints are public                                          |
| More advanced UI                      | ⏳ Planned    | Current interface is minimal   |
| Video file support (ffmpeg)    | ❌ Removed  | Dropped from current scope for simplicity     |
