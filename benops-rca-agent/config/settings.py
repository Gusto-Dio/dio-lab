import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise EnvironmentError(f"Required env var missing: {key}")
    return val


class Settings:
    anthropic_api_key: str = _require("ANTHROPIC_API_KEY")
    github_token: str = _require("GITHUB_TOKEN")
    orchestrator_org: str = os.getenv("ORCHESTRATOR_ORG", "Gusto")
    orchestrator_repo: str = os.getenv("ORCHESTRATOR_REPO", "biztech-uipath-rpa")
    jira_token: str = _require("JIRA_TOKEN")
    jira_base_url: str = _require("JIRA_BASE_URL")
    jira_project_key: str = os.getenv("JIRA_PROJECT_KEY", "BT")
    slack_token: str = _require("SLACK_TOKEN")
    slack_alert_channel: str = os.getenv("SLACK_ALERT_CHANNEL", "#benops-rpa-alerts")
    slack_dev_channel: str = os.getenv("SLACK_DEV_CHANNEL", "#benops-rpa-dev")
    orchestrator_folder_key: str = _require("ORCHESTRATOR_FOLDER_KEY")
    poll_interval: int = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))


settings = Settings()
