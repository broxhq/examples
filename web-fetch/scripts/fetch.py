#!/usr/bin/env python3
"""Fetch a URL and output clean readable text.

Strips HTML tags, scripts, styles, and collapses whitespace.
Uses only Python stdlib — no external dependencies.

Usage:
    fetch.py <url>
    fetch.py <url> --raw       # output raw HTML
    fetch.py <url> --json      # output {title, text, url, status}
    fetch.py <url> --max 5000  # truncate text to N characters
"""
import gzip
import json
import re
import sys
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


USER_AGENT = "Mozilla/5.0 (compatible; brox-web-fetch/0.1; +https://brox.dev)"
DROP_TAGS = {"script", "style", "noscript", "iframe", "svg", "head", "nav", "footer", "aside"}
BLOCK_TAGS = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "section", "article", "header"}


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in DROP_TAGS:
            self.skip_depth += 1
        if tag == "title":
            self.in_title = True
        if tag in BLOCK_TAGS and self.skip_depth == 0:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in DROP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
        if tag == "title":
            self.in_title = False
        if tag in BLOCK_TAGS and self.skip_depth == 0:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.parts.append(data)
        if self.in_title:
            self.title_parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        # collapse whitespace within lines, preserve paragraph breaks
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in raw.splitlines()]
        # collapse consecutive blank lines
        out = []
        last_blank = False
        for line in lines:
            if not line:
                if not last_blank:
                    out.append("")
                last_blank = True
            else:
                out.append(line)
                last_blank = False
        return "\n".join(out).strip()

    def title(self) -> str:
        return " ".join(self.title_parts).strip()


def fetch(url: str, timeout: int = 20) -> tuple[int, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, data.decode(charset, errors="replace")
    except HTTPError as e:
        return e.code, ""
    except URLError as e:
        sys.stderr.write(f"network error: {e.reason}\n")
        sys.exit(2)


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.stderr.write(__doc__)
        sys.exit(0 if args else 1)

    url = args[0]
    mode = "text"
    max_chars = None

    i = 1
    while i < len(args):
        a = args[i]
        if a == "--raw":
            mode = "raw"
            i += 1
        elif a == "--json":
            mode = "json"
            i += 1
        elif a == "--max":
            max_chars = int(args[i + 1])
            i += 2
        else:
            sys.stderr.write(f"Unknown argument: {a}\n")
            sys.exit(1)

    if not re.match(r"^https?://", url):
        url = "https://" + url

    status, html = fetch(url)
    if status >= 400:
        sys.stderr.write(f"HTTP {status}\n")
        sys.exit(1)

    if mode == "raw":
        print(html)
        return

    parser = TextExtractor()
    parser.feed(html)
    text = parser.text()
    title = parser.title()
    if max_chars and len(text) > max_chars:
        text = text[:max_chars] + "\n…[truncated]"

    if mode == "json":
        json.dump({"url": url, "status": status, "title": title, "text": text}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if title:
            print(f"# {title}\n")
        print(text)


if __name__ == "__main__":
    main()
