"""
validate.py — So sánh OpenAPI live với spec đã commit.

Usage:
    python scripts/contracts/validate.py [--host http://localhost:8000]

Exit code:
    0 = match
    1 = drift detected (in ra diff)
    2 = error (cannot connect, missing file)
"""
import sys
import json
import argparse
from pathlib import Path

try:
    import httpx
    import yaml
except ImportError:
    print("Missing deps. Run: pip install httpx pyyaml")
    sys.exit(2)


def _extract_paths(spec: dict) -> dict[str, list[str]]:
    """Extract {path: [methods]} from OpenAPI spec."""
    result = {}
    for path, methods in spec.get("paths", {}).items():
        result[path] = sorted(m for m in methods if m in {"get", "post", "put", "patch", "delete"})
    return result


def _extract_schemas(spec: dict) -> set[str]:
    return set(spec.get("components", {}).get("schemas", {}).keys())


def validate(host: str) -> None:
    committed_path = Path("docs/contracts/api/ha_lac.yaml")
    if not committed_path.exists():
        print(f"ERROR: {committed_path} not found. Run capture.py first.")
        sys.exit(2)

    committed_spec = yaml.safe_load(committed_path.read_text(encoding="utf-8"))

    url = f"{host.rstrip('/')}/openapi.json"
    print(f"Fetching live spec: {url}")
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        live_spec = response.json()
    except httpx.ConnectError:
        print(f"ERROR: Cannot connect to {url}. Is the backend running?")
        sys.exit(2)

    drifts = []

    # 1. Compare paths
    committed_paths = _extract_paths(committed_spec)
    live_paths = _extract_paths(live_spec)

    for path, methods in live_paths.items():
        if path not in committed_paths:
            drifts.append(f"  [NEW ENDPOINT] {path} {methods} — not in committed spec")
        elif methods != committed_paths[path]:
            drifts.append(f"  [METHODS CHANGED] {path}: committed={committed_paths[path]}, live={methods}")

    for path in committed_paths:
        if path not in live_paths:
            drifts.append(f"  [REMOVED ENDPOINT] {path} — in spec but not in live API")

    # 2. Compare schemas (top-level)
    committed_schemas = _extract_schemas(committed_spec)
    live_schemas = _extract_schemas(live_spec)

    for s in live_schemas - committed_schemas:
        drifts.append(f"  [NEW SCHEMA] {s} — in live API but not in committed spec")
    for s in committed_schemas - live_schemas:
        drifts.append(f"  [REMOVED SCHEMA] {s} — in spec but not in live API")

    if drifts:
        print("CONTRACT DRIFT DETECTED:")
        for d in drifts:
            print(d)
        print()
        print("Action: update docs/contracts/api/ha_lac.yaml and _registry.md")
        sys.exit(1)
    else:
        print("OK — live API matches committed spec.")
        committed_version = committed_spec.get("info", {}).get("version", "?")
        print(f"Spec version: {committed_version}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate live API against committed OpenAPI spec")
    parser.add_argument("--host", default="http://localhost:8000", help="Backend host URL")
    args = parser.parse_args()
    validate(args.host)


if __name__ == "__main__":
    main()
