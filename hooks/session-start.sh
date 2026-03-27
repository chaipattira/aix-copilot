#!/bin/bash
# ABOUTME: SessionStart hook for the aix-data-analysis plugin
# ABOUTME: Injects Socratic Tutoring Style into every session so all skills share consistent dialogue pacing

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
CONTENT=$(cat "${PLUGIN_ROOT}/hooks/socratic-style.md")

# Use python3 for reliable JSON string escaping (handles quotes, newlines, special chars)
JSON_CONTENT=$(python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))" <<< "$CONTENT")

printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$JSON_CONTENT"
