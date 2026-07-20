"""
BBO-3591 RPA tool demo dashboard.

A simple, didactic screen: pick a tool, see the exact instruction it's given,
hit Run, watch progress, and see a results table (success/failure, environment,
timing, loan ID/APR) with evidence screenshots per item.

Usage:
    source venv/bin/activate
    streamlit run dashboard.py
"""
import re
import time
from pathlib import Path

import requests
import streamlit as st

BASE_URL = "http://localhost:8000"
ENV_PATH = Path(__file__).parent / ".env"
CREDENTIAL_ID = "cred_553496609955839682"  # UiBank test login, stored in Skyvern's vault
UIBANK_URL = "https://uibank.uipath.com/"

DEFAULT_ITEMS = [
    {"label": "Item 1", "amount": 5000, "term_months": 24, "purpose": "debt consolidation"},
    {"label": "Item 2", "amount": 15000, "term_months": 36, "purpose": "home improvement"},
    {"label": "Item 3", "amount": 30000, "term_months": 48, "purpose": "auto purchase"},
]

DEFAULT_INSTRUCTION = (
    "You are already logged in to UiBank. Navigate to the Loan Center and click "
    "'Apply For A Loan'. Complete the loan application form using placeholder test data: "
    "loan amount ${amount}, purpose '{purpose}', term {term_months} months if asked, and "
    "reasonable fake placeholder values for any other required fields (income, employment, etc). "
    "Do not use real personal or financial information. Submit the application. "
    "The portal may either approve or reject/deny the application — both are valid outcomes, "
    "do not treat a rejection as a task failure or retry the form. "
    "COMPLETE as soon as the final result page is displayed (approved or rejected), and report "
    "the confirmation/rejection message, loan/application ID if shown, APR if shown, and "
    "approval status (approved or rejected)."
)


def load_api_key():
    text = ENV_PATH.read_text()
    m = re.search(r"SKYVERN_API_KEY=['\"]?([^'\"\n]+)", text)
    return m.group(1)


def h(api_key):
    return {"x-api-key": api_key, "Content-Type": "application/json"}


def poll_run(run_id, api_key, on_update=None):
    terminal = {"completed", "failed", "terminated", "timed_out", "canceled"}
    start = time.time()
    while True:
        resp = requests.get(f"{BASE_URL}/v1/runs/{run_id}", headers=h(api_key)).json()
        status = resp.get("status")
        if on_update:
            on_update(status, resp.get("step_count"), round(time.time() - start, 1))
        if status in terminal:
            resp["_elapsed_seconds"] = round(time.time() - start, 1)
            return resp
        time.sleep(4)


