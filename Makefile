SCHEMA=hew-model/schema/hew.yaml
PYTHON ?= python3

.PHONY: validate jsonschema jsonld-context artifacts docs clean

validate:
	./hew-model/scripts/validate_examples.sh

jsonschema:
	mkdir -p build
	gen-json-schema $(SCHEMA) > build/hew.schema.json

jsonld-context:
	PYTHONPATH=hew-model $(PYTHON) hew/generate_jsonld_context.py --schema $(SCHEMA) --output build/hew.context.jsonld

# Refresh the generated files committed next to the schema.
artifacts: jsonschema jsonld-context
	cp build/hew.schema.json build/hew.context.jsonld hew-model/schema/

docs:
	mkdir -p build/docs
	gen-doc $(SCHEMA) --directory build/docs

clean:
	rm -rf build
