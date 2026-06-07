# Production Deployment Guide

This document provides step-by-step instructions for deploying the website to production on Cloudflare Pages.

## Prerequisites

Before deploying, ensure you have:

1. **Terraform configured** with Cloudflare credentials (see `terraform/README.md`)
2. **Domain ownership verified** for `bisschoff.dev` and `werner.bisschoff.dev`
3. **Google Analytics 4 Measurement ID** (optional, for analytics)
4. **Google Search Console** property created (recommended)

## Deployment Steps

### 1. Provision Infrastructure with Terraform

Navigate to the terraform directory and apply the configuration:

```bash
cd terraform

# Source environment variables with credentials
source .env

# Initialize Terraform (if not already done)
terraform init \
  -backend-config="endpoint=https://${TF_VAR_cloudflare_account_id}.r2.cloudflarestorage.com"

# Review the execution plan
terraform plan

# Apply the configuration
terraform apply
```

**What this creates:**

- Cloudflare Pages project (`bisschoff-dev-website`)
- DNS records for `werner.bisschoff.dev` (CNAME)
- Custom domain bindings
- SSL certificates (automatically provisioned)

**Note:** Confirm the plan with `yes` when prompted.

### 2. Build the Production Site

From the project root:

```bash
# Install dependencies (if not already done)
pnpm install

# Build the production site
pnpm run build
```

**Expected output:**

- Build completes in ~5-10 seconds
- Files generated in `dist/` directory
- Optimized assets (HTML, CSS, JS, images)
- Sitemap generated at `dist/sitemap-index.xml`

### 3. Deploy to Cloudflare Pages

You have two options for deployment:

#### Option A: Direct Upload (Recommended for Initial Deployment)

1. **Go to Cloudflare Dashboard**
   - Navigate to: https://dash.cloudflare.com/
   - Select your account
   - Go to Workers & Pages > `bisschoff-dev-website`

2. **Upload Build Artifacts**
   - Click "Create deployment" or "Upload assets"
   - Upload the entire `dist/` directory
   - Wait for deployment to complete (~1-2 minutes)

3. **Verify Deployment**
   - Check the deployment status in the dashboard
   - View the preview URL to confirm the site is working

#### Option B: Git Integration (For Future Deployments)

The Terraform config has GitHub integration disabled for manual deployments. To enable:

1. Update `terraform/main.tf`:

   ```hcl
   deployments_enabled = true  # Change from false
   ```

2. Re-run `terraform apply`

3. Push to main branch to trigger automatic deployment

### 4. Configure Custom Domains

After the first deployment:

1. **Verify Custom Domains**
   - In Cloudflare Pages dashboard, go to Custom Domains
   - Confirm `werner.bisschoff.dev` is listed
   - Check SSL certificate status (should be "Active")

2. **DNS Verification**
   - DNS records are already created by Terraform
   - Verify with: `dig werner.bisschoff.dev`
   - Should point to Cloudflare Pages

### 5. SSL Certificate Verification

Cloudflare automatically provisions SSL certificates:

1. **Check Certificate Status**
   - Cloudflare Dashboard > SSL/TLS
   - Verify encryption mode is "Full (strict)"
   - Check certificate status for custom domains

2. **Wait for Propagation**
   - SSL certificates may take 5-15 minutes to provision
   - Check certificate status in Cloudflare Pages dashboard

### 6. Final Verification

#### Domain Access Verification

```bash
# Check both domains respond with 200 OK
curl -I https://werner.bisschoff.dev
curl -I https://bisschoff.dev

# Verify SSL certificates
openssl s_client -connect werner.bisschoff.dev:443 -servername werner.bisschoff.dev
```

#### Browser Verification Checklist

- [ ] Site loads without SSL warnings
- [ ] All pages are accessible (Home, Work, Resume, Contact, Notes)
- [ ] Images load correctly
- [ ] Social links work (GitHub, LinkedIn)
- [ ] Resume PDF downloads correctly
- [ ] Navigation menu works on mobile
- [ ] Dark theme is applied correctly

#### SEO Verification

1. **Sitemap Access**
   - Navigate to: https://werner.bisschoff.dev/sitemap-index.xml
   - Verify XML sitemap is accessible

2. **Robots.txt**
   - Navigate to: https://werner.bisschoff.dev/robots.txt
   - Verify sitemap reference is present

