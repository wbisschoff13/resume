# OpenTofu Configuration

This directory contains OpenTofu configuration for deploying the website to Cloudflare Pages with DNS management.

**What is OpenTofu?**

OpenTofu is a community-driven fork of Terraform that is open-source, programmable, and extensible. It is a drop-in replacement for Terraform - all commands and configurations work identically. We use OpenTofu for its open governance and commitment to community needs.

## Prerequisites

1. **Cloudflare R2 Bucket**: Create a bucket named `terraform-state` in Cloudflare R2 for remote state storage
2. **Cloudflare API Token**: Create an API token with permissions:
   - Account - Cloudflare Pages - Edit
   - Zone - DNS - Edit
   - Account - Account Settings - Read (for R2)
3. **R2 Access Keys**: Create AWS-compatible API tokens for R2 access:
   - Go to Cloudflare Dashboard > R2 > Manage R2 API Tokens
   - Create API token (these are AWS-compatible access keys)
   - Save the Access Key ID and Secret Access Key

## Setup

### 1. Configure Environment Variables

Copy the example variables file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your domain and repository configuration.

### 2. Configure Environment Variables

You need to configure credentials for both Cloudflare resources and R2 backend:

**Cloudflare Credentials** (for managing resources):

```bash
# Add to terraform/.env
export TF_VAR_cloudflare_api_token="your_cloudflare_api_token"
export TF_VAR_cloudflare_account_id="your_cloudflare_account_id"
```

**R2 Access Keys** (for OpenTofu state backend):

```bash
# Create terraform/.env
# Copy from .env.r2 and add your R2 access keys
export AWS_ACCESS_KEY_ID="your_r2_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_r2_secret_access_key"
```

**Source both files:**

```bash
source terraform/.env.cloudflare
source terraform/.env
```

### 3. Initialize OpenTofu Backend

Initialize the R2 remote state backend:

```bash
source .env && tofu init \
  -backend-config="endpoints.s3=https://${TF_VAR_cloudflare_account_id}.r2.cloudflarestorage.com"
```

This configures OpenTofu to store state in Cloudflare R2.

### 4. Validate Configuration

```bash
tofu validate
```

## Usage

### Plan Changes

```bash
source .env && tofu plan
```

### Apply Changes

```bash
source .env && tofu apply
```

### Import Existing Resources

If you have existing Cloudflare resources:

```bash
tofu import cloudflare_pages_project.website <account_id>/<project_name>
```

## State Management

- **Backend**: Cloudflare R2 (S3-compatible)
- **State File**: `terraform-state/website/terraform.tfstate`
- **Locking**: Automatic state locking via R2

## Outputs

After applying, OpenTofu outputs:

- `pages_project_name` - Name of the Cloudflare Pages project
- `pages_project_url` - Default Cloudflare Pages URL
- `root_domain` - Root domain name
- `subdomain` - Full subdomain
- `production_branch` - Git branch for production
- `github_repo` - GitHub repository URL

## Security

- **Never commit** `terraform.tfvars` with real credentials
- **Never commit** `.env` file (already in .gitignore)
- **Never commit** `*.tfstate` files (already in .gitignore)
- API tokens and account IDs should be kept secure

## Migration from Portfolio App

This configuration improves upon the portfolio app's Terraform setup:

1. **Remote State**: Uses Cloudflare R2 instead of local backend
2. **Team Collaboration**: State locking and remote storage enable multiple runners
3. **Better Security**: State not stored in Git repository

## Troubleshooting

### Backend Initialization Fails

Ensure:

1. R2 bucket `terraform-state` exists
2. `.env` file is sourced: `source .env`
3. Account ID is correct (visible in Cloudflare dashboard URL)

### Provider Authentication Fails

Ensure:

1. API token has required permissions
2. API token is not expired
3. `TF_VAR_cloudflare_api_token` is set in `.env`

### DNS Records Not Propagating

- DNS changes can take up to 24 hours
- Use `dig` or `nslookup` to verify: `dig werner.bisschoff.dev`
- Check Cloudflare dashboard for DNS record status
