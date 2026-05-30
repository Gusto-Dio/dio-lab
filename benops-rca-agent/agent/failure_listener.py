"""Polls UiPath Orchestrator for Faulted jobs via uip CLI."""

import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime

from config.settings import settings


@dataclass
class FaultedJob:
    key: str
    process_name: str
    error_message: str
    start_time: str
    end_time: str
    machine_name: str
    robot_name: str
    folder_key: str


def _uip(*args: str) -> dict:
    uip_bin = shutil.which("uip")
    if not uip_bin:
        raise RuntimeError("uip CLI not found in PATH. Run: npm -g install @uipath/cli")
    result = subprocess.run(
        [uip_bin, *args, "--output", "json"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"uip error: {result.stderr.strip()}")
    return json.loads(result.stdout)


class FailureListener:
    def __init__(self):
        self._processed: set[str] = set()

    def poll(self) -> list[FaultedJob]:
        """Returns newly discovered Faulted jobs not yet processed."""
        try:
            data = _uip(
                "or", "jobs", "list",
                "--folder-key", settings.orchestrator_folder_key,
                "--state", "Faulted",
            )
        except Exception as exc:
            print(f"[FailureListener] Poll error: {exc}")
            return []

        jobs = data.get("Data", data) if isinstance(data, dict) else data
        new_jobs = []
        for job in jobs:
            key = str(job.get("Key") or job.get("Id", ""))
            if not key or key in self._processed:
                continue
            self._processed.add(key)
            info = job.get("Info", "") or ""
            new_jobs.append(FaultedJob(
                key=key,
                process_name=job.get("ReleaseName", job.get("ProcessName", "unknown")),
                error_message=info[:500],
                start_time=job.get("StartTime", ""),
                end_time=job.get("EndTime", ""),
                machine_name=job.get("MachineName", ""),
                robot_name=job.get("Robot", {}).get("Name", "") if isinstance(job.get("Robot"), dict) else "",
                folder_key=settings.orchestrator_folder_key,
            ))
        return new_jobs
