from copy import deepcopy
import json
from pathlib import Path
import unittest

from jsonschema import Draft7Validator, FormatChecker
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml_runtime.utils.schemaview import SchemaView
import yaml

from hew_model.amadeus import normalize_crs, validate_amadeus_metadata
from hew_model.jsonld import round_trip_jsonld, to_jsonld


ROOT = Path(__file__).parents[1]
SCHEMA_DIR = ROOT / "hew-model" / "schema"


class TestAmadeusAlignment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = SCHEMA_DIR / "profiles" / "hew_amadeus.yaml"
        generated = json.loads(JsonSchemaGenerator(str(cls.profile)).serialize())
        generated["$ref"] = "#/$defs/AmadeusGeospatialResource"
        cls.validator = Draft7Validator(generated, format_checker=FormatChecker())
        cls.example = yaml.safe_load(
            (ROOT / "hew-model/examples/amadeus_aligned_grid.yaml").read_text()
        )

    def test_all_schema_imports_are_local_acyclic_and_standalone(self):
        active = set()
        visited = set()

        def visit(path):
            path = path.resolve()
            self.assertNotIn(path, active, f"Circular schema import: {path}")
            if path in visited:
                return
            active.add(path)
            schema = yaml.safe_load(path.read_text())
            for imported in schema.get("imports", []):
                if imported == "linkml:types":
                    continue
                self.assertNotIn(":", imported, "External schema dependency introduced")
                target = (path.parent / imported).with_suffix(".yaml").resolve()
                self.assertTrue(target.is_relative_to(SCHEMA_DIR.resolve()))
                visit(target)
            active.remove(path)
            visited.add(path)

        for path in SCHEMA_DIR.rglob("*.yaml"):
            visit(path)
            view = SchemaView(str(path))
            valid_ranges = set(view.all_classes()) | set(view.all_types()) | set(view.all_enums())
            for class_name in view.all_classes():
                for slot in view.class_induced_slots(class_name):
                    self.assertIn(slot.range, valid_ranges, f"{path}: {class_name}.{slot.name}")

    def test_shared_extent_definitions_exist_only_in_core(self):
        owners = {}
        for path in (SCHEMA_DIR / "modules").glob("*.yaml"):
            schema = yaml.safe_load(path.read_text())
            for section in ("classes", "slots", "types", "enums"):
                for name in schema.get(section, {}):
                    key = (section, name)
                    self.assertNotIn(key, owners, f"Duplicate definition: {key}")
                    owners[key] = path.name
        for name in ("SpatialExtent", "TemporalExtent", "Geometry", "BoundingBox"):
            self.assertEqual(owners[("classes", name)], "hew_core.yaml")
        core = SchemaView(str(SCHEMA_DIR / "modules/hew_core.yaml"))
        self.assertIn("spatial_extent", core.class_slots("DatasetResource"))
        self.assertIn("temporal_extent", core.class_slots("Distribution"))
        self.assertNotIn("GeospatialResource", core.all_classes())

    def test_structured_coverage_is_available_without_geospatial_extension(self):
        core_path = SCHEMA_DIR / "modules/hew_core.yaml"
        generated = json.loads(JsonSchemaGenerator(str(core_path)).serialize())
        generated["$ref"] = "#/$defs/DatasetResource"
        validator = Draft7Validator(generated, format_checker=FormatChecker())
        record = {
            "id": "HEWRES:survey-coverage", "resource_type": "dataset",
            "spatial_extent": {"bounding_box": {
                "west": -100.0, "south": 35.0, "east": -99.0, "north": 36.0
            }},
            "temporal_extent": {"start_time": "2020-01-01T00:00:00Z"},
        }
        self.assertEqual(list(validator.iter_errors(record)), [])

    def test_projected_grid_and_asset_intervals(self):
        self.assertEqual(list(self.validator.iter_errors(self.example)), [])
        self.assertEqual(validate_amadeus_metadata(self.example), [])
        document = to_jsonld(self.example, class_name="GeospatialResource")
        self.assertEqual(document["grid_definition"]["@type"], "GridDefinition")
        self.assertTrue(round_trip_jsonld(document))

    def test_point_ongoing_and_timeless_products(self):
        point = {
            "id": "HEWRES:monitor", "resource_type": "geospatial_dataset",
            "spatial_support": {"support_type": "monitoring_station"},
            "temporal_support": {
                "temporal_resolution_category": "hourly", "temporal_resolution": "PT1H"
            },
            "temporal_extent": {
                "coverage_status": "ongoing", "start_time": "2020-01-01T00:00:00Z"
            },
        }
        self.assertEqual(list(self.validator.iter_errors(point)), [])
        self.assertEqual(validate_amadeus_metadata(point), [])
        point["temporal_support"] = {"temporal_resolution_category": "timeless"}
        point["temporal_extent"] = {"coverage_status": "timeless"}
        self.assertEqual(list(self.validator.iter_errors(point)), [])
        self.assertEqual(validate_amadeus_metadata(point), [])
        point["temporal_extent"]["start_time"] = "2020-01-01T00:00:00Z"
        self.assertTrue(validate_amadeus_metadata(point))

    def test_semantic_failures_cannot_silently_align(self):
        mutations = [
            lambda record: record.pop("grid_definition"),
            lambda record: record["grid_definition"].update(srid=4326),
            lambda record: record["grid_definition"].update(resolution_x=0),
            lambda record: record["spatial_support"].update(support_type="point"),
            lambda record: record["temporal_support"].pop("day_boundary_convention"),
            lambda record: record["temporal_support"].update(temporal_resolution="PT1H"),
            lambda record: record["spatial_extent"]["bounding_box"].update(south=40),
            lambda record: record["temporal_extent"].update(end_time="2019-01-01T00:00:00Z"),
            lambda record: record["temporal_extent"].update(start_time="2020-01-01T00:00:00"),
        ]
        for mutation in mutations:
            record = deepcopy(self.example)
            mutation(record)
            with self.subTest(record=record):
                self.assertTrue(validate_amadeus_metadata(record))

    def test_duration_calendar_and_category_are_validated(self):
        for support in (
            {"temporal_resolution": "daily"},
            {"aggregation_window": "yesterday"},
            {"calendar": "invented"},
            {"temporal_resolution_category": "every_three_days"},
        ):
            record = deepcopy(self.example)
            record["temporal_support"].update(support)
            with self.subTest(support=support):
                self.assertTrue(list(self.validator.iter_errors(record)))

    def test_delivery_overrides_replace_dataset_defaults(self):
        record = deepcopy(self.example)
        delivery = record["variable_deliveries"][0]
        delivery["temporal_support"] = {
            "temporal_resolution_category": "hourly", "temporal_resolution": "PT1H"
        }
        delivery["spatial_support"] = {"support_type": "point"}
        self.assertEqual(validate_amadeus_metadata(record), [])
        delivery["spatial_support"] = {"support_type": "model_grid_cell"}
        self.assertTrue(validate_amadeus_metadata(record))

    def test_crs_normalization_requires_known_authority(self):
        self.assertEqual(normalize_crs("epsg:5070"), "EPSG:5070")
        self.assertEqual(
            normalize_crs("http://www.opengis.net/def/crs/EPSG/0/4326"), "EPSG:4326"
        )
        with self.assertRaises(ValueError):
            normalize_crs("+proj=longlat +datum=WGS84")


if __name__ == "__main__":
    unittest.main()
