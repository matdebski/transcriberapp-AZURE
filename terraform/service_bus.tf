resource "azurerm_servicebus_namespace" "sb" {
  name                = "sb-${var.project_name}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Basic"
}

resource "azurerm_servicebus_queue" "transcribe_queue" {
  name                = "queue-${var.project_name}"
  namespace_id        = azurerm_servicebus_namespace.sb.id

  depends_on = [
    azurerm_servicebus_namespace.sb
  ]
}