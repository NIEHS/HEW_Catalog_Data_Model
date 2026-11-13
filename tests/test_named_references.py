"""Reference labels remain literals even when identifiers are absent."""
import json
from pathlib import Path
import unittest

from jsonschema import Draft201909Validator
from rdflib import Literal, URIRef
import yaml

from hew_model.jsonld import jsonld_graph, round_trip_jsonld, to_jsonld

ROOT = Path(__file__).resolve().parents[1]


class TestNamedReferences(unittest.TestCase):
    def test_names_identifiers_and_citations_survive_rdf(self):
        instance = yaml.safe_load((ROOT / 'hew-model/examples/publication_named_references.yaml').read_text())
        document = to_jsonld(instance, class_name='LiteratureResource')
        graph = jsonld_graph(document)
        self.assertIn(Literal('Jane Example'), set(graph.objects()))
        self.assertIn(URIRef('https://w3id.org/hew/person/example_curator'), set(graph.objects()))
        self.assertEqual(document['contacts_details'][0]['@type'], 'EntityReference')
        self.assertEqual(document['funding_sources_details'][0]['@type'], 'FundingReference')
        self.assertTrue(round_trip_jsonld(document))

    def test_provenance_citation_remains_literal(self):
        instance = yaml.safe_load((ROOT / 'hew-model/examples/example_program_project_people.yaml').read_text())
        graph = jsonld_graph(to_jsonld(instance, class_name='Project'))
        self.assertIn(Literal('Project team roster supplied by the principal investigator.'), set(graph.objects()))

    def test_reference_allows_identifier_name_description_or_both(self):
        schema = json.loads((ROOT / 'hew-model/schema/hew.schema.json').read_text())
        schema['$ref'] = '#/$defs/EntityReference'
        validator = Draft201909Validator(schema)
        for entry in [
            {'reference_id': 'HEWRES:example'},
            {'name': 'Unregistered dataset'},
            {'description': 'Unpublished study protocol'},
            {'reference_id': 'HEWRES:example', 'name': 'Example dataset'},
        ]:
            with self.subTest(entry=entry):
                validator.validate(entry)
