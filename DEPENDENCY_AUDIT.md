# Dependency Audit Report

**Generated:** 2025-11-11  
**Purpose:** Systematic dependency management and security maintenance

---

## Executive Summary

This audit identifies outdated dependencies across the HoppyBrew project and categorizes them by risk level to enable safe, incremental updates.

### Key Statistics

**Python Dependencies (services/backend/requirements.txt):**
- Total packages in requirements.txt: 43
- System packages with updates available: 55+
- **Risk Categories:**
  - 🟢 Low Risk (Patch): ~15 packages
  - 🟡 Medium Risk (Minor): ~25 packages  
  - 🔴 High Risk (Major): ~15 packages

**Node.js Dependencies (services/nuxt3-shadcn/package.json):**
- Total dependencies: 20
- Total devDependencies: 17
- **Notable Updates Available:**
  - Nuxt: 3.11.2 → 3.20.1 (minor) or 4.2.1 (major)
  - @vueuse/core: 10.11.1 → 14.0.0 (major)
  - shadcn-nuxt: 0.10.4 → 2.3.2 (major)

---

## Python Dependencies Analysis

### Currently Installed (requirements.txt)

These are the direct dependencies specified in the project:

```
fastapi==0.121.1
python-multipart==0.0.9  # ⚠️ Security fix applied, but 0.0.20 available
uvicorn==0.38.0
SQLAlchemy==2.0.30  # → 2.0.44 (patch update available)
sqlalchemy-utils==0.42.0
psycopg==3.2.12
alembic==1.17.1
pydantic==2.7.3  # → 2.12.4 (minor update available)
pydantic-settings==2.11.0  # → 2.12.0 (minor update available)
pydantic-extra-types==2.10.6
email-validator==2.1.1  # → 2.3.0 (minor update available)
python-jose[cryptography]==3.5.0
passlib[bcrypt]==1.7.4
config==0.5.1
python-dotenv==1.2.1
pandas==2.3.3
requests==2.32.5
beautifulsoup4==4.14.2
bs4==0.0.2
pytest==8.2.2  # → 9.0.0 (major update available)
pytest-asyncio==0.23.7  # → 1.3.0 (major update available)
pytest-cov==5.0.0  # → 7.0.0 (major update available)
httpx==0.28.1
selenium==4.38.0
factory-boy==3.3.0  # → 3.3.3 (patch update available)
flake8==7.3.0
```

### Risk Categorization

#### 🟢 Low Risk - Patch Updates (Recommended for immediate update)
Safe to apply with minimal risk of breaking changes:

| Package | Current | Latest | Update Type |
|---------|---------|--------|-------------|
| SQLAlchemy | 2.0.30 | 2.0.44 | Patch |
| factory-boy | 3.3.0 | 3.3.3 | Patch |
| Jinja2 | 3.1.2 | 3.1.6 | Patch |
| PyYAML | 6.0.1 | 6.0.3 | Patch |
| configobj | 5.0.8 | 5.0.9 | Patch |
| packaging | 24.0 | 25.0 | Minor (but low risk) |
| jsonpatch | 1.32 | 1.33 | Patch |
| lazr.uri | 1.0.6 | 1.0.7 | Patch |
| six | 1.16.0 | 1.17.0 | Patch |
| pyparsing | 3.1.1 | 3.2.5 | Patch |
| service-identity | 24.1.0 | 24.2.0 | Patch |
| starlette | 0.49.3 | 0.50.0 | Patch |

#### 🟡 Medium Risk - Minor Updates (Require testing)
May include new features or deprecations:

| Package | Current | Latest | Update Type |
|---------|---------|--------|-------------|
| pydantic | 2.7.3 | 2.12.4 | Minor |
| pydantic-settings | 2.11.0 | 2.12.0 | Minor |
| email-validator | 2.1.1 | 2.3.0 | Minor |
| python-multipart | 0.0.9 | 0.0.20 | Patch/Minor |
| rich | 13.7.1 | 14.2.0 | Minor |
| Pygments | 2.17.2 | 2.19.2 | Patch |
| python-dateutil | 2.8.2 | 2.9.0.post0 | Minor |
| pytz | 2024.1 | 2025.2 | Version |
| oauthlib | 3.2.2 | 3.3.1 | Minor |
| PyJWT | 2.7.0 | 2.10.1 | Patch |
| MarkupSafe | 2.1.5 | 3.0.3 | Minor |
| idna | 3.6 | 3.11 | Patch |

