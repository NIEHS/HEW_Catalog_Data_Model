import unittest

from rdflib import URIRef

from hew_model.jsonld import jsonld_graph, round_trip_jsonld, to_jsonld


class TestJsonLdRoundTrip(unittest.TestCase):
    def test_literature_resource_round_trip_preserves_graph(self):
        instance = {
            "id": "HEWRES:laserai_3541",
            "title": "Assessment of biometeorological conditions",
            "resource_type": "literature",
            "doi": "10.1007/s00484-024-02666-w",
            "pmid": "38639787",
            "annotations": [
                {
                    "id": "HEWANN:laserai_3541",
                    "subject": "HEWRES:laserai_3541",
                    "coding_scheme": "LaserAI Export",
                    "coding_method": "laser_ai_generated",
                    "reference_type": "research_article",
                    "information_source": "complete_resource",
                    "exposure_annotations": [
                        {"coded_concept": "Temperature"},
                        {"coded_concept": "Extreme Heat/Heat"},
                    ],
                }
            ],
        }

        document = to_jsonld(instance)
        graph = jsonld_graph(document)

        self.assertIn("@context", document)
        self.assertIn(
            URIRef("https://w3id.org/hew/resource/laserai_3541"),
            set(graph.subjects()),
        )
        self.assertTrue(round_trip_jsonld(document))


if __name__ == "__main__":
    unittest.main()
