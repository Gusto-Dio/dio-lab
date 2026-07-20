# Skyvern PoC — BBO-3591

Hands-on test of [Skyvern](https://www.skyvern.com) (open-source, LLM+vision browser automation) as a candidate to complement/replace UiPath for BenOps RPA. Full write-up, scoring, and comparison against Browserbase/DataLand/Felicity AI: [Google Doc](https://docs.google.com/document/d/1CnebJubU1ho5mD802nqRNonmf60uCgjd9riZ6Me50YY/edit) and the [Notion matrix](https://app.notion.com/p/Dio-s-Lab-3a3ad673c6c280fa94c6ddfe63b5471a).

Test scenario: log in and submit loan applications on [uibank.uipath.com](https://uibank.uipath.com/), UiPath's own public demo site — chosen so the same task can later be run on UiPath for a direct comparison.

## What's here

- `run_demo.py` — CLI script: logs in once, submits 3 loan applications (fixed scenarios), writes a markdown report + raw JSON to `demo_reports/` (not committed — local only).
- `dashboard.py` — Streamlit screen for live demos: pick a tool (only Skyvern wired up so far), see and edit the literal prompt sent to the AI, edit the items table (add exception cases — e.g. a large amount — to see how the portal/tool handles a rejection), hit Run, watch progress, see a results table with evidence screenshots per item.

## Setup (self-hosted, no Docker)

Docker's VM image download failed here because it pulls from GitHub, which Gusto's network blocks. This path uses pip + local Homebrew Postgres/Python instead — SQLite (Skyvern's default) also works fine for a single-user local test, Postgres isn't strictly required.

```bash
brew install python@3.12          # Skyvern needs 3.11–3.13; check your default first
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

cp .env.example .env              # fill in a real OPENAI_API_KEY (or swap to Anthropic/etc — see LLM_KEY in skyvern's settings)
skyvern run server &              # starts the API on :8000, auto-generates SKYVERN_API_KEY into .env
```

Then either:

```bash
python run_demo.py                # CLI run, writes a report to demo_reports/
```

or

```bash
streamlit run dashboard.py        # visual screen, http://localhost:8501
```

## Credential setup (one-time)

The UiBank login is stored in Skyvern's own local vault, not in code. Create it once via the API (Swagger UI at `http://localhost:8000/docs` also works for this):

```bash
curl -X POST http://localhost:8000/v1/credentials \
  -H "x-api-key: $SKYVERN_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"UiBank test login","credential_type":"password","vault_type":"skyvern",
       "credential":{"username":"YOUR_USER","password":"YOUR_PASSWORD"}}'
```

Copy the returned `credential_id` into `CREDENTIAL_ID` at the top of both scripts. (`vault_type` must be set explicitly to `"skyvern"` — the default pointed at Bitwarden here and errored without it.)

## Known gaps found during setup (worth remembering)

- The pip package does **not** ship the web UI — `skyvern run ui` fails with "Frontend directory not found." Building it needs a separate Node/npm step. Swagger at `/docs` is the fallback for browser-based control without that build.
- Skyvern infers nothing about auth — a blind first attempt against a login-gated flow failed after 3 steps ("browser does not have a valid page"). Login has to be its own step (dedicated `/v1/run/tasks/login` call + a persistent `browser_session_id` shared with the follow-up task).
- Output field names in `output` are whatever the model decides unless you pass `data_extraction_schema` — without it, the same prompt returned `application_id`/`reference_id` on one run and `loan_or_application_id` on another. Both scripts here pass an explicit schema to keep parsing reliable.
