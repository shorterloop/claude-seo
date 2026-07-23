"""Tests for Content Sentinel extension layout, script execution, and metrics."""

import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXTENSION = ROOT / "extensions" / "content-sentinel"
SKILL_MD = EXTENSION / "skills" / "seo-content-sentinel" / "SKILL.md"
AGENT_MD = EXTENSION / "agents" / "seo-content-sentinel.md"
AUDIT_SCRIPT = EXTENSION / "scripts" / "audit_content.py"
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"


def test_extension_layout_exists():
    """Verify that all required files and folders exist in the repository layout."""
    assert EXTENSION.is_dir()
    assert SKILL_MD.is_file()
    assert AGENT_MD.is_file()
    assert AUDIT_SCRIPT.is_file()
    assert (EXTENSION / "install.sh").is_file()
    assert (EXTENSION / "install.ps1").is_file()
    assert (EXTENSION / "uninstall.sh").is_file()
    assert (EXTENSION / "README.md").is_file()
    assert (EXTENSION / "references" / "principles.md").is_file()
    assert (EXTENSION / "references" / "rubric.md").is_file()
    assert (EXTENSION / "references" / "signatures-v1.md").is_file()
    assert (EXTENSION / "references" / "webpage-copy.md").is_file()


def test_skill_version_matches_plugin_version():
    """Verify that metadata version in the extension skill matches plugin.json."""
    plugin_data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    expected_version = plugin_data["version"]

    skill_content = SKILL_MD.read_text(encoding="utf-8")
    import re
    match = re.search(r"^\s*version:\s*\"([^\"]+)\"", skill_content, re.MULTILINE)
    assert match, "Could not find version in skill frontmatter"
    assert match.group(1) == expected_version, f"Skill version {match.group(1)} != Plugin version {expected_version}"


def test_syllable_counter():
    """Unit test the heuristic syllable counter in audit_content.py."""
    import sys
    sys.path.insert(0, str(EXTENSION / "scripts"))
    from audit_content import count_syllables

    assert count_syllables("word") == 1
    assert count_syllables("syllable") == 3
    assert count_syllables("behaviour") == 3
    assert count_syllables("organise") == 3
    assert count_syllables("") == 0


def test_readability_calculations():
    """Unit test the Flesch Reading Ease calculations in audit_content.py."""
    from audit_content import calculate_readability

    text = "This is a simple sentence. It is designed to test reading ease. We want to see if the score is correct."
    res = calculate_readability(text)
    
    assert res["word_count"] > 0
    assert res["sentence_count"] == 3
    assert 0 <= res["flesch_reading_ease"] <= 100


def test_banned_phrases_detection():
    """Unit test the banned phrases checker in audit_content.py."""
    from audit_content import check_banned_phrases

    text = "In today's fast-paced world, we need to leverage next-generation paradigm shift."
    found = check_banned_phrases(text)
    
    assert "in today's fast-paced world" in found
    assert "leverage" in found
    assert "paradigm shift" in found
    assert "next-generation" in found  # next-generation is in principles and present in text


def test_british_spellings_detection():
    """Unit test the British spelling checker in audit_content.py."""
    from audit_content import check_british_spellings

    text = "We need to organise our behaviour and analyse the centre."
    found = check_british_spellings(text)
    
    assert "organise" in found
    assert "behaviour" in found
    assert "analyse" in found
    assert "centre" in found
    assert "behavior" not in found


def test_web_banned_phrases_detection():
    """Unit test the web-specific banned phrases check when is_web=True."""
    from audit_content import check_banned_phrases

    text = "Our all-in-one platform helps teams collaborate seamlessly."
    
    # By default, is_web=False, so web-specific phrases are NOT flagged
    found_default = check_banned_phrases(text, is_web=False)
    assert "all-in-one platform" not in found_default
    assert "collaborate seamlessly" not in found_default

    # With is_web=True, they should be flagged
    found_web = check_banned_phrases(text, is_web=True)
    assert "all-in-one platform" in found_web
    assert "collaborate seamlessly" in found_web
