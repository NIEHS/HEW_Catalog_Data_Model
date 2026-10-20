#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEMA="$MODEL_DIR/schema/hew.yaml"
EXAMPLES="$MODEL_DIR/examples"

cd "$MODEL_DIR/.."
linkml-validate "$SCHEMA"

linkml-validate -s "$SCHEMA" -C LiteratureResource "$EXAMPLES/publication_resource.yaml"
linkml-validate -s "$SCHEMA" -C LiteratureResource "$EXAMPLES/example_literature_annotation.yaml"
linkml-validate -s "$SCHEMA" -C SurveyInstrument "$EXAMPLES/survey_instrument.yaml"
linkml-validate -s "$SCHEMA" -C SurveyInstrument "$EXAMPLES/survey_measure_mappings.yaml"
linkml-validate -s "$SCHEMA" -C SurveyDataset "$EXAMPLES/survey_dataset.yaml"
linkml-validate -s "$SCHEMA" -C GeospatialResource "$EXAMPLES/example_dataset_resource.yaml"
linkml-validate -s "$SCHEMA" -C GeospatialResource "$EXAMPLES/geospatial_dataset.yaml"
linkml-validate -s "$SCHEMA" -C EnvironmentalVariable "$EXAMPLES/environmental_variable.yaml"
linkml-validate -s "$SCHEMA" -C SpatiotemporalExposure "$EXAMPLES/example_spatiotemporal_exposure.yaml"
linkml-validate -s "$SCHEMA" -C SpatiotemporalExposure "$EXAMPLES/spatiotemporal_exposure_optional.yaml"
linkml-validate -s "$SCHEMA" -C CovariateCalculation "$EXAMPLES/amadeus_covariate_calculation.yaml"
linkml-validate -s "$SCHEMA" -C ExternalExposureLinkage "$EXAMPLES/omop_gaia_external_exposure_linkage.yaml"
linkml-validate -s "$SCHEMA" -C Project "$EXAMPLES/example_program_project_people.yaml"
linkml-validate -s "$SCHEMA" -C ToolResource "$EXAMPLES/tool_resource.yaml"
linkml-validate -s "$SCHEMA" -C ResourceCollection "$EXAMPLES/resource_collection.yaml"
