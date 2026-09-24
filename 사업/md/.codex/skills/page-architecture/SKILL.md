---
name: page-architecture
description: Design the section order and information hierarchy for the selected page type
triggers:
  - page architecture
  - section order
  - landing structure
  - information hierarchy
argument-hint: "<PageBrief message/proof/page_type>"
---

# page-architecture Skill

## Purpose
Turn strategy into a page structure whose order supports comprehension and action.

## When to activate
Use this skill when the page-production pipeline needs to design the section order and information hierarchy for the selected page type.

## Inputs
- PageBrief.page_goal
- PageBrief.audience
- PageBrief.positioning
- PageBrief.message
- PageBrief.evidence.proof_assets

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
page:
  section_order:
    - id:
      title:
      purpose:
      required_inputs: []
      proof_needed: []
      page_type_reason:
      conversion_role: attention | comprehension | trust | desire | objection | action
      success_criteria:
  above_fold_requirements:
    value_proposition:
    primary_cta:
    proof_or_context_cue:
  distraction_policy:
    navigation:
    secondary_links:
    competing_ctas:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Each section must serve the primary page goal.
- The first screen must include a clear value proposition, the primary CTA, and either proof or context cue.
- Landing/campaign pages must minimize navigation and competing links unless the page goal requires exploration.
- Do not copy SaaS-only sections into non-SaaS pages unless justified.
- Avoid feature dumps and autobiographical ordering.
- Include mobile-first ordering: the primary CTA and value proposition must survive narrow screens.

## Failure / retry behavior
If proof is missing, keep proof-dependent sections but mark proof requirements explicitly.