#### 🔴 High Risk - Major Updates (Require careful planning)
Breaking changes expected:

| Package | Current | Latest | Update Type | Notes |
|---------|---------|--------|-------------|-------|
| pytest | 8.2.2 | 9.0.0 | Major | Test framework - review changelog |
| pytest-asyncio | 0.23.7 | 1.3.0 | Major | Breaking changes in async testing |
| pytest-cov | 5.0.0 | 7.0.0 | Major | Coverage plugin updates |
| bcrypt | 3.2.2 | 5.0.0 | Major | Password hashing - security critical |
| cryptography | 41.0.7 | 46.0.3 | Major | Crypto library - security critical |
| pyOpenSSL | 23.2.0 | 25.3.0 | Major | SSL/TLS - security critical |
| Babel | 2.10.3 | 2.17.0 | Minor | i18n library |
| boto3 | 1.34.46 | 1.40.70 | Minor | AWS SDK |
| botocore | 1.34.46 | 1.40.70 | Minor | AWS core |
| s3transfer | 0.10.1 | 0.14.0 | Patch | AWS S3 transfers |
| jsonpointer | 2.0 | 3.0.0 | Major | JSON pointer spec |
| jsonschema | 4.10.3 | 4.25.1 | Patch | JSON schema validation |
| Twisted | 24.3.0 | 25.5.0 | Minor | Async networking |
| Automat | 22.10.0 | 25.4.16 | Major | State machines |
| incremental | 22.10.0 | 24.7.2 | Major | Versioning |
| attrs | 23.2.0 | 25.4.0 | Major | Class decorators |
| zope.interface | 6.1 | 8.1 | Major | Interface definitions |
| markdown-it-py | 3.0.0 | 4.0.0 | Major | Markdown parser |
| netaddr | 0.8.0 | 1.3.0 | Major | Network address handling |

---

## Node.js Dependencies Analysis

### Production Dependencies (package.json)

```json
{
  "@heroicons/vue": "^2.2.0",           // ✅ Current
  "@nuxtjs/proxy": "^2.1.0",            // ✅ Current
  "@vueuse/core": "^10.11.1",           // → 14.0.0 (major)
  "axios": "^1.13.2",                    // ✅ Current
  "buffer": "^6.0.3",                    // ✅ Current
  "class-variance-authority": "^0.7.1",  // ✅ Current
  "clsx": "^2.1.1",                      // ✅ Current
  "cors": "^2.8.5",                      // ✅ Current
  "lucide-vue-next": "^0.553.0",        // ✅ Current
  "nuxt": "^3.11.2",                     // → 3.20.1 (minor) or 4.2.1 (major)
  "nuxt-highcharts": "^3.1.1",          // ✅ Current
  "nuxt-socket-io": "^3.0.13",          // ✅ Current
  "radix-vue": "^1.9.17",               // ✅ Current
  "shadcn-nuxt": "^0.10.4",             // → 2.3.2 (major)
  "tailwind-merge": "^3.4.0",           // ✅ Current
  "tailwindcss-animate": "^1.0.7",      // ✅ Current
  "uuid": "^13.0.0",                     // ✅ Current
  "vue": "^3.5.24",                      // ✅ Current
  "vue-router": "^4.6.3",                // ✅ Current
  "xml2js": "^0.6.2"                     // ✅ Current
}
```

### Notable Updates Required

#### 🟡 Medium Risk - Minor Updates
- **nuxt**: 3.11.2 → 3.20.1 (minor within v3)
  - Already partially applied in PR #437
  - Consider updating to latest v3 stable

#### 🔴 High Risk - Major Updates
- **nuxt**: 3.11.2 → 4.2.1 (major - Nuxt 4)
  - Breaking changes expected
  - Requires migration guide review
  - Defer to future dedicated PR

