---
name: seo-audit
description: "Full website SEO audit with parallel subagent delegation. Crawls up to 500 pages, detects business type, delegates to up to 15 specialists (8 always + 7 conditional), generates health score. Use when user says audit, full SEO check, analyze my site, or website health check."
user-invocable: true
argument-hint: "[url]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "2.2.4"
  category: seo
---

# Full Website SEO Audit

## Process

1. **Render homepage**: use `claude-seo run render_page.py <url> --mode auto --json` to capture raw HTML, rendered HTML, extracted text, SPA status, and accessibility data when needed
2. **Detect business type**: analyze homepage signals per seo orchestrator
3. **Crawl site**: follow internal links up to 500 pages, respect robots.txt
4. **Delegate to subagents** (if available, otherwise run inline sequentially). Include
   in every subagent prompt: "Apply the seo-human-first policy at
   `skills/seo-human-first/SKILL.md` to your recommendations before returning them."
   - `seo-technical` -- robots.txt, sitemaps, canonicals, Core Web Vitals, security headers
   - `seo-content` -- E-E-A-T, readability, thin content, AI citation readiness
   - `seo-schema` -- detection, validation, generation recommendations
   - `seo-sitemap` -- structure analysis, quality gates, missing pages
   - `seo-performance` -- LCP, INP, CLS measurements
   - `seo-visual` -- screenshots, mobile testing, above-fold analysis
   - `seo-geo` -- AI crawler access, llms.txt, citability, brand mention signals
   - `seo-local` -- GBP signals, NAP consistency, reviews, local schema, industry-specific local factors (spawn when Local Service industry detected: brick-and-mortar, SAB, or hybrid business type)
   - `seo-maps` -- Geo-grid rank tracking, GBP audit, review intelligence, competitor radius mapping (spawn when Local Service detected AND DataForSEO MCP available)
   - `seo-google` -- CWV field data (CrUX), URL indexation (GSC), organic traffic (GA4) (spawn when Google API credentials detected via `claude-seo run google_auth.py --check`)
   - `seo-backlinks` -- Backlink profile data: DA/PA, referring domains, anchor text, toxic links (spawn when Moz or Bing API credentials detected via `claude-seo run backlinks_auth.py --check`, or always include Common Crawl domain-level metrics)
   - `seo-cluster` -- Semantic clustering analysis (spawn when content strategy signals detected: blog, pillar pages, topic clusters)
   - `seo-sxo` -- Search experience analysis: page-type mismatch, user stories, persona scoring (always include in full audits)
   - `seo-drift` -- Drift analysis: compare against stored baseline (spawn when drift baseline exists for the URL via `claude-seo run drift_history.py <url>`)
   - `seo-ecommerce` -- Product schema, marketplace intelligence (spawn when E-commerce industry detected)
   - `seo-content-sentinel` -- Brand voice, banned phrases, and style audit (spawn when content-sentinel extension is installed)
5. **Score** -- aggregate into SEO Health Score (0-100)
6. **Persist audit artifacts** -- write all outputs under `{domain}-audit/`. Specialist
   findings and raw data are final here; the action plan and the envelope's policy
   fields are not, because the filter has not run yet
7. **Filter** -- load `skills/seo-human-first/SKILL.md` and gate every recommendation
   through the five-question policy. Failures move to the Declined table with the
   pattern matched and the rewrite offered, never dropped silently
8. **Report** -- generate the action plan in the three-bucket contract (Fix / Consider /
   Declined) and optional PDF/HTML report. Write the same contract into
   `audit-data.json` as data (`bucket`, `declined`, `policy`) so the buckets do not
   exist only as markdown headings -- step 6's artifacts are rewritten here, after
   the filter, not before it

## Crawl Configuration

```
Max pages: 500
Respect robots.txt: Yes
Follow redirects: Yes (max 3 hops)
Timeout per page: 30 seconds
Concurrent requests: 5
Delay between requests: 1 second
```

## Output Files

- `{domain}-audit/FULL-AUDIT-REPORT.md`: Comprehensive findings
- `{domain}-audit/ACTION-PLAN.md`: Three-bucket action plan -- **Fix** (findability; prioritized Critical > High > Medium > Low), **Consider** (substance; reader problem stated first), **Declined** (policy; pattern matched + rewrite offered). An empty Declined table is stated explicitly, not omitted
- `{domain}-audit/audit-data.json`: Structured audit envelope for report generation and for downstream tooling. Carries the same three-bucket contract as data: `bucket` on every finding, an always-present `declined` array, and a `policy` block recording that the gate ran
- `{domain}-audit/findings/*.md`: Per-category specialist findings (`technical.md`, `content.md`, `schema.md`, `performance.md`, `visual.md`, etc.)
- `{domain}-audit/screenshots/`: Desktop + mobile captures (if Playwright available)
- **PDF Report** (recommended): Generate a professional A4 PDF using `claude-seo run google_report.py --type full --data {domain}-audit/audit-data.json --domain <domain> --output-dir {domain}-audit/`. This produces a white-cover enterprise report with TOC, executive summary, charts (Lighthouse gauges, query bars, index donut), metric cards, threshold tables, prioritized recommendations with effort estimates, and implementation roadmap. Always offer PDF generation after completing an audit.

