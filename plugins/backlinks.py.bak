"""Backlinks plugin for DocsForge.

Injects a blockquote containing backlinks (pages that link to the current page)
at the end of each page's markdown content.

Usage in docsforge.yml:

    plugins:
      - backlinks:
          heading: "Backlinks"          # Quote heading text
          empty_message: "None"          # Message when no backlinks exist
          enabled: true                   # Toggle on/off

Or as a hook (single file, no packaging):

    hooks:
      - plugins/backlinks.py

This plugin parses standard markdown links `[text](path)` that point to local
files within the documentation. External links (http://, https://, mailto:, etc.)
and anchor-only links (#section) are ignored.
"""
from __future__ import annotations

import posixpath
import re
from urllib.parse import unquote

from docsforge.config_base import Config
from docsforge.config_options import Type
from docsforge.core.plugin_base import BasePlugin


class BacklinksConfig(Config):
    """Configuration for the backlinks plugin."""
    heading = Type(str, default="Backlinks")
    """Heading text for the backlinks quote block."""
    empty_message = Type(str, default="No backlinks found.")
    """Message shown when a page has no backlinks."""
    enabled = Type(bool, default=True)
    """Whether to enable the plugin."""


class BacklinksPlugin(BasePlugin[BacklinksConfig]):
    """Inject a backlink quote block into each page.

    Scans all markdown files for links to local files, builds a backlink map,
    then appends a > blockquote with the list of pages that link to the
    current page.
    """

    def __init__(self) -> None:
        super().__init__()
        # target_src_uri -> [(source_file, link_text), ...]
        self._backlinks: dict[str, list[tuple]] = {}
        # Set of all markdown src_uris
        self._doc_uris: set[str] = set()

    def on_files(self, files, *, config):
        """Scan all documentation pages to build the backlink map."""
        if not self.config.enabled:
            return files

        # Cache all documentation page URIs
        self._doc_uris = {
            f.src_uri for f in files.documentation_pages()
        }

        # Match markdown links: [text](url)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        for file in files.documentation_pages():
            content = file.content_string

            # Strip YAML frontmatter so we don't match links inside meta
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2]

            for match in link_pattern.finditer(content):
                link_text = match.group(1)
                link_path = match.group(2).strip()

                # Skip external links and special protocols
                if not link_path:
                    continue
                if link_path.startswith(('#', 'http://', 'https://', 'mailto:',
                                        'ftp://', 'data:', 'javascript:')):
                    continue

                # Remove anchor and query strings
                clean_path = link_path.split('#')[0].split('?')[0]
                if not clean_path:
                    continue

                # Resolve relative path to src_uri
                target_uri = self._resolve_link_path(clean_path, file.src_uri)
                if not target_uri:
                    continue

                # Check if target is a documentation page in this site
                if target_uri in self._doc_uris:
                    self._backlinks.setdefault(target_uri, []).append(
                        (file, link_text)
                    )

        return files

    def _resolve_link_path(self, link_path: str, from_src_uri: str) -> str | None:
        """Resolve a markdown link path to a src_uri.

        Args:
            link_path: The path from the markdown link (e.g., "../foo.md", "/bar.md")
            from_src_uri: The src_uri of the file containing the link

        Returns:
            Resolved src_uri or None if it cannot be resolved
        """
        # URL-decode the path
        link_path = unquote(link_path)

        if link_path.startswith('/'):
            # Absolute from docs root
            target = link_path.lstrip('/')
        else:
            # Relative to current file
            from_dir = posixpath.dirname(from_src_uri)
            target = posixpath.normpath(posixpath.join(from_dir, link_path))

        # Ensure it doesn't escape the docs root
        if target.startswith('..'):
            return None

        # Add .md extension if missing (handles "foo" and "foo.html")
        _, ext = posixpath.splitext(target)
        if not ext:
            target += '.md'
        elif ext == '.html':
            # Convert .html links to .md src_uri
            target = target[:-5] + '.md'

        return target

    def on_page_markdown(self, markdown, *, page, config, files):
        """Append a backlink quote block to the page markdown."""
        if not self.config.enabled:
            return markdown

        src_uri = page.file.src_uri
        backlinks = self._backlinks.get(src_uri, [])

        if not backlinks:
            # Optionally inject an empty backlinks section
            if self.config.empty_message:
                quote = (
                    f'\n\n> **{self.config.heading}**\n'
                    f'> \n'
                    f'> *{self.config.empty_message}*\n'
                )
                return markdown + quote
            return markdown

        # Build the quote block
        lines = [f'> **{self.config.heading}**', '> ']
        seen = set()

        for source_file, link_text in backlinks:
            # Deduplicate by source file
            if source_file.src_uri in seen:
                continue
            seen.add(source_file.src_uri)

            # Compute relative URL from current page to source page
            rel_url = source_file.url_relative_to(page.file)

            # Escape the link text if it contains markdown characters
            # (basic escaping for ] and [)
            safe_text = link_text.replace(']', '\\]').replace('[', '\\[')

            lines.append(f'> - [{safe_text}]({rel_url})')

        return markdown + '\n\n' + '\n'.join(lines) + '\n'
