"""Test hook to verify on_page_markdown is called."""
from __future__ import annotations

def on_page_markdown(markdown, *, page, config, files):
    print(f"[TEST HOOK] on_page_markdown called for {page.file.src_uri}")
    return markdown + "\n\n> **TEST HOOK WORKS**\n"
