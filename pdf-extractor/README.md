# @brox/pdf-extractor

Extract text from PDF files. Pure Python — only requires `pypdf` (no system tools, no native compilation).

## Install

```bash
brox install @brox/pdf-extractor
```

## Requirements

- Python 3.8+
- `pypdf` (`pip install pypdf`)

## What the agent can do after installing

- Summarize PDF contents
- Extract data from invoices, contracts, reports
- Answer questions grounded in PDF text
- Process specific page ranges

## Direct usage

```bash
python3 scripts/extract.py file.pdf
python3 scripts/extract.py file.pdf --pages 1-3,7
python3 scripts/extract.py file.pdf --json
```

## Limits

- Scanned/image-based PDFs are **not supported** (no OCR).
- Encrypted PDFs raise an error.
- Complex multi-column layouts may extract in unexpected order.

## License

MIT
