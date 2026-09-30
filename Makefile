SCHEMA=hew-model/schema/hew-geospatial.yaml
PYTHON ?= python3

.PHONY: validate jsonschema jsonld-context docs clean

validate:
	./hew-model/scripts/validate_examples.sh

jsonschema:
	mkdir -p build
	gen-json-schema $(SCHEMA) > build/hew.schema.json

jsonld-context:
	$(PYTHON) scripts/generate_jsonld_context.py --schema $(SCHEMA) --output build/hew.context.jsonld

docs:
	mkdir -p build/docs
	gen-doc $(SCHEMA) --directory build/docs

clean:
	rm -rf build
