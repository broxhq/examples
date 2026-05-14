---
name: web-fetch
trigger: When the user provides a URL or asks you to read, summarize, quote from, or analyze content from the web.
---

# Web Fetch

You can fetch a URL and get back clean readable text using the `fetch.py` script.

## How to use

The script lives at `<skill-dir>/scripts/fetch.py`.

### Most common: get readable text from a page
```bash
python3 <skill-dir>/scripts/fetch.py <url>
```
Output: the page title (as a `# heading`) followed by clean text content. HTML, scripts, styles, navigation, and footers are stripped.

### Get structured JSON
```bash
python3 <skill-dir>/scripts/fetch.py <url> --json
```
Returns `{url, status, title, text}`. Use this when you need to access fields programmatically.

### Limit output length
```bash
python3 <skill-dir>/scripts/fetch.py <url> --max 5000
```
Truncate text to N characters. Useful for long pages — pull a preview first, fetch more if needed.

### Get raw HTML (advanced)
```bash
python3 <skill-dir>/scripts/fetch.py <url> --raw
```
Returns unprocessed HTML. Use only when you specifically need markup (e.g. extracting links, meta tags).

## Examples

> User: "What does this article say? https://example.com/article"

Run `python3 scripts/fetch.py https://example.com/article --max 8000`, read the text, summarize.

> User: "Get the latest headlines from news.ycombinator.com"

Run `python3 scripts/fetch.py https://news.ycombinator.com --max 5000`, identify the headline list in the output, return the top items.

> User: "Compare what these two pages say"

Fetch each URL with `--json`, store the text, compare.

## Setup requirements

**None.** Uses Python stdlib only.

## Limits and caveats

- **JavaScript-rendered pages**: The script fetches HTML as-served, so pages that render content via client-side JS (SPAs, infinite scroll, lazy-loaded content) will return empty or partial text. If the result looks too short, mention this — the user may need a headless-browser-based skill.
- **Rate limits and blocks**: Some sites block non-browser User-Agents or rate-limit requests. The script identifies itself as `brox-web-fetch/0.1`. If you get HTTP 403 or 429, tell the user.
- **Authentication**: The script does not handle login, cookies, or paywalls. Public pages only.
- **Length**: Large pages are returned in full unless `--max` is used. For very long content, prefer `--max` first to avoid excessive context usage.
