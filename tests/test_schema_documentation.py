"""Ensure HEW-owned entities and slots have user-facing definitions."""

from pathlib import Path
import unittest

import yaml


class TestSchemaDocumentation(unittest.TestCase):
    def test_all_class_and_slot_definitions_have_descriptions(self):
        schema_dir = Path(__file__).resolve().parents[1] / 'hew-model' / 'schema'
        paths = sorted(schema_dir.rglob('*.yaml'))
        self.assertTrue(paths)
        for path in paths:
            schema = yaml.safe_load(path.read_text())
            for section in ('classes', 'slots'):
                for name, definition in schema.get(section, {}).items():
                    with self.subTest(schema=path.name, section=section, name=name):
                        description = (definition or {}).get('description')
                        self.assertIsInstance(description, str)
                        self.assertTrue(description.strip())
