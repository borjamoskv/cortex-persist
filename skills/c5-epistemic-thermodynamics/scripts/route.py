#!/usr/bin/env python3
"""Resolve preserved aliases without loading or executing the modules."""
import argparse
import json
from pathlib import Path
import re
import unicodedata

def normalize(value):
    text = unicodedata.normalize('NFKD', value.casefold())
    return ' '.join(''.join(c for c in text if not unicodedata.combining(c)).split())

def select(query, records):
    query = normalize(query)
    exact = [r for r in records if query in [normalize(a) for a in r['aliases']]]
    if exact:
        return exact
    return [r for r in records if any(re.search(r'(?<!\w)' + re.escape(normalize(a)) + r'(?!\w)', query) for a in r['aliases'])]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query', required=True)
    args = parser.parse_args()
    root = Path(__file__).absolute().parent.parent
    data = json.loads((root / 'references/aliases.json').read_text())
    matches = select(args.query, data['modules'])
    print(json.dumps([{'name': r['name'], 'module': str(root / r['module'])} for r in matches], ensure_ascii=False))
    return 0 if matches else 2

if __name__ == '__main__':
    raise SystemExit(main())
