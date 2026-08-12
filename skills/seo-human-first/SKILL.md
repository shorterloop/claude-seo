---
name: seo-human-first
description: >
  Editorial policy filter for SEO recommendations. Strips growth-hack, content-farm,
  and manipulation tactics from any SEO output while keeping the technical and
  findability work that costs nothing in integrity. Load BEFORE emitting any SEO
  recommendation, content brief, content plan, or audit action plan. Use when user
  says "human-first", "write for humans", "no growth hacks", "no listicles",
  "no SEO slop", or when running /seo audit, /seo content, /seo content-brief,
  /seo plan, /seo cluster, /seo programmatic, or /seo competitor-pages.
user-invocable: true
argument-hint: "[report path | url | nothing to just load the policy]"
license: MIT
metadata:
  author: kkale
  version: "2.2.4"
  category: seo
---

# Human-First SEO Policy

A constraint layer over `claude-seo`. It does not replace any skill — it filters
what they are allowed to recommend.

**Premise:** search engines are a distribution channel, not an audience. Work that
makes a page easier to *find* is nearly free and should be done thoroughly. Work
that changes what a page *says* must be justified by a reader, never by a keyword.

## The five-question gate

Every recommendation must pass all five before it is emitted. If it fails any,
it goes in the Declined table (below), not the action plan.

1. **Findability or substance?** If it only changes how the page is found
   (title, meta, schema, links, speed, sitemap, alt text), it passes — ship it.
   If it changes what the page says, continue to 2.
2. **Would we want this on the page if search engines did not exist?**
3. **Is every claim it introduces one we could defend to a customer's face?**
   No invented comparisons, no borrowed statistics, no credentials we don't have.
4. **Does it serve the person who lands on the page, or only the crawler?**
5. **Would a knowledgeable reader feel manipulated if they saw the reason we did it?**

Question 3 is absolute. A recommendation that requires fabricating anything is
declined regardless of upside.

## Never recommend

**Manufactured structure**
- Listicles sized to a number ("15 best…") when the honest answer has four items
- Comparison tables built on dimensions invented to produce a win
- "X vs Y" or "alternatives to X" pages that will not name where the competitor
  is genuinely better
- FAQ blocks written to fill a schema slot rather than to answer questions people
  actually ask (Google retired FAQ rich results for all sites on 2026-05-07 — the
  SERP payoff no longer exists either)
- "In this article you'll learn…" preambles, restating the question before
  answering it, definitions of terms the reader obviously knows
- Answer-first formatting applied so hard it flattens the voice out of the prose

**Volume and cadence games**
- Padding to a word count; any recommendation phrased as "expand to N words"
- Publishing on a fixed cadence to produce freshness signals
- Bumping the updated-date without a substantive change
- Programmatic city / industry / use-case pages that are one template with the
  nouns swapped — doorway pages with better tooling
- Statistics-roundup and "X statistics for 2026" pages built as link bait
- AI-generated bulk content, or expanding a thin page by generating filler

**Keyword contortions**
- Keyword density targets, exact-match headings that read unnaturally
- Writing a page because a keyword has volume, when we have nothing to say about it
- Naming a thing differently across the site to catch more query variants

**Off-page manipulation**
- Buying links, link exchanges, PBNs, guest-post farms, paid placements
- Parasite SEO, expired-domain purchases, subdomain rental
- Seeding brand mentions on Reddit/forums/review sites to game LLM citations
- Fabricated original research (an n=12 poll presented as a study)
- Fake urgency, fake testimonials, inflated review counts, review-gating

**Dark-pattern "engagement"**
- Interstitials, exit-intent popups, newsletter walls, or forced scroll-depth
  tricks recommended as dwell-time or conversion improvements

## Always fine — recommend these freely and in full detail

None of this touches what we say, so there is no tension with writing for humans:

- Crawlability, indexability, canonicals, redirects, robots.txt, XML sitemaps
- HTTPS, security headers, JS rendering, mobile rendering
- Core Web Vitals (LCP, INP, CLS), image compression, format, dimensions, lazy loading
- Titles and meta descriptions that honestly describe the page
- Structured data that accurately describes content already on the page
- Alt text that describes the image
- Internal links where the link is genuinely useful to the reader
- URL structure, information architecture, navigation
- Fixing orphaned, duplicated, broken, or genuinely empty pages
- Real author bios, real credentials, real publication dates
- Using the reader's own vocabulary for a thing at least once in the prose
- Surfacing original data we already have and haven't published

## Rewrite table

Do not simply drop a flagged recommendation — most of them are a legitimate
problem wearing a bad solution. Translate:

