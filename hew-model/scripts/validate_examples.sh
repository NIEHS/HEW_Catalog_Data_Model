#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEMA="$MODEL_DIR/schema/hew-geospatial.yaml"

cd "$MODEL_DIR/.."
linkml-validate "$SCHEMA"
linkml-validate "$MODEL_DIR/schema/modules/hew_geospatial.yaml"
linkml-validate -s "$SCHEMA" -C LiteratureResource "$MODEL_DIR/examples/example_literature_annotation.yaml"
linkml-validate -s "$SCHEMA" -C DatasetResource "$MODEL_DIR/examples/example_dataset_resource.yaml"
linkml-validate -s "$SCHEMA" -C Project "$MODEL_DIR/examples/example_program_project_people.yaml"
linkml-validate -s "$SCHEMA" -C SpatiotemporalExposure "$MODEL_DIR/examples/example_spatiotemporal_exposure.yaml"
linkml-validate -s "$SCHEMA" -C LiteratureResource "$MODEL_DIR/examples/publication_resource.yaml"
linkml-validate -s "$SCHEMA" -C SurveyInstrument "$MODEL_DIR/examples/survey_instrument.yaml"
linkml-validate -s "$SCHEMA" -C SurveyDataset "$MODEL_DIR/examples/survey_dataset.yaml"
linkml-validate -s "$SCHEMA" -C ToolResource "$MODEL_DIR/examples/tool_resource.yaml"
linkml-validate -s "$SCHEMA" -C ResourceCollection "$MODEL_DIR/examples/resource_collection.yaml"
linkml-validate -s "$SCHEMA" -C EnvironmentalVariable "$MODEL_DIR/examples/environmental_variable.yaml"
linkml-validate -s "$SCHEMA" -C CovariateCalculation "$MODEL_DIR/examples/amadeus_covariate_calculation.yaml"
linkml-validate -s "$SCHEMA" -C ExternalExposureLinkage "$MODEL_DIR/examples/omop_gaia_external_exposure_linkage.yaml"
linkml-validate -s "$SCHEMA" -C DatasetResource "$MODEL_DIR/examples/geospatial_dataset.yaml"
linkml-validate -s "$SCHEMA" -C SpatiotemporalExposure "$MODEL_DIR/examples/spatiotemporal_exposure_optional.yaml"
