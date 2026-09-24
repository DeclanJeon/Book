---
name: page-hero-cta
description: Generate first-screen message and CTA stack consistent with page goal and positioning
triggers:
  - hero copy
  - page CTA
  - above the fold
  - primary CTA
argument-hint: "<PageBrief message/page_goal>"
---

# page-hero-cta Skill

## Purpose
Make the first screen understandable and action-ready in five seconds.

## When to activate
Use this skill when the page-production pipeline needs to generate first-screen message and cta stack consistent with page goal and positioning.

## Inputs
- PageBrief.page_goal
- PageBrief.message
- PageBrief.positioning
- PageBrief.evidence.proof_assets

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
hero:
  eyebrow:
  headline:
  subheadline:
  proof_line:
  primary_cta:
    label:
    destination:
    intent:
  secondary_cta:
    label:
    destination:
    intent:
cta_stack:
  primary:
  secondary:
  low_commitment:
  high_intent:
  repeat_locations: []
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Headline must be understandable without scrolling.
- Do not use 'Learn more' as the primary CTA.
- Proof line must use only verified proof assets or be omitted.

## Failure / retry behavior
If no proof exists, remove proof line and add a missing proof note.
