# DockerHub Publishing Setup Guide

This guide explains how to set up DockerHub credentials for automated Docker image publishing in the HoppyBrew repository.

## Overview

HoppyBrew uses GitHub Actions to automatically build and publish Docker images to:
1. **GitHub Container Registry (GHCR)** - Automatically configured via GitHub tokens
2. **DockerHub** - Requires manual setup of credentials

## Why DockerHub?

- **Unraid Compatibility**: Unraid Community Applications primarily use DockerHub
- **Public Accessibility**: Easier for users to pull images without authentication
- **Wide Adoption**: Most self-hosted solutions expect DockerHub images

## Setting Up DockerHub Publishing

### Step 1: Create a DockerHub Account

1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for a free account or log in
3. Note your username (you'll need this later)

### Step 2: Create a DockerHub Access Token

1. Log in to DockerHub
2. Click on your username in the top-right corner
3. Select **Account Settings**
4. Go to **Security** tab
5. Click **New Access Token**
6. Set the following:
   - **Access Token Description**: `GitHub Actions - HoppyBrew`
   - **Access permissions**: `Read, Write, Delete` (or `Read & Write` minimum)
7. Click **Generate**
8. **IMPORTANT**: Copy the access token immediately - you won't be able to see it again!

### Step 3: Add Secrets to GitHub Repository

1. Go to your GitHub repository (`asbor/HoppyBrew`)
2. Click **Settings** tab
3. In the left sidebar, expand **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add the first secret:
   - **Name**: `DOCKERHUB_USERNAME`
   - **Secret**: Your DockerHub username (e.g., `asbor` or your DockerHub username)
   - Click **Add secret**
6. Add the second secret:
   - **Name**: `DOCKERHUB_TOKEN`
   - **Secret**: The access token you copied in Step 2
   - Click **Add secret**

### Step 4: Verify Setup

Once the secrets are added, the workflows will automatically start publishing to DockerHub when:
- Code is pushed to the `main` branch
- A new tag is created (for releases)

You can verify the setup by:
1. Triggering a workflow manually via the Actions tab
2. Pushing to main branch
3. Checking DockerHub for new images at: `https://hub.docker.com/u/<your-username>/`

## Published Images

After setup, the following images will be published to DockerHub:

### Backend Service
- `<your-username>/hoppybrew-backend:latest` - Latest from main branch
- `<your-username>/hoppybrew-backend:<sha>` - Specific commit
- `<your-username>/hoppybrew-backend:v1.0.0` - Version releases

### Frontend Service
- `<your-username>/hoppybrew-frontend:latest` - Latest from main branch
- `<your-username>/hoppybrew-frontend:<sha>` - Specific commit
- `<your-username>/hoppybrew-frontend:v1.0.0` - Version releases

## Image Tagging Strategy

| Tag Format | Example | Description | When Created |
|------------|---------|-------------|--------------|
| `latest` | `latest` | Latest stable from main | Every main branch push |
| `<sha>` | `d0de8ad` | Specific commit | Every main branch push |
| `<branch>` | `develop` | Branch name | Every branch push |
| `v<version>` | `v1.0.0` | Full tag name | On release/tag creation |
| `<version>` | `1.0.0` | Semantic version | On semver release |
| `<major>.<minor>` | `1.0` | Minor version | On semver release |
| `<major>` | `1` | Major version | On semver release |

## Workflows That Publish to DockerHub

### 1. Main Build & Deploy (`.github/workflows/main-build-deploy.yml`)
- **Trigger**: Push to `main` branch
- **Images**: Tagged with `latest` and commit SHA
- **Purpose**: Deploy latest stable code

### 2. Docker Build (`.github/workflows/docker-build.yml`)
- **Trigger**: Push to `main`, `develop`, or `release/**` branches
- **Images**: Tagged with branch name, tag name, or SHA
- **Purpose**: Build and test Docker images

### 3. Release Automation (`.github/workflows/release.yml`)
- **Trigger**: Creating a release or pushing a version tag (e.g., `v1.0.0`)
- **Images**: Tagged with version numbers (semver)
- **Purpose**: Publish versioned releases

## Troubleshooting

### Images Not Appearing on DockerHub

1. **Check Secrets**: Ensure `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` are set correctly
2. **Check Workflow Logs**: Go to Actions tab and review the workflow run logs
3. **Verify Token Permissions**: Ensure the token has write permissions
4. **Check Token Expiry**: DockerHub tokens can expire; create a new one if needed

### Authentication Errors

If you see "unauthorized" errors in workflow logs:
1. Verify the token is still valid in DockerHub
2. Regenerate the token and update the GitHub secret
3. Ensure the username matches exactly (case-sensitive)

### Wrong Image Names

The image naming convention is:
- DockerHub: `<username>/hoppybrew-<service>:<tag>`
- GHCR: `ghcr.io/<owner>/<repo>-<service>:<tag>`

Make sure your DockerHub username is set correctly in the `DOCKERHUB_USERNAME` secret.

## Security Best Practices

1. **Use Access Tokens**: Never use your DockerHub password in secrets
2. **Minimal Permissions**: Create tokens with only the permissions needed
3. **Rotate Tokens**: Periodically rotate access tokens for security
4. **Monitor Usage**: Check DockerHub for unexpected pulls or pushes
5. **Separate Tokens**: Use different tokens for different projects

## Updating Documentation for Users

After setup, update the README to include your actual DockerHub username. Replace `<dockerhub_username>` with your actual username in:
- README.md Docker Deployment section
- Any Unraid templates
- User documentation

Example:
```yaml
services:
  backend:
    image: <your-username>/hoppybrew-backend:latest  # Replace with your DockerHub username
```

## Additional Resources

- [DockerHub Access Tokens Documentation](https://docs.docker.com/docker-hub/access-tokens/)
- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
