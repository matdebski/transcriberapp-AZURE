resource "azurerm_storage_account" "functions" {
  name                     = "transcriberfuncsa"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

#Function returns SAS token for Blob Storage
resource "azurerm_function_app" "upload" {
  name                       = "upload-function"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  storage_account_name       = azurerm_storage_account.functions.name
  storage_account_access_key = azurerm_storage_account.functions.primary_access_key
  os_type                    = "linux"
  runtime_stack              = "python"
  version                    = "4"
}


resource "azurerm_function_app" "preprocess" {
  name                       = "preprocess-function"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  storage_account_name       = azurerm_storage_account.functions.name
  storage_account_access_key = azurerm_storage_account.functions.primary_access_key
  os_type                    = "linux"
  runtime_stack              = "python"
  version                    = "4"
}


resource "azurerm_function_app" "transcribe" {
  name                       = "transcribe-function"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  storage_account_name       = azurerm_storage_account.functions.name
  storage_account_access_key = azurerm_storage_account.functions.primary_access_key
  os_type                    = "linux"
  runtime_stack              = "python"
  version                    = "4"
}