---
name: page-proof-trust
description: Map page claims to proof assets and block unsupported trust claims
triggers:
  - proof trust
  - trust signals
  - claim proof
  - social proof
argument-hint: "<PageBrief claims/proof_assets>"
---

# page-proof-trust Skill

## Purpose
Ensure claims are credible and proof is placed where it reduces doubt.

## When to activate
Use this skill when the page-production pipeline needs to map page claims to proof assets and block unsupported trust claims.

## Inputs
- PageBrief.evidence.proof_assets
- Generated claims from prior skills
- PageBrief.page_goal.page_type

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
proof_blocks:
  - claim:
    proof_type:
    proof_value:
    source:
    evidence_kind: direct_observed | customer_reported | interview_reported | third_party | inferred
    permission_status: approved | anonymized | internal_only | unknown
    allowed_wording:
    placement:
missing_proof:
  - claim:
    needed_proof:
    risk_if_published:
    safe_revision:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- No proof-like claim may pass without source.
- Testimonials require exact quote text, attribution level, and permission status.
- Anonymous/anonymized proof can support process or craft claims, but not named-customer trust or quantified commercial outcomes unless the metric source is supplied.
- Interview-reported metrics must be labeled as reported, not guaranteed, audited, or telemetry-backed.
- Use page-type-specific proof: logos/security for SaaS, portfolio/results for services, proof-of-work/media for personal brands.
- Place proof near the claim it supports.

## Failure / retry behavior
Move unsupported claims to `missing_proof` and recommend removal or revision.
