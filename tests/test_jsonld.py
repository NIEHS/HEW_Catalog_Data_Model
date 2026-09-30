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

    def test_geospatial_nested_objects_receive_types(self):
        instance = {
            "id": "HEWRES:heat-grid",
            "title": "Example heat grid",
            "resource_type": "geospatial_dataset",
            "spatial_extent": {
                "geometry": {
                    "geometry_type": "polygon",
                    "wkt": "POLYGON((-1 0, 1 0, 1 1, -1 1, -1 0))",
                },
                "named_locations": [
                    {"location_id": "geonames:6252001", "name": "United States"}
                ],
            },
            "environmental_variables": [
                {
                    "id": "HEWVAR:tmax",
                    "name": "tmax",
                    "spatial_support": {"support_type": "raster_grid_cell"},
                    "temporal_support": {"temporal_alignment": "end"},
                }
            ],
        }

        document = to_jsonld(instance, class_name="DatasetResource")

        self.assertEqual(document["@type"], "DatasetResource")
        self.assertEqual(document["spatial_extent"]["@type"], "SpatialExtent")
        self.assertEqual(
            document["spatial_extent"]["geometry"]["@type"], "Geometry"
        )
        self.assertEqual(
            document["environmental_variables"][0]["@type"], "EnvironmentalVariable"
        )
        self.assertTrue(round_trip_jsonld(document))


if __name__ == "__main__":
    unittest.main()
