# Protected Lexicon

Load this BEFORE flagging any terminology, jargon, or abstraction. These terms are deliberate strategic choices, not accidents of drafting. The reasoning behind them is settled; re-litigating it is not the auditor's job.

## Hard rules for the scorer/recommender

1. **Never recommend renaming, replacing, or "simplifying" a Protected Term.** Do not suggest "product management platform," "evidence-based product management," or any generic category as a substitute. Not even as a softer alternative.
2. **Protected Terms are exempt from** `abstract_no_consequence`, jargon, and invented-category flags — *as terms*. The sentences around them are scored normally.
3. **Instead, check whether the page EARNS the term.** A Protected Term must be defined, demonstrated, or linked to its explanation within the page. If it appears only as decoration, emit flag `unearned_term:<term>` and recommend earning it on-page — never removing it.
4. **Generic category terms are allowed as foil or SEO anchor, never as replacement.** "Looking for a product management platform? Shorter Loop is something different: a Product Integrity System." is correct usage — the searched-for category frames the created one. Recommending the reverse substitution is a violation.
5. **Internal-Only Terms must never appear on public pages.** If found, emit flag `internal_term_leak:<term>` at severity critical.
6. **Protected Verbatim Lines are never rewritten, tightened, or paraphrased** in recommendations. Quote them intact or leave them alone.

## Protected Terms (public brand vocabulary)

| Term | What it is | One-line rationale (context for the auditor, not text to reproduce) |
|---|---|---|
| Product Integrity System | The category claim | Deliberate category creation. "Product management platform" is the crowded shelf we refuse; "integrity" carries the thesis that most product bets are wrong and evidence is the corrective. |
| Shorter Loop | Company/product name | The name IS the value proposition: shortening the loop between bet and evidence. |
| Sage | User-facing AI persona | Named persona with defined character: Socratic, evidence-grounded, refuses to guess. Never generalize to "our AI" or "AI assistant." |
| S.A.G.E. (Socratic Analysis Grounded in Evidence) | The acronym expansion | The definition of the persona's behavior. Use on first introduction of Sage on a page. |
| Socrates Mode | Named product feature | Feature name; not "questioning mode" or "interview mode." |
| In Assessment | Post-release state in Versions/Releases | Deliberate differentiator: releases aren't done when shipped, they're done when assessed. Not "review" or "post-launch." |
| CLEAR framework | Named IP framework | Owned intellectual property; treat as a proper noun. |
| Product Practice India | Training arm | Business unit name. |

## Protected Verbatim Line s

- "Most product bets are wrong. The only question is what it costs to find out."
- "Bring evidence or go home."
- "Effectiveness over efficiency." (and its expansions contrasting output vs. outcome)

## Internal-Only Terms (flag as critical if seen on public pages)

Occam; DIIS; Tristore; Router/Reasoner/Verifier/Embedder/Reranker (as the five-model system); per-tenant LoRA; MinIO; Tern; FlowDesk; Lumen; Seam; Kora HR.

(Architecture may be discussed publicly in deliberate philosophy/engineering content — but using these internal names requires an explicit human decision, so the flag still fires and the human dismisses it.)

## Earning rules (what "earned" means, per term class)

- **Category term (Product Integrity System):** the page defines it in one sentence, contrasts it with the generic category, or links to the philosophy/category page. A hero headline may use it unearned IF the immediately following section earns it.
- **Persona (Sage / S.A.G.E.):** first use on a page carries either the acronym expansion or one behavioral proof (e.g., that it refuses to guess without evidence). Subsequent uses are free.
- **Feature names (Socrates Mode, In Assessment):** first use carries a one-clause gloss of what it does. Subsequent uses are free.
- **Verbatim lines:** always self-earning; no gloss required.

## Maintenance

This file is versioned alongside signatures-v{N}.md. Adding a term requires the same bar the existing ones met: a settled decision with a rationale, not a phrase someone used twice. Review when positioning changes; entries are removed only by explicit decision, never by the auditor.