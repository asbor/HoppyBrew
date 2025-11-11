# Consolidated Security Vulnerability Report

**Date:** 2025-11-11  
**Repository:** asbor/HoppyBrew  
**Report Type:** Security Audit

## Executive Summary

This report consolidates all security vulnerabilities detected in the HoppyBrew project from automated security scans. The analysis identified:

- **Python**: 2 vulnerabilities (1 fixed, 1 unfixable)
- **Node.js**: 42 unique vulnerabilities across severity levels

### Remediation Status

- ✅ **Python**: Primary vulnerability fixed (`python-multipart`)
- 🔄 **Node.js**: Major framework updated (`nuxt` 3.11.2 → 3.16.0)
- 🔧 **Workflow**: Fixed to prevent duplicate issue creation

---

## Python Vulnerabilities

### Fixed Vulnerabilities

#### 1. python-multipart - DoS via Form Data Parsing
- **Package**: `python-multipart`
- **Affected Version**: 0.0.9
- **Fixed Version**: 0.0.18
- **CVE**: CVE-2024-53981
- **GitHub Advisory**: GHSA-59g5-xgcq-4qw3
- **Severity**: HIGH
- **Status**: ✅ FIXED

**Description:**
When parsing form data, `python-multipart` skips line breaks (CR `\r` or LF `\n`) in front of the first boundary and any tailing bytes after the last boundary. This happens one byte at a time and emits a log event each time, which may cause excessive logging for certain inputs. An attacker could abuse this by sending a malicious request with lots of data before the first or after the last boundary, causing high CPU load and stalling the processing thread for a significant amount of time. In ASGI applications, this could stall the event loop and prevent other requests from being processed, resulting in a denial of service (DoS).

**Remediation:**
- Updated `requirements.txt`: `python-multipart==0.0.9` → `python-multipart==0.0.18`

### Unfixable Vulnerabilities

#### 2. ecdsa - Timing Attack on P-256 Curve
- **Package**: `ecdsa`
- **Affected Version**: 0.19.1
- **Fixed Version**: None available
- **CVE**: CVE-2024-23342
- **GitHub Advisory**: GHSA-wj6h-64fc-37mp
- **Severity**: MEDIUM
- **Status**: ⚠️ ACCEPTED RISK

**Description:**
python-ecdsa has been found to be subject to a Minerva timing attack on the P-256 curve. Using the `ecdsa.SigningKey.sign_digest()` API function and timing signatures, an attacker can leak the internal nonce which may allow for private key discovery. Both ECDSA signatures, key generation, and ECDH operations are affected. ECDSA signature verification is unaffected.

**Risk Assessment:**
- **Dependency Type**: Transitive (via `python-jose[cryptography]`)
- **Exploitability**: Low - requires precise timing measurements and specific conditions
- **Impact**: Medium - could potentially leak private keys under specific circumstances
- **Upstream Status**: The python-ecdsa project considers side channel attacks out of scope and there is no planned fix

**Mitigation Strategy:**
1. Monitor `python-jose` for alternative cryptography backend options
2. Consider migrating to more modern cryptographic libraries if critical
3. Ensure production environments are not exposing timing information
4. Keep monitoring for upstream updates

---

## Node.js Vulnerabilities

### Critical Severity (1)

#### 1. nuxt - Remote Code Execution via Browser Test Runner
- **Package**: `nuxt`
- **Affected Version**: 3.11.2
- **Fixed Version**: 3.12.4+
- **CVE**: CVE-2024-34344
- **Severity**: CRITICAL
- **Status**: 🔄 FIXED (updating to 3.16.0)

### High Severity (8)

#### 2. nuxt - Cache Poisoning DoS
- **CVE**: CVE-2025-27415
- **Fixed Version**: 3.16.0+
- **Status**: 🔄 FIXED

#### 3. nuxt - XSS in navigateTo
- **CVE**: CVE-2024-34343
- **Fixed Version**: 3.12.4+
- **Status**: 🔄 FIXED

#### 4. @nuxt/devtools - Path Traversal
- **CVE**: CVE-2024-23657
- **Fixed Version**: 1.3.9+
- **Status**: 🔄 Will be updated via nuxt upgrade

#### 5. devalue - Prototype Pollution
- **CVE**: CVE-2025-57820
- **Fixed Version**: 5.3.2+
- **Status**: 🔄 Transitive dependency

