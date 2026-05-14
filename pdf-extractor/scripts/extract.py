#!/usr/bin/env python3
"""Extract text from a PDF. Placeholder for the example skill."""
import sys

if len(sys.argv) < 2:
    print("usage: extract.py <pdf-path> [--tables]", file=sys.stderr)
    sys.exit(1)

print(f"[placeholder] would extract text from {sys.argv[1]}")
