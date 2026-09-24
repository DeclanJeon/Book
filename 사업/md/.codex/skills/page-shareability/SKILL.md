---
name: page-shareability
description: Design share-worthy message, artifact, trigger, or referral mechanism when appropriate
triggers:
  - page shareability
  - word of mouth
  - share artifact
  - referral CTA
argument-hint: "<PageBrief message/product-output>"
---

# page-shareability Skill

## Purpose
Create a credible reason for visitors or users to share the page, result, or artifact.

## When to activate
Use this skill when the page-production pipeline needs to design share-worthy message, artifact, trigger, or referral mechanism when appropriate.

## Inputs
- PageBrief.message
- Product/service/content outputs
- Audience social context
- PageBrief.page_goal

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
share_blocks:
  - talker:
    topic:
    trigger:
    shareable_artifact:
    social_currency:
    referral_or_invite_cta:
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Share mechanism must support the page goal.
- Do not use fake scarcity or manipulative viral loops.
- If sharing is not natural for the page type, say so and omit the block.

## Failure / retry behavior
If no credible share mechanism exists, return an empty list with rationale.
