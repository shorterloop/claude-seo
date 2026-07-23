#!/usr/bin/env python3
"""
Content Sentinel Voice Auditor.

Performs deterministic local checks on a text body or URL against voice
principles (banned phrases, British spellings) and computes readability metrics
(Flesch Reading Ease, sentence stats).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable

# Add core scripts to path so we can reuse render_page / url_safety
_ROOT = Path(__file__).resolve().parents[3]
_SCRIPTS_DIR = _ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

try:
    from render_page import render_page
except ImportError:
    render_page = None

# British to American spelling dictionary for voice consistency checks
BRITISH_TO_AMERICAN = {
    "colour": "color",
    "colours": "colors",
    "behaviour": "behavior",
    "behaviours": "behaviors",
    "flavour": "flavor",
    "flavours": "flavors",
    "humour": "humor",
    "labour": "labor",
    "neighbour": "neighbor",
    "neighbours": "neighbors",
    "organise": "organize",
    "organised": "organized",
    "organising": "organizing",
    "organisation": "organization",
    "organisations": "organizations",
    "realise": "realize",
    "realised": "realized",
    "realising": "realizing",
    "realisation": "realization",
    "realisations": "realizations",
    "analyse": "analyze",
    "analysed": "analyzed",
    "analysing": "analyzing",
    "sceptical": "skeptical",
    "scepticism": "skepticism",
    "theatre": "theater",
    "centre": "center",
    "centres": "centers",
    "cancelled": "canceled",
    "travelling": "traveling",
    "modelling": "modeling",
    "favour": "favour",
    "favours": "favours",
    "favourite": "favorite",
    "favourites": "favorites",
    "defence": "defense",
    "offence": "offense",
    "licence": "license",
    "pretence": "pretense",
}

BANNED_PHRASES = (
    "in today's fast-paced world",
    "the key takeaway",
    "it is important to remember",
    "game-changer",
    "unlock",
    "leverage",
    "empower",
    "navigate the complexities",
    "ever-evolving landscape",
    "rapidly evolving landscape",
    "embark on a journey",
    "journey of innovation",
    "at the end of the day",
    "paradigm shift",
    "best-in-class",
    "next-generation",
    "supercharge",
    "reimagine",
    "seamless collaboration",
    "single pane of glass",
    "drive transformation",
    "actionable insights",
    "customer-centric",
    "robust and scalable",
    "north star",
)

WEB_BANNED_PHRASES = (
    "all-in-one platform",
    "everything you need",
    "complete solution",
    "end-to-end",
    "build better products",
    "ship faster",
    "collaborate seamlessly",
    "trusted by teams worldwide",
    "loved by thousands",
    "powerful, intuitive, flexible",
)

_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def count_syllables(word: str) -> int:
    """Heuristic syllable counter for English words."""
    word = word.lower().strip(".:;?!,()[]{}'\"")
    if not word:
        return 0
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        count += 1
    return max(1, count)


def calculate_readability(text: str) -> dict[str, Any]:
    """Compute word counts, sentences, and Flesch Reading Ease score."""
    # Simple sentence tokenizer based on punctuation
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    sentence_count = len(sentences)

    words = _TOKEN_RE.findall(text)
    word_count = len(words)

    if word_count == 0 or sentence_count == 0:
        return {
            "word_count": 0,
            "sentence_count": 0,
            "avg_sentence_length": 0.0,
            "flesch_reading_ease": 0.0,
        }

    total_syllables = sum(count_syllables(w) for w in words)
    avg_sentence_length = word_count / sentence_count
    avg_syllables_per_word = total_syllables / word_count

    # Flesch Reading Ease Formula
    fre = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    fre = max(0.0, min(100.0, fre))

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "flesch_reading_ease": round(fre, 2),
    }


def check_banned_phrases(text: str, is_web: bool = False) -> list[str]:
    """Return a list of banned phrases found in the text."""
    found = []
    lowered = text.lower()
    phrases_to_check = list(BANNED_PHRASES)
    if is_web:
        phrases_to_check.extend(WEB_BANNED_PHRASES)

    for phrase in phrases_to_check:
        # Match as word boundaries where possible to avoid substring false positives
        if len(phrase.split()) == 1:
            pattern = rf"\b{re.escape(phrase)}\b"
            if re.search(pattern, lowered):
                found.append(phrase)
        else:
            # Multi-word phrase matching
            if phrase in lowered:
                found.append(phrase)
    return found


def check_british_spellings(text: str) -> list[str]:
    """Return a list of British spelling words found in the text."""
    found = []
    words = [w.lower() for w in _TOKEN_RE.findall(text)]
    seen = set()
    for word in words:
        if word in BRITISH_TO_AMERICAN and word not in seen:
            found.append(word)
            seen.add(word)
    return found


def analyse(text: str, is_web: bool = False) -> dict[str, Any]:
    """Run all checks and aggregate results."""
    if not text or len(text.strip()) < 100:
        return {"error": "insufficient_content"}

    readability = calculate_readability(text)
    banned = check_banned_phrases(text, is_web=is_web)
    british = check_british_spellings(text)

    # Simple heuristic-based score
    # Penalize for banned phrases (10 points each, cap at 50)
    # Penalize for British spelling (5 points each, cap at 30)
    banned_penalty = min(50, len(banned) * 10)
    british_penalty = min(30, len(british) * 5)
    
    # Readability penalty (optimum Flesch score is 60-70)
    fre = readability["flesch_reading_ease"]
    if 60.0 <= fre <= 70.0:
        fre_penalty = 0
    else:
        # Out-of-bounds penalty
        fre_penalty = min(20, int(abs(65.0 - fre) * 0.5))

    heuristic_score = 100 - banned_penalty - british_penalty - fre_penalty
    heuristic_score = max(0, heuristic_score)

    return {
        "word_count": readability["word_count"],
        "sentence_count": readability["sentence_count"],
        "avg_sentence_length": readability["avg_sentence_length"],
        "flesch_reading_ease": readability["flesch_reading_ease"],
        "banned_phrases_found": banned,
        "british_spellings_found": british,
        "heuristic_score": heuristic_score,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Content Sentinel Voice Auditor")
    parser.add_argument(
        "source",
        nargs="?",
        help="URL, file path, or '-' to read from stdin (default: '-')",
        default="-",
    )
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--web", "--marketing", action="store_true", dest="web", help="Enable web/marketing copy checks (adds web-specific banned phrases)")
    args = parser.parse_args()

    text = ""
    if args.source == "-":
        text = sys.stdin.read()
    elif args.source.startswith(("http://", "https://")):
        if not render_page:
            print("Error: render_page module not found. Check path settings.", file=sys.stderr)
            return 1
        res = render_page(args.source, mode="auto")
        if res.get("error"):
            print(f"Error fetching URL: {res['error']}", file=sys.stderr)
            return 1
        text = res.get("extracted_text") or ""
    else:
        path = Path(args.source)
        if not path.is_file():
            print(f"Error: file not found: {args.source}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8", errors="replace")

    results = analyse(text, is_web=args.web)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if "error" in results:
            print(f"Audit failed: {results['error']}")
            return 1

        print("=== Content Sentinel Voice Audit ===")
        print(f"Word Count:             {results['word_count']}")
        print(f"Sentence Count:         {results['sentence_count']}")
        print(f"Avg Sentence Length:    {results['avg_sentence_length']} words")
        print(f"Flesch Reading Ease:    {results['flesch_reading_ease']}")
        print(f"Heuristic Voice Score:  {results['heuristic_score']}/100")
        
        if results["banned_phrases_found"]:
            print(f"Banned Phrases Found:   {', '.join(results['banned_phrases_found'])}")
        else:
            print("Banned Phrases Found:   None")

        if results["british_spellings_found"]:
            print(f"British Spellings:      {', '.join(results['british_spellings_found'])}")
        else:
            print("British Spellings:      None")

    return 0


if __name__ == "__main__":
    sys.exit(main())
