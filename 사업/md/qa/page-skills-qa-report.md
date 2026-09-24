# UltraQA Report — Page Production Skills

## Goal and success criteria
- Goal: Test whether the page-production skills actually improve page briefs toward pages that can sell, then fix defects found by QA.
- Success criteria:
  - External web criteria define what “sales-ready” means.
  - Skills block unsupported proof, vague promises, fake urgency, and page-type mismatches.
  - Skills produce better briefs than naive one-shot page prompts across multiple page types.
  - QA defects found during dry-runs are patched in the skill files.
- Safety bounds applied:
  - No production publishing.
  - No fake customer proof, metrics, logos, testimonials, or security claims.
  - No destructive commands.
  - Dry-run outputs are treated as sales-readiness proxies, not proof of real revenue.

## External criteria used

| Criterion | Source evidence | QA interpretation |
|---|---|---|
| Clear value proposition fast | Nielsen Norman Group: users make harsh stay/leave judgments in the first seconds; pages must communicate value proposition within 10 seconds. Source: https://www.nngroup.com/articles/how-long-do-users-stay-on-web-pages/ | Hero must make audience, problem, outcome, and CTA clear in first screen. |
| Single conversion goal, above-fold CTA, message match, authentic social proof, product/service in action, speed/mobile, A/B testing | Unbounce landing page best practices: message match, action above fold, show product/service in action, remove distractions, authentic social proof, clear copy, speed, right device, A/B testing. Source: https://unbounce.com/landing-page-articles/landing-page-best-practices/ | Page brief must lock one goal, one primary CTA, source-message fit, demonstration, proof, low distraction, mobile/speed and experiment plan. |
| Performance thresholds | web.dev Core Web Vitals: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1 at 75th percentile; Core Web Vitals apply to all pages. Source: https://web.dev/articles/vitals | Implementation notes must include fast critical content and CWV targets when implementation is in scope. |
| Accessibility | W3C WAI accessibility principles: text alternatives, adaptable content, contrast/readability, keyboard-accessible functionality, sufficient time and motion controls. Source: https://www.w3.org/WAI/fundamentals/accessibility-principles/ | Final brief must require semantic headings, alt text, keyboard/focus behavior, contrast, reduced motion / non-motion dependence where relevant. |

## Scenario matrix

| ID | User/attacker model | Scenario | Harness | Expected signal | Actual result | Status | Evidence | Cleanup |
|---|---|---|---|---|---|---|---|
| STATIC-001 | Maintainer using skills later | All `page-*` skills have required sections and matching names | Python static scanner | 15 files, no missing required sections, frontmatter names match directories | 15 files, no missing sections, no name mismatches | PASS | eval output: `skill count: 15`, `missing sections: none`, `frontmatter issues: none` | No temp files |
| ADV-001 | Hostile marketer tries fake proof and multiple CTAs | Adversarial PageBrief with fake Nike/Apple logos, multiple goals, fake urgency, vague audience | LLM QA harness using `page-conversion-qa` | QA must fail and return exact `page-*` rerun skills | Failed with score 5, blocked unsupported logos/superlatives, multiple goals, weak CTAs, missing demo/objections/mobile/measurement; rerun names all valid `page-*` | PASS after fix | eval output from `Retesting QA routing` | No temp files |
| ADV-002 | Lead magnet owner tries revenue claims without proof | Email-course brief with unknown traffic source, missing quote permission, MRR claim, unknown privacy/delivery | LLM QA harness using patched `page-conversion-qa` | QA must fail for message-match unknown, unsupported revenue, testimonial missing permission, lead magnet mechanics unknown | Failed and routed to `page-evidence-intake`, `page-goal`, `page-hero-cta`, `page-demonstration`, `page-proof-trust`, `page-offer-conversion` | PASS | eval output from `Testing lead magnet QA` | No temp files |
| DRY-SaaS | Founder building SaaS homepage | LedgerPilot AI trial signup page | Task dry-run through skills | More specific than generic SaaS page; blocks logos/security/certification claims | PASS as blocked/draft sales-ready brief; not publish-ready until security/setup/trial facts supplied | PASS WITH BLOCKERS | `agent://DryRunSaaS` | No edits by agent |
| DRY-Service | Consultant building service page | SignalOps Studio qualified booking page | Task dry-run through skills | One booking CTA, proof mapped to testimonials/examples, no uplift claims | PASS with constraints; blocks revenue/conversion lift and invented trust claims | PASS | `agent://DryRunService` | No edits by agent |
| DRY-Content | Lead magnet creator | Founder Pricing Teardown email course page | Task dry-run through skills | One email opt-in goal, sample value shown, no revenue guarantee | PASS directionally; blocks MRR/revenue claims and requires course/privacy/quote details before publish | PASS WITH BLOCKERS | `agent://DryRunContent` | No edits by agent |

## Dry-run findings

### DRY-SaaS — LedgerPilot AI
- Improved over naive generic SaaS brief by forcing:
  - Narrow audience: 10-50 person ecommerce operators reconciling Stripe, Shopify, and bank feeds.
  - One CTA: trial signup.
  - Concrete demo: reconciliation dashboard walkthrough.
  - Safe proof wording: “Beta stores reported saving an average 4 hours/week in founder interviews.”
  - Blocked claims: public logos, SOC2/bank-grade security, guaranteed savings, perfect accuracy, every-bank support, no setup.
