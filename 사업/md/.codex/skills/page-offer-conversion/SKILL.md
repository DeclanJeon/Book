---
name: page-offer-conversion
description: Design offer/value framing, commitment level, pricing context, and risk reversal
triggers:
  - page offer
  - conversion offer
  - pricing framing
  - risk reversal
argument-hint: "<PageBrief page_goal/audience>"
---

# page-offer-conversion Skill

## Purpose
Make the next action feel economically and practically justified.

## When to activate
Use this skill when the page-production pipeline needs to design offer/value framing, commitment level, pricing context, and risk reversal.

## Inputs
- PageBrief.page_goal
- Offer/product/service facts
- PageBrief.audience.desired_outcome
- Pricing, guarantee, deadline, or commitment facts

## Constraints
- Do not invent proof, metrics, testimonials, logos, credentials, or user claims.
- Mark uncertainty explicitly as `evidence`, `inference`, or `unknown`.
- Preserve upstream locked decisions; do not silently re-position the page.
- Respect `PageBrief.metadata.page_type` and `PageBrief.page_goal`.
- Return only the requested schema plus concise notes.

## Output schema

```yaml
offer_blocks:
  - offer_name:
    included_value:
    expected_outcome:
    cost_or_commitment:
    risk_reversal:
    urgency_or_deadline:
    page_type_mechanics:
      trial_terms:
      booking_qualification:
      lead_magnet_delivery:
      privacy_or_consent:
      unsubscribe_or_cancel:
      what_happens_after_submit:
    evidence_status: evidence | inference | unknown
```

## Workflow
1. Read upstream `PageBrief` fields required by this skill.
2. Preserve locked upstream decisions.
3. Produce only the schema above plus concise notes if needed.
4. Mark missing or uncertain inputs explicitly.
5. Run the quality gate before returning.

## Quality gate
- Use urgency or scarcity only when factual.
- Connect price/cost/commitment to expected value or outcome.
- Do not add guarantees that are not provided.
- Trial/signup pages must capture trial length, payment requirement, cancellation terms, setup expectation, and what happens after signup or mark them unknown.
- Consultation/booking pages must distinguish booking qualification, scope, price visibility, and next step; price may be nonblocking only if the page intentionally qualifies first.
- Lead magnets and email courses must cover delivery format/cadence, privacy or consent copy, unsubscribe expectation, and what happens after submit.
- Free offers still have friction: time cost, inbox trust, spam/privacy, and relevance must be handled.

## Failure / retry behavior
If offer details are incomplete, identify the minimum needed to publish.
