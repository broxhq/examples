<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/broxhq/.github/main/profile/assets/logo-dark.svg">
  <img alt="brox" src="https://raw.githubusercontent.com/broxhq/.github/main/profile/assets/logo.svg" width="240">
</picture>

### Example Skills

</div>

---

Reference skills that demonstrate the [Brox skill format](https://github.com/broxhq/spec). Each is **ready to install** and use.

## Skills in this repo

| Skill | Install | What it does |
|-------|---------|--------------|
| [`pdf-extractor/`](pdf-extractor/) | `brox install @brox/pdf-extractor` | Extract text from PDFs. Pure Python (needs `pypdf`). |
| [`web-fetch/`](web-fetch/) | `brox install @brox/web-fetch` | Fetch a URL → clean readable text. Python stdlib only. |
| [`git-context/`](git-context/) | `brox install @brox/git-context` | Status, recent commits, branch, diff summary for any repo. |
| [`sqlite-query/`](sqlite-query/) | `brox install @brox/sqlite-query` | Inspect schema and run SELECT queries on `.db` files. |

## Using these as templates

Each subdirectory has the canonical layout:

```
my-skill/
├── skill.json      # manifest (required)
├── SKILL.md        # agent instructions (required)
├── scripts/        # executable scripts (optional)
└── README.md       # human-facing docs
```

Copy one as a starting point, edit `skill.json` and `SKILL.md`, then publish with `brox publish`.

## License

MIT — copy, fork, and adapt freely.
