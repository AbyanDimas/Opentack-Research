#!/usr/bin/env python3
"""
Internal Markdown Link Checker for OpenStack Research Documentation.
Validates that all internal links in markdown files resolve to existing files or permalinks.
"""
import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# Collect permalinks from all markdown files
permalinks = {}
for md_file in ROOT_DIR.rglob("*.md"):
    if ".git" in md_file.parts or "_site" in md_file.parts:
        continue
    try:
        content = md_file.read_text(encoding="utf-8")
        match = re.search(r"^permalink:\s*(.+)$", content, re.MULTILINE)
        if match:
            pl = match.group(1).strip()
            permalinks[pl] = md_file
            # Also register without trailing slash
            permalinks[pl.rstrip("/")] = md_file
    except Exception as e:
        print(f"Warning: could not read {md_file}: {e}")

# Register root permalinks
permalinks["/"] = ROOT_DIR / "index.md"
permalinks[""] = ROOT_DIR / "index.md"

link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
errors = []

for md_file in ROOT_DIR.rglob("*.md"):
    if ".git" in md_file.parts or "_site" in md_file.parts:
        continue
    rel_source = md_file.relative_to(ROOT_DIR)
    try:
        content = md_file.read_text(encoding="utf-8")
    except Exception as e:
        continue

    for match in link_pattern.finditer(content):
        text, url = match.group(1), match.group(2).strip()

        # Skip external web links, mailto, anchor-only links
        if url.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
            continue

        # Strip anchor fragment
        clean_url = url.split("#")[0]
        if not clean_url:
            continue

        resolved = False

        # 1. Check against permalinks table
        if clean_url in permalinks or clean_url.rstrip("/") in permalinks:
            resolved = True

        # 2. Check as absolute path from repo root
        if not resolved and clean_url.startswith("/"):
            test_path = ROOT_DIR / clean_url.lstrip("/")
            if test_path.exists() or (test_path.with_suffix(".md")).exists():
                resolved = True

        # 3. Check as relative path from current file
        if not resolved:
            test_path = (md_file.parent / clean_url).resolve()
            if test_path.exists() or (test_path.with_suffix(".md")).exists():
                resolved = True

        if not resolved:
            errors.append(f"{rel_source}: Broken link '{url}' (text: '{text}')")

if errors:
    print(f"❌ Found {len(errors)} broken link(s):")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("✅ All internal markdown links validated successfully.")
    sys.exit(0)
