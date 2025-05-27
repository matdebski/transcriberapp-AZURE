resource "azurerm_storage_account" "functions_storage" {
  name                     = "transcriberfunct"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_function_app" "upload_function" {
  name                       = "upload-function"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  storage_account_name       = azurerm_storage_account.functions_storage.name
  storage_account_access_key = azurerm_storage_account.functions_storage.primary_access_key
  app_service_plan_id        = azurerm_app_service_plan.functions.id

  os_type        = "linux"
  version        = "~4"
  runtime_stack  = "python"
  functions_extension_version = "~4"

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }
}