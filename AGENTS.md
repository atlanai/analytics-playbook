# AGENTS.md — Atlan AI Agent Guidelines

> **Version:** 6.1 | **Updated:** 2026-03-26  
> **Applies To:** All AI agents (Claude, GPT, Copilot, Cursor, Cline, etc.)  
> **Companion:** See `CLAUDE.md` for a lean quick-reference optimized for Claude Code.  
> **Security Contact:** Slack `#bu-security-and-it`

---

## Project Overview

<!-- Teams: Add project description, architecture, tech stack, data stores here. -->

## Project Commands

<!-- Teams: Add build, test, lint, deploy commands here. -->

## Coding Conventions

<!-- Teams: Add language, style guide, naming conventions, patterns here. -->

## Architecture Notes

<!-- Teams: Add design decisions, service boundaries, data flow, auth patterns here. -->

---

## Security

### How to Use This Section

1. **Every change:** Apply the 5 Always-Check Invariants.
2. **Based on what you're changing:** Apply the relevant Conditional Checks.
3. **When you find issues:** Use the Severity & Response rules.

**Tags:** `[MUST]` = required | `[REDLINE]` = forbidden | `[SHOULD]` = best practice

---

### Always-Check Invariants (Every Change)

1. **[MUST] No secrets** in code, config, logs, CI output, or `.env` files in version control.
2. **[MUST] Authentication & authorization must be real** — every protected endpoint must verify identity (JWT, OAuth, API key, session token, OIDC, or whatever mechanism the service uses) and enforce permissions. No "phantom auth" (imported but unused middleware).
3. **[MUST] No wildcards** — no `CORS: *`, `Action:"*"`, RBAC `resources:["*"]`, or GitHub `write-all`.
4. **[MUST] No untrusted execution** — no `eval`, unsafe deserialization, command injection, or untrusted input in CI `run:` blocks.
5. **[MUST] Pin supply chain** — actions→full SHA, images→version/SHA, no `latest`, verify deps exist and are reputable.

---

### Conditional Checks

Apply when the described pattern is present in the change:

| When you see... | Check |
|-----------------|-------|
| **DB queries** | **[MUST]** Parameterized only; scope to tenant/org if multi-tenant. **[REDLINE]** String concatenation with user input. |
| **Auth/session code** | **[MUST]** Validate credentials properly (JWT signature + claims, API key lookup, OAuth token introspection, session validity — whatever the service uses). **[MUST]** Tokens/sessions must expire. **[SHOULD]** httpOnly + secure + sameSite cookies for browser sessions. **[SHOULD]** Use established auth libraries, not hand-rolled crypto. |
| **New API endpoint** | **[MUST]** Must ship with authentication, authorization, input validation, and rate limiting. Not a follow-up. Add tenant scoping if the service is multi-tenant. |
| **Error responses** | **[MUST]** Generic to clients. **[REDLINE]** Stack traces, SQL, file paths, internal IPs in client responses. |
| **Outbound HTTP with user input** | **[MUST]** Allowlist hosts; block internal/metadata IPs (10.x, 172.16-31.x, 192.168.x, 169.254.169.254, localhost). |
| **Logging code** | **[REDLINE]** Never log tokens, cookies, secrets, Authorization headers, full request/response bodies. **[SHOULD]** Include contextual identifiers (tenant, user, request ID) in structured logs for audit. |
| **Dependency changes** | **[MUST]** Block CRITICAL/HIGH CVEs; flag MEDIUM. Check for typosquatting (new pkg, low downloads, similar name). Verify lockfile matches manifest. |
| **`.env` files** | **[MUST]** In `.gitignore`; `.env.example` has placeholders only. Block real secrets. |
| **CI/CD workflows** | **[MUST]** Pin actions to SHA. Minimum permissions. **[REDLINE]** PR metadata in `run:` blocks; `pull_request_target` with secrets + PR checkout; `write-all` permissions. |
| **Helm/K8s manifests** | **[MUST]** `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, `drop: ["ALL"]`. Least-privilege RBAC (Role over ClusterRole, no wildcards). **[REDLINE]** Secrets in `values.yaml`; `privileged: true`; `latest` tags. |
| **Shell scripts** | **[MUST]** `set -euo pipefail`. Quote variables. `mktemp` + cleanup trap. **[REDLINE]** `eval` with user input; `curl \| bash`; secrets in CLI args. |
| **Frontend code** | **[REDLINE]** `dangerouslySetInnerHTML`/`v-html`/`innerHTML` with user-controlled data. **[MUST]** No tokens/secrets in localStorage or sessionStorage. **[MUST]** Validate redirect targets against allowlist (prevent open redirects). **[MUST]** CSRF protection on state-changing requests if cookie-based auth. **[MUST]** Sanitize rich text with DOMPurify or equivalent before rendering. **[SHOULD]** Set strict CSP headers; avoid `unsafe-inline`/`unsafe-eval`. **[SHOULD]** No source maps in production. **[SHOULD]** Avoid exposing PII, internal IDs, or debug data in client state/URLs. **[SHOULD]** Use `rel="noopener noreferrer"` on external links with `target="_blank"`. |
| **IaC (Terraform/CF)** | **[MUST]** No public buckets. Encrypt at rest. Least-privilege IAM (no `Action:"*"`). **[SHOULD]** Minimize `0.0.0.0/0` ingress. |
| **AI/LLM code** | **[MUST]** No raw user input in system/privileged prompts — use clear delimiters between instructions and user content. **[MUST]** Mask PII/secrets/tenant data before sending to any LLM. **[MUST]** Sanitize model output before rendering in UI (XSS risk). **[MUST]** Do not use LLM output for auth/authz decisions. **[MUST]** Do not send customer data to external LLMs without explicit approval/DPA. **[REDLINE]** Passing LLM output directly to `eval`, SQL, shell commands, or `innerHTML` — leads to code injection, command injection, SQLi, and XSS. **[SHOULD]** Validate/filter model outputs before any downstream use. **[SHOULD]** Log categories of data sent to LLMs (not raw content). **[SHOULD]** Rate limit LLM API calls to prevent abuse/cost overrun. |
| **Docker** | **[MUST]** Non-root user. Pin base image versions. **[REDLINE]** Secrets in build layers; `privileged: true`. |
| **Code references/imports** | **[MUST]** All code in approved GitHub org (AtlanHQ). Flag personal repos or non-org imports. |

---

### Severity & Response

| Severity | Criteria | Action |
|----------|----------|--------|
| **CRITICAL** | RCE, data breach, cross-tenant access, credential exposure, full auth bypass, CRITICAL CVEs | **Block.** Fix immediately. No opt-out. |
| **HIGH** | Endpoint auth bypass, privilege escalation, tenant isolation gap, HIGH CVEs | **Block.** Fix before merge. No opt-out. |
| **MEDIUM** | Info disclosure via errors, weak config, CORS issues, missing controls | **Flag** with fix. Can be follow-up. |
| **LOW** | Best practice gaps, defense-in-depth | **Note** briefly. |

**Review format (MEDIUM+):**
```txt
🔒 SECURITY REVIEW
Issue: [description]
Severity: CRITICAL | HIGH | MEDIUM
Location: [file:line]
Risk: [what attacker gains, Atlan-specific impact]
Fix: [concrete fix — implement immediately for CRITICAL/HIGH]
```

**Quick format (LOW):** `⚡ Security note: [risk] → [fix]`

---

### Handling Existing Violations

- **In your diff:** Fix or flag with 🔒 format.
- **Outside your diff:** Note briefly. Don't refactor without explicit approval.
- **Never** use existing violations to justify new ones.

---

### Multi-Tenant Security (When Applicable)

> **Note:** Not all services are multi-tenant. If your service is single-tenant or internal-only, this section may not apply. Check your Architecture Notes above.

For multi-tenant services, every data path must enforce tenant/org isolation.

**The rule:** Tenant/org identifier from authenticated session → enforced in every data access → return 404 on miss (not 403).

```txt
✅ tenantId = extractTenantId(authenticatedSession)
✅ resource = query(filters={ id: resourceId, tenant_id: tenantId })
✅ if not resource: return 404

