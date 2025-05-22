provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "transcriberapp-rg"
  location = "East Europe"
}

resource "azurerm_storage_account" "storage" {
  name                     = "transcriberstorage1"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
