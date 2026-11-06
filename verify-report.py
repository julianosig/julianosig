"""Check selected measurements against the pinned benchmark reference; Python 3, no dependencies."""

import json
import math
from pathlib import Path
import sys


def compare(expected, actual, path="report"):
    errors = []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path}: expected an object"]
        for key, value in expected.items():
            if key == "notes":
                continue
            if key not in actual:
                errors.append(f"{path}.{key}: missing")
            else:
                errors.extend(compare(value, actual[key], f"{path}.{key}"))
    elif isinstance(expected, (int, float)):
        if type(actual) not in (int, float) or not math.isclose(expected, actual, rel_tol=0, abs_tol=1e-9):
            errors.append(f"{path}: expected {expected!r}, got {actual!r}")
    elif expected != actual:
        errors.append(f"{path}: expected {expected!r}, got {actual!r}")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verify-report.py REPORT.json", file=sys.stderr)
        return 2
    try:
        reference = json.loads(Path(__file__).with_name("agent-report.example.json").read_text())
        report = json.loads(Path(sys.argv[1]).read_text())
    except (OSError, ValueError) as exc:
        print(f"Cannot read report: {exc}", file=sys.stderr)
        return 2
    errors = compare(reference, report)
    notes = report.get("notes") if isinstance(report, dict) else None
    if not isinstance(notes, list) or len(notes) < 2 or any(not isinstance(n, str) or not n.strip() for n in notes):
        errors.append("report.notes: include at least two non-empty notes for human review")
    if errors:
        print("FAIL\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: selected measurements, units and source match the pinned reference. Review notes manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
