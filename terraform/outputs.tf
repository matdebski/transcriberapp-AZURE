output "resource_group" {
  value = azurerm_resource_group.rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "uploads_container_name" {
  value = azurerm_storage_container.input.name
}

output "transcripts_container_name" {
  value = azurerm_storage_container.output.name
}

output "servicebus_namespace" {
  value = azurerm_servicebus_namespace.sb.name
}

output "queue_name" {
  value = azurerm_servicebus_queue.transcribe_queue.name
}

output "upload_function_app_name" {
  value = azurerm_linux_function_app.upload_function.name
}

output "processing_function_app_name" {
  value = azurerm_linux_function_app.processing_function.name
}

output "cognitive_service_endpoint" {
  value = azurerm_cognitive_account.cognitive.endpoint
}

output "cognitive_service_key" {
  value     = azurerm_cognitive_account.cognitive.primary_access_key
  sensitive = true
}

output "frontend_url" {
  value = azurerm_static_web_app.frontend.default_host_name
}