- Remaining blockers:
  - Traffic source unknown, so message match can only partially pass.
  - Security, setup, trial terms, supported banks/accounting tools missing.

### DRY-Service — SignalOps Studio
- Improved over naive consultant page by forcing:
  - Specific ICP: bootstrapped B2B founders with confusing homepages.
  - One CTA: book a homepage diagnosis call.
  - Position: 10-day homepage clarity sprint.
  - Demonstration: before/after examples and process document.
  - Proof discipline: exact named testimonials only; anonymized examples cannot imply revenue/conversion uplift.
  - Measurement plan: booking submit, qualified-booking rate, CTA/example/process/testimonial events.
- Remaining blockers:
  - Exact testimonial wording/permission required.
  - Pricing/guarantee/scheduling policy unknown.

### DRY-Content — The Founder Pricing Teardown
- Improved over naive newsletter signup by forcing:
  - Specific lead magnet: pricing-page teardown course.
  - One CTA: email subscription.
  - Demonstration: sample teardown screenshot.
  - Proof discipline: 47 analyzed pages supports research activity, not revenue uplift.
  - Objections: no revenue guarantee, time required, fit, privacy/spam.
  - Measurement plan: CTA, form submit/error, screenshot engagement, source/UTM, lesson engagement.
- Remaining blockers:
  - Course cadence/content, exact quote/permission, traffic-source promise, privacy/unsubscribe mechanics missing.

## Failures found and fixes applied

| Failure | Impact | Fix applied |
|---|---|---|
| `page-orchestrator` lacked standard Inputs/Workflow/Output/Quality/Retry sections | Orchestrator was weaker than individual skills | Added missing sections and sales-readiness benchmark to `.codex/skills/page-orchestrator/SKILL.md`. |
| QA returned generic rerun names instead of exact skill IDs | Automation handoff would break | Added `skills_to_rerun` schema and exact allowed `page-*` names to `.codex/skills/page-conversion-qa/SKILL.md`; retest passed with valid names. |
| Sales-readiness criteria were too implicit | Skills could produce “complete” but not conversion-ready briefs | Added sales-readiness schema/checks to `page-conversion-qa`, `page-final-brief`, `page-architecture`, and `page-orchestrator`. |
| Message match lacked first-class traffic-source input | QA could pass internal consistency while acquisition promise is unknown | Added `traffic_source_promises` to `page-evidence-intake` and `traffic_source` to `page-goal`; QA now marks unknown source as partial/unknown. |
| Proof assets lacked permission/evidence-kind granularity | Testimonials, anonymized examples, and interview metrics could be overclaimed | Added `permission_status`, `evidence_kind`, `allowed_wording`, and `safe_revision` to evidence/proof skills. |
| Lead magnet/free offer mechanics were underspecified | Email-course pages could omit privacy, cadence, unsubscribe, after-submit flow | Added page-type mechanics to `page-offer-conversion`: trial terms, booking qualification, lead magnet delivery, privacy/consent, unsubscribe/cancel, after-submit. |
| Design source became stale after skill patches | Future changes could follow old schema | Updated `DESIGN.md` with QA-validated sales-readiness additions. |

## Files changed
- `DESIGN.md`
- `.codex/skills/page-orchestrator/SKILL.md`
- `.codex/skills/page-conversion-qa/SKILL.md`
- `.codex/skills/page-architecture/SKILL.md`
- `.codex/skills/page-final-brief/SKILL.md`
- `.codex/skills/page-evidence-intake/SKILL.md`
- `.codex/skills/page-goal/SKILL.md`
- `.codex/skills/page-proof-trust/SKILL.md`
- `.codex/skills/page-offer-conversion/SKILL.md`

## Commands / harnesses run
- Static Python scanner in `eval`: verified 15 skill files, required sections, frontmatter names.
- Adversarial QA completion harness `ADV-001`: fake proof / multiple goals / fake urgency.
- Adversarial QA completion harness `ADV-002`: lead magnet overclaim / unknown traffic / missing consent.
- Three read-only task dry-runs: `DryRunSaaS`, `DryRunService`, `DryRunContent`.

## Verdict
- The skills are effective as a **sales-ready page-brief generator** after the applied fixes.
- They reliably improve over naive one-shot prompts in the tested scenarios by narrowing audience, locking one goal, forcing proof discipline, requiring demonstration, handling objections, and adding measurement/accessibility/performance requirements.
- They do **not** prove that a real page will sell without traffic. The externally grounded standard requires publishing, measuring conversion events, and iterating/A-B testing. The skills now force that measurement plan into the final brief.

## Residual risks
- Real conversion rate cannot be verified until a page is implemented, launched, instrumented, and tested with target traffic.
- LLM-based dry-runs can show process behavior, not market truth.
- Exact proof assets still need human/source verification before publication.
- Implementation QA remains separate: Core Web Vitals, accessibility, responsive screenshots, and form/CTA behavior must be tested on the actual built page.
