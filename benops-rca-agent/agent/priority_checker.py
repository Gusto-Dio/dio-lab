"""Checks if a process is high-priority via Orchestrator Asset."""

import json
import shutil
import subprocess

from config.settings import settings

_priority_cache: list[str] | None = None


def _uip(*args: str) -> dict:
    uip_bin = shutil.which("uip")
    result = subprocess.run(
        [uip_bin, *args, "--output", "json"],
        capture_output=True, text=True, timeout=15,
    )
    if result.returncode != 0:
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def _load_priority_list() -> list[str]:
    global _priority_cache
    if _priority_cache is not None:
        return _priority_cache

    data = _uip(
        "or", "assets", "get", "RCA_Priority_Processes",
        "--folder-key", settings.orchestrator_folder_key,
    )
    value = data.get("Value", data.get("StringValue", ""))
    try:
        processes = json.loads(value) if value else []
        _priority_cache = [p.strip() for p in processes]
    except (json.JSONDecodeError, TypeError):
        # Fallback: comma-separated list
        _priority_cache = [p.strip() for p in str(value).split(",") if p.strip()]

    print(f"[PriorityChecker] Loaded {len(_priority_cache)} high-priority processes")
    return _priority_cache


def is_high_priority(process_name: str) -> bool:
    priority_list = _load_priority_list()
    return any(
        p.lower() in process_name.lower() or process_name.lower() in p.lower()
        for p in priority_list
    )


def invalidate_cache() -> None:
    global _priority_cache
    _priority_cache = None
