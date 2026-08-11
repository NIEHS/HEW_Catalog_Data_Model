# HEW Data Commons Schema Design

## Purpose

This repository contains the starting point for a LinkML schema for the Health and Extreme Weather (HEW) Data Commons. The first implementation target is systematic-review literature coding from LaserAI using the HEW Resource Library Coding Guide. The model is intentionally kept general and extensible so it can later catalog exposure-related resources of many types, including survey instruments, geospatial datasets, exposome datasets, cohorts, tools, software, notebooks, tutorials, and data dictionaries.

The initial design is based on three related but distinct layers:

1. **Resource**: a paper, report, dataset, cohort, survey instrument, software package, geospatial layer, model, notebook, tutorial, tool, or data dictionary.
2. **Coding / Annotation**: a LaserAI, human, or machine-assisted systematic-review assessment of a resource.
3. **Concepts / Terms**: exposure concepts, health impacts, geographic features, special topics, resource types, model types, populations, interventions, and external ontology mappings.

The key design point is that the LaserAI coding guide should not become the whole ontology. It should be represented as a **coding profile** over a more general HEW resource model.

## Why annotations rather than direct fields only?

A simple model might say:

```text
Article has exposure = Heatwave
```

That is useful, but too flat for a commons. The HEW model should instead support:

```text
Resource
  has Annotation
    uses Coding Scheme = HEW Resource Library Coding Guide
    coded Exposure Concept = Heatwave
    coded Health Impact Concept = Asthma
    coded Geographic Feature = Urban
    evidence Source = Complete Resource
    coded By = LaserAI / human curator
```

This lets the commons preserve provenance, support multiple coding passes, represent AI-generated versus human-reviewed assertions, and allow disagreement or refinement without overwriting earlier evidence.

## Initial source: HEW Resource Library Coding Guide

The coding guide is organized into six tabs:

1. Reference Information
2. Exposure
3. Health Impact
4. Geography
5. Data Tools and Methods
6. Special Topics

The first tab includes required coding fields for `Reference Type` and `Information Source`, plus a LaserAI-generated `Study Objective` that should be treated as advisory and subject to human verification.

The Exposure tab defines the exposure pathway by which extreme weather affects health. The field is multi-value, supports `Not Reported`, and contains Level 2 coding values for Air Pollution, Extreme Weather-Related Event or Disaster, Food Quality, Food Security, Human Conflict/Violence, Temperature, and Water Quality.

The Health Impact tab is also multi-value, supports `Not Reported`, and includes Level 2 values for Cardiovascular Impact, Developmental Impact, Infectious Disease, Mental Health and Well-Being, Respiratory Impact, and Temperature-Related Health Impact. Infectious Disease includes Level 3 codes for Vectorborne Disease.

The Geography tab separates broad geographic location from geographic feature. It emphasizes regional coding rather than specific countries, and separately captures features such as Built Environment, Desert, Forest, Freshwater, Island, Mountain, Ocean/Coastal, Polar, Rural, Tropical, Urban, and Wetland.

The Data Tools and Methods tab is a key bridge to the broader commons. It captures data resource types such as Cohort, Source Cohort Publication, Dataset, Software Code/Library, and Survey, along with model types such as Artificial Intelligence/Machine Learning, Exposure Modeling, and Geospatial Modeling.

The Special Topics tab captures cross-cutting themes such as Climate Justice/Climate Equity, Communication, Economic Impact, Health Sector Influence, Intervention, Policy, Population Displacement/Forced Migration, Research Gap, Sociodemographic Vulnerability, and Study Population.

## Core class design

### `HEWResource`

A cataloged resource relevant to health and extreme weather. This is the general superclass for literature, datasets, cohorts, survey instruments, software, models, geospatial resources, exposome resources, tutorials, notebooks, tools, and data dictionaries.

### `LiteratureResource`

A bibliographic resource such as a research article, review article, commentary, report, assessment, or book. This is the first target class for LaserAI systematic-review coding.

### `DatasetResource`

A dataset relevant to health and extreme weather, including health, environmental, exposure, geospatial, survey, cohort, and derived datasets.

### `SoftwareResource`

Software, code, library, workflow, notebook, or computational tool relevant to health and extreme weather.

### `CohortResource`

A cohort or cohort-derived resource relevant to exposure-health research.

