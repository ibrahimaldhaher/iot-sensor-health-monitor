#!/usr/bin/env bash
# Create the GitHub repository and push this project to it.
#
#   ./scripts/publish.sh                      # uses the default name below
#   ./scripts/publish.sh my-other-repo-name
#
# Requires the GitHub CLI (https://cli.github.com) and `gh auth login` once.
set -euo pipefail

REPO_NAME="${1:-iot-sensor-health-monitor}"
VISIBILITY="${VISIBILITY:-public}"

command -v gh >/dev/null || { echo "GitHub CLI (gh) is not installed."; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first."; exit 1; }

gh repo create "$REPO_NAME" \
  --"$VISIBILITY" \
  --source=. \
  --remote=origin \
  --description "Lecture 1 exercise — rule-based Normal/Abnormal monitoring of IoT motor readings, with a Colab notebook and a VS Code dev container" \
  --push

git push -u origin try 2>/dev/null || true

echo
echo "Done: $(gh repo view "$REPO_NAME" --json url -q .url)"
