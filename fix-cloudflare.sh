#!/bin/bash
# Quick fix script for Cloudflare Pages deployment

echo "=========================================="
echo "Cloudflare Pages Deployment Fix"
echo "=========================================="
echo ""

# Check if project exists in Cloudflare
echo "Step 1: Verify project name in Cloudflare"
echo "Go to: https://dash.cloudflare.com"
echo "Click: Pages (left sidebar)"
echo "Look for: wilkesboro-today"
echo ""

# Check GitHub secrets
echo "Step 2: Check GitHub Secrets"
echo "Go to: https://github.com/pipeln/wilkesboro-today/settings/secrets/actions"
echo ""
echo "Required secrets:"
echo "  - CLOUDFLARE_API_TOKEN"
echo "  - CLOUDFLARE_ACCOUNT_ID"
echo "  - AITABLE_TOKEN"
echo ""

# Create proper API token instructions
echo "Step 3: Create Proper API Token"
echo ""
echo "In Cloudflare dashboard:"
echo "1. Click your profile (top right)"
echo "2. Select 'My Profile'"
echo "3. Click 'API Tokens' tab"
echo "4. Click 'Create Token'"
echo "5. Click 'Get started' (Custom token)"
echo ""
echo "Token Configuration:"
echo "  Name: GitHub Actions Deploy"
echo "  Permissions:"
echo "    - Zone: Read"
echo "    - Cloudflare Pages: Edit"
echo "    - Account: Read"
echo "  Resources:"
echo "    - Include: All zones"
echo "    - Include: All accounts"
echo ""
echo "6. Click 'Continue to summary'"
echo "7. Click 'Create Token'"
echo "8. COPY THE TOKEN IMMEDIATELY"
echo ""

# Get Account ID
echo "Step 4: Get Account ID"
echo "In Cloudflare dashboard:"
echo "1. Look at the right sidebar"
echo "2. Copy 'Account ID'"
echo ""

# Update GitHub secrets
echo "Step 5: Update GitHub Secrets"
echo "Go to: https://github.com/pipeln/wilkesboro-today/settings/secrets/actions"
echo ""
echo "Update these secrets:"
echo "  CLOUDFLARE_API_TOKEN = [paste new token]"
echo "  CLOUDFLARE_ACCOUNT_ID = [paste account ID]"
echo "  AITABLE_TOKEN = uskNPM9fPVHOgAGbDepyKER"
echo ""

# Re-run workflow
echo "Step 6: Re-run Failed Workflow"
echo "Go to: https://github.com/pipeln/wilkesboro-today/actions"
echo "Find failed workflow"
echo "Click 'Re-run jobs'"
echo ""

echo "=========================================="
echo "If still failing, try Global API Key:"
echo "=========================================="
echo "1. In Cloudflare: Profile > API Tokens"
echo "2. Scroll to 'Global API Key'"
echo "3. Click 'View' and enter password"
echo "4. Copy that key as CLOUDFLARE_API_TOKEN"
echo ""
