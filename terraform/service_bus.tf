resource "azurerm_servicebus_namespace" "sb" {
  name                = "transcribersb"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Basic"
}

resource "azurerm_servicebus_queue" "upload" {
  name                = "upload"
  namespace_name      = azurerm_servicebus_namespace.sb.name
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_servicebus_queue" "preprocess" {
  name                = "preprocess"
  namespace_name      = azurerm_servicebus_namespace.sb.name
  resource_group_name = azurerm_resource_group.rg.name
}