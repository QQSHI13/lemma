"""
Lemma build resolver.

Post-processing script that runs after docsforge build to:
1. Build a title→url index from all pages
2. Resolve [[ref:Page Title]] to actual URLs
3. Collect {#labels} and assign sequential numbers
4. Replace [[thm:X]] / [[eq:X]] with proper "Theorem 3.1" text
5. Inject "Referenced by" footers
6. Generate lemma-index.json for CI gap detection
"""

from __future__ import annotations

import json
import logging
import os
import re
import hashlib
from collections import defaultdict
from pathlib import Path

log = logging.getLogger('lemma')


class LemmaResolver:
    """Resolves lemma cross-references in built HTML."""

    def __init__(self, site_dir: str):
        self.site_dir = Path(site_dir)
        # title → url mapping
        self.title_map: dict[str, str] = {}
        # label → {type, number, page_url}
        self.label_map: dict[str, dict] = {}
        # page_url → [titles that reference it]
        self.backlinks: dict[str, list[tuple[str, str]]] = defaultdict(list)
        # page-level counters for sequential numbering
        self.page_counters: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        # cross-page: global theorem numbering per field
        self.global_counters: dict[str, int] = defaultdict(int)

    def build_index(self) -> None:
        """Scan all HTML files to build title→url index."""
        html_files = list(self.site_dir.rglob('*.html'))
        # Exclude 404.html
        html_files = [f for f in html_files if f.name != '404.html']

        for html_path in html_files:
            rel = html_path.relative_to(self.site_dir)
            # Compute the URL path
            if rel.name == 'index.html':
                url = str(rel.parent)
                if url == '.':
                    url = '/'
                else:
                    url = '/' + url + '/'
            else:
                url = '/' + str(rel.with_suffix('')).replace('\\', '/') + '/'

            content = html_path.read_text(encoding='utf-8')

            # Find the page title from <title> tag or first <h1>
            title_match = re.search(r'<title>(.+?)</title>', content)
            if title_match:
                title = title_match.group(1).strip()
                # Remove site name suffix like " - Lemma"
                title = re.sub(r'\s*[-–—|]\s*Lemma.*$', '', title).strip()
                if title:
                    self.title_map[title] = url
                    self.title_map[title.lower()] = url  # case-insensitive lookup

    def _resolve_ref(self, target: str) -> str | None:
        """Resolve a [[ref:target]] to a page URL."""
        # Try exact match first
        if target in self.title_map:
            return self.title_map[target]
        # Try case-insensitive
        if target.lower() in self.title_map:
            return self.title_map[target.lower()]
        # Try fuzzy: strip trailing period, question mark, etc.
        clean = re.sub(r'[.?!,;:]$', '', target)
        if clean != target:
            return self._resolve_ref(clean)
        return None

    def collect_labels(self) -> None:
        """Scan HTML files for {#labels} and collect them."""
        label_names = {'thm': 'Theorem', 'def': 'Definition',
                       'lem': 'Lemma', 'cor': 'Corollary', 'eq': 'Equation'}

        html_files = list(self.site_dir.rglob('*.html'))
        for html_path in html_files:
            if html_path.name == '404.html':
                continue
            content = html_path.read_text(encoding='utf-8')

            # Find {#thm:xxx} / {#eq:xxx} labels
            for m in re.finditer(r'\{#(thm|def|lem|cor|eq):([a-zA-Z0-9_-]+)\}', content):
                kind = m.group(1)
                label = m.group(2)
                rel = html_path.relative_to(self.site_dir)
                url = '/' + str(rel.parent).replace('\\', '/') + '/'
                if rel.name == 'index.html':
                    url = '/' + str(rel.parent).replace('\\', '/') + '/'
                else:
                    url = '/' + str(rel.with_suffix('')).replace('\\', '/') + '/'

                self.global_counters[kind] += 1
                number = self.global_counters[kind]

                name = label_names.get(kind, kind)
                self.label_map[label] = {
                    'type': kind,
                    'number': number,
                    'display': f'{name} {number}',
                    'url': url,
                }

    def resolve_labels_in_html(self) -> None:
        """Replace [[thm:X]] / [[eq:X]] in HTML with actual references."""
        html_files = list(self.site_dir.rglob('*.html'))
        for html_path in html_files:
            if html_path.name == '404.html':
                continue
            content = html_path.read_text(encoding='utf-8')
            original = content

            def replace_label_ref_from_tag(m: re.Match) -> str:
                tag = m.group(1)  # e.g. 'lemma-thm-ref'
                label = m.group(2)
                # Extract kind from tag: 'lemma-thm-ref' -> 'thm'
                kind = tag.replace('lemma-', '').replace('-ref', '')
                if label in self.label_map:
                    info = self.label_map[label]
                    display = info['display']
                    url = info['url']
                    return f'<a href="{url}" class="lemma-ref">{display}</a>'
                return f'<span class="lemma-ref lemma-ref-missing">{label}?</span>'

            content = re.sub(
                r'<lemma-(thm|eq|def|lem|cor)-ref\s+label="?([^">]+)"?>([^<]*)</\1-ref>',
                replace_label_ref_from_tag, content)

            # Also handle the simpler [[thm:label]] / [[eq:label]] pattern directly
            # (catch any that weren't processed by the markdown extension)
            def replace_label_ref(m: re.Match) -> str:
                kind = m.group(1)
                label = m.group(2)
                if label in self.label_map:
                    info = self.label_map[label]
                    display = info['display']
                    url = info['url']
                    return f'<a href="{url}" class="lemma-ref">{display}</a>'
                return f'<span class="lemma-ref lemma-ref-missing">{label}?</span>'

            content = re.sub(
                r'\[\[(thm|eq|def|lem|cor):([a-zA-Z0-9_-]+)\]\]',
                replace_label_ref, content)

            if content != original:
                html_path.write_text(content, encoding='utf-8')

    def process_page(self, html_path: Path) -> tuple[str, list, list]:
        """Process a single HTML file: resolve refs, collect labels, build backlinks."""
        content = html_path.read_text(encoding='utf-8')
        rel = html_path.relative_to(self.site_dir)
        url = '/' + str(rel.parent).replace('\\', '/') + '/'
        if rel.name == 'index.html':
            url = '/' + str(rel.parent).replace('\\', '/') + '/'
        else:
            url = '/' + str(rel.with_suffix('')).replace('\\', '/') + '/'

        modified = False
        refs_found = []
        gaps_found = []

        # Resolve [[ref:Title]] patterns (from the markdown extension placeholder elements)
        # The markdown extension emits <lemma-ref target="Title">Title</lemma-ref>
        ref_pattern = re.compile(
            r'<lemma-ref\s+target="([^"]*)">([^<]*)</lemma-ref>')

        def replace_ref(m: re.Match) -> str:
            nonlocal modified
            target = m.group(1)
            resolved = self._resolve_ref(target)
            if resolved:
                refs_found.append((target, resolved))
                # Record backlink
                self.backlinks[resolved].append((target, url))
                modified = True
                return f'<a href="{resolved}" class="lemma-ref">{target}</a>'
            else:
                gaps_found.append(target)
                modified = True
                return f'<a href="#" class="lemma-ref lemma-ref-missing" title="Page not yet written">{target}</a>'

        content = ref_pattern.sub(replace_ref, content)

        # Also handle raw [[ref:Title]] that weren't processed
        content = re.sub(
            r'\[\[ref:([^\]]+)\]\]',
            lambda m: replace_ref(
                type('m', (), {'group': lambda self, g: m.group(g)})()),
            content
        )

        if modified:
            html_path.write_text(content, encoding='utf-8')

        return url, refs_found, gaps_found

    def inject_backlinks(self) -> None:
        """Inject 'Referenced by' sections at the bottom of each page."""
        for html_path in self.site_dir.rglob('*.html'):
            if html_path.name == '404.html':
                continue
            rel = html_path.relative_to(self.site_dir)
            url = '/' + str(rel.parent).replace('\\', '/') + '/'
            if rel.name == 'index.html':
                url = '/' + str(rel.parent).replace('\\', '/') + '/'
            else:
                url = '/' + str(rel.with_suffix('')).replace('\\', '/') + '/'

            if url in self.backlinks and self.backlinks[url]:
                content = html_path.read_text(encoding='utf-8')
                links = self.backlinks[url]
                items = ''.join(
                    f'<li><a href="{ref_url}" class="lemma-ref">{title}</a></li>'
                    for title, ref_url in links
                )
                backlinks_html = (
                    '<nav class="md-nav md-nav--secondary">'
                    '<span class="md-nav__title">Referenced by</span>'
                    '<ul class="md-nav__list">' + items + '</ul></nav>'
                )
                # Insert before the closing </article> tag
                content = content.replace('</article>', backlinks_html + '\n</article>')
                html_path.write_text(content, encoding='utf-8')

    def inject_copyright(self) -> None:
        """Inject CC BY-SA 4.0 copyright footer at bottom of each page."""
        footer_html = (
            '<footer class="lemma-copyright" style="margin-top: 2rem; padding-top: 1rem; '
            'border-top: 1px solid #e0e0e0; font-size: 0.85rem; color: #666; text-align: center;">'
            '© 2026 <a href="https://github.com/QQSHI13">QQ (Cyrus)</a>. '
            'This work is licensed under '
            '<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.'
            '</footer>'
        )
        for html_path in self.site_dir.rglob('*.html'):
            if html_path.name == '404.html':
                continue
            content = html_path.read_text(encoding='utf-8')
            # Only inject if not already present
            if 'lemma-copyright' not in content:
                # Insert before closing </body> tag
                content = content.replace('</body>', footer_html + '\n</body>')
                html_path.write_text(content, encoding='utf-8')

    def run(self) -> dict:
        """Run the full resolution pipeline."""
        log.info("Building page index...")
        self.build_index()
        log.info(f"  Found {len(self.title_map)} pages")

        log.info("Collecting labels...")
        self.collect_labels()
        log.info(f"  Found {len(self.label_map)} labels")

        log.info("Resolving cross-references...")
        all_gaps = []
        all_refs = 0
        for html_path in sorted(self.site_dir.rglob('*.html')):
            if html_path.name == '404.html':
                continue
            url, refs, gaps = self.process_page(html_path)
            all_refs += len(refs)
            all_gaps.extend(gaps)

        log.info(f"  Resolved {all_refs} references")

        log.info("Resolving label references...")
        self.resolve_labels_in_html()

        log.info("Injecting backlinks...")
        self.inject_backlinks()

        result = {
            'pages': len(self.title_map),
            'references': all_refs,
            'gaps': all_gaps,
            'labels': len(self.label_map),
        }
        return result


def resolve(site_dir: str) -> dict:
    """Convenience function to run the resolver."""
    resolver = LemmaResolver(site_dir)
    return resolver.run()


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO)
    site_dir = sys.argv[1] if len(sys.argv) > 1 else 'site'
    result = resolve(site_dir)
    print(json.dumps(result, indent=2))
    if result['gaps']:
        print(f"\n⚠️  {len(result['gaps'])} gaps detected:")
        for g in result['gaps']:
            print(f"    - {g}")