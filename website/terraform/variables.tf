# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

variable "cloudflare_api_token" {
  description = "Cloudflare API token with appropriate permissions"
  type        = string
  sensitive   = true

  # Set via environment variable: CLOUDFLARE_API_TOKEN
  # Never commit actual token values to git
}

variable "cloudflare_account_id" {
  description = "Cloudflare Account ID"
  type        = string

  # Set via environment variable: CLOUDFLARE_ACCOUNT_ID
  # Found in Cloudflare dashboard: URL path or right sidebar
}

variable "domain_name" {
  description = "Root domain name (e.g., bisschoff.dev)"
  type        = string
  default     = "bisschoff.dev"

  validation {
    condition     = can(regex("^[a-z0-9.-]+\\.[a-z]{2,}$", var.domain_name))
    error_message = "The domain_name must be a valid domain name (e.g., 'example.com')."
  }
}

variable "subdomain_name" {
  description = "Subdomain for website (e.g., werner for werner.bisschoff.dev)"
  type        = string
  default     = "werner"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.subdomain_name))
    error_message = "The subdomain_name must contain only lowercase letters, numbers, and hyphens."
  }
}

variable "repo_owner" {
  description = "GitHub repository owner (username or organization)"
  type        = string
  default     = "wbisschoff13"
}

variable "repo_name" {
  description = "GitHub repository name"
  type        = string
  default     = "website"
}

variable "production_branch" {
  description = "Git branch to deploy for production"
  type        = string
  default     = "main"
}

variable "build_command" {
  description = "Build command for Cloudflare Pages"
  type        = string
  default     = "npm run build"
}

variable "destination_dir" {
  description = "Directory containing built files"
  type        = string
  default     = "dist"
}
