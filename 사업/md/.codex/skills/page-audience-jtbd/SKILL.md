---
name: page-audience-jtbd
description: Define the specific visitor, situation, job, trigger, desired outcome, and objections
triggers:
  - page audience
  - jtbd
  - visitor job
  - customer situation
argument-hint: "<PageBrief evidence/page_goal>"
---

# page-audience-jtbd Skill

## Purpose
Identify who should act on the page and why now.

## When to activate
Use this skill when the page-production pipeline needs to define the specific visitor, situation, job, trigger, desired outcome, and objections.

## Inputs
- PageBrief.page_goal
- PageBrief.evidence.audience_facts
- PageBrief.evidence.unknowns

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
audience:
  primary_audience:
  secondary_audiences: []
  situation:
  urgent_job:
  current_pain:
  desired_outcome:
  buying_or_action_trigger:
  success_metric:
  objections:
    - objection:
      severity: high | medium | low
      evidence:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Reject audiences like 'everyone', 'all teams', or 'people interested in X'.
- The audience must have a concrete action context.
- Objections must be plausible for the page type and conversion event.

## Failure / retry behavior
If audience evidence is weak, produce a narrow inferred audience and mark confidence low.
