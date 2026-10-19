#!/usr/bin/env python3
"""Execute all finite checks and compare with committed reference outputs."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = ("check_circuits", "check_statistics", "check_precision", "resource_table")


def compare(actual, expected, location="root"):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), location
        assert actual.keys() == expected.keys(), (location, actual.keys(), expected.keys())
        for key in expected:
            compare(actual[key], expected[key], location + "." + key)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), location
        for i, (a, b) in enumerate(zip(actual, expected)):
            compare(a, b, f"{location}[{i}]")
    elif isinstance(expected, float):
        assert isinstance(actual, (int, float)) and math.isfinite(actual), location
        assert math.isclose(actual, expected, rel_tol=1e-7, abs_tol=1e-10), (location, actual, expected)
    else:
        assert actual == expected, (location, actual, expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true", help="Replace reference JSON after all script assertions pass.")
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("Do not use Python -O: verification uses assertions.")
    results = {}
    # All script assertions run before any reference output is replaced.
    for name in SCRIPTS:
        process = subprocess.run([sys.executable, str(ROOT / (name + ".py"))],
                                 cwd=ROOT.parent, check=True, text=True, capture_output=True)
        results[name] = json.loads(process.stdout)
    reference = ROOT / "expected"
    if args.record:
        reference.mkdir(exist_ok=True)
        for name, result in results.items():
            (reference / (name + ".json")).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        for name, result in results.items():
            compare(result, json.loads((reference / (name + ".json")).read_text()), name)
    print(json.dumps({"status": "passed", "scripts": list(SCRIPTS),
                      "reference_mode": "recorded" if args.record else "compared",
                      "scope": "finite ideal-circuit, perturbation, statistics and resource checks"}, indent=2))


if __name__ == "__main__":
    main()
