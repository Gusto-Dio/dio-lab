"""Collects all context needed for root cause analysis in parallel."""

import base64
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timedelta

import requests

from agent.failure_listener import FaultedJob
from config.settings import settings

_xaml_cache: dict[str, dict] = {}


def _uip(*args: str) -> dict:
    uip_bin = shutil.which("uip")
    result = subprocess.run(
        [uip_bin, *args, "--output", "json"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout[:2000]}


@dataclass
class JobContext:
    job: FaultedJob
    job_details: dict = field(default_factory=dict)
    execution_logs: list = field(default_factory=list)
    job_history: list = field(default_factory=list)
    execution_traces: dict = field(default_factory=dict)
    xaml_source: dict[str, str] = field(default_factory=dict)
    pr_history: list = field(default_factory=list)


def _fetch_job_details(job: FaultedJob) -> dict:
    return _uip("or", "jobs", "get", job.key)


def _fetch_execution_logs(job: FaultedJob) -> list:
    data = _uip("or", "jobs", "logs", job.key)
    logs = data.get("Data", data) if isinstance(data, dict) else data
    return logs if isinstance(logs, list) else []


def _fetch_job_history(job: FaultedJob) -> list:
    data = _uip("or", "jobs", "history", job.key)
    history = data.get("Data", data) if isinstance(data, dict) else data
    return history if isinstance(history, list) else []


def _fetch_execution_traces(job: FaultedJob) -> dict:
    return _uip("traces", "spans", "get", "--job-key", job.key)


def _fetch_xaml_file(process_name: str, filename: str) -> str:
    cache_key = f"{process_name}/{filename}"
    cached = _xaml_cache.get(cache_key)
    if cached and datetime.now() - cached["fetched_at"] < timedelta(minutes=30):
        return cached["content"]

    org = settings.orchestrator_org
    repo = settings.orchestrator_repo
    headers = {
        "Authorization": f"token {settings.github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    path = f"{process_name}/{filename}"
    url = f"https://api.github.com/repos/{org}/{repo}/contents/{path}"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        _xaml_cache[cache_key] = {"content": content, "fetched_at": datetime.now()}
        return content
    except Exception as exc:
        return f"[Could not fetch {filename}: {exc}]"


def _fetch_pr_history(process_name: str, n: int = 3) -> list:
    org = settings.orchestrator_org
    repo = settings.orchestrator_repo
    headers = {
        "Authorization": f"token {settings.github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{org}/{repo}/pulls"
    params = {"state": "closed", "per_page": 20}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        prs = resp.json()
        relevant = [
            {"number": pr["number"], "title": pr["title"], "merged_at": pr.get("merged_at"),
             "body": (pr.get("body") or "")[:300]}
            for pr in prs
            if process_name.lower() in (pr.get("title", "") + pr.get("body", "")).lower()
            and pr.get("merged_at")
        ]
        return relevant[:n]
    except Exception as exc:
        return [{"error": str(exc)}]


def collect(job: FaultedJob) -> JobContext:
    ctx = JobContext(job=job)
    tasks = {
        "details": lambda: _fetch_job_details(job),
        "logs": lambda: _fetch_execution_logs(job),
        "history": lambda: _fetch_job_history(job),
        "traces": lambda: _fetch_execution_traces(job),
        "process_xaml": lambda: _fetch_xaml_file(job.process_name, "Process.xaml"),
        "main_xaml": lambda: _fetch_xaml_file(job.process_name, "Main.xaml"),
        "prs": lambda: _fetch_pr_history(job.process_name),
    }
    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = {executor.submit(fn): key for key, fn in tasks.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                result = future.result()
                if key == "details":
                    ctx.job_details = result
                elif key == "logs":
                    ctx.execution_logs = result
                elif key == "history":
                    ctx.job_history = result
                elif key == "traces":
                    ctx.execution_traces = result
                elif key in ("process_xaml", "main_xaml"):
                    filename = "Process.xaml" if key == "process_xaml" else "Main.xaml"
                    ctx.xaml_source[filename] = result
                elif key == "prs":
                    ctx.pr_history = result
            except Exception as exc:
                print(f"[ContextCollector] {key} failed: {exc}")
    return ctx
