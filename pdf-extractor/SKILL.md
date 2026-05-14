---
name: pdf-extractor
trigger: When the user provides a PDF file path and asks to extract, summarize, analyze, or search text within it.
---

# PDF Extractor

You can extract text from PDF files using the `extract.py` script in this skill's `scripts/` directory.

## How to use

1. **Locate the script.** It lives at `<skill-dir>/scripts/extract.py`. The skill directory is `.claude/skills/@brox__pdf-extractor/` (local) or `~/.claude/skills/@brox__pdf-extractor/` (global).

2. **Extract all pages as plain text:**
   ```bash
   python3 <skill-dir>/scripts/extract.py <pdf-path>
   ```

3. **Extract specific pages:**
   ```bash
   python3 <skill-dir>/scripts/extract.py <pdf-path> --pages 1-3,7
   ```

4. **Get structured JSON** (useful when you need to process pages individually):
   ```bash
   python3 <skill-dir>/scripts/extract.py <pdf-path> --json
   ```

5. **Parse the result** according to the user's intent:
   - Summarize: read the text, produce a concise summary
   - Extract structured fields: scan for invoice numbers, dates, line items
   - Q&A: locate the section relevant to the user's question

## Examples

> User: "Summarize what's in report.pdf"

Run `python3 scripts/extract.py report.pdf`, read the output, summarize key points.

> User: "Pull the line items from invoice.pdf, just page 2"

Run `python3 scripts/extract.py invoice.pdf --pages 2 --json`, parse the JSON, identify the table rows, return as structured data.

> User: "What does the contract say about termination?"

Run `python3 scripts/extract.py contract.pdf`, search the text for sections matching "termination", "terminate", "end of agreement", quote the relevant clauses.

## Setup requirements

The script needs `pypdf` (pure Python, no system dependencies). If `python3 -c "import pypdf"` fails, install it once:

```bash
pip install pypdf
# or
pip3 install pypdf
```

You can run this install yourself the first time the script fails — the error message in stderr will tell you.

## Limits and caveats

- **Scanned PDFs**: The script extracts only embedded text. Scanned/image-based PDFs return empty results. If the script prints `warning: no text extracted`, tell the user the PDF appears to be scanned and would need OCR (out of scope for this skill).
- **Complex layouts**: Multi-column layouts may produce text in an unexpected reading order. If results look jumbled, mention this to the user.
- **Tables**: Embedded text from tables comes out as plain text, often without column alignment. For high-quality table extraction, the user may need a dedicated tool.
- **Encrypted PDFs**: Will raise an error. Tell the user the file is password-protected.
