import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('release_version', Path(__file__).parents[1] / 'scripts/release_version.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseVersionTests(unittest.TestCase):
    def test_matching_version_preserves_manifest_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'package.json'
            original = b'{"id":"org.example.brick", "version":"1.0.0"}\r\n'
            path.write_bytes(original)
            module.inject(path, 'v1.0.0')
            self.assertEqual(original, path.read_bytes())

    def test_tag_overrides_stale_missing_and_invalid_manifest_version(self):
        for previous in ['0.1.0', None, 'invalid']:
            with self.subTest(previous=previous), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'package.json'
                path.write_text(json.dumps({'id': 'org.example.brick', 'version': previous, 'dependencies': {}}))
                module.inject(path, 'v1.2.3-rc.1+build.2')
                self.assertEqual('1.2.3-rc.1+build.2', json.loads(path.read_text())['version'])
                self.assertEqual({}, json.loads(path.read_text())['dependencies'])

    def test_invalid_tag_never_changes_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'package.json'
            path.write_text('{"version":"1.0.0"}')
            for tag in ['1.0.0', 'v01.0.0', 'v1.0', 'v1.0.0-01', 'v1.0.0+']:
                with self.subTest(tag=tag), self.assertRaises(ValueError):
                    module.inject(path, tag)
                self.assertEqual('{"version":"1.0.0"}', path.read_text())