## Structured Audit Data Envelope

Write `{domain}-audit/audit-data.json` with this shape so `claude-seo run google_report.py --type full --data {domain}-audit/audit-data.json --domain <domain> --output-dir {domain}-audit/` can generate a report even when Google API data is unavailable:

```json
{
  "summary": {
    "health_score": 0,
    "business_type": "detected type",
    "top_findings": [],
    "quick_wins": []
  },
  "policy": {
    "skill": "seo-human-first",
    "version": "2.2.4",
    "applied": true
  },
  "categories": [
    {
      "name": "Technical SEO",
      "score": 0,
      "what_works": [],
      "findings": [
        {
          "title": "Finding title",
          "bucket": "fix|consider",
          "severity": "Critical|High|Medium|Low|Info",
          "description": "Evidence-backed detail",
          "recommendation": "Specific fix",
          "urls": ["/path/the/finding/applies/to"]
        }
      ]
    }
  ],
  "declined": [
    {
      "recommendation": "The recommendation as the underlying skill generated it",
      "pattern": "The policy pattern it matched",
      "offered_instead": "The rewrite offered, or null if the policy offers none",
      "source": "seo-content-brief"
    }
  ],
  "action_plan": {
    "phases": [
      {"name": "Phase 1: Critical Fixes", "timeframe": "Week 1", "items": []},
      {"name": "Phase 2: High-Impact Improvements", "timeframe": "Weeks 2-3", "items": []},
      {"name": "Phase 3: Content & Authority", "timeframe": "Month 2", "items": []},
      {"name": "Phase 4: Monitoring & Iteration", "timeframe": "Ongoing", "items": []}
    ]
  },
  "artifacts": {
    "findings_dir": "findings/",
    "screenshots_dir": "screenshots/"
  }
}
```

### The policy fields are not optional

`ACTION-PLAN.md` states the three-bucket contract in prose. The envelope states
the same contract as data, so a downstream consumer never has to parse headings
to learn which bucket a finding landed in.

- **`bucket`** on every finding. `fix` -- the change only affects how the page is
  found (question 1 of the policy). `consider` -- it changes what the page says
  and passed all five questions. A recommendation that failed the gate is not a
  finding at all; it belongs in `declined`.
- **`declined`** is always present. Write `[]` when nothing was declined; never
  omit the key. An absent `declined` and an empty one must not read the same --
  one says the filter ran and removed nothing, the other says nothing at all
  about whether it ran. Same rule as the Declined table in the markdown.
- **`policy.applied`** records that the gate ran. An envelope carrying no
  `policy` block was produced without the filter, and a consumer should treat its
  recommendations as unfiltered rather than as clean.
- **`urls`** on every finding: the pages it applies to, as site-relative paths.
  Write `[]` for a genuinely sitewide finding, and list every affected page for a
  finding that spans several -- do not write one entry and describe the rest in
  the title. Never omit the key. A finding nobody can locate cannot be applied,
  verified, or reverted, and "applies everywhere" and "nobody wrote it down" must
  not arrive looking the same.

Each `declined` entry mirrors a row of the policy's Declined table, plus
`source`: the sub-skill whose output the recommendation came from, so a
repeatedly-filtered skill is visible rather than merely quiet.

## Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

## Report Structure

### Executive Summary
- Overall SEO Health Score (0-100)
- Business type detected
- Top 5 critical issues
- Top 5 quick wins

### Technical SEO
- Crawlability issues
- Indexability problems
- Security concerns
- Core Web Vitals status

### Content Quality
- E-E-A-T assessment
- Thin content pages
- Duplicate content issues
- Readability scores

### On-Page SEO
- Title tag issues
- Meta description problems
- Heading structure
- Internal linking gaps

### Schema & Structured Data
- Current implementation
- Validation errors
- Missing opportunities

### Performance
- LCP, INP, CLS scores
- Resource optimization needs
- Third-party script impact

### Images
- Missing alt text
- Oversized images
- Format recommendations

### AI Search Readiness
- Citability score
- Structural improvements
- Authority signals

## Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, spawn the `seo-dataforseo` agent alongside existing subagents to enrich the audit with live data: real SERP positions, backlink profiles with spam scores, on-page analysis (Lighthouse), business listings, and AI visibility checks (ChatGPT scraper, LLM mentions).

## Google API Integration (Optional)

If Google API credentials are configured (`claude-seo run google_auth.py --check`), spawn the `seo-google` agent to enrich the audit with real Google field data: CrUX Core Web Vitals (replaces lab-only estimates), GSC URL indexation status, search performance (clicks, impressions, CTR), and GA4 organic traffic trends. The Performance (CWV) category score benefits most from field data.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| robots.txt blocks crawling | Report which paths are blocked. Analyze only accessible pages and note the limitation in the report. |
| Rate limiting (429 responses) | Back off and reduce concurrent requests. Report partial results with a note on which sections could not be completed. |
| Timeout on large sites (500+ pages) | Cap the crawl at the timeout limit. Report findings for pages crawled and estimate total site scope. |
