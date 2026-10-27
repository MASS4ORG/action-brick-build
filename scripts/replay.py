#!/usr/bin/env python3
"""Replay hash-verified stored archives and validate rebuilds of inaccessible variants."""

import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys


def verify(path, integrity):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').digest()
    if 'sha256-' + base64.b64encode(digest).decode() != integrity:
        raise ValueError(f'Recorded archive integrity mismatch: {path.name}')


def replay(directory, output, twin, version, restore):
    records = json.loads((directory / 'recorded.json').read_text())
    needed = {'source'} | ({'turian' + '.'.join(version.split('.')[:2])} if twin else set())
    available = set()
    for record in records:
        filename = record['file']
        expected = f'{record["packageId"]}-{record["version"]}--{record["variant"]}.brick'
        if filename != expected or Path(filename).name != filename:
            raise ValueError('Recorded archive has an invalid filename.')
        if record['variant'] not in needed:
            continue
        if record['available']:
            source = directory / filename
            verify(source, record['integrity'])
            available.add(record['variant'])
            if restore:
                shutil.copyfile(source, output / filename)
                print(f'Replayed verified {filename}.')
        elif restore:
            try:
                verify(output / filename, record['integrity'])
            except (ValueError, OSError) as error:
                raise ValueError('Recorded archive is unavailable and the rebuild differs; immutable release bytes were preserved.') from error
    return not needed.issubset(available)


if __name__ == '__main__':
    try:
        required = replay(Path(sys.argv[2]), Path(sys.argv[3]), os.environ['TWIN'] == 'true',
                          os.environ['SELECTED_CLI_VERSION'], sys.argv[1] == 'restore')
        if sys.argv[1] == 'prepare':
            print(str(required).lower())
    except (ValueError, KeyError, OSError) as error:
        print(f'::error::{error}', file=sys.stderr)
        sys.exit(1)
