terraform {
  cloud {
    organization = "matdebski"
    workspaces {
      name = "transcriberapp-2"
    }
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.29.0"
    }
  }
}
provider "azurerm" {
  features {}
  use_oidc = true
}

resource "azurerm_resource_group" "rg" {
  name     = "transcriberapp-rg"
  location = "polandcentral"
}

resource "azurerm_storage_account" "storage" {
  name                     = "transcriberstorage1"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

