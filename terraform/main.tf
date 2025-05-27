terraform {
//  cloud {
//    organization = "matdebski"
//    workspaces {
//      name = "transcriberapp-2"
//    }
// }

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
