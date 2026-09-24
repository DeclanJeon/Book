---
name: page-conversion-qa
description: Block unsupported, vague, unethical, or page-type-mismatched page brief content
triggers:
  - conversion QA
  - page QA
  - claim audit
  - landing page review
argument-hint: "<full PageBrief>"
---

# page-conversion-qa Skill

## Purpose
Act as the final quality gate before assembling or implementing the page brief.

## When to activate
Use this skill when the page-production pipeline needs to block unsupported, vague, unethical, or page-type-mismatched page brief content.

## Inputs
- Full PageBrief from all prior skills
- Allowed upstream skill names for rerun routing: `page-evidence-intake`, `page-goal`, `page-audience-jtbd`, `page-positioning`, `page-core-message`, `page-architecture`, `page-hero-cta`, `page-demonstration`, `page-proof-trust`, `page-objection-risk`, `page-offer-conversion`, `page-shareability`.

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
qa:
  readiness_score: 0-100
  sales_readiness:
    value_proposition_10s:
      pass: true | false
      evidence:
      fix:
    single_conversion_goal:
      pass: true | false
      evidence:
      fix:
    message_match:
      pass: true | false
      evidence:
      fix:
    above_fold_cta:
      pass: true | false
      evidence:
      fix:
    demonstration_of_value:
      pass: true | false
      evidence:
      fix:
    authentic_proof:
      pass: true | false
      evidence:
      fix:
    objection_handling:
      pass: true | false
      evidence:
      fix:
    mobile_speed_accessibility:
      pass: true | false
      evidence:
      fix:
    measurement_plan:
      pass: true | false
      evidence:
      fix:
  unsupported_claims:
    - claim:
      location:
      action: remove | revise | needs_proof
  vague_phrases:
    - phrase:
      replacement:
  ethical_risks:
    - risk:
      location:
      severity: high | medium | low
      fix:
  page_type_mismatches:
    - mismatch:
      location:
      fix:
  missing_inputs:
    - input:
      blocking: true | false
  skills_to_rerun:
    - page-evidence-intake | page-goal | page-audience-jtbd | page-positioning | page-core-message | page-architecture | page-hero-cta | page-demonstration | page-proof-trust | page-objection-risk | page-offer-conversion | page-shareability
  pass: true | false
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- `pass: true` requires zero critical unsupported claims.
- The page must communicate a clear value proposition within the first screen / first 10 seconds.
- The page must have one primary conversion goal and one matching primary CTA.
- For campaign pages, hero copy must match the ad/source promise; otherwise flag `message_match`.
- If traffic source or visitor intent is unknown, `message_match` cannot fully pass; mark it partial/unknown and route to `page-evidence-intake` or `page-goal`.
- The page must show the product, service, process, work sample, or result in action.
- Social proof must be authentic and sourced; anonymous or invented testimonials fail.
- Testimonials must include exact quote text, attribution level, and permission status; otherwise route to `page-proof-trust`.
- Reported/interview metrics must be worded as reported evidence, not guaranteed results.
- The brief must include mobile, speed, and accessibility requirements: responsive layout, fast critical content, keyboard/focus/contrast/alt-text considerations, and Core Web Vitals targets when implementation is in scope.
- The brief must include a measurement plan: conversion event, success metric, and experiment or post-launch learning loop.
- Block mismatched CTAs or SaaS-only sections on non-SaaS pages unless justified.
- Flag vague phrases and supply replacements.
- When QA fails, populate `skills_to_rerun` with exact upstream `page-*` skill names; do not invent generic skill names.

## Failure / retry behavior
Return `pass: false` with exact upstream `page-*` skill names in `skills_to_rerun`.
