#!/usr/bin/env python3
"""Apply the release tag's version without rewriting manifests that already agree."""

import json
import os
from pathlib import Path
import re
import sys

SEMVER = re.compile(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'
                    r'(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?'
                    r'(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z')


def inject(path, tag):
    if not SEMVER.fullmatch(tag):
        raise ValueError('Release tag must be v<semver>.')
    text = path.read_text()
    manifest = json.loads(text)
    version = tag[1:]
    previous = manifest.get('version')
    if previous == version:
        return
    print(f'::warning::package.json version {previous!r} disagrees with tag {tag}; packing version {version}.')
    manifest['version'] = version
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    try:
        inject(Path(os.environ.get('BRICK_PATH', '.')) / 'package.json', os.environ['RELEASE_TAG'])
    except (ValueError, KeyError, OSError) as error:
        print(f'::error::{error}', file=sys.stderr)
        sys.exit(1)
