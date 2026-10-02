"""JSON-LD serialization helpers for HEW LinkML instances."""

from __future__ import annotations

import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph
from rdflib.compare import to_isomorphic


# The extended schema is a superset of the core, so its context covers every module.
SCHEMA_PATH = Path(__file__).parents[1] / "schema" / "hew-extended.yaml"


def generate_context(schema_path: str | Path = SCHEMA_PATH) -> dict[str, Any]:
    """Generate the JSON-LD context directly from the HEW LinkML schema."""
    context = json.loads(ContextGenerator(str(schema_path)).serialize(model=True))
    # The generator only emits prefixes declared on the root schema; instance-data
    # prefixes such as HEWRES and PERSON are declared in imported modules.
    terms = context["@context"]
    for schema in SchemaView(str(schema_path)).all_schema(imports=True):
        for prefix in schema.prefixes.values():
            terms.setdefault(prefix.prefix_prefix, prefix.prefix_reference)
    return context


@lru_cache(maxsize=None)
def _nested_class_types(schema_path: str) -> dict[str, str]:
    """Map each inlined slot to its class range.

    LinkML's context generator maps slots, but plain dictionaries do not carry
    Python class metadata, so nested objects need their @type added.
    """
    schema = SchemaView(schema_path)
    classes = schema.all_classes()
    return {
        slot.name: slot.range
        for slot in schema.all_slots().values()
        if slot.range in classes and (slot.inlined or slot.inlined_as_list)
    }


def _add_nested_types(value: Any, types: dict[str, str], slot_name: str | None = None) -> Any:
    if isinstance(value, list):
        return [_add_nested_types(item, types, slot_name) for item in value]
    if not isinstance(value, dict):
        return value

    result = {key: _add_nested_types(item, types, key) for key, item in value.items()}
    # Inlined agents name their concrete class; other nested objects take the slot range.
    nested_type = value.get("agent_type") or types.get(slot_name)
    if slot_name is not None and nested_type:
        result.setdefault("@type", nested_type)
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
    return _add_nested_types(document, _nested_class_types(str(schema_path)))


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
