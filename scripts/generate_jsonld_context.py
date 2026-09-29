#!/usr/bin/env python3
"""Generate the HEW JSON-LD context from the LinkML schema."""

import argparse
import json
from pathlib import Path

from hew_model.jsonld import generate_context


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=Path("schema/hew-geospatial.yaml"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(generate_context(args.schema), indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
