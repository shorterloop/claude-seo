"""Static instruction guards for full audit persistence and SPA wiring."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_seo_audit_starts_with_render_page_auto() -> None:
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    process = text[text.index("## Process"):text.index("## Crawl Configuration")]
    assert "claude-seo run render_page.py" in process
    assert "python3 scripts/render_page.py" not in process
    assert "--mode auto" in process
    assert "scripts/fetch_page.py` to retrieve HTML" not in process


def test_seo_audit_requires_persistent_artifacts() -> None:
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    for artifact in (
        "FULL-AUDIT-REPORT.md",
        "ACTION-PLAN.md",
        "audit-data.json",
        "findings/",
        "screenshots/",
    ):
        assert artifact in text
    assert "{domain}-audit" in text


def test_audit_agents_use_renderer_or_capture_script() -> None:
    expectations = {
        "seo-performance.md": "render_page.py",
        "seo-visual.md": "capture_screenshot.py",
        "seo-technical.md": "render_page.py",
        "seo-content.md": "render_page.py",
        "seo-schema.md": "render_page.py",
    }
    for filename, marker in expectations.items():
        text = (REPO_ROOT / "agents" / filename).read_text(encoding="utf-8")
        assert marker in text, f"{filename} must mention {marker}"


def test_audit_agents_document_output_dir_findings_contract() -> None:
    for filename in (
        "seo-performance.md",
        "seo-visual.md",
        "seo-technical.md",
        "seo-content.md",
        "seo-schema.md",
        "seo-sitemap.md",
        "seo-geo.md",
        "seo-local.md",
        "seo-maps.md",
        "seo-google.md",
        "seo-backlinks.md",
        "seo-cluster.md",
        "seo-sxo.md",
        "seo-drift.md",
        "seo-ecommerce.md",
    ):
        text = (REPO_ROOT / "agents" / filename).read_text(encoding="utf-8")
        assert "output_dir" in text
        assert "findings/" in text


def test_seo_audit_report_command_keeps_outputs_in_audit_dir() -> None:
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    assert "--output-dir {domain}-audit/" in text


def test_audit_envelope_carries_the_three_bucket_contract() -> None:
    """The buckets must exist as data, not only as markdown headings.

    ACTION-PLAN.md states the contract in prose. A downstream consumer reading
    audit-data.json would otherwise have to parse headings to learn which bucket
    a finding landed in, or -- worse -- read an ungated envelope as a clean one.
    """
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    envelope = text[text.index("## Structured Audit Data Envelope"):text.index("## Scoring Weights")]
    assert '"bucket": "fix|consider"' in envelope
    assert '"declined"' in envelope
    assert '"policy"' in envelope
    assert '"applied"' in envelope
    # A finding nobody can locate cannot be applied, verified, or reverted.
    assert '"urls"' in envelope
    # An absent `declined` and an empty one mean different things; the skill has
    # to say which, or the distinction is lost the first time a run declines
    # nothing. Collapse whitespace so the assertion survives re-wrapping.
    flat = " ".join(envelope.split())
    assert "`declined`** is always present" in flat
    assert "never omit the key" in flat


def test_rule_id_is_optional_and_omitting_it_is_documented_as_safe() -> None:
    """A wrong tag claims a mechanical remedy for something needing a person.

    The vocabulary lets a downstream pipeline merge our findings with its own.
    But a guessed tag is worse than a blank one: untagged means "a human decides",
    which is the correct handling for almost everything an audit produces.
    """
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    envelope = text[text.index("## Structured Audit Data Envelope"):text.index("## Scoring Weights")]
    flat = " ".join(envelope.split())
    assert '"rule_id"' in envelope
    assert "Omit `rule_id` unless" in flat
    # The tag must not read as an instruction to apply anything.
    assert "a claim, not an instruction" in flat
    for rule in ("brand-spelling", "internal-link-insertion", "price-inconsistency"):
        assert rule in envelope


def test_human_first_defines_the_structured_contract() -> None:
    text = (REPO_ROOT / "skills" / "seo-human-first" / "SKILL.md").read_text(encoding="utf-8")
    assert "audit-data.json" in text, "the policy must define the machine-readable contract it gates"
    for field in ("`bucket` on every finding", "`declined[]`", "`policy.applied`"):
        assert field in text


def test_envelope_declares_links_as_data():
    """The internal-linking plan must be emitted as data, not only as prose.

    A plan that exists only in a markdown table has to be transcribed by hand
    before anything can act on it, and that copy goes stale silently: a phrase
    that stopped being in the copy and a phrase that was mistyped look identical
    downstream.
    """
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    assert '"links"' in text, "the envelope must carry a links array"
    for field in ('"from"', '"to"', '"phrase"'):
        assert field in text, f"a link entry needs {field}"


def test_links_state_the_already_present_constraint():
    """A link needing a sentence written is editorial, not mechanical.

    Downstream tooling treats this array as safe to execute precisely because no
    copy is rewritten to accommodate an anchor. If the skill stops saying so, the
    array stops meaning that.
    """
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    assert 'ALREADY in' in text
    assert 'verbatim' in text


def test_absent_links_is_distinguished_from_empty():
    """Absent and empty are different claims, and the difference is load-bearing.

    An absent key means the audit did not look. An empty array means it looked
    and found none — which is what lets a consumer decide whether a previously
    approved link plan has been withdrawn rather than merely unexamined.
    """
    text = (REPO_ROOT / "skills" / "seo-audit" / "SKILL.md").read_text(encoding="utf-8")
    assert 'Omit the key entirely' in text
    assert '"links": []' in text
