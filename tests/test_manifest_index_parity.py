#!/usr/bin/env python3
"""Deterministic parity test: plugins/*/plugin.json <-> index.json.

Every field the packager copies from a source manifest into `index.json` must
match exactly (capabilities, type, settings_schema, versions metadata, ...).
It uses `package_plugins.package_plugin()` itself (with a throwaway dist dir)
so the test verifies precisely what packaging produces — nothing more, nothing
less. This is the regression guard for manifest/index drift (e.g. the
`fnack.deezer-batch` capability inconsistency).

Run from the repo root with plain python (no pytest, no network):

    python3 tests/test_manifest_index_parity.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import package_plugins  # noqa: E402

PLUGINS_DIR = ROOT / "plugins"
INDEX_FILE = ROOT / "index.json"


def load_index() -> dict:
    data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    entries = data["plugins"]
    return {e["id"]: e for e in entries}


def packaged_entry(plugin_dir: Path, dist_dir: Path) -> dict:
    """What package_plugins.py would write into the index for this dir."""
    old_dist = package_plugins.DIST_DIR
    try:
        package_plugins.DIST_DIR = dist_dir
        return package_plugins.package_plugin(plugin_dir)
    finally:
        package_plugins.DIST_DIR = old_dist


def compare(expected: dict, actual: dict, pid: str) -> list[str]:
    """Return a list of mismatch descriptions (empty == consistent)."""
    problems: list[str] = []
    scalar_keys = ["id", "name", "latest_version", "type", "description",
                   "author", "homepage", "permissions", "trust_level",
                   "capabilities", "settings_schema", "ui"]
    for key in scalar_keys:
        if expected.get(key) != actual.get(key):
            problems.append(
                f"{pid}: {key} mismatch\n  source/packaged: {json.dumps(expected.get(key))}\n"
                f"  index:           {json.dumps(actual.get(key))}"
            )
    # versions metadata
    exp_ver = expected.get("versions", {})
    act_ver = actual.get("versions", {})
    if set(exp_ver) != set(act_ver):
        problems.append(f"{pid}: version keys mismatch {sorted(exp_ver)} vs {sorted(act_ver)}")
    else:
        for v in exp_ver:
            for key in ["min_core_version", "api_version"]:
                if exp_ver[v].get(key) != act_ver[v].get(key):
                    problems.append(f"{pid} v{v}: {key} mismatch "
                                    f"{exp_ver[v].get(key)!r} vs {act_ver[v].get(key)!r}")
            # download_url shape is versioned by design; compare the pattern.
            if act_ver[v].get("download_url") != package_plugins.BASE_DOWNLOAD_URL.format(
                    version=v, plugin_id=pid):
                problems.append(f"{pid} v{v}: download_url does not match the repo pattern")
            if not act_ver[v].get("sha256") or len(act_ver[v]["sha256"]) != 64:
                problems.append(f"{pid} v{v}: sha256 missing or not a hex digest")
    return problems


def main() -> int:
    index = load_index()
    problems: list[str] = []
    source_dirs = sorted(
        p for p in PLUGINS_DIR.iterdir()
        if p.is_dir() and (p / "plugin.json").exists()
    )

    # 1. Every source manifest has an index entry (and the id is the key).
    missing = [p.name for p in source_dirs if p.name not in index]
    if missing:
        problems.append(f"plugins missing from index.json: {missing}")

    # 2. Every index entry has a source manifest (no stale/orphan entries).
    stale = sorted(set(index) - {p.name for p in source_dirs})
    if stale:
        problems.append(f"index.json entries with no source manifest: {stale}")

    # 3. Field-by-field parity using the packager's own output.
    with tempfile.TemporaryDirectory() as tmp:
        dist = Path(tmp) / "dist"
        for pdir in source_dirs:
            try:
                expected = packaged_entry(pdir, dist)
            except Exception as exc:  # noqa: BLE001
                problems.append(f"{pdir.name}: package_plugin() failed: {exc}")
                continue
            actual = index.get(pdir.name)
            if actual is None:
                continue  # already reported missing
            problems.extend(compare(expected, actual, pdir.name))

    if problems:
        print(f"MANIFEST/INDEX PARITY FAILED ({len(problems)} problem(s)):\n")
        for p in problems:
            print(f"- {p}\n")
        print("Fix the source manifest (plugins/<id>/plugin.json), then run "
              "`python3 package_plugins.py` to regenerate index.json.")
        return 1

    print(f"MANIFEST/INDEX PARITY OK: {len(source_dirs)} plugins, "
          f"{len(index)} index entries, all fields consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
