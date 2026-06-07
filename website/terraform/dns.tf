# -----------------------------------------------------------------------------
# DNS Configuration
# -----------------------------------------------------------------------------
# Manages DNS records for the website via Cloudflare
# Records point to Cloudflare Pages for global CDN and SSL termination

# -----------------------------------------------------------------------------
# Look up Cloudflare Zone
# -----------------------------------------------------------------------------
# Looks up the existing Cloudflare zone by domain name
# Simpler than requiring zone_id - user only needs to provide domain name

data "cloudflare_zone" "main_zone" {
  name = var.domain_name
}

# -----------------------------------------------------------------------------
# CNAME Record: werner -> Cloudflare Pages
# -----------------------------------------------------------------------------
# Creates werner.bisschoff.dev subdomain for website
# Enables global CDN, DDoS protection, and automatic SSL via Cloudflare proxy

resource "cloudflare_record" "werner_subdomain" {
  zone_id = data.cloudflare_zone.main_zone.id
  name    = var.subdomain_name
  content = cloudflare_pages_project.website.subdomain
  type    = "CNAME"
  ttl     = 1    # Auto TTL when proxied
  proxied = true # Enable Cloudflare proxy (CDN, caching, SSL)

  # Allow Terraform to manage this record even if manually modified
  allow_overwrite = true
}

# -----------------------------------------------------------------------------
# Custom Domain Binding: werner.bisschoff.dev -> Cloudflare Pages Project
# -----------------------------------------------------------------------------
# Binds the custom domain to the Cloudflare Pages project
# This is REQUIRED for Cloudflare Pages to accept traffic for the custom domain
# Without this, DNS alone will cause 522 errors (connection timeout)
#
# Cloudflare Pages needs to:
# 1. Know about the custom domain (this resource)
# 2. Provision SSL certificate for the domain (automatic after binding)
# 3. Route incoming requests to the correct Pages project

resource "cloudflare_pages_domain" "werner_subdomain" {
  account_id   = var.cloudflare_account_id
  project_name = cloudflare_pages_project.website.name
  domain       = "${var.subdomain_name}.${var.domain_name}"

  # IMPORTANT: Ensure DNS record exists before binding domain
  # This prevents the need for manual "recheck" in Cloudflare dashboard
  depends_on = [
    cloudflare_record.werner_subdomain
  ]
}

# -----------------------------------------------------------------------------
# CNAME Record: Root Domain -> Cloudflare Pages
# -----------------------------------------------------------------------------
# Creates bisschoff.dev pointing to Cloudflare Pages
# Will redirect to werner.bisschoff.dev via public/_redirects file

resource "cloudflare_record" "root_domain" {
  zone_id = data.cloudflare_zone.main_zone.id
  name    = var.domain_name
  content = cloudflare_pages_project.website.subdomain
  type    = "CNAME"
  ttl     = 1    # Auto TTL when proxied
  proxied = true # Enable Cloudflare proxy (CDN, caching, SSL)

  # Allow Terraform to manage this record even if manually modified
  allow_overwrite = true
}

# -----------------------------------------------------------------------------
# Custom Domain Binding: bisschoff.dev -> Cloudflare Pages Project
# -----------------------------------------------------------------------------
# Binds the root domain to the Cloudflare Pages project
# Redirects to werner.bisschoff.dev via public/_redirects file

resource "cloudflare_pages_domain" "root_domain" {
  account_id   = var.cloudflare_account_id
  project_name = cloudflare_pages_project.website.name
  domain       = var.domain_name

  # IMPORTANT: Ensure DNS record exists before binding domain
  depends_on = [
    cloudflare_record.root_domain
  ]
}

# -----------------------------------------------------------------------------
# Note on DNS Propagation
# -----------------------------------------------------------------------------
# After running `terraform apply`:
# 1. DNS records are created immediately
# 2. Custom domains are bound to the Pages project
# 3. SSL certificates are provisioned automatically (may take a few minutes)
# 4. Use `dig bisschoff.dev` or `dig werner.bisschoff.dev` to verify propagation
# 5. Check Cloudflare dashboard for SSL certificate status
