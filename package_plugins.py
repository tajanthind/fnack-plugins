#!/usr/bin/env python3
"""Builds and packages plugins in fnack-plugins into distribution zip files,
calculates SHA-256 checksums, and generates index.json.
"""

from __future__ import annotations

import hashlib
import json
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLUGINS_DIR = ROOT / "plugins"
DIST_DIR = ROOT / "dist"
INDEX_FILE = ROOT / "index.json"

REPO_NAME = "Official fnack Plugins"
BASE_DOWNLOAD_URL = "https://github.com/tajanthind/fnack-plugins/releases/download/v{version}/{plugin_id}.zip"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def package_plugin(plugin_dir: Path) -> dict:
    manifest_file = plugin_dir / "plugin.json"
    if not manifest_file.exists():
        raise FileNotFoundError(f"Missing plugin.json in {plugin_dir}")

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    plugin_id = manifest["id"]
    version = manifest["version"]

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DIST_DIR / f"{plugin_id}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in plugin_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                rel_path = file_path.relative_to(plugin_dir)
                zf.write(file_path, arcname=rel_path)

    sha = sha256_file(zip_path)
    download_url = BASE_DOWNLOAD_URL.format(version=version, plugin_id=plugin_id)

    types = manifest.get("type", [])
    if isinstance(types, str):
        types = [types]

    return {
        "id": plugin_id,
        "name": manifest.get("name", plugin_id),
        "latest_version": version,
        "type": types,
        "description": manifest.get("description", ""),
        "author": manifest.get("author", "fnack"),
        "homepage": manifest.get("homepage", ""),
        "permissions": manifest.get("permissions", []),
        "trust_level": manifest.get("trust_level", "official"),
        "settings_schema": manifest.get("settings_schema", []),
        "ui": manifest.get("ui", {}),
        "versions": {
            version: {
                "download_url": download_url,
                "sha256": sha,
                "min_core_version": manifest.get("min_core_version", "0.2.0"),
                "api_version": manifest.get("api_version", "^1.0"),
            }
        },
    }


def main():
    plugin_entries = []
    for pdir in sorted(PLUGINS_DIR.iterdir()):
        if pdir.is_dir() and (pdir / "plugin.json").exists():
            entry = package_plugin(pdir)
            plugin_entries.append(entry)
            print(f"Packaged {entry['id']} v{entry['latest_version']} -> sha256 {entry['versions'][entry['latest_version']]['sha256'][:16]}...")

    index_data = {
        "name": REPO_NAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "plugins": plugin_entries,
    }

    INDEX_FILE.write_text(json.dumps(index_data, indent=2), encoding="utf-8")
    print(f"\nGenerated {INDEX_FILE} with {len(plugin_entries)} plugins.")


if __name__ == "__main__":
    main()
