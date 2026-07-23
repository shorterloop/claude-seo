#!/usr/bin/env bash
# Claude SEO — Content Sentinel extension installer.
set -euo pipefail

main() {
    SKILL_DIR="${HOME}/.claude/skills/seo-content-sentinel"
    AGENT_DIR="${HOME}/.claude/agents"
    BASE_SKILL_DIR="${HOME}/.claude/skills/seo"

    echo "════════════════════════════════════════"
    echo "║   Claude SEO — Content Sentinel      ║"
    echo "════════════════════════════════════════"

    command -v python3 >/dev/null 2>&1 || { echo "✗ Python 3 required."; exit 1; }
    [ ! -d "${BASE_SKILL_DIR}" ] && { echo "✗ claude-seo base not installed."; exit 1; }

    SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" >/dev/null 2>&1 && pwd)"

    echo "→ Creating directories..."
    mkdir -p "${SKILL_DIR}/scripts"
    mkdir -p "${SKILL_DIR}/references"
    mkdir -p "${AGENT_DIR}"

    echo "→ Copying extension files..."
    cp "${SOURCE_DIR}/skills/seo-content-sentinel/SKILL.md" "${SKILL_DIR}/SKILL.md"
    cp "${SOURCE_DIR}/agents/seo-content-sentinel.md" "${AGENT_DIR}/seo-content-sentinel.md"
    cp "${SOURCE_DIR}/scripts/audit_content.py" "${SKILL_DIR}/scripts/audit_content.py"
    cp "${SOURCE_DIR}/references/"*.md "${SKILL_DIR}/references/"

    chmod +x "${SKILL_DIR}/scripts/audit_content.py"

    # Rewrite only files copied by this extension install to use the managed runtime wrapper
    for installed_doc in "${SKILL_DIR}/SKILL.md" "${SKILL_DIR}/references/"*.md "${AGENT_DIR}/seo-content-sentinel.md"; do
        [ -f "${installed_doc}" ] || continue
        temp_doc="${installed_doc}.claude-seo-tmp"
        sed -e 's#claude-seo run#"$HOME/.claude/skills/seo/bin/claude-seo" run#g' \
            "${installed_doc}" > "${temp_doc}"
        mv "${temp_doc}" "${installed_doc}"
    done

    echo "✓ Installed skill: ${SKILL_DIR}"
    echo "✓ Installed agent: ${AGENT_DIR}/seo-content-sentinel.md"
    echo "Done. Try: /seo content-sentinel https://example.com"
}
main "$@"
