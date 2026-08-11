SCHEMA=schema/hew.yaml

.PHONY: validate jsonschema docs clean

validate:
	./scripts/validate_examples.sh

jsonschema:
	mkdir -p build
	gen-json-schema $(SCHEMA) > build/hew.schema.json

docs:
	mkdir -p build/docs
	gen-doc $(SCHEMA) --directory build/docs

clean:
	rm -rf build
