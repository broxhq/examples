---
name: pdf-extractor
trigger: When the user provides a PDF file path and asks to extract text, tables, or structured data from it.
---

# PDF Extractor

You are equipped to extract text and tabular data from PDF documents.

## How to use

1. Identify the PDF file path from the user's request.
2. Use `scripts/extract.py <path>` to get raw text. The script outputs plain text to stdout.
3. For table-heavy documents, pass the `--tables` flag — output will be JSON with one object per detected table.
4. Parse the result according to the user's intent (summarize, restructure, extract specific fields).

## Examples

User: "Pull the line items from invoice.pdf"
You: Run `scripts/extract.py invoice.pdf --tables`, then locate the line-items table and return rows as structured data.

User: "What does this contract say about termination?"
You: Run `scripts/extract.py contract.pdf`, scan output for termination-related sections, summarize.

## Limits

- Scanned/image PDFs require OCR — this skill does NOT handle those. If the script returns an empty or near-empty result, tell the user the PDF appears to be scanned.
- Max recommended file size: 50MB.
