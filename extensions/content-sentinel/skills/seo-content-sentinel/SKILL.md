---
name: seo-content-sentinel
description: "Voice principles, banned phrases, and brand alignment check. Compares page content to brand specifications and outputs a voice score and audit rubric. Use when user says \"brand voice\", \"voice check\", \"content-sentinel\", \"banned phrases\", \"tone check\", or \"voice audit\"."
argument-hint: "[url|file]"
user-invocable: true
license: MIT
compatibility: "Requires the content-sentinel extension to be installed."
metadata:
  author: AgriciDaniel
  version: "2.2.4"
  category: seo
---

# Brand Voice & Content Sentinel Auditor (Extension)

Analyze main content text against brand voice principles, a specific scoring rubric, and signature checks.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo content-sentinel <url>` | Fetch page, run spelling/banned phrases check, and perform LLM-based rubric analysis |
| `/seo content-sentinel <file>` | Audit a local text draft against voice guidelines |

## Voice Principles

Read the full principles in `${CLAUDE_SKILL_DIR}/references/principles.md`. Key checks:
- **Language**: American English spelling and idioms. Flag British spelling (e.g. `behaviour`, `realise`).
- **Earned Authority**: Claims must come from concrete experience or visible reasoning.
- **Plain Language**: Short/medium sentences, natural contractions, plain nouns/verbs.
- **Banned Phrases**: Flag clichés like `"in today's fast-paced world"`, `"game-changer"`, `"paradigm shift"`, etc.
- **Web Register**: For marketing page types, apply the web-compress registers defined in `${CLAUDE_SKILL_DIR}/references/webpage-copy.md`.

## Scoring Rubric

Each dimension is scored 1–5 (see `${CLAUDE_SKILL_DIR}/references/rubric.md` for full details):
1. **specificity**: Generic vs. concrete behaviors/consequences.
2. **earned_pov**: Generic advice vs. emerges from experience.
3. **directness**: Corporate/diplomatic vs. clear/plain-spoken.
4. **intellectual_honesty**: Sweep claims/invented certainty vs. matched confidence/support.
5. **human_stakes**: Abstract process vs. impact on actors (customers, money, morale).
6. **structure**: Listicle vs. coherent argument arc.
7. **humor_personality**: Sterile vs. dry humor/personality.
8. **ending**: Generic recap vs. memorable diagnostic question/distinction.

*Exemptions*: Docs pages omit `humor_personality` and `ending`.

## Output Contract

The command returns valid JSON matching this schema:

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
    "generic_ending"
  ],
  "worst_dimension": "<dimension_key>",
  "evidence": {
    "<failing_dimension>": "<quoted phrase, under 15 words>"
  }
}
```

Interpretation: mean score &ge; 4.2 is a strong match, 3.2–4.1 is acceptable, and &le; 3.2 or any dimension &le; 2 triggers a recommendation.

## Rewriting & Voice Signatures

When recommending rewrites, refer to `${CLAUDE_SKILL_DIR}/references/signatures-v1.md` to emulate the target voice (e.g. concrete market casualties, numbers as rhetoric, personified artifacts, or two-word parenthetical verdicts). Never use more than 1 or 2 signatures per piece.
