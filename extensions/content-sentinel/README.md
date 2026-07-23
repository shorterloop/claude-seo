# Content Sentinel Voice Auditor Extension for Claude SEO

Audits page content drafts against brand voice guidelines, evaluates them using a scoring rubric, and applies signature moves for recommended rewrites.

## Prerequisites

- **Claude SEO** base installed (`~/.claude/skills/seo/`)
- **Python 3.10+** (in managed environment)

## Installation

```bash
./extensions/content-sentinel/install.sh
```

For Windows:
```powershell
.\extensions\content-sentinel\install.ps1
```

The installer will copy:
1. The `seo-content-sentinel` skill definition to `~/.claude/skills/seo-content-sentinel/`
2. The `seo-content-sentinel` subagent to `~/.claude/agents/`
3. Supporting Python audit scripts and voice guidelines references

## Commands

| Command | What it does |
|---------|-------------|
| `/seo content-sentinel <url>` | Fetches and audits a live web page |
| `/seo content-sentinel <file_path>` | Audits a local text draft against voice guidelines |

## Scoring & Rubric

Content is evaluated on 8 dimensions (scored 1 to 5):
1. **specificity**: Concrete details vs. generic advice.
2. **earned_pov**: Opinion derived from experience vs. unreasoned claims.
3. **directness**: Clear and plain-spoken vs. diplomatic corporate padding.
4. **intellectual_honesty**: Acknowledging evidence/inference vs. inventing certainty.
5. **human_stakes**: Showing impact on actors (customers, money, morale) vs. abstract process.
6. **structure**: Logical argument arc vs. listicles.
7. **humor_personality**: Natural dry humor vs. sterile corporate tone.
8. **ending**: Memorably sharp closing distinction/diagnostic vs. summary recaps.

*Exemptions*: Docs pages omit `humor_personality` and `ending` from the scores and mean calculations.

## Audit Integration

During `/seo audit`, if the Content Sentinel extension is installed, the orchestrator spawns the `seo-content-sentinel` subagent alongside standard checks to perform a full brand-alignment check on the site's content.

## Uninstallation

```bash
./extensions/content-sentinel/uninstall.sh
```
