#!/usr/bin/env python3
"""
Lemma - Post-build script.

Run this after `docsforge build` to resolve cross-references and inject backlinks.
"""
import sys
import os
import json

# Add plugins to path
sys.path.insert(0, os.path.dirname(__file__))

from plugins.lemma_resolver import resolve


def main():
    site_dir = os.path.join(os.path.dirname(__file__), 'site')
    
    print("=" * 50)
    print("  Lemma Post-Build: Resolving Cross-References")
    print("=" * 50)
    
    result = resolve(site_dir)
    
    print(f"\n  Pages:      {result['pages']}")
    print(f"  References: {result['references']}")
    print(f"  Labels:     {result['labels']}")
    
    if result['gaps']:
        print(f"\n  ⚠️  Gaps ({len(result['gaps'])}):")
        for gap in result['gaps']:
            print(f"      ❌ {gap}")
    
    # Save gap report
    gap_path = os.path.join(site_dir, 'lemma-gaps.json')
    with open(gap_path, 'w') as f:
        json.dump({
            'gaps': result['gaps'],
            'pages': result['pages'],
            'references': result['references'],
        }, f, indent=2)
    print(f"\n  Gap report saved to: {gap_path}")
    
    return 1 if result['gaps'] else 0


if __name__ == '__main__':
    sys.exit(main())