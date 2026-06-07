# -----------------------------------------------------------------------------
# Cloudflare Pages Project for Website
# -----------------------------------------------------------------------------

# Resource: Cloudflare Pages project for website
resource "cloudflare_pages_project" "website" {
  account_id        = var.cloudflare_account_id
  name              = "${replace(var.domain_name, ".", "-")}-website"
  production_branch = var.production_branch

  source {
    type = "github"

    # GitHub repository configuration
    config {
      owner                      = var.repo_owner
      repo_name                  = var.repo_name
      production_branch          = var.production_branch
      pr_comments_enabled        = true
      deployments_enabled        = true   # Manual deployment via terraform only
      preview_deployment_setting = "none" # Disable preview deployments
    }
  }

  build_config {
    build_command   = var.build_command
    destination_dir = var.destination_dir
    root_dir        = "/"
    build_caching   = true
  }

  # Note: Environment variables can be added via Cloudflare dashboard or API
  # The provider doesn't support environment_variables in build_config block
  # Use Cloudflare dashboard for: NODE_VERSION, etc.
}

# -----------------------------------------------------------------------------
# Note: DNS records and custom domains are managed in dns.tf
# -----------------------------------------------------------------------------
# DNS configuration has been separated to dns.tf for better organization
# This includes the zone data source and all DNS records for both domains
