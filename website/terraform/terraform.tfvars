# -----------------------------------------------------------------------------
# Terraform Variables
# -----------------------------------------------------------------------------
# Non-sensitive variables for the website Terraform configuration
#
# Sensitive variables (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID) should be
# set via environment variables for security:
#
#   export CLOUDFLARE_API_TOKEN="your_api_token_here"
#   export CLOUDFLARE_ACCOUNT_ID="your_account_id_here"
#
# To persist these variables across sessions, add them to your shell profile
# (~/.zshrc, ~/.bashrc, etc.) or use a tool like direnvn.

# -----------------------------------------------------------------------------
# Domain Configuration
# -----------------------------------------------------------------------------

domain_name    = "bisschoff.dev"
subdomain_name = "werner"

# -----------------------------------------------------------------------------
# GitHub Repository Configuration
# -----------------------------------------------------------------------------

repo_owner        = "wbisschoff13"
repo_name         = "website"
production_branch = "main"

# -----------------------------------------------------------------------------
# Build Configuration
# -----------------------------------------------------------------------------

build_command   = "npm run build"
destination_dir = "dist"

# -----------------------------------------------------------------------------
# Sensitive Variables
# -----------------------------------------------------------------------------
# CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID are now sourced from .env
# Run: source .env before running terraform commands