- **@vueuse/core**: 10.11.1 → 14.0.0 (major)
  - Composition API utilities
  - Check breaking changes in v11-v14

- **shadcn-nuxt**: 0.10.4 → 2.3.2 (major)
  - UI component library
  - Significant version jump
  - Review migration guide

---

## Recommended Update Strategy

### Phase 1: Immediate (Patch Updates) ✅
**Target:** Low-risk patch updates with security benefits

**Python:**
1. SQLAlchemy: 2.0.30 → 2.0.44
2. factory-boy: 3.3.0 → 3.3.3
3. six: 1.16.0 → 1.17.0
4. pyparsing: 3.1.1 → 3.2.5
5. service-identity: 24.1.0 → 24.2.0
6. starlette: 0.49.3 → 0.50.0
7. jsonpatch: 1.32 → 1.33
8. PyYAML: 6.0.1 → 6.0.3

**Action:** Apply in this PR with test validation

### Phase 2: Short-term (Minor Updates) 🔜
**Target:** Minor updates with moderate testing

**Python:**
1. pydantic: 2.7.3 → 2.12.4
2. pydantic-settings: 2.11.0 → 2.12.0
3. python-multipart: 0.0.9 → 0.0.20
4. email-validator: 2.1.1 → 2.3.0
5. PyJWT: 2.7.0 → 2.10.1

**Node.js:**
1. nuxt: 3.11.2 → 3.20.1 (stay within v3)

**Action:** Separate PR with comprehensive testing

### Phase 3: Long-term (Major Updates) 📅
**Target:** Major version upgrades requiring migration

**Python:**
1. pytest ecosystem: 8.x → 9.x (test framework)
2. Security libraries: bcrypt, cryptography, pyOpenSSL
3. AWS SDK: boto3, botocore

**Node.js:**
1. nuxt: 3.x → 4.x (major framework upgrade)
2. @vueuse/core: 10.x → 14.x
3. shadcn-nuxt: 0.10.x → 2.x

**Action:** Dedicated PRs with extensive testing and documentation

---

## Security Considerations

### Critical Security Updates
These packages handle security-sensitive operations and should be prioritized:

1. **python-multipart** (0.0.9 → 0.0.20)
   - Security fix already applied in PR #437
   - Further updates available

2. **cryptography** (41.0.7 → 46.0.3)
   - Major version update
   - Contains security patches
   - **Recommendation:** Phase 3, requires testing

3. **pyOpenSSL** (23.2.0 → 25.3.0)
   - SSL/TLS handling
   - **Recommendation:** Phase 3, with SSL cert testing

4. **bcrypt** (3.2.2 → 5.0.0)
   - Password hashing
   - **Recommendation:** Phase 3, verify hash compatibility

5. **PyJWT** (2.7.0 → 2.10.1)
   - JWT token handling
   - **Recommendation:** Phase 2, test auth flows

### Vulnerability Scanning
- ✅ pip-audit configured (runs daily)
- ✅ yarn audit configured (runs daily)
- ✅ Trivy container scanning enabled
- ✅ Dependabot security updates enabled

---

## Implementation Checklist

### ✅ Completed
- [x] Dependency audit performed
- [x] Dependencies categorized by risk
- [x] Dependabot configuration reviewed
- [x] Security scanning workflows verified

### 🔄 In Progress (This PR)
- [ ] Enhanced Dependabot with reviewers
- [ ] Added versioning-strategy for npm
- [ ] Added dependency review to PR validation
- [ ] Apply Phase 1 patch updates
- [ ] Update CONTRIBUTING.md with procedures
- [ ] Validate all tests pass

### 📋 Future Work
- [ ] Phase 2: Minor updates (separate PR)
- [ ] Phase 3: Major updates (multiple dedicated PRs)
- [ ] Nuxt 4 migration planning
- [ ] Automated update testing pipeline

---

## References

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Dependency Review Action](https://github.com/actions/dependency-review-action)
- [Python Semantic Versioning](https://peps.python.org/pep-0440/)
- [Node.js Semantic Versioning](https://docs.npmjs.com/about-semantic-versioning)
