#!/usr/bin/env python3
"""Validate and optionally fix authors.yaml sorting (case-insensitive alphabetical)."""

import argparse
import sys
from pathlib import Path

import yaml

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

AUTHORS_FILE = Path(__file__).parent.parent / "authors.yaml"

HEADER = """\
# yaml-language-server: $schema=./.github/authors_schema.json
# Authors mapping: GitHub username -> Author details
# This file maps author GitHub usernames (used in registry.yaml) to their full details
# for display on the website.

"""


def load_authors():
    """Load authors.yaml and return the data."""
    with open(AUTHORS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_sorted(data: dict) -> bool:
    """Check if the keys are sorted alphabetically (case-insensitive)."""
    keys = list(data.keys())
    return keys == sorted(keys, key=str.lower)


def sort_authors(data: dict):
    """Sort and write authors.yaml."""
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0].lower()))

    with open(AUTHORS_FILE, "w", encoding="utf-8") as f:
        f.write(HEADER)
        for username, details in sorted_data.items():
            f.write(f"{username}:\n")
            for key, value in details.items():
                f.write(f"  {key}: {value}\n")

    print("authors.yaml sorted successfully")


def show_diff(keys: list, sorted_keys: list):
    """Show the difference between current and expected order."""
    print("authors.yaml is not sorted alphabetically (case-insensitive).")
    print("\nCurrent order:")
    for k in keys:
        print(f"  {k}")

    print("\nExpected order:")
    for k in sorted_keys:
        print(f"  {k}")

    print("\nOut of place entries:")
    for i, (current, expected) in enumerate(zip(keys, sorted_keys)):
        if current != expected:
            print(f"  Position {i}: got '{current}', expected '{expected}'")


def main():
    parser = argparse.ArgumentParser(description="Validate or fix authors.yaml sorting")
    parser.add_argument("--fix", action="store_true", help="Sort the file instead of just validating")
    args = parser.parse_args()

    data = load_authors()

    if not data:
        print("authors.yaml is empty")
        sys.exit(0)

    if args.fix:
        sort_authors(data)
        sys.exit(0)

    # Validation mode
    if is_sorted(data):
        print("authors.yaml is sorted correctly")
        sys.exit(0)

    keys = list(data.keys())
    sorted_keys = sorted(keys, key=str.lower)
    show_diff(keys, sorted_keys)
    print("\nRun with --fix to sort automatically")
    sys.exit(1)


if __name__ == "__main__":
    main()
