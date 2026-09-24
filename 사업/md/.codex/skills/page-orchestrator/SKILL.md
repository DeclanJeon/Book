---
name: page-orchestrator
description: Run the full page-production skill pipeline from evidence intake to final brief
triggers:
  - page production
  - create page brief
  - landing page strategy
  - page skill pipeline
  - landing page
  - sales page
  - service page
  - product page
  - homepage
  - website copy
  - conversion page
  - lead magnet
  - page brief
  - CTA strategy
argument-hint: "<page project materials>"
---

# page-orchestrator Skill

## Purpose
Coordinate page-* skills in the correct order, preserve locked decisions, run QA, and assemble the final brief.

## When to activate
Use this skill when the user wants a page strategy, landing page brief, website page plan, sales page plan, product/service page plan, or page-production agent workflow.

## Inputs
- Page project materials: product/service/person/campaign/content description.
- Existing evidence: customer notes, reviews, sales notes, current page, competitor or alternative pages.
- Proof assets: logos, metrics, testimonials, case studies, screenshots, credentials, portfolio, security, integrations, media, or results.
- Desired page type or business goal, if known.

## Supported page types
- SaaS homepage
- Landing page
- Product page
- Service page
- Sales page
- Personal/brand page
- Campaign page
- Freelancer/agency proposal page
- Content conversion page

## Shared object
All steps read and write a single `PageBrief` object. Never replace the object with unstructured prose.

```yaml
PageBrief:
  metadata:
    project_name:
    page_type:
    page_url:
    product_or_offer_stage:
    market_or_context:
    source_materials:
  evidence:
    factual_inputs: []
    audience_facts: []
    competitor_or_alternative_facts: []
    proof_assets: []
    unknowns: []
  page_goal:
    primary_goal:
    secondary_goals: []
    conversion_event:
    success_metric:
    non_goals: []
  audience:
    primary_audience:
    secondary_audiences: []
    situation:
    urgent_job:
    current_pain:
    desired_outcome:
    buying_or_action_trigger:
    objections: []
  positioning:
    frame:
    category_or_context:
    owned_word:
    main_alternative:
    contrast:
    not_for: []
    tradeoffs: []
  message:
    core_claim:
    repeatable_phrase:
    emotional_hook:
    concrete_scene:
    anti_jargon_rules: []
  page:
    section_order: []
    hero:
    cta_stack:
    demonstration_blocks: []
    proof_blocks: []
    objection_blocks: []
    offer_blocks: []
    share_blocks: []
  qa:
    unsupported_claims: []
    vague_phrases: []
    ethical_risks: []
    page_type_mismatches: []
    readiness_score:
```

## Execution order
1. `page-evidence-intake`
2. `page-goal`
3. `page-audience-jtbd`
4. `page-positioning`
5. `page-core-message`
6. `page-architecture`
7. `page-hero-cta`
8. `page-demonstration`
9. `page-proof-trust`
10. `page-objection-risk`
11. `page-offer-conversion`
12. `page-shareability`
13. `page-conversion-qa`
14. `page-final-brief`

## Parallelization
After `page-architecture` locks section order, these skills may run independently if their inputs exist:
- `page-demonstration`
- `page-proof-trust`
- `page-objection-risk`
- `page-offer-conversion`
- `page-shareability`

## Sales-readiness benchmark
The pipeline is considered useful only if it improves a page against these externally grounded checks:
- Clear value proposition visible within the first screen / first 10 seconds.
- One primary conversion goal and one matching primary CTA.
- Message match between traffic source, visitor expectation, headline, and offer.
- Product, service, process, sample, or result shown in action.
- Authentic proof near claims; unsupported proof blocks final assembly.
- Real objections answered before the final CTA.
- Mobile-first layout, fast critical content, accessible semantics, keyboard/focus/contrast/alt text, and Core Web Vitals targets when implementation is in scope.
- Measurement plan: conversion event, success metric, analytics events, and A/B or iteration plan.

## Retry rules
- If `page-conversion-qa` finds unsupported claims, return to `page-proof-trust` or remove the claim.
- If audience is too broad, return to `page-audience-jtbd`.
- If positioning has more than one owned word, return to `page-positioning`.
- If page type and CTA conflict, return to `page-goal` and then regenerate downstream fields.
- If hero copy is vague, return to `page-core-message` or `page-hero-cta` depending on source.

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.
- Do not skip `page-conversion-qa` before `page-final-brief`.
- Do not treat SaaS-specific sections as universal requirements.

## Workflow
1. Initialize or update a `PageBrief` object from the provided materials.
2. Run `page-evidence-intake` before strategy or copy work.
3. Run the locked sequence through `page-architecture`.
4. Run eligible downstream skills in parallel only after section order is locked.
5. Run `page-conversion-qa`.
6. If QA fails, return to the named upstream skill and regenerate affected downstream fields.
7. Run `page-final-brief` only after QA passes or after explicitly marking the brief as blocked.

## Output schema

```yaml
final_or_blocked_result:
  status: passed | blocked
  page_brief:
  qa_summary:
  skills_run: []
  skills_to_rerun: []
  final_brief:
```

## Quality gate
- The final output must include a coherent `PageBrief`, not disconnected copy suggestions.
- The page type, primary goal, audience, positioning, hero CTA, proof, and QA verdict must agree.
- Unsupported critical claims must block final assembly.
- The `sales_readiness` checks from `page-conversion-qa` must all pass or be listed as blockers.
- SaaS-specific sections must not appear on non-SaaS pages unless the page type reason justifies them.

## Failure / retry behavior
- If the pipeline lacks enough evidence, return `status: blocked` with exact missing inputs.
- If QA fails, do not produce a final brief; identify the upstream skill to rerun.
- If the user asks for speed over certainty, still mark unsupported claims and unknowns explicitly.

## Final output
Return a `final_brief` only when QA passes. If QA fails, return a blocked summary with the exact skill(s) to rerun.
