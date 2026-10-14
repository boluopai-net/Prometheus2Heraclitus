"""Build a local download using the collection's canonical allowlist."""
import argparse
import importlib.util
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--revision', required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
project = Path(__file__).resolve().parents[1]
target = args.output.resolve()
if target.is_relative_to(project):
    raise SystemExit('The sharing package must be outside the website checkout')
spec = importlib.util.spec_from_file_location('collection_download', args.repo / 'scripts/publish-download.py')
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)
payload, metadata = publisher.build(args.repo, args.revision)
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(payload)
print(json.dumps(metadata))
