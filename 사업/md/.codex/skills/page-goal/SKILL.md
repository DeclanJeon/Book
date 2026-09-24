---
name: page-goal
description: Define page type, primary conversion goal, success metric, and required sections
triggers:
  - page goal
  - page type
  - conversion goal
  - landing objective
argument-hint: "<PageBrief evidence/objective>"
---

# page-goal Skill

## Purpose
Lock what the page is for before audience, positioning, or copy work begins.

## When to activate
Use this skill when the page-production pipeline needs to define page type, primary conversion goal, success metric, and required sections.

## Inputs
- PageBrief.metadata
- Evidence from page-evidence-intake
- User/project request
- Known business model or campaign context

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
page_goal:
  page_type: saas_homepage | landing_page | product_page | service_page | sales_page | personal_brand_page | agency_or_freelancer_page | content_conversion_page
  primary_goal:
  secondary_goals: []
  conversion_event:
  traffic_source:
    channel:
    promise_or_intent:
    message_match_required: true | false
  success_metric:
  non_goals: []
  required_sections_by_type: []
  optional_sections_by_type: []
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Choose one primary goal; do not allow competing first-priority conversions.
- Ensure CTA type matches page type and conversion event.
- Capture the acquisition channel, referral context, ad/email/search promise, or mark `traffic_source` unknown.
- If `traffic_source` is unknown, downstream QA must mark message match as partial/unknown rather than pass.
- List non-goals to prevent scope drift.

## Failure / retry behavior
If the page type is ambiguous, choose the safest type from evidence and list ambiguity in notes.
