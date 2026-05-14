# @brox/git-context

Give your AI agent fast situational awareness of any git repo it walks into.

## Install

```bash
brox install @brox/git-context
```

## Requirements

- `git` (you already have it if you're using git)
- bash

## What the agent can do after installing

- Tell you where you left off in a project
- Warn you about uncommitted changes before risky operations
- Summarize what's been happening in the repo
- Show top contributors

## Direct usage

```bash
bash scripts/context.sh         # quick summary
bash scripts/context.sh --full  # adds diff stats + contributors
```

## Output

Plain markdown — easy for both humans and LLMs to parse.

## License

MIT
