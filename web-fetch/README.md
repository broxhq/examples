# @brox/web-fetch

Fetch any URL and get back clean readable text. HTML stripped, scripts and styles removed, whitespace collapsed.

## Install

```bash
brox install @brox/web-fetch
```

## Requirements

- Python 3.8+
- **Zero external dependencies** — uses only stdlib

## What the agent can do after installing

- Summarize web articles
- Extract content from documentation pages
- Compare information across URLs
- Pull current data from public APIs (use `--raw` for JSON responses)

## Direct usage

```bash
python3 scripts/fetch.py https://example.com
python3 scripts/fetch.py https://example.com --json
python3 scripts/fetch.py https://example.com --max 5000
python3 scripts/fetch.py https://example.com --raw
```

## Limits

- **JavaScript-heavy SPAs are not rendered** — you get the initial HTML only
- No login, no cookies, no paywalls
- Some sites block non-browser User-Agents (HTTP 403/429)

## License

MIT
