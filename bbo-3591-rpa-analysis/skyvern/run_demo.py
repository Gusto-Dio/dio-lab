#!/usr/bin/env python3
"""
BBO-3591 Skyvern demo runner.

Logs in once to UiBank, then submits 3 loan applications with different
amounts/terms/purposes in the same session, capturing status, timing,
and evidence (screenshots) for each. Ends with a markdown report.

Usage:
    source venv/bin/activate
    python run_demo.py
"""
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "http://localhost:8000"
ENV_PATH = Path(__file__).parent / ".env"
REPORT_DIR = Path(__file__).parent / "demo_reports"
REPORT_DIR.mkdir(exist_ok=True)

LOAN_ITEMS = [
    {"label": "Item 1", "amount": 5000, "term_months": 24, "purpose": "debt consolidation"},
    {"label": "Item 2", "amount": 15000, "term_months": 36, "purpose": "home improvement"},
    {"label": "Item 3", "amount": 30000, "term_months": 48, "purpose": "auto purchase"},
]

CREDENTIAL_ID = "cred_553496609955839682"  # UiBank test login, stored in Skyvern's vault
UIBANK_URL = "https://uibank.uipath.com/"


def load_api_key():
    text = ENV_PATH.read_text()
    m = re.search(r"SKYVERN_API_KEY=['\"]?([^'\"\n]+)", text)
    if not m:
        raise SystemExit("SKYVERN_API_KEY not found in .env")
    return m.group(1)


def headers(api_key):
    return {"x-api-key": api_key, "Content-Type": "application/json"}


def poll_run(run_id, api_key, label):
    terminal = {"completed", "failed", "terminated", "timed_out", "canceled"}
    start = time.time()
    while True:
        resp = requests.get(f"{BASE_URL}/v1/runs/{run_id}", headers=headers(api_key)).json()
        status = resp.get("status")
        if status in terminal:
            resp["_elapsed_seconds"] = round(time.time() - start, 1)
            return resp
        print(f"  [{label}] status={status} steps={resp.get('step_count')} ({int(time.time()-start)}s)")
        time.sleep(5)


def main():
    api_key = load_api_key()
    run_started_at = datetime.now(timezone.utc).isoformat()

    print("Creating browser session...")
    session = requests.post(f"{BASE_URL}/v1/browser_sessions", headers=headers(api_key), json={"timeout": 60}).json()
    session_id = session["browser_session_id"]
    print(f"  session_id={session_id}")

    print("Logging in...")
    login_run = requests.post(
        f"{BASE_URL}/v1/run/tasks/login",
        headers=headers(api_key),
        json={
            "prompt": "Log in to UiBank using the provided credential.",
            "url": UIBANK_URL,
            "credential_type": "skyvern",
            "credential_id": CREDENTIAL_ID,
            "browser_session_id": session_id,
        },
    ).json()
    login_result = poll_run(login_run["run_id"], api_key, "login")
    print(f"  login status={login_result['status']} in {login_result['_elapsed_seconds']}s")

    results = []
    for item in LOAN_ITEMS:
        print(f"\nSubmitting {item['label']}: ${item['amount']} / {item['term_months']}mo / {item['purpose']}")
        prompt = (
            "You are already logged in to UiBank. Navigate to the Loan Center and click "
            "'Apply For A Loan'. Complete the loan application form using placeholder test data: "
            f"loan amount ${item['amount']}, purpose '{item['purpose']}', term {item['term_months']} months "
            "if asked, and reasonable fake placeholder values for any other required fields "
            "(income, employment, etc). Do not use real personal or financial information. "
            "Submit the application. COMPLETE when the final confirmation/result page is displayed, "
            "and report the confirmation message, loan/application ID, APR if shown, and approval status."
        )
        task_run = requests.post(
            f"{BASE_URL}/v1/run/tasks",
            headers=headers(api_key),
            json={
                "prompt": prompt,
                "browser_session_id": session_id,
                "max_steps": 15,
                "title": f"BBO-3591 demo - {item['label']}",
                "data_extraction_schema": {
                    "type": "object",
                    "properties": {
                        "confirmation_message": {"type": "string"},
                        "loan_id": {"type": "string"},
                        "apr": {"type": "string"},
                        "approval_status": {"type": "string"},
                    },
                },
            },
        ).json()
        result = poll_run(task_run["run_id"], api_key, item["label"])
        results.append({"item": item, "run": result})
        print(f"  {item['label']} -> status={result['status']} steps={result.get('step_count')} "
              f"time={result['_elapsed_seconds']}s")

    close = requests.post(f"{BASE_URL}/v1/browser_sessions/{session_id}/close", headers=headers(api_key))
    print(f"\nSession closed: {close.status_code}")

    write_report(run_started_at, login_result, results)


def write_report(run_started_at, login_result, results):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"demo_report_{ts}.md"
    raw_path = REPORT_DIR / f"demo_raw_{ts}.json"

    lines = []
    lines.append("# Skyvern demo run - UiBank loan applications (BBO-3591)")
    lines.append("")
    lines.append(f"Run started: {run_started_at}")
    lines.append(f"Login: {login_result['status']} in {login_result['_elapsed_seconds']}s "
                 f"({login_result.get('step_count')} steps)")
    lines.append("")
    lines.append("| Item | Amount | Term | Purpose | Status | Steps | Time (s) | Result |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in results:
        item, run = r["item"], r["run"]
        out = run.get("output") or {}
        loan_id = out.get("loan_id") or out.get("application_id") or out.get("reference_id") or out.get("loan_or_application_id")
        result_str = out.get("confirmation_message") or out.get("summary") or run.get("failure_reason") or "-"
        if loan_id:
            result_str = f"{result_str} (loan ID: {loan_id})"
        result_str = result_str.replace("|", "/").replace("\n", " ")
        lines.append(
            f"| {item['label']} | ${item['amount']} | {item['term_months']}mo | {item['purpose']} | "
            f"{run['status']} | {run.get('step_count')} | {run['_elapsed_seconds']} | {result_str} |"
        )
    lines.append("")
    lines.append("## Details per item")
    for r in results:
        item, run = r["item"], r["run"]
        out = run.get("output") or {}
        lines.append(f"### {item['label']} (${item['amount']}, {item['term_months']}mo, {item['purpose']})")
        lines.append(f"- run_id: `{run['run_id']}`")
        lines.append(f"- status: **{run['status']}**")
        loan_id = out.get("loan_id") or out.get("application_id") or out.get("reference_id") or out.get("loan_or_application_id")
        lines.append(f"- application/loan ID: {loan_id or 'n/a'}")
        lines.append(f"- confirmation: {out.get('confirmation_message') or 'n/a'}")
        lines.append(f"- APR: {out.get('apr') or 'n/a'}")
        lines.append(f"- approval status: {out.get('approval_status') or out.get('status') or 'n/a'}")
        if run.get("screenshot_urls"):
            lines.append(f"- evidence screenshots ({len(run['screenshot_urls'])}):")
            for s in run["screenshot_urls"]:
                lines.append(f"  - {s}")
        lines.append("")

    report_path.write_text("\n".join(lines))
    raw_path.write_text(json.dumps({"login": login_result, "results": results}, indent=2, default=str))

    print(f"\nReport written to: {report_path}")
    print(f"Raw data written to: {raw_path}")


if __name__ == "__main__":
    main()
