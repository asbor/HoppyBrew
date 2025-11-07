# Post-Merge Actions for DockerHub Publishing

This document outlines the steps needed after merging the DockerHub publishing PR.

## Quick Start (5 minutes)

### Step 1: Create DockerHub Access Token
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Name: `GitHub Actions - HoppyBrew`
4. Permissions: Read & Write (minimum)
5. Click "Generate" and **copy the token immediately**

### Step 2: Add GitHub Secrets
1. Go to https://github.com/asbor/HoppyBrew/settings/secrets/actions
2. Add two new secrets:
   - Name: `DOCKERHUB_USERNAME`, Value: Your DockerHub username
   - Name: `DOCKERHUB_TOKEN`, Value: The token from Step 1

### Step 3: Trigger First Build
Push to main branch or manually trigger the "Main Build & Deploy" workflow to test DockerHub publishing.

## What Happens Next

Once secrets are configured:

### Automatic Publishing on Main Branch
- Every push to `main` publishes to DockerHub with tags:
  - `latest`
  - `<commit-sha>` (e.g., `d2c4ea4`)

### Automatic Publishing on Releases
- Every release (e.g., `v1.0.0`) publishes with tags:
  - `v1.0.0` (full tag)
  - `1.0.0` (semantic version)
  - `1.0` (minor version)
  - `1` (major version)
  - `latest`

### Published Images
- `<your-username>/hoppybrew-backend:latest`
- `<your-username>/hoppybrew-frontend:latest`

## Updating README

After setting up, update the README to replace `<dockerhub_username>` with your actual DockerHub username in:
- Docker Deployment section (line ~260)
- Docker Compose examples

## Verification

Check DockerHub for published images:
1. Visit https://hub.docker.com/u/<your-username>/
2. Look for `hoppybrew-backend` and `hoppybrew-frontend` repositories
3. Verify tags are present

## Troubleshooting

### Images Not Publishing
- Check workflow logs in GitHub Actions
- Verify secrets are set correctly (case-sensitive)
- Ensure token has write permissions

### Authentication Failed
- Regenerate DockerHub token
- Update `DOCKERHUB_TOKEN` secret in GitHub

## Documentation

Full setup guide: `documents/DOCKERHUB_SETUP.md`

## Support

If issues arise, check:
1. GitHub Actions workflow logs
2. DockerHub activity logs
3. Secret configuration in GitHub settings