def run_skyvern_demo(items, instruction_template, log):
    api_key = load_api_key()

    log("Creating browser session...")
    session = requests.post(f"{BASE_URL}/v1/browser_sessions", headers=h(api_key), json={"timeout": 60}).json()
    session_id = session["browser_session_id"]
    log(f"Session created: {session_id}")

    log("Logging in to UiBank...")
    login_run = requests.post(
        f"{BASE_URL}/v1/run/tasks/login",
        headers=h(api_key),
        json={
            "prompt": "Log in to UiBank using the provided credential.",
            "url": UIBANK_URL,
            "credential_type": "skyvern",
            "credential_id": CREDENTIAL_ID,
            "browser_session_id": session_id,
        },
    ).json()
    login_result = poll_run(
        login_run["run_id"], api_key,
        on_update=lambda s, steps, t: log(f"  login: {s} (step {steps}, {t}s)"),
    )
    if login_result["status"] != "completed":
        log(f"Login failed: {login_result.get('failure_reason')}")
        return login_result, []

    results = []
    for item in items:
        log(f"Submitting {item['label']}: ${item['amount']} / {item['term_months']}mo / {item['purpose']}")
        prompt = instruction_template.format(**item)
        task_run = requests.post(
            f"{BASE_URL}/v1/run/tasks",
            headers=h(api_key),
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
        result = poll_run(
            task_run["run_id"], api_key,
            on_update=lambda s, steps, t, lbl=item["label"]: log(f"  {lbl}: {s} (step {steps}, {t}s)"),
        )
        results.append({"item": item, "run": result})
        log(f"{item['label']} -> {result['status']} in {result['_elapsed_seconds']}s")

    requests.post(f"{BASE_URL}/v1/browser_sessions/{session_id}/close", headers=h(api_key))
    log("Session closed.")
    return login_result, results


st.set_page_config(page_title="BBO-3591 RPA Tool Demo", layout="wide")
st.title("RPA Tool Demo — BBO-3591")
st.caption("UiPath replacement evaluation: run a live automation and see what happened, item by item.")

tool = st.selectbox("Tool", ["Skyvern (self-hosted, GPT-5.5)"], help="More tools get added here as they're tested.")

st.subheader("Instruction given to the tool")
st.caption(
    "This is the literal text sent to the AI for each item — no pre-recorded clicks, no selectors. "
    "{amount}, {term_months}, and {purpose} get filled in per item below."
)
instruction = st.text_area("Prompt template", value=DEFAULT_INSTRUCTION, height=160)

st.subheader("Items to submit on the portal")
st.caption(
    "Editable — change values, add rows, or set one up to be an exception case "
    "(e.g. a very large amount) to see how the tool behaves when the portal doesn't approve it."
)
edited_items = st.data_editor(
    DEFAULT_ITEMS,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "label": st.column_config.TextColumn("Label"),
        "amount": st.column_config.NumberColumn("Amount ($)", min_value=0, step=500),
        "term_months": st.column_config.NumberColumn("Term (months)", min_value=1, step=6),
        "purpose": st.column_config.TextColumn("Purpose"),
    },
)

run_clicked = st.button("▶ Run Demo", type="primary")

if run_clicked:
    log_box = st.empty()
    log_lines = []

    def log(line):
        log_lines.append(line)
        log_box.code("\n".join(log_lines))

    with st.spinner("Running against uibank.uipath.com ..."):
        login_result, results = run_skyvern_demo(edited_items, instruction, log)

    st.subheader("Results")
    if login_result["status"] != "completed":
        st.error(f"Login failed — nothing else ran. Reason: {login_result.get('failure_reason')}")
    else:
        table_rows = []
        for r in results:
            item, run = r["item"], r["run"]
            out = run.get("output") or {}
            ran_ok = run["status"] == "completed"
            approval = (out.get("approval_status") or "").lower()
            if not ran_ok:
                result_label = "Error (tool couldn't finish)"
            elif "reject" in approval or "deny" in approval or "denied" in approval:
                result_label = "Rejected by portal"
            elif "approv" in approval:
                result_label = "Approved"
            else:
                result_label = "Completed (status unclear)"
            table_rows.append({
                "Item": item["label"],
                "Amount": f"${item['amount']}",
                "Term": f"{item['term_months']}mo",
                "Purpose": item["purpose"],
                "Result": result_label,
                "Environment": "Skyvern (self-hosted) + uibank.uipath.com",
                "Time (s)": run["_elapsed_seconds"],
                "Steps": run.get("step_count"),
                "Loan ID": out.get("loan_id") or out.get("application_id") or "-",
                "APR": out.get("apr") or "-",
                "Notes": out.get("confirmation_message") or run.get("failure_reason") or "-",
            })
        st.dataframe(table_rows, use_container_width=True)

        for r in results:
            item, run = r["item"], r["run"]
            ok = run["status"] == "completed"
            with st.expander(f"{item['label']} — evidence ({'ran ok' if ok else 'tool error'})"):
                shots = run.get("screenshot_urls") or []
                for s in shots[-2:]:
                    local_path = s.replace("file://", "")
                    if Path(local_path).exists():
                        st.image(local_path)
