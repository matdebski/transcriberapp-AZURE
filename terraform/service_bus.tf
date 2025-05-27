resource "azurerm_servicebus_namespace" "sb" {
  name                = "transcriberapp-sb"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Basic"
}

resource "azurerm_servicebus_queue" "upload" {
  name         = "upload"
  namespace_id = azurerm_servicebus_namespace.sb.id
}

resource "azurerm_servicebus_queue" "preprocess" {
  name         = "preprocess"
  namespace_id = azurerm_servicebus_namespace.sb.id
}

resource "azurerm_servicebus_queue" "transcribe" {
  name         = "transcribe"
  namespace_id = azurerm_servicebus_namespace.sb.id
}