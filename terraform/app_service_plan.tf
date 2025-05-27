resource "azurerm_service_plan" "functions" {
  name                = "transcriberapp-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "Y1"
  sku_tier            = "Dynamic"
}