3. **Structured Data**
   - View page source
   - Search for `application/ld+json`
   - Verify Person schema is present

4. **Open Graph Tags**
   - Use Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
   - Enter your URL to verify social sharing tags

5. **Twitter Card Validator**
   - Use: https://cards-dev.twitter.com/validator
   - Verify Twitter Card tags render correctly

#### Analytics Verification

If you've configured GA4:

1. **Real-Time Verification**
   - Navigate to your site
   - Open Google Analytics > Real-Time report
   - Verify you appear as an active user

2. **DebugView**
   - Enable debug mode in GA4
   - Verify events are being tracked

#### Search Console Verification

1. **Verify Ownership**
   - Go to Google Search Console
   - Add property: `https://werner.bisschoff.dev`
   - Verify using the meta tag (already in site)

2. **Submit Sitemap**
   - In Search Console, go to Sitemaps
   - Submit: `https://werner.bisschoff.dev/sitemap-index.xml`

3. **Request Indexing**
   - Use URL Inspection tool
   - Request indexing for main pages

## Post-Deployment Checklist

### Performance

- [ ] Run Lighthouse audit on production URLs
- [ ] Verify Core Web Vitals are green
- [ ] Check PageSpeed Insights scores

### Security

- [ ] SSL certificate is valid
- [ ] HTTPS redirects work correctly
- [ ] Security headers are present
- [ ] No mixed content warnings

### SEO

- [ ] Meta titles and descriptions are correct
- [ ] Canonical URLs point to production domain
- [ ] Sitemap is accessible and submitted
- [ ] robots.txt allows crawling
- [ ] Structured data is valid (use Rich Results Test)

### Analytics

- [ ] GA4 tracking is active
- [ ] Real-time users are visible
- [ ] Events are being recorded

## Monitoring and Maintenance

### Regular Tasks

**Weekly:**

- Check Google Analytics for traffic anomalies
- Verify site uptime

**Monthly:**

- Review Core Web Vitals in Search Console
- Check for broken links (use Search Console)
- Review security advisories for dependencies

**Quarterly:**

- Run full Lighthouse audits
- Update dependencies (`pnpm update`)
- Review and optimize performance

### Updating the Site

To update the site after the initial deployment:

1. Make your changes
2. Build locally: `pnpm run build`
3. Upload `dist/` to Cloudflare Pages (or push to main if Git integration is enabled)
4. Verify changes are live

## Rollback Procedure

If something goes wrong:

1. **Cloudflare Pages**
   - Go to Deployments in the dashboard
   - Find the previous working deployment
   - Click "Rollback" to revert

2. **DNS Issues**
   - DNS changes are managed by Terraform
   - Revert Terraform changes if needed: `terraform rollback`

## Troubleshooting

### Site Not Loading

1. Check Cloudflare Pages deployment status
2. Verify DNS records have propagated
3. Check SSL certificate status
4. Review Cloudflare dashboard for errors

### SSL Certificate Issues

1. Wait 15-30 minutes for provisioning
2. Check DNS records point to Cloudflare
3. Verify domain ownership in Cloudflare

### Analytics Not Working

1. Verify GA4 Measurement ID in `src/config.yaml`
2. Check browser console for errors
3. Ensure ad blockers are disabled for testing
4. Verify Partytown is forwarding `dataLayer.push`

### SEO Issues

1. Use Rich Results Test to verify structured data
2. Check robots.txt allows crawling
3. Verify sitemap is accessible
4. Submit to Search Console for indexing

## Resources

- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Terraform Cloudflare Provider](https://registry.terraform.io/providers/cloudflare/cloudflare/latest/docs)
- [Google Analytics 4](https://support.google.com/analytics/answer/10089681)
- [Google Search Console](https://search.google.com/search-console)
- [Astro Deployment Guide](https://docs.astro.build/en/guides/deploy/)

## Success Criteria

Deployment is successful when:

- ✅ Both domains load without SSL warnings
- ✅ All pages are accessible and functional
- ✅ SSL certificates are active
- ✅ Sitemap and robots.txt are accessible
- ✅ GA4 is tracking visitors (if configured)
- ✅ Search Console ownership is verified
- ✅ Lighthouse scores meet targets (Performance 90+, Accessibility 90+, SEO 100)

# Cloudflare Pages rebuild test
