---
Document-ID: MND-L1-CI-INFRA-005-INDEX
Version: v1.0.0
Status: Active / Enforcement Locked
Layer: L3 — CI/CD Infrastructure
Owner: Prospera Global Engineering Council
Created: 2026-03-24
Last-Updated: 2026-05-21
---

# SYSTEM_INDEX — prospera-ci-shared

Authoritative governance surface for the `prospera-ci-shared` repository.
All CI/CD enforcement scripts, validation workflows, and skills are indexed here.

## 1. Governance Documents

| File | Role | Status |
|------|------|--------|
| `README.md` | Repo identity + purpose | ACTIVE |
| `AGENTS.md` | AI agent operating contract | ACTIVE |
| `GOVERNANCE_STATUS.md` | Current maturity level | ACTIVE |
| `00_governance/GOVERNANCE.md` | Governance authority reference | ACTIVE |
| `00_governance/constitution.md` | Immutable operating principles | ACTIVE |
| `01_ARCHITECTURE/ADR-000-INDEX.md` | Architecture decision record index | ACTIVE |

## 2. Enforcement Scripts

| File | Purpose |
|------|---------|
| `check_api_contracts.py` | Validates API contract compliance |
| `check_architecture_dependencies.py` | Validates layer dependency rules |
| `check_repository_registry.py` | Validates repository registry |
| `tools/validate_plane_boundaries.py` | Ensures dynamic state does not enter KB governance files |

## 3. CI/CD Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `.github/workflows/governance_validation_v2.yml` | workflow_call | Three-class governance validation |
| `.github/workflows/governance_daily_sprint.yml` | cron 02:00 UTC / manual | Daily auto-remediation + email notification |

## 4. Skills

| File | Skill | Scope |
|------|-------|-------|
| `skills/SKILL-CORE.md` | Core skill router | All tasks |
| `skills/SKILL-01.md` | YAML governance | CI workflow files |
| `skills/SKILL-02.md` | Python kernel | 02_kernel modules |
| `skills/SKILL-03.md` | Git discipline | Commit + PR standards |
| `skills/SKILL-04.md` | Test discipline | Unit + integration tests |
| `skills/SKILL-05.md` | Documentation | Governance docs |
| `skills/SKILL-06.md` | Docker | Container builds |
| `skills/SKILL-07.md` | Security | Auth + token handling |
| `skills/SKILL-08.md` | API contracts | Interface definitions |
| `skills/SKILL-09.md` | Monitoring | Health + pulse |
| `skills/SKILL-10.md` | DORA metrics | Deployment frequency |

## 5. Three-Class Validation Standard

| Class | Condition | Action |
|-------|-----------|--------|
| `VERIFIED` | All checks pass (AGENTS.md ✓, SYSTEM_INDEX.md ✓, naming ✓) | Allow merge |
| `ACCEPTABLE_FAIL` | Known gaps (AGENTS.md missing in new repo) | Allow merge |
| `STRUCTURAL_WARNING` | SYSTEM_INDEX.md missing / core doc modified without review | Block merge |

## 6. Kernel Modules

| File | Role |
|------|------|
| `02_kernel/governance/authority_matrix.py` | Authority-level decision matrix |
| `02_kernel/registry/__init__.py` | Registry initialization |

## 7. Invariants

- **I-01 NO_BYPASS**: No repo merges if this validation fails (MND-level bypass only).
- **I-02 SSOT**: CI logic must align with `REPO_MASTER_INDEX.json`.
- **I-03 AUDIT**: Every CI result must be emitted to `prospera-audit-ledger`.
