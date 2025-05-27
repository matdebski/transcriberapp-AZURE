output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "upload_container_url" {
  value = azurerm_storage_account.storage.primary_blob_endpoint
}