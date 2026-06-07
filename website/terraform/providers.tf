# -----------------------------------------------------------------------------
# Provider Configuration
# -----------------------------------------------------------------------------
# Terraform configuration with Cloudflare R2 remote state backend
# State is stored remotely in Cloudflare R2 for durability and collaboration
# Requires: CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID environment variables

terraform {
  required_version = ">= 1.5.0, < 2.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

# -----------------------------------------------------------------------------
# Cloudflare Provider Configuration
# -----------------------------------------------------------------------------
# Authenticates with Cloudflare API for infrastructure management
# Required permissions:
#   - Account - Cloudflare Pages - Edit
#   - Zone - DNS - Edit
#   - Account - Account Settings - Read (for R2 state backend)
#
# API Token Creation: https://dash.cloudflare.com/profile/api-tokens
# Required scopes:
#   - Account - Cloudflare Pages - Edit
#   - Zone - DNS - Edit
#   - Zone - Zone - Read
#   - Account - Account Settings - Read (for R2)

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}
