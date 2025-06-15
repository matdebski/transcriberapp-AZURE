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
