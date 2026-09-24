---
name: page-core-message
description: Compress positioning into a memorable, concrete, repeatable page message
triggers:
  - core message
  - headline strategy
  - sticky message
  - one sentence
argument-hint: "<PageBrief goal/audience/positioning>"
---

# page-core-message Skill

## Purpose
Create the one idea the visitor should remember and repeat.

## When to activate
Use this skill when the page-production pipeline needs to compress positioning into a memorable, concrete, repeatable page message.

## Inputs
- PageBrief.page_goal
- PageBrief.audience
- PageBrief.positioning

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
message:
  core_claim:
  one_sentence:
  repeatable_phrase:
  concrete_scene:
  emotional_hook:
  before_after:
    before:
    after:
  banned_phrases: []
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Center the visitor's change, not a feature list.
- Replace abstractions with a concrete scene.
- Add banned phrases that would dilute the positioning.

## Failure / retry behavior
If message options compete, select the one closest to the primary conversion event.
