resource "azurerm_app_service_plan" "functions" {
  name                = "transcriberapp-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "FunctionApp"
  reserved            = true  # Linux

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}