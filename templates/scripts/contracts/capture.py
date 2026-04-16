"""
capture.py — Export OpenAPI từ FastAPI đang chạy → docs/contracts/api/ha_lac.yaml

Usage:
    python scripts/contracts/capture.py [--host http://localhost:8000]

Yêu cầu: backend đang chạy.
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
    sys.exit(1)


def capture(host: str) -> None:
    out_path = Path("docs/contracts/api/ha_lac.yaml")
    url = f"{host.rstrip('/')}/openapi.json"

    print(f"Fetching: {url}")
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
    except httpx.ConnectError:
        print(f"ERROR: Cannot connect to {url}. Is the backend running?")
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"ERROR: HTTP {e.response.status_code}")
        sys.exit(1)

    spec = response.json()

    # Convert JSON → YAML
    yaml_content = yaml.dump(spec, allow_unicode=True, sort_keys=False, default_flow_style=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml_content, encoding="utf-8")

    print(f"Saved to: {out_path}")
    print(f"Title: {spec.get('info', {}).get('title', 'unknown')}")
    print(f"Version: {spec.get('info', {}).get('version', 'unknown')}")
    paths = list(spec.get("paths", {}).keys())
    print(f"Endpoints ({len(paths)}): {', '.join(paths)}")
    print()
    print("Next: update _registry.md with new version + date.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture OpenAPI spec from running FastAPI")
    parser.add_argument("--host", default="http://localhost:8000", help="Backend host URL")
    args = parser.parse_args()
    capture(args.host)


if __name__ == "__main__":
    main()
