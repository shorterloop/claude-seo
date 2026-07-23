#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="${HOME}/.claude/skills/seo-content-sentinel"
AGENT_FILE="${HOME}/.claude/agents/seo-content-sentinel.md"

[ -d "${SKILL_DIR}" ] && rm -rf "${SKILL_DIR}" && echo "✓ Removed ${SKILL_DIR}"
[ -f "${AGENT_FILE}" ] && rm -f "${AGENT_FILE}" && echo "✓ Removed ${AGENT_FILE}"

echo "Done. Content Sentinel extension uninstalled."
