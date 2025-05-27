resource "azurerm_cognitive_account" "cognitive" {
  name                = "az-cognitive-${var.project_name}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "SpeechServices"
  sku_name            = "S0"
}
