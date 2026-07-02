"""Backlinks plugin for DocsForge - injects backlink quotes."""
from __future__ import annotations

import posixpath
import re
from urllib.parse import unquote

print("[backlinks] TOP OF MODULE")

_backlinks_cache: dict[str, list] = {}
_doc_uris: set[str] = set()


def _resolve_link(link_path: str, from_src_uri: str) -> str | None:
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


def _extract_title(content: str) -> str:
    if content.startswith('---'):
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            title_match = re.search(r'^title:\s*(.+)$', fm_match.group(1), re.MULTILINE)
            if title_match:
                return title_match.group(1).strip().strip('"\'')
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    return "Untitled"


def on_files(files, *, config):
    global _backlinks_cache, _doc_uris
    _backlinks_cache.clear()
    _doc_uris = {f.src_uri for f in files.documentation_pages()}
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for file in files.documentation_pages():
        content = file.content_string
        title = _extract_title(content)
        body = content
        if body.startswith('---'):
            parts = body.split('---', 2)
            if len(parts) >= 3:
                body = parts[2]
        for match in link_pattern.finditer(body):
            path = match.group(2).strip()
            if not path or path.startswith(('#', 'http://', 'https://', 'mailto:',
                                            'ftp://', 'data:', 'javascript:')):
                continue
            clean = path.split('#')[0].split('?')[0]
            if not clean:
                continue
            target = _resolve_link(clean, file.src_uri)
            if target and target in _doc_uris:
                _backlinks_cache.setdefault(target, []).append((file, title))
    return files


def on_page_markdown(markdown, *, page, config, files):
    try:
        src_uri = page.file.src_uri
        backlinks = _backlinks_cache.get(src_uri, [])

        lines = ['> **Backlinks**', '> ']
        if backlinks:
            seen = set()
            for source_file, source_title in backlinks:
                if source_file.src_uri in seen:
                    continue
                seen.add(source_file.src_uri)
                rel_url = source_file.url_relative_to(page.file)
                safe_title = source_title.replace(']', '\\]').replace('[', '\\[')
                lines.append(f'> - [{safe_title}]({rel_url})')
        else:
            lines.append('> *No other pages link here yet.*')

        return markdown + '\n\n' + '\n'.join(lines) + '\n'
    except Exception as e:
        import traceback
        print(f"[backlinks] ERROR in on_page_markdown: {e}")
        traceback.print_exc()
        return markdown
