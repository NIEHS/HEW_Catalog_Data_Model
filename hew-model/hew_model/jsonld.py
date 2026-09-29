"""JSON-LD serialization helpers for HEW LinkML instances."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from linkml.generators.jsonldcontextgen import ContextGenerator
from rdflib import Graph
from rdflib.compare import to_isomorphic


SCHEMA_PATH = Path(__file__).parents[1] / "schema" / "hew-geospatial.yaml"

# LinkML's context generator maps slots, but plain dictionaries do not carry
# Python class metadata. Add the class types needed for nested HEW instances.
NESTED_CLASS_TYPES = {
    "annotations": "HEWSystematicReviewAnnotation",
    "exposure_annotations": "ExposureAnnotation",
    "health_impact_annotations": "HealthImpactAnnotation",
    "geography_annotations": "GeographyAnnotation",
    "data_tool_method_annotations": "DataToolMethodAnnotation",
    "special_topic_annotations": "SpecialTopicAnnotation",
    "mentioned_resources": "MentionedResource",
}


def generate_context(schema_path: str | Path = SCHEMA_PATH) -> dict[str, Any]:
    """Generate the JSON-LD context directly from the HEW LinkML schema."""
    context = ContextGenerator(str(schema_path)).serialize(model=True)
    return json.loads(context)


def _add_nested_types(value: Any, slot_name: str | None = None) -> Any:
    if isinstance(value, list):
        return [_add_nested_types(item, slot_name) for item in value]
    if not isinstance(value, dict):
        return value

    result = {key: _add_nested_types(item, key) for key, item in value.items()}
    if slot_name in NESTED_CLASS_TYPES:
        result.setdefault("@type", NESTED_CLASS_TYPES[slot_name])
    return result


def to_jsonld(
    instance: dict[str, Any],
    schema_path: str | Path = SCHEMA_PATH,
    class_name: str = "HEWResource",
) -> dict[str, Any]:
    """Return a JSON-LD document for a LinkML-shaped HEW dictionary."""
    document = deepcopy(instance)
    document["@context"] = generate_context(schema_path)["@context"]
    document["@type"] = class_name
    return _add_nested_types(document)


def to_jsonld_string(
    instance: dict[str, Any],
    schema_path: str | Path = SCHEMA_PATH,
    class_name: str = "HEWResource",
) -> str:
    """Serialize a LinkML-shaped HEW dictionary as JSON-LD text."""
    return json.dumps(to_jsonld(instance, schema_path, class_name), indent=2)


def jsonld_graph(document: dict[str, Any] | str) -> Graph:
    """Parse a JSON-LD document into an RDFLib graph."""
    data = document if isinstance(document, str) else json.dumps(document)
    graph = Graph()
    graph.parse(data=data, format="json-ld")
    return graph


def round_trip_jsonld(document: dict[str, Any] | str) -> bool:
    """Check that JSON-LD -> RDF -> JSON-LD preserves the RDF graph."""
    graph = jsonld_graph(document)
    round_tripped = jsonld_graph(graph.serialize(format="json-ld"))
    return to_isomorphic(graph) == to_isomorphic(round_tripped)
