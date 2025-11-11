# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in HoppyBrew, please report it by emailing the maintainers or opening a confidential security advisory on GitHub.

**Please do not open public issues for security vulnerabilities.**

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < latest| :x:                |

## Security Update Process

### Automated Scanning

HoppyBrew uses automated security scanning via GitHub Actions:

- **Python Dependencies**: Scanned using `pip-audit` daily
- **Node.js Dependencies**: Scanned using `yarn audit` daily
- **Container Images**: Scanned using Trivy when dependency scans pass

Security scan results are consolidated in a single issue that is updated automatically:
- **When scans fail**: The issue is created or updated with latest findings
- **When scans pass**: The issue is automatically closed

### Monitoring

The repository uses:
1. **Dependabot**: Automated dependency updates (configured in `.github/dependabot.yml`)
2. **GitHub Security Advisories**: Direct integration with vulnerability databases
3. **Workflow Notifications**: Security alerts from the `security-scan.yml` workflow

### Update Procedures

#### Python Dependencies

1. Check for vulnerabilities:
   ```bash
   cd services/backend
   pip-audit -r requirements.txt
   ```

2. Update vulnerable packages in `requirements.txt`:
   ```bash
   # Check available versions
   pip index versions <package-name>
   
   # Update to fixed version
   # Edit requirements.txt
   ```

3. Test the application after updates

#### Node.js Dependencies

1. Check for vulnerabilities:
   ```bash
   cd services/nuxt3-shadcn
   yarn audit
   ```

2. Update vulnerable packages:
   ```bash
   # Interactive fix (be careful with breaking changes)
   yarn upgrade-interactive
   
   # Or update specific package
   yarn upgrade <package-name>@<version>
   ```

3. Test the application after updates

#### Container Images

Container security is handled through base image updates in Dockerfiles. Update base images regularly:

```dockerfile
# services/backend/Dockerfile
FROM python:3.11-slim

# services/nuxt3-shadcn/Dockerfile
FROM node:20-alpine
```

## Current Security Status

### Known Vulnerabilities

#### Python Dependencies

**Resolved:**
- ✅ `python-multipart` 0.0.9 → 0.0.18 (CVE-2024-53981) - DoS vulnerability FIXED

**Unresolved:**
- ⚠️ `ecdsa` 0.19.1 (CVE-2024-23342) - Timing attack on P-256 curve
  - **Status**: No fix available from upstream
  - **Risk**: Low - transitive dependency via `python-jose`
  - **Mitigation**: This is a timing attack that requires specific conditions to exploit. The package maintainers consider side-channel attacks out of scope. Monitor for updates from `python-jose` or `ecdsa` projects.

#### Node.js Dependencies

**Major Updates:**
- ✅ `nuxt` 3.11.2 → 3.16.0+ (Multiple CVEs including CVE-2024-34344, CVE-2025-27415)
  - Fixes critical RCE vulnerability
  - Fixes cache poisoning DoS
  - Fixes XSS in navigateTo

**Remaining Vulnerabilities:**
- Many transitive dependencies have vulnerabilities that require upstream updates
- These are monitored through Dependabot and the security scan workflow

## Security Best Practices

1. **Never commit secrets** to the repository
2. **Use environment variables** for sensitive configuration
3. **Keep dependencies up to date** using Dependabot
4. **Review security alerts** from the automated workflow
5. **Test updates** before deploying to production
6. **Follow the principle of least privilege** for service accounts

## Security Contacts

For security issues that should not be disclosed publicly, please contact the maintainers directly through GitHub's security advisory feature.
