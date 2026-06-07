# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "pages_project_name" {
  description = "Name of the Cloudflare Pages project"
  value       = cloudflare_pages_project.website.name
}

output "pages_project_url" {
  description = "Default Cloudflare Pages URL for the project"
  value       = "https://${cloudflare_pages_project.website.name}.pages.dev"
}

output "root_domain" {
  description = "Root domain name"
  value       = var.domain_name
}

output "subdomain" {
  description = "Full subdomain"
  value       = "${var.subdomain_name}.${var.domain_name}"
}

output "production_branch" {
  description = "Git branch deployed for production"
  value       = var.production_branch
}

output "github_repo" {
  description = "GitHub repository URL"
  value       = "https://github.com/${var.repo_owner}/${var.repo_name}"
}