### `SurveyInstrument`

A survey instrument or questionnaire used to collect HEW-relevant data.

### `DataDictionary`

A structured description of variables, fields, measures, or data elements.

## Systematic-review annotation design

### `HEWSystematicReviewAnnotation`

A structured coding annotation for a literature resource using the HEW Resource Library Coding Guide or a compatible systematic-review coding profile.

Important fields include:

- `subject`
- `coding_scheme`
- `coding_scheme_version`
- `annotation_date`
- `coded_by`
- `coding_method`
- `information_source`
- `reference_type`
- `study_objective`
- `exposure_annotations`
- `health_impact_annotations`
- `geography_annotations`
- `data_tool_method_annotations`
- `special_topic_annotations`
- `notes`
- `confidence`
- `needs_human_review`

LaserAI output should be marked as machine-generated or machine-assisted. Human review should be represented explicitly.

## Annotation component classes

### `ExposureAnnotation`

Represents a coded exposure pathway by which extreme weather affects health. It supports parent-child coding, free-text `Other/Specify` values, evidence text, coding depth, and `Not Reported`.

### `HealthImpactAnnotation`

Represents a coded health impact related to an extreme weather exposure. It supports hierarchical coding and evidence-bearing annotations.

### `GeographyAnnotation`

Represents geographic location and geographic feature codes. Geographic location and geographic feature should remain separate, because they answer different questions.

### `DataToolMethodAnnotation`

Represents data resources and model types used, created, deposited, or described by a literature resource. This class creates the path from literature review to commons resource catalog.

### `SpecialTopicAnnotation`

Represents cross-cutting themes such as communication, intervention, policy, research gaps, sociodemographic vulnerability, and study population.

### `MentionedResource`

A data, software, model, cohort, survey, or tool resource mentioned, used, generated, deposited, evaluated, or described by a literature resource. Mentioned resources can later be promoted into first-class `HEWResource` records.

## Modeling distinction: coding values versus domain concepts

Some guide terms are real-world concepts:

- wildfire smoke
- particulate matter
- extreme heat
- asthma
- flood
- drought
- harmful algal bloom
- low socioeconomic status
- geospatial model

Other terms are review-management or coding constructs:

- Not Reported
- General Exposure
- Other Exposure, Specify
- Abstract and Title, Only
- Source Cohort Publication
- Medical Visit as a surrogate metric
- General Health Impact

The model should avoid treating review-management values as if they were real-world exposure or health entities. `Not Reported`, for example, should be a coding state, not an exposure concept.

## Alignment strategy

The schema is LinkML-native, but should support mappings to existing ontologies and metadata standards:

- BioLink Model for broad biomedical relationship and entity alignment;
- ECTO for exposure events and exposure-related concepts;
- ENVO for environmental features and environmental context;
- MONDO / DOID for disease terms;
- HPO for phenotypic abnormalities where useful;
- OBI / IAO for information artifacts, studies, measurements, and planned processes;
- schema.org, DCAT, and Dublin Core Terms for web catalog and dataset metadata;
- DRS and GA4GH-compatible identifiers where object access becomes relevant.

The first release should include mapping slots and mapping tables, not force premature exact ontology mappings for every HEW coding value.

## Suggested schema modules

```text
hew-core.yaml
hew-literature.yaml
hew-review-coding.yaml
hew-exposure.yaml
hew-health.yaml
hew-geography.yaml
hew-resource-types.yaml
hew-special-topics.yaml
hew-alignments.yaml
```

The current repository starts with a compact combined schema plus modular stubs. As the model matures, terms and classes can be split cleanly into these modules.

## Version 0.1 scope

Version 0.1 should support:

- literature resources;
- LaserAI systematic-review annotations;
- Reference Type;
- Information Source;
- Study Objective;
- Exposure codes;
- Health Impact codes;
- Geography codes;
- Data Tools and Methods codes;
- Special Topic codes;
- free-text `Other/Specify` values;
- annotation provenance;
- example YAML records;
- validation using LinkML tooling.

Version 0.2 can promote discovered datasets, cohorts, surveys, software, models, and tools into richer first-class catalog records.

## Practical design rule

Start with the systematic review, but model it as **evidence-bearing annotations over general HEW resources**. That lets LaserAI be useful now without locking the commons into a spreadsheet-shaped universe forever.
