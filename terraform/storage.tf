resource "azurerm_storage_account" "storage" {
  name                     = "storage0${var.project_name}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "input" {
  name                  = "input-${var.project_name}"
  storage_account_id  = azurerm_storage_account.storage.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "output" {
  name                  = "output-${var.project_name}"
  storage_account_id  = azurerm_storage_account.storage.id
  container_access_type = "blob"
    cors_rule {
    allowed_origins    = ["*.azurestaticapps.net"]
    allowed_methods    = ["GET"]
    allowed_headers    = ["*"]
    exposed_headers    = ["*"]
    max_age_in_seconds = 3600
  }
}