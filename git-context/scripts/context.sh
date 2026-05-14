#!/usr/bin/env bash
# Print a concise situational summary of the current git repo.
# Usage: context.sh [--full]
set -euo pipefail

if ! command -v git >/dev/null 2>&1; then
  echo "git not installed" >&2
  exit 2
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "not a git repository" >&2
  exit 1
fi

FULL=0
if [[ "${1-}" == "--full" ]]; then
  FULL=1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || echo "no upstream")
HEAD_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "no commits")

echo "## Repository"
echo "- path: $REPO_ROOT"
echo "- branch: $BRANCH"
echo "- upstream: $UPSTREAM"
echo "- HEAD: $HEAD_SHA"
echo

if [[ "$UPSTREAM" != "no upstream" ]]; then
  AHEAD_BEHIND=$(git rev-list --left-right --count "@{u}"...HEAD 2>/dev/null || echo "0	0")
  BEHIND=$(echo "$AHEAD_BEHIND" | awk '{print $1}')
  AHEAD=$(echo "$AHEAD_BEHIND" | awk '{print $2}')
  echo "- ahead: $AHEAD commits"
  echo "- behind: $BEHIND commits"
  echo
fi

echo "## Status"
STATUS_OUT=$(git status --porcelain=v1)
if [[ -z "$STATUS_OUT" ]]; then
  echo "clean working tree"
else
  STAGED=$(echo "$STATUS_OUT" | grep -c '^[MADRC]' || true)
  UNSTAGED=$(echo "$STATUS_OUT" | grep -c '^.[MADRC]' || true)
  UNTRACKED=$(echo "$STATUS_OUT" | grep -c '^??' || true)
  echo "- staged: $STAGED"
  echo "- unstaged: $UNSTAGED"
  echo "- untracked: $UNTRACKED"
  echo
  echo "### Changed files"
  echo "$STATUS_OUT" | head -40
  TOTAL=$(echo "$STATUS_OUT" | wc -l | tr -d ' ')
  if [[ "$TOTAL" -gt 40 ]]; then
    echo "...and $((TOTAL - 40)) more"
  fi
fi
echo

echo "## Recent commits (last 10)"
git log --oneline -n 10 --no-decorate 2>/dev/null || echo "no commits yet"
echo

if [[ "$FULL" -eq 1 ]]; then
  echo "## Diff summary (staged + unstaged)"
  git diff HEAD --stat 2>/dev/null | tail -30 || true
  echo

  echo "## Top contributors (last 100 commits)"
  git log -n 100 --format='%an' 2>/dev/null | sort | uniq -c | sort -rn | head -5 || true
fi
