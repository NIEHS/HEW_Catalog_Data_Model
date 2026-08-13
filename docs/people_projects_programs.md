# People, Organizations, Programs, Projects, and Funding

The HEW model represents coordination and provenance separately from the LaserAI systematic-review coding profile.

## Core pattern

```text
Agent
  Person
  Organization
  SoftwareAgent

Program
  has_projects -> Project

Project
  uses_resources -> HEWResource
  produces_resources -> HEWResource

AgentAssociation
  agent -> Person | Organization | SoftwareAgent
  associated_with -> Program | Project | Resource | Annotation | FundingSource
  role -> AgentRoleEnum
```

## Why associations?

A person or organization can play different roles in different contexts. For example, the same person may be a principal investigator on one project, a curator on a systematic-review annotation, and a maintainer of a software resource. `AgentAssociation` lets each relationship carry a role, date range, source, affiliation context, and contribution description.

## Reuse targets

- `Person` maps to `schema:Person`, `biolink:Person`, and `prov:Person`.
- `Organization` maps to `schema:Organization`, `biolink:Organization`, and `prov:Organization`.
- `Project` and `Program` map to `schema:Project` and are close to `prov:Activity`.
- `FundingSource` maps to `schema:Grant`.
- `AgentAssociation` maps to `prov:Association` and is close to `schema:Role` and `schema:OrganizationRole`.

The model keeps HEW-specific classes while making JSON-LD/RDF exports friendly to common web, provenance, and biomedical graph tooling.
