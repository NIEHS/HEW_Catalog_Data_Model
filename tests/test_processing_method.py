import json
from pathlib import Path
import unittest

from jsonschema import Draft201909Validator, ValidationError
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Literal, URIRef
from hew_model.jsonld import jsonld_graph, to_jsonld

SCHEMA = Path(__file__).resolve().parents[1] / 'hew-model/schema/hew.yaml'


class TestProcessingMethod(unittest.TestCase):
    def test_method_is_shared_descriptive_metadata(self):
        view = SchemaView(str(SCHEMA))
        self.assertNotIn('CovariateCalculation', view.all_classes())
        self.assertNotIn('ParameterValue', view.all_classes())
        for cls in ('LiteratureResource', 'GeospatialResource', 'SpatiotemporalExposure'):
            self.assertIn('processing_methods', [s.name for s in view.class_induced_slots(cls)])
        schema = json.loads(SCHEMA.with_name('hew.schema.json').read_text())
        schema['$ref'] = '#/$defs/ProcessingMethod'
        validator = Draft201909Validator(schema)
        validator.validate({'name': 'Area summary', 'software_details': {'name': 'Amadeus'}})
        for key in ('parameters', 'function_name', 'buffer_radius', 'extraction_method'):
            with self.subTest(field=key), self.assertRaises(ValidationError):
                validator.validate({'name': 'Area summary', key: 'execution setting'})

    def test_processing_provenance_keeps_names_and_identifiers_distinct(self):
        record = {'id': 'HEWRES:processed', 'title': 'Processed data', 'resource_type': 'dataset', 'processing_methods': [{
            'name': 'Area summary', 'software_details': {'name': 'Amadeus'},
            'provenance_reference': 'https://example.org/runs/one',
        }]}
        document = to_jsonld(record, schema_path=SCHEMA, class_name='DatasetResource')
        graph = jsonld_graph(document)
        self.assertEqual(document['processing_methods'][0]['@type'], 'ProcessingMethod')
        self.assertIn(Literal('Amadeus'), set(graph.objects()))
        self.assertIn(URIRef('https://example.org/runs/one'), set(graph.objects()))
