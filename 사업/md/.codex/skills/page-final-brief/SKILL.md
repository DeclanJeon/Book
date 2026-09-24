---
name: page-final-brief
description: Assemble QA-passed page strategy into an implementation-ready brief
triggers:
  - page final brief
  - landing brief
  - assemble page brief
  - implementation brief
argument-hint: "<QA-passed PageBrief>"
---

# page-final-brief Skill

## Purpose
Create the final handoff for designer, developer, copywriter, marketer, or orchestrator.

## When to activate
Use this skill when the page-production pipeline needs to assemble qa-passed page strategy into an implementation-ready brief.

## Inputs
- QA-passed PageBrief
- PageBrief.qa.pass must be true or explicitly waived by the user

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
final_brief:
  strategy_summary:
  page_type:
  page_goal:
  target_audience:
  positioning:
  core_message:
  page_sections:
  hero_copy:
  cta_stack:
  demonstration_requirements:
  proof_requirements:
  objection_handling:
  offer_blocks:
  shareability:
  open_questions:
  sales_readiness_checklist:
    value_proposition_10s:
    single_conversion_goal:
    message_match:
    above_fold_cta:
    demonstration_of_value:
    authentic_proof:
    objection_handling:
    mobile_speed_accessibility:
    measurement_plan:
  post_launch_measurement:
    conversion_event:
    success_metric:
    analytics_events:
    ab_test_or_iteration_plan:
  implementation_notes:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Do not assemble final brief when QA fails, unless clearly marked as draft blocked by QA.
- Make handoff immediately usable by implementation roles.
- Include the sales-readiness checklist so implementers can verify the page against conversion criteria, not just content completeness.
- The checklist must explicitly cover: value proposition within 10 seconds, single conversion goal, message match, above-fold CTA, demonstration of value, authentic proof, objection handling, mobile/speed/accessibility, and measurement plan.
- Include post-launch measurement: conversion event, success metric, analytics events, and A/B or iteration plan.
- Include implementation notes for mobile responsiveness, fast critical content, accessibility, and proof/source handling.
- Keep open questions explicit and tied to impact.

## Failure / retry behavior
If QA failed, produce a blocked brief summary and next required fixes instead of final brief.
