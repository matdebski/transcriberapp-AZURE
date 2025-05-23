provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "transcriberapp-rg"
  location = "East Europe"
}

resource "azurerm_storage_account" "storage" {
  name                     = "transcribersa123"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "raw" {
  name                  = "raw"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "audio" {
  name                  = "audio"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "transcripts" {
  name                  = "transcripts"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_servicebus_namespace" "sb" {
  name                = "transcriberbus"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Basic"
}

resource "azurerm_servicebus_queue" "queue" {
  name                = "transcriberqueue"
  namespace_id        = azurerm_servicebus_namespace.sb.id
  max_delivery_count  = 10
  enable_partitioning = true
}
