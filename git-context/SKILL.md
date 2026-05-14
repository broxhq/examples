---
name: git-context
trigger: When the user asks about the state of a git repo, recent changes, what they were working on, or before making non-trivial code changes you want grounding.
---

# Git Context

You can get a concise situational summary of a git repository using the `context.sh` script.

## When to invoke

**Proactively use this skill when:**
- The user opens a project and asks "where was I?", "what's going on?", "what changed recently?"
- Before you make non-trivial edits — knowing the branch, ahead/behind state, and pending changes prevents mistakes
- The user asks what's pending, what's staged, or what's modified

**Don't use this skill for:**
- Running git commands the user explicitly asks you to run (just run them directly)
- Performing git operations like commits, pushes, merges — use git directly

## How to use

The script lives at `<skill-dir>/scripts/context.sh`. Run from the repo directory you want to inspect.

### Quick summary (default)
```bash
bash <skill-dir>/scripts/context.sh
```
Returns: repo path, current branch, upstream, ahead/behind counts, working-tree status, list of changed files, last 10 commits.

### Full summary (includes diff stats and contributors)
```bash
bash <skill-dir>/scripts/context.sh --full
```
Adds: diff summary of pending changes, top contributors over last 100 commits.

## Examples

> User: "I just opened this repo. What's going on?"

Run `bash scripts/context.sh`, summarize: current branch, whether there are pending changes, what was the last commit about.

> User: "Before you fix that bug, what's my repo state?"

Run `bash scripts/context.sh --full`. Read the output. Tell the user about uncommitted work in progress they might not want to lose, whether they're up to date with upstream.

> User: "Who's been working on this codebase?"

Run `bash scripts/context.sh --full`, look at the contributors section.

## Output format

Output is markdown-structured for easy reading and parsing:

```
## Repository
- path: ...
- branch: ...
- upstream: ...
- HEAD: ...
- ahead: N commits
- behind: N commits

## Status
- staged: N
- unstaged: N
- untracked: N
### Changed files
M  src/foo.js
?? newfile.txt

## Recent commits (last 10)
abc1234 Fix bug in parser
...
```

## Setup requirements

**None.** Requires only `git` (which the user must already have to be in a repo).

## Limits and caveats

- Outputs the first 40 changed files only — for huge changesets, the count line tells you how many were truncated
- The `--full` diff stat shows last 30 files of the diff
- Doesn't show actual diff content (just file-level stats). To see code, the user should ask for `git diff <file>` directly.
