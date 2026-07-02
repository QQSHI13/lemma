"""Single-file hook plugin — no packaging required.

Drop this in your docs_dir and reference it in docsforge.yml:

    hooks:
      - plugins/backlinks_hook.py

Injects a "> **Backlinks**" quote block at the end of every page that has
incoming links from other local markdown files.
"""
from __future__ import annotations

import posixpath
import re
from urllib.parse import unquote

# Module-level cache built during the first call and reused across pages
_backlinks_cache: dict[str, list] = {}
_doc_uris: set[str] = set()


def _resolve_link(link_path: str, from_src_uri: str) -> str | None:
    """Resolve a markdown link to a src_uri."""
    link_path = unquote(link_path).strip()
    if link_path.startswith('/'):
        target = link_path.lstrip('/')
    else:
        from_dir = posixpath.dirname(from_src_uri)
        target = posixpath.normpath(posixpath.join(from_dir, link_path))
    if target.startswith('..'):
        return None
    _, ext = posixpath.splitext(target)
    if not ext:
        target += '.md'
    elif ext == '.html':
        target = target[:-5] + '.md'
    return target


def on_files(files, *, config):
    """Build backlink map from all documentation pages."""
    global _backlinks_cache, _doc_uris
    _backlinks_cache.clear()
    _doc_uris = {f.src_uri for f in files.documentation_pages()}
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for file in files.documentation_pages():
        content = file.content_string
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        for match in link_pattern.finditer(content):
            text = match.group(1)
            path = match.group(2).strip()
            if not path or path.startswith(('#', 'http://', 'https://', 'mailto:')):
                continue
            clean = path.split('#')[0].split('?')[0]
            if not clean:
                continue
            target = _resolve_link(clean, file.src_uri)
            if target and target in _doc_uris:
                _backlinks_cache.setdefault(target, []).append((file, text))
    return files


def on_page_markdown(markdown, *, page, config, files):
    """Append backlink quote block to page."""
    src_uri = page.file.src_uri
    backlinks = _backlinks_cache.get(src_uri, [])
    if not backlinks:
        return markdown

    lines = ['> **Backlinks**', '> ']
    seen = set()
    for source_file, link_text in backlinks:
        if source_file.src_uri in seen:
            continue
        seen.add(source_file.src_uri)
        rel_url = source_file.url_relative_to(page.file)
        safe_text = link_text.replace(']', '\\]').replace('[', '\\[')
        lines.append(f'> - [{safe_text}]({rel_url})')

    return markdown + '\n\n' + '\n'.join(lines) + '\n'