#### 6. rollup - DOM Clobbering XSS
- **CVE**: CVE-2024-47068
- **Fixed Version**: 4.22.4+
- **Status**: 🔄 Transitive dependency

#### 7. engine.io - Uncaught Exception
- **CVE**: CVE-2022-21676
- **Fixed Version**: 5.2.1+
- **Status**: 🔄 Transitive dependency via nuxt-socket-io

#### 8-9. Additional High Severity
- Various transitive dependencies requiring upstream updates

### Moderate Severity (24)

Includes vulnerabilities in:
- `@nuxt/vite-builder` - Malicious website attack on dev server
- `esbuild` - Request manipulation
- `@nuxt/devtools` - XSS
- `vite` - Multiple issues (path bypass, DOM clobbering)
- Various transitive dependencies

### Low Severity (9)

Includes:
- `brace-expansion` - ReDoS
- `vite` - Various minor issues
- `serve-static` - Template injection
- `parseuri` - ReDoS (via nuxt-socket-io)

---

## Remediation Summary

### Completed Actions

1. ✅ Fixed `python-multipart` DoS vulnerability
2. ✅ Updated `nuxt` from 3.11.2 to 3.16.0 (fixes 3 critical/high CVEs)
3. ✅ Fixed security-scan.yml workflow to prevent duplicate issues
4. ✅ Created comprehensive security documentation

### Pending Actions

1. 🔄 Test updated dependencies in local environment
2. 🔄 Update yarn.lock after package.json changes
3. 🔄 Run full test suite to ensure compatibility
4. 🔄 Deploy and monitor for any breaking changes

### Monitoring

All remaining transitive dependency vulnerabilities are:
- Tracked by Dependabot (configured for weekly checks)
- Monitored by automated security scans (daily)
- Will be updated automatically when upstream packages release fixes

---

## Workflow Improvements

### Previous Issue

The `security-scan.yml` workflow created a new GitHub issue for every failed scan, using a unique run ID in the title. This resulted in 40+ duplicate security alert issues.

### Solution Implemented

1. **Standardized Issue Title**: Changed from `Security scan alerts for ${runId}` to `🔒 Security Scan Alert - Vulnerabilities Detected`
2. **Update Existing Issues**: Workflow now searches for and updates existing open security alert issues
3. **Auto-close on Success**: When all scans pass, the workflow automatically closes the security alert issue
4. **Better Tracking**: Each update includes a timestamp and link to the workflow run

### New Workflow Behavior

- **First failure**: Creates a new security alert issue
- **Subsequent failures**: Updates the existing issue with latest scan results
- **All scans pass**: Automatically closes the issue with a success comment

---

## Recommendations

### Immediate
- ✅ Update Python dependencies (completed)
- ✅ Update Node.js dependencies (completed)
- ⏭️ Run test suites to verify compatibility
- ⏭️ Close duplicate security alert issues

### Short-term
- Monitor for breaking changes after dependency updates
- Review and update any deprecated API usage
- Consider removing or replacing `nuxt-socket-io` (has unmaintained transitive deps)

### Long-term
- Establish quarterly security audit schedule
- Consider implementing automated security testing in PR workflow
- Evaluate alternative packages for `python-jose` to eliminate `ecdsa` dependency
- Keep dependencies up to date through Dependabot

---

## Related Issues

This report consolidates and addresses:
- asbor/HoppyBrew#360-368
- asbor/HoppyBrew#380-388
- asbor/HoppyBrew#391
- asbor/HoppyBrew#395
- asbor/HoppyBrew#396
- asbor/HoppyBrew#417
- asbor/HoppyBrew#422-428
- asbor/HoppyBrew#432
- asbor/HoppyBrew#433

All duplicate issues should be closed with reference to this report.

---

## References

- [SECURITY.md](./SECURITY.md) - Security policy and update procedures
- [.github/dependabot.yml](./.github/dependabot.yml) - Automated dependency updates
- [.github/workflows/security-scan.yml](./.github/workflows/security-scan.yml) - Security scanning workflow
- [GitHub Security Advisory Database](https://github.com/advisories)
- [pip-audit](https://github.com/pypa/pip-audit)
- [yarn audit](https://classic.yarnpkg.com/en/docs/cli/audit/)
