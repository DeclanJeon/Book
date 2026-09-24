---
name: page-demonstration
description: Specify concrete demo, process, portfolio, before-after, or sample-output blocks
triggers:
  - page demo
  - show value
  - product demonstration
  - portfolio block
argument-hint: "<PageBrief page/audience>"
---

# page-demonstration Skill

## Purpose
Show the promised value instead of only explaining it.

## When to activate
Use this skill when the page-production pipeline needs to specify concrete demo, process, portfolio, before-after, or sample-output blocks.

## Inputs
- PageBrief.page_goal
- Product/service/process/content capabilities
- PageBrief.audience.urgent_job
- PageBrief.page.section_order

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
demonstration_blocks:
  - type: product_demo | process | before_after | portfolio | sample_output | walkthrough | case_snapshot
    name:
    before_state:
    input_or_starting_point:
    action_or_method:
    output_or_result:
    measurable_result:
    visual_needed:
    caption:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Every block needs an observable before/action/after or sample value.
- Match demo type to page type: UI for SaaS, process/results for service, work samples for personal/agency pages.
- Do not invent screenshots or results.

## Failure / retry behavior
If visuals are unavailable, specify exactly what visual or sample must be produced.
