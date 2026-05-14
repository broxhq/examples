#!/usr/bin/env python3
"""Extract text from a PDF file.

Outputs plain text to stdout. One line per page, separated by blank lines.

Usage:
    extract.py <pdf-path>
    extract.py <pdf-path> --pages 1-3
    extract.py <pdf-path> --json     # outputs structured JSON
"""
import json
import os
import sys


def parse_pages(spec: str, total: int) -> list[int]:
    """Parse a page range spec like '1-3,5,7-9' into a sorted list of 1-indexed pages."""
    if not spec:
        return list(range(1, total + 1))
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.update(range(int(start), int(end) + 1))
        else:
            pages.add(int(part))
    return sorted(p for p in pages if 1 <= p <= total)


def extract(path: str, page_spec: str = "", as_json: bool = False) -> None:
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.stderr.write(
            "pypdf is required. Install with: pip install pypdf\n"
        )
        sys.exit(2)

    if not os.path.isfile(path):
        sys.stderr.write(f"File not found: {path}\n")
        sys.exit(1)

    reader = PdfReader(path)
    total = len(reader.pages)
    pages = parse_pages(page_spec, total)

    extracted = []
    for page_num in pages:
        page = reader.pages[page_num - 1]
        text = page.extract_text() or ""
        extracted.append({"page": page_num, "text": text})

    if as_json:
        json.dump(
            {
                "file": path,
                "total_pages": total,
                "pages": extracted,
            },
            sys.stdout,
            indent=2,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
    else:
        for i, item in enumerate(extracted):
            if i > 0:
                print()
            print(f"--- Page {item['page']} ---")
            print(item["text"])

    nonempty = sum(1 for p in extracted if p["text"].strip())
    if nonempty == 0:
        sys.stderr.write(
            "warning: no text extracted. PDF may be scanned/image-based — OCR is required.\n"
        )


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.stderr.write(__doc__)
        sys.exit(0 if args else 1)

    path = args[0]
    page_spec = ""
    as_json = False

    i = 1
    while i < len(args):
        a = args[i]
        if a == "--pages":
            page_spec = args[i + 1]
            i += 2
        elif a == "--json":
            as_json = True
            i += 1
        else:
            sys.stderr.write(f"Unknown argument: {a}\n")
            sys.exit(1)

    extract(path, page_spec, as_json)


if __name__ == "__main__":
    main()
