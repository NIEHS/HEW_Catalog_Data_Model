#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CORE="$MODEL_DIR/schema/hew.yaml"
EXTENDED="$MODEL_DIR/schema/hew-extended.yaml"
EXAMPLES="$MODEL_DIR/examples"

cd "$MODEL_DIR/.."
linkml-validate "$CORE"
linkml-validate "$EXTENDED"

# Core: publications and surveys validate against the core schema alone.
linkml-validate -s "$CORE" -C LiteratureResource "$EXAMPLES/publication_resource.yaml"
linkml-validate -s "$CORE" -C LiteratureResource "$EXAMPLES/example_literature_annotation.yaml"
linkml-validate -s "$CORE" -C SurveyInstrument "$EXAMPLES/survey_instrument.yaml"
linkml-validate -s "$CORE" -C SurveyInstrument "$EXAMPLES/survey_measure_mappings.yaml"
linkml-validate -s "$CORE" -C SurveyDataset "$EXAMPLES/survey_dataset.yaml"

# Extensions.
linkml-validate -s "$EXTENDED" -C GeospatialResource "$EXAMPLES/example_dataset_resource.yaml"
linkml-validate -s "$EXTENDED" -C GeospatialResource "$EXAMPLES/geospatial_dataset.yaml"
linkml-validate -s "$EXTENDED" -C EnvironmentalVariable "$EXAMPLES/environmental_variable.yaml"
linkml-validate -s "$EXTENDED" -C SpatiotemporalExposure "$EXAMPLES/example_spatiotemporal_exposure.yaml"
linkml-validate -s "$EXTENDED" -C SpatiotemporalExposure "$EXAMPLES/spatiotemporal_exposure_optional.yaml"
linkml-validate -s "$EXTENDED" -C CovariateCalculation "$EXAMPLES/amadeus_covariate_calculation.yaml"
linkml-validate -s "$EXTENDED" -C ExternalExposureLinkage "$EXAMPLES/omop_gaia_external_exposure_linkage.yaml"
linkml-validate -s "$EXTENDED" -C Project "$EXAMPLES/example_program_project_people.yaml"
linkml-validate -s "$EXTENDED" -C ToolResource "$EXAMPLES/tool_resource.yaml"
linkml-validate -s "$EXTENDED" -C ResourceCollection "$EXAMPLES/resource_collection.yaml"