❌ tenant_id = request.params["tenant_id"]     // attacker swaps tenant
❌ SELECT * FROM resources WHERE id = ?        // missing tenant/org filter
❌ /api/tenants/{tenant_id}/resources          // who verifies ownership?
```

**Enforce in:** DB queries, cache keys (`tenant:{id}:…`), file storage paths, search filters, queue messages, webhook destinations.

---

### New API Endpoint Checklist

Every new endpoint **[MUST]** have before merging:
- [ ] Authentication (verify identity via JWT, API key, OAuth, session, or service-appropriate mechanism)
- [ ] Authorization (user/role permissions verified; tenant scoping if multi-tenant)
- [ ] Input validation (schema, allowlists, length limits)
- [ ] Rate limiting (keyed by user/tenant/IP as appropriate, return 429 + Retry-After)

---

### Security Review Checklist

**Universal:**
- [ ] No secrets in code/config/logs/CI output
- [ ] Client errors don't expose internals
- [ ] Existing security patterns reused (no new auth flows without review)

**Data Access:**
- [ ] Tenant/org scoping enforced from auth context (if multi-tenant)
- [ ] Input validated; parameterized queries only
- [ ] Auth + authz enforced; rate limiting on sensitive endpoints

**Infrastructure:**
- [ ] Containers non-root; minimal capabilities; images pinned
- [ ] RBAC least privilege; secrets managed externally
- [ ] TLS enforced; network exposure minimized

**CI/CD:**
- [ ] Actions pinned to SHAs; minimum permissions; no injection patterns

**Frontend:**
- [ ] No unsafe HTML rendering; tokens not in localStorage/sessionStorage
- [ ] Redirects validated against allowlist; CSP headers configured
- [ ] CSRF protection on state-changing requests (if cookie-based auth)

---

### When to Request Manual Security Review

Reach out to `#bu-security-and-it` before merging when changes touch:
- Auth/authz flows or multi-tenant isolation logic
- Secrets management or new external integrations
- New public-facing endpoints or services
- Any change where you're unsure about security impact

---

### Appendix: References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) | [API Security Top 10](https://owasp.org/www-project-api-security/)
- [STRIDE Threat Model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [GitHub Actions Hardening](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-for-github-actions)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/) | [SLSA](https://slsa.dev/) | [OpenSSF Scorecard](https://securityscorecards.dev/)