---
name: page-positioning
description: Choose the page frame, category/context, owned word, contrast, and non-fit audience
triggers:
  - page positioning
  - category
  - owned word
  - differentiation
argument-hint: "<PageBrief audience/alternatives>"
---

# page-positioning Skill

## Purpose
Make the page occupy one clear position in the visitor's mind.

## When to activate
Use this skill when the page-production pipeline needs to choose the page frame, category/context, owned word, contrast, and non-fit audience.

## Inputs
- PageBrief.page_goal
- PageBrief.audience
- Competitor or alternative facts
- Offer/product/service capabilities

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
positioning:
  frame: product | service | expertise | campaign | content | community
  category_or_context:
  owned_word:
  main_alternative:
  contrast:
  why_now:
  not_for:
    - audience:
      reason:
  tradeoffs:
    - chosen:
      sacrificed:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Use exactly one `owned_word`.
- Prefer a clear contrast over generic 'better' language.
- Name at least one non-fit audience or tradeoff when positioning is broad.

## Failure / retry behavior
If competitor facts are missing, position against the current workaround or status quo.
