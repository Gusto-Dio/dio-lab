"""Posts RCA alerts to Slack using Block Kit."""

import requests

from agent.ai_analyst import RCAResult
from agent.failure_listener import FaultedJob
from config.settings import settings

_SEVERITY_EMOJI = {"critical": "🔴", "high": "🟠", "medium": "🟡"}
_TYPE_EMOJI = {
    "portal_change": "🌐",
    "data_quality": "📋",
    "business_rule": "📜",
    "network_timeout": "⏱️",
    "library_incompatibility": "📦",
    "credential_error": "🔑",
    "unknown": "❓",
}


def _post(channel: str, blocks: list, text: str) -> None:
    headers = {
        "Authorization": f"Bearer {settings.slack_token}",
        "Content-Type": "application/json",
    }
    payload = {"channel": channel, "blocks": blocks, "text": text}
    try:
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            json=payload,
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            print(f"[SlackNotifier] Slack error: {data.get('error')}")
        else:
            print(f"[SlackNotifier] Posted to {channel}")
    except Exception as exc:
        print(f"[SlackNotifier] Failed: {exc}")


def notify_high_priority(job: FaultedJob, rca: RCAResult, jira_key: str | None) -> None:
    sev_emoji = _SEVERITY_EMOJI.get(rca.severity, "⚠️")
    type_emoji = _TYPE_EMOJI.get(rca.failure_type, "❓")
    jira_link = f"{settings.jira_base_url}/browse/{jira_key}" if jira_key else "N/A"
    transactions = ", ".join(rca.affected_transactions[:3]) or "none"

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"{sev_emoji} BOT FAILURE — {job.process_name}"},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Failure type:*\n{type_emoji} `{rca.failure_type}`"},
                {"type": "mrkdwn", "text": f"*Severity:*\n{sev_emoji} {rca.severity.upper()}"},
                {"type": "mrkdwn", "text": f"*Confidence:*\n{rca.confidence}"},
                {"type": "mrkdwn", "text": f"*Transactions:*\n{transactions}"},
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Root Cause:*\n{rca.root_cause[:300]}"},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Suggested Fix:*\n{rca.suggested_fix[:300]}"},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Job Key:*\n`{job.key}`"},
                {"type": "mrkdwn", "text": f"*Ticket:*\n<{jira_link}|{jira_key or 'N/A'}>"},
            ],
        },
    ]
    text = f"[BOT FAILURE] {job.process_name} — {rca.failure_type} — {rca.severity.upper()}"
    _post(settings.slack_alert_channel, blocks, text)


def notify_standard(job: FaultedJob, rca: RCAResult) -> None:
    type_emoji = _TYPE_EMOJI.get(rca.failure_type, "❓")
    file_ref = f"`{rca.affected_file}`" if rca.affected_file else "unknown file"

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*[BOT ALERT]* {job.process_name} failed\n"
                    f"{type_emoji} Cause: `{rca.failure_type}` | File: {file_ref}\n"
                    f"Note: Non-priority process — no ticket opened"
                ),
            },
        }
    ]
    text = f"[BOT ALERT] {job.process_name} failed — {rca.failure_type}"
    _post(settings.slack_dev_channel, blocks, text)
