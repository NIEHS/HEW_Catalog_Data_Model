#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
linkml-validate -s schema/hew-geospatial.yaml examples/example_literature_annotation.yaml
linkml-validate -s schema/hew-geospatial.yaml examples/example_dataset_resource.yaml
linkml-validate -s schema/hew-geospatial.yaml examples/example_program_project_people.yaml
