---
name: page-objection-risk
description: Identify and answer the risks that prevent visitors from taking the next action
triggers:
  - page objections
  - FAQ
  - risk reversal
  - conversion blockers
argument-hint: "<PageBrief audience/offer>"
---

# page-objection-risk Skill

## Purpose
Pre-answer the visitor's real reasons not to act.

## When to activate
Use this skill when the page-production pipeline needs to identify and answer the risks that prevent visitors from taking the next action.

## Inputs
- PageBrief.audience.objections
- Pricing, onboarding, process, security, support, compatibility, or policy facts

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
objection_blocks:
  - objection:
    answer:
    proof_or_policy_needed:
    page_placement:
faq:
  - question:
    answer:
    evidence_status: evidence | inference | unknown
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Reject filler FAQs.
- Address price, time, trust, difficulty, fit, and risk when relevant.
- Do not invent policy, guarantee, support, or security terms.

## Failure / retry behavior
If policy facts are unknown, write the objection as a missing input instead of an answer.
