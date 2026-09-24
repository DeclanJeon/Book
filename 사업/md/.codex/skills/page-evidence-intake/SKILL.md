---
name: page-evidence-intake
description: Separate page-production source material into facts, proof assets, and unknowns
triggers:
  - page evidence
  - source material
  - proof intake
  - claim audit
argument-hint: "<page/source materials>"
---

# page-evidence-intake Skill

## Purpose
Build the evidence foundation before any positioning, copy, or design decision.

## When to activate
Use this skill when the page-production pipeline needs to separate page-production source material into facts, proof assets, and unknowns.

## Inputs
- Product, service, person, campaign, or content description
- Existing page/copy, interviews, reviews, sales notes, competitor or alternative pages
- Available proof assets: logos, metrics, testimonials, case studies, screenshots, credentials, portfolio, security, integrations
- Relevant research or marketing principles

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
evidence:
  factual_inputs:
    - claim:
      source:
      confidence: high | medium | low
  audience_facts:
    - claim:
      source:
      confidence: high | medium | low
  competitor_or_alternative_facts:
    - claim:
      source:
      confidence: high | medium | low
  traffic_source_promises:
    - source_channel:
      promise_or_intent:
      match_confidence: high | medium | low | unknown
  proof_assets:
    - type: logo | metric | testimonial | case_study | screenshot | portfolio | credential | security | integration | media | result
      value:
      source:
      permission_status: approved | anonymized | internal_only | unknown
      evidence_kind: direct_observed | customer_reported | interview_reported | third_party | inferred
      usable_on_page: true | false
  unknowns:
    - question:
      impact:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Do not accept unsourced numbers, logos, testimonials, or credentials as proof assets.
- Testimonials require exact quote text, attribution level, and permission status before use in final page copy.
- Metrics must distinguish telemetry/audited data from customer-reported or interview-reported data.
- Capture traffic source or mark it unknown; message match cannot fully pass without a source promise or visitor intent.
- Keep uncertain claims in `unknowns`; do not upgrade them to facts.
- Flag claims that could become page copy but lack proof.

## Failure / retry behavior
If evidence is too thin, stop with `unknowns` and recommended evidence to collect.
