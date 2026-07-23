# Voice Evaluation Rubric

Score each dimension 1–5. Anchors define 1 and 5; interpolate for 2–4. Judge only the main content text provided — not navigation, footers, or CTAs.

## Dimensions

**1. specificity**
1: Could apply to any company or team.
5: Contains concrete behaviors, actors, and consequences specific to the subject.

**2. earned_pov**
1: Generic advice with no visible reasoning.
5: The opinion clearly emerges from experience or a well-built argument.

**3. directness**
1: Corporate, diplomatic, and padded.
5: Clear, sharp, and plain-spoken without being careless.

**4. intellectual_honesty**
1: Sweeping claims, invented certainty, or unsupported numbers.
5: Distinguishes experience, inference, and evidence; confidence matches support.

**5. human_stakes**
1: Describes process, features, or activity in the abstract.
5: Shows what it means for customers, trust, morale, careers, quality, or money.

**6. structure**
1: Listicle or disconnected observations.
5: A coherent argument arc (e.g., belief → collision → principle → action, or apparent success → hidden failure → sharper test).

**7. humor_personality**
1: Sterile, or artificially jokey.
5: Occasional dry humor or personality that strengthens the point.

**8. ending**
1: Repeats the content or offers generic inspiration.
5: Leaves the reader with a memorable test, distinction, question, or action.

## Page-type exemptions

- **docs**: do not score `humor_personality` or `ending`; omit them from the mean.
- **marketing**, **blog**: score all eight dimensions.

## Output contract

Return only valid JSON:

```json
{
  "scores": {"specificity": 0, "earned_pov": 0, "directness": 0,
             "intellectual_honesty": 0, "human_stakes": 0,
             "structure": 0, "humor_personality": 0, "ending": 0},
  "flags": ["banned_phrase:<phrase>", "unverified_statistic", "british_spelling",
            "invented_certainty", "abstract_no_consequence", "generic_ending"],
  "worst_dimension": "<dimension_key>",
  "evidence": {"<failing_dimension>": "<quoted phrase, under 15 words>"}
}
```

Rules for the scorer:
- Quote at most one short phrase per failing dimension; never reproduce long passages.
- Omit exempted dimensions from `scores` entirely for docs pages.
- If the extracted text is too short or garbled to judge (<100 words of real prose), return `{"error": "insufficient_content"}` instead of guessing.
- Interpretation bands (computed downstream, listed here for humans): mean ≥4.2 strong match; 3.2–4.1 acceptable; <3.2 or any dimension ≤2 triggers a recommendation.