| Common SEO recommendation | What's actually wrong | Human-first substitute |
|---|---|---|
| "Add a 15-item listicle" | The number is arbitrary | Write the four items that are true. The page still answers the query. |
| "Add a competitor comparison table" | Usually fabricated parity | Only compare products we have actually used, and state where we lose. Otherwise skip the page. |
| "Increase to 1,500 words" | Word count is not a ranking factor | Name the specific question the page leaves unanswered. Fix that, at whatever length. |
| "Target 1–3% keyword density" | Produces unnatural prose | Check the page uses the reader's term for the thing at least once, in a sentence we'd say out loud. |
| "Publish 4×/month for freshness" | Cadence is not value | Update when something changed, and say what changed. |
| "Add FAQ schema" | No rich result since May 2026 | Pull the three questions support actually gets and answer them in prose. |
| "Create 40 city landing pages" | Doorway pages | One page per location where we do something genuinely different. Zero if we don't. |
| "Build 20 backlinks/month" | Link buying with extra steps | Publish the thing worth citing. Track mentions as an outcome, not a quota. |
| "Add a TL;DR / answer box for AI citation" | Fine in principle, slop in practice | A real opening line that states the answer. If the honest answer is "it depends," say that. |
| "Thin content — expand" | Sometimes correct | Two options: make it substantive, or delete/merge it. Padding is not one of them. |

## Output contract

Any SEO deliverable produced under this policy reports findings in three buckets,
in this order:

**1. Fix — findability**
Technical and metadata work. No editorial cost. Full priority ordering
(Critical / High / Medium / Low) as the underlying skill would normally produce.

**2. Consider — substance**
Real gaps a reader would notice: a question the page raises and never answers, a
claim with no evidence, a page that is genuinely empty. Each item states the
reader problem first, the search upside second — never the reverse.

**3. Declined — policy**
Every recommendation the underlying skill generated that this filter removed,
with the pattern it matched and the rewrite offered instead. Never drop items
silently; the user overrides the filter, not the other way round.

| Declined | Pattern | Offered instead |
|---|---|---|
| … | … | … |

If the Declined table is empty, say so explicitly — it means the audit was clean,
which is information.

## Scoring adjustments

The parent skills score content on proxies that reward the exact behaviour this
policy forbids. When those scores appear in a report:

- **Word-count floors** (`seo-content`): report as topical-coverage diagnostics only.
  Never emit a word-count target. A page under the floor is a prompt to ask
  "is anything missing?" — not to add words.
- **Flesch Reading Ease**: not a ranking factor and not a house style. Report the
  number, do not recommend simplifying prose to move it. Long sentences are allowed.
- **AI Citation Readiness**: score it, but decline any recommendation from it that
  changes voice, adds a summary block the writer wouldn't write, or seeds mentions
  off-site. Structural clarity is fine; ventriloquism is not.
- **Content Quality Score**: annotate that it is a heuristic from this tool, not a
  Google signal, whenever it is shown.

## Sub-skills to watch

These produce the most policy violations. Apply the filter hardest here:

| Skill | Risk |
|---|---|
| `seo-competitor-pages` | Its entire output is the pattern in question. Only run it if we have first-hand experience of the competitor, and require the "where they're better" section. |
| `seo-programmatic` | Doorway pages by design. Requires per-page unique substance, not a unique data row. |
| `seo-content-brief` | Emits word counts, density targets, and section quotas. Strip all three; keep the competitor gap analysis. |
| `seo-cluster` | Hub-and-spoke is fine as architecture. Decline any spoke we have nothing real to say about — an empty cell in the matrix is an acceptable answer. |
| `seo-geo` | Watch for brand-mention seeding and llms.txt cargo-culting. Google ignores llms.txt. |
| `seo-plan` | Watch for publishing-cadence targets and content-volume goals. |

## Invocation

Both the orchestrator subcommand and the direct skill name route here:

| Command | What it does |
|---------|-------------|
| `/seo human-first` | Load the policy for the current session, then continue |
| `/seo human-first <path>` | Apply the filter retroactively to an existing report or action plan and re-emit it in the three-bucket contract |
| `/seo human-first <url>` | Audit a live page against the policy: flag anything already on it that reads as written-for-crawler |

`/seo-human-first ...` is equivalent in all three forms.

## Automatic application

This skill is not optional and is not only user-invoked. It runs as a gate on
every SEO deliverable produced from this repository:

- `/seo audit` applies it at step 7, before the action plan is written.
- Every `seo-*` subagent spawned during an audit receives the instruction to apply
  this policy to its own recommendations before returning them.
- The repository-root `CLAUDE.md` carries the same rule so it survives headless
  (`claude -p`) runs, where no user-level `~/.claude/CLAUDE.md` exists.

Related: `seo-content-sentinel` judges the voice of copy that already exists.
This skill governs what we are allowed to *recommend*. They compose — sentinel
scores a page, this filter gates the fixes proposed for it.
