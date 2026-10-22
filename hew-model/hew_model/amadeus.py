"""Semantic checks for the optional HEW Amadeus interoperability profile."""

from datetime import datetime
import re
from typing import Any


GRID_SUPPORTS = {"raster_grid_cell", "model_grid_cell"}


def normalize_crs(value: str) -> str:
    """Normalize authority identifiers without inventing numeric SRIDs."""
    authority_code = re.fullmatch(r"([A-Za-z]+):(\d+)", value)
    ogc_uri = re.fullmatch(
        r"https?://www\.opengis\.net/def/crs/([A-Za-z]+)/[^/]+/(\d+)", value
    )
    match = authority_code or ogc_uri
    if match is None:
        raise ValueError(f"CRS has no supported authority-code representation: {value}")
    return f"{match[1].upper()}:{match[2]}"


def validate_amadeus_metadata(resource: dict[str, Any]) -> list[str]:
    """Check semantic relationships after validation against hew_amadeus.yaml.

    Returns actionable errors without modifying the record. Calendar-aware
    bounds for non-Gregorian data need validation by the source adapter.
    """
    errors = []
    spatial = resource.get("spatial_support", {})
    temporal = resource.get("temporal_support", {})
    grid = resource.get("grid_definition") or spatial.get("grid_definition")
    support_type = spatial.get("support_type")
    if support_type is None:
        errors.append("spatial_support.support_type is required")
    if support_type in GRID_SUPPORTS and not grid:
        errors.append("grid_definition is required for raster/model grid support")
    if support_type not in GRID_SUPPORTS and grid:
        errors.append("grid_definition is forbidden for non-grid support")
    if resource.get("grid_definition") and spatial.get("grid_definition"):
        if resource["grid_definition"] != spatial["grid_definition"]:
            errors.append("dataset and spatial support grid definitions disagree")
    if grid:
        if not grid.get("coordinate_reference_system_uri"):
            errors.append("grid_definition.coordinate_reference_system_uri is required")
        if not grid.get("resolution_unit"):
            errors.append("grid_definition.resolution_unit is required")
        for axis in ("resolution_x", "resolution_y"):
            if grid.get(axis, 0) <= 0:
                errors.append(f"grid_definition.{axis} must be positive")
        if ("origin_x" in grid) != ("origin_y" in grid):
            errors.append("grid origins must supply both origin_x and origin_y")
        if "origin_y" in grid and not grid.get("row_direction"):
            errors.append("grid origin requires an explicit row_direction")
        dataset_crs = resource.get("coordinate_reference_system_uri")
        grid_crs = grid.get("coordinate_reference_system_uri")
        if grid_crs:
            try:
                normalized = normalize_crs(grid_crs)
                if dataset_crs and normalize_crs(dataset_crs) != normalized:
                    errors.append("dataset and grid CRS identifiers disagree")
                if "srid" in grid:
                    if not normalized.startswith("EPSG:"):
                        errors.append("non-EPSG SRID requires an external authority mapping")
                    elif grid["srid"] != int(normalized.split(":")[1]):
                        errors.append("grid SRID disagrees with its EPSG CRS")
            except ValueError as error:
                errors.append(str(error))
    if support_type == "hex_cell":
        if not spatial.get("spatial_index_system"):
            errors.append("hex_cell support requires spatial_index_system")
        if "spatial_index_resolution" not in spatial:
            errors.append("hex_cell support requires spatial_index_resolution")

    extent = resource.get("spatial_extent", {})
    bbox = extent.get("bounding_box", {})
    if bbox and bbox["south"] > bbox["north"]:
        errors.append("bounding_box.south must not exceed north")

    def check_temporal(support: dict[str, Any], path: str) -> None:
        category = support.get("temporal_resolution")
        if category is None:
            errors.append(f"{path}.temporal_resolution is required")
        if category == "daily" and support.get("day_boundary_convention") in (
            None, "not_applicable"
        ):
            errors.append(f"{path} requires a daily day_boundary_convention")
        if support.get("day_boundary_convention") == "local_midnight":
            if not support.get("timezone"):
                errors.append(f"{path} local_midnight requires timezone")

    check_temporal(temporal, "temporal_support")
    for position, delivery in enumerate(resource.get("variable_deliveries", [])):
        effective = {
            "spatial_support": delivery.get("spatial_support", spatial),
            "temporal_support": delivery.get("temporal_support", temporal),
        }
        if "spatial_support" not in delivery:
            if grid:
                effective["grid_definition"] = grid
            if resource.get("coordinate_reference_system_uri"):
                effective["coordinate_reference_system_uri"] = resource["coordinate_reference_system_uri"]
        for error in validate_amadeus_metadata(effective):
            errors.append(f"variable_deliveries[{position}]: {error}")

    def check_extent(interval: dict[str, Any], path: str) -> None:
        status = interval.get("coverage_status")
        if status == "timeless" and (interval.get("start_time") or interval.get("end_time")):
            errors.append(f"{path} timeless coverage cannot have bounds")
        if status == "ongoing" and (not interval.get("start_time") or interval.get("end_time")):
            errors.append(f"{path} ongoing coverage requires a start and no end")
        if status == "bounded" and not (interval.get("start_time") and interval.get("end_time")):
            errors.append(f"{path} bounded coverage requires both bounds")
        bounds = []
        for field in ("start_time", "end_time"):
            if interval.get(field):
                try:
                    timestamp = datetime.fromisoformat(str(interval[field]).replace("Z", "+00:00"))
                    if timestamp.tzinfo is None:
                        errors.append(f"{path}.{field} requires a UTC offset")
                    else:
                        bounds.append(timestamp)
                except ValueError:
                    errors.append(f"{path}.{field} is not an interoperable datetime")
        if len(bounds) == 2 and bounds[0] >= bounds[1]:
            errors.append(f"{path} requires start_time before exclusive end_time")

    interval = resource.get("temporal_extent", {})
    check_extent(interval, "temporal_extent")
    for field in ("calendar", "temporal_resolution"):
        if interval.get(field) and temporal.get(field):
            if interval[field] != temporal[field]:
                errors.append(f"temporal_extent and temporal_support disagree on {field}")
    if temporal.get("temporal_resolution") == "timeless":
        if interval.get("start_time") or interval.get("end_time"):
            errors.append("timeless products cannot declare temporal bounds")
        if interval.get("coverage_status") not in (None, "timeless"):
            errors.append("timeless product conflicts with coverage_status")
    elif interval.get("coverage_status") == "timeless":
        errors.append("timeless coverage conflicts with temporal resolution")
    for position, distribution in enumerate(resource.get("distributions", [])):
        check_extent(distribution.get("temporal_extent", {}), f"distributions[{position}]")
    return errors
