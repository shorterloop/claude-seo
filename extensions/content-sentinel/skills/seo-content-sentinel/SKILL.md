---
name: seo-content-sentinel
description: "Voice principles, protected lexicon, banned phrases, and brand alignment check. Compares page content to brand specifications and outputs a voice score and audit rubric. Use when user says \"brand voice\", \"voice check\", \"content-sentinel\", \"banned phrases\", \"tone check\", or \"voice audit\"."
argument-hint: "[url|file]"
user-invocable: true
license: MIT
compatibility: "Requires the content-sentinel extension to be installed."
metadata:
  author: Kinshuk
  version: "2.3.0"
  category: seo
---

# Brand Voice & Content Sentinel Auditor (Extension)

Analyze main content text against the protected lexicon, brand voice principles, a scoring rubric, and signature checks.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo content-sentinel <url>` | Fetch page, run lexicon + spelling/banned-phrase checks, then LLM-based rubric analysis |
| `/seo content-sentinel <file>` | Audit a local text draft against voice guidelines |

## Workflow (order matters)

1. **Load `${CLAUDE_SKILL_DIR}/references/lexicon.md` FIRST**, before any terminology or abstraction analysis. Protected Terms are never flagged as jargon and never appear in rename/replace recommendations. Never suggest generic category substitutes (e.g., "product management platform", "evidence-based product management") for a Protected Term. Instead, apply the lexicon's earning rules: a Protected Term used without being defined, demonstrated, or linked on-page gets `unearned_term:<term>` and a recommendation to earn it — never to remove it. Internal-Only Terms found on public pages get `internal_term_leak:<term>` (critical).
2. Determine page type (marketing / blog / docs) from URL pattern or user input.
3. Load `${CLAUDE_SKILL_DIR}/references/principles.md` and run deterministic checks: American English (flag `behaviour`, `realise`, etc.), banned phrases, unverified statistics.
4. For marketing page types, also load `${CLAUDE_SKILL_DIR}/references/web-copy.md` and apply its register and scoring adjustments (fragments/triads are on-register; CTA block is the ending; competitor-paste test).
5. Load `${CLAUDE_SKILL_DIR}/references/rubric.md` and score all applicable dimensions.
6. If a recommendation is triggered, load `${CLAUDE_SKILL_DIR}/references/signatures-v1.md` and draft it in the voice.

## Voice Principles (summary — principles.md is authoritative)

- **Language**: American English spelling and idiom.
- **Earned Authority**: Claims come from concrete experience or visible reasoning.
- **Concrete consequences**: Abstraction without anyone affected is off-voice.
- **Plain Language**: Short/medium sentences, natural contractions, plain nouns/verbs.
- **Banned Phrases**: "in today's fast-paced world", "game-changer", "paradigm shift", etc. (full list in principles.md). Protected Terms are exempt.

## Scoring Rubric

Each dimension is scored 1–5 (see rubric.md for anchors):
1. **specificity** · 2. **earned_pov** · 3. **directness** · 4. **intellectual_honesty** · 5. **human_stakes** · 6. **structure** · 7. **humor_personality** · 8. **ending**

*Exemptions*: docs pages omit `humor_personality` and `ending` (excluded from the mean). Marketing pages use the web-copy.md scoring adjustments.

## Output Contract

Return valid JSON matching this schema:

```json
{
  "scores": {
    "specificity": 0,
    "earned_pov": 0,
    "directness": 0,
    "intellectual_honesty": 0,
    "human_stakes": 0,
    "structure": 0,
    "humor_personality": 0,
    "ending": 0
  },
  "flags": [
    "banned_phrase:<phrase>",
    "unverified_statistic",
    "british_spelling",
    "invented_certainty",
    "abstract_no_consequence",
    "generic_ending",
    "unearned_term:<term>",
    "internal_term_leak:<term>"
  ],
  "worst_dimension": "<dimension_key>",
  "evidence": {
    "<failing_dimension>": "<quoted phrase, under 15 words>"
  }
}
```

If the extracted text is too short or garbled to judge (<100 words of real prose), return `{"error": "insufficient_content"}` instead of guessing.

Interpretation: mean ≥ 4.2 strong match; 3.2–4.1 acceptable; mean < 3.2 OR any dimension ≤ 2 OR any `internal_term_leak` triggers a recommendation.

## Rewriting & Voice Signatures

When drafting recommendations: obey principles.md and lexicon.md absolutely; use web-copy.md register for marketing pages; then emulate at most 1–2 signatures from signatures-v1.md (market casualties, numbers as rhetoric, personified artifacts, parenthetical verdicts). Never rewrite, tighten, or paraphrase a Protected Verbatim Line.

## References expected in ${CLAUDE_SKILL_DIR}/references/

lexicon.md · principles.md · web-copy.md · rubric.md · signatures-v1.md