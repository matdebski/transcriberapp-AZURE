resource "azurerm_service_plan" "function_plan" {
  name                = "service-plan-${var.project_name}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "upload_function" {
  name                = "upload-${var.project_name}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  service_plan_id            = azurerm_service_plan.function_plan.id

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    INPUT_CONTAINER_NAME  = azurerm_storage_container.input.name
    STORAGE_ACCOUNT_NAME  = azurerm_storage_account.storage.name
    STORAGE_ACCOUNT_KEY   = azurerm_storage_account.storage.primary_access_key
    WEBSITE_RUN_FROM_PACKAGE = "1"
  }

  depends_on = [
    azurerm_storage_account.storage,
    azurerm_service_plan.function_plan
  ]
}

resource "azurerm_linux_function_app" "processing_function" {
  name                = "processing-${var.project_name}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  service_plan_id            = azurerm_service_plan.function_plan.id

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  depends_on = [
  azurerm_storage_account.storage,
  azurerm_service_plan.function_plan,
  azurerm_servicebus_queue.transcribe_queue  
  ]
}

resource "azurerm_static_web_app" "frontend" {
  name                = "frontend-${var.project_name}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku_tier = "Free"
}
