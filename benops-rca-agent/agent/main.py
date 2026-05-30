"""BenOps RCA Agent — main polling loop."""

import sys
import time
from datetime import datetime

from agent import ai_analyst, context_collector, jira_creator, priority_checker, slack_notifier
from agent.failure_listener import FailureListener
from config.settings import settings


def process_job(job, listener_ref=None):
    started_at = datetime.now()
    print(f"\n{'='*60}")
    print(f"[Main] Processing: {job.process_name} | Key: {job.key}")
    print(f"[Main] Error: {job.error_message[:100]}")

    # Collect context in parallel
    print("[Main] Collecting context...")
    ctx = context_collector.collect(job)

    # Run 3-phase AI analysis
    print("[Main] Running AI analysis...")
    rca = ai_analyst.analyze(ctx)

    # Check priority
    high_priority = priority_checker.is_high_priority(job.process_name)
    print(f"[Main] Priority: {'HIGH' if high_priority else 'STANDARD'}")

    if high_priority:
        # Create Jira ticket + alert channel
        jira_key = jira_creator.create_ticket(job, rca)
        slack_notifier.notify_high_priority(job, rca, jira_key)
    else:
        # Dev channel only
        slack_notifier.notify_standard(job, rca)

    elapsed = (datetime.now() - started_at).total_seconds()
    print(f"[Main] Done in {elapsed:.1f}s — {rca.failure_type} ({rca.severity})")
    print(f"{'='*60}")


def run():
    print("[Main] BenOps RCA Agent starting...")
    print(f"[Main] Poll interval: {settings.poll_interval}s")
    print(f"[Main] Folder key: {settings.orchestrator_folder_key}")

    listener = FailureListener()

    # Warm up: pre-load skill knowledge into cache
    print("[Main] Pre-loading UiPath skill knowledge...")
    ai_analyst._load_skill_knowledge()
    print("[Main] Skill knowledge loaded. Ready.\n")

    while True:
        try:
            jobs = listener.poll()
            if jobs:
                print(f"[Main] Found {len(jobs)} new Faulted job(s)")
                for job in jobs:
                    try:
                        process_job(job)
                    except Exception as exc:
                        print(f"[Main] Error processing job {job.key}: {exc}")
            else:
                print(f"[Main] No new failures. Next poll in {settings.poll_interval}s...")
        except KeyboardInterrupt:
            print("\n[Main] Shutting down.")
            sys.exit(0)
        except Exception as exc:
            print(f"[Main] Poll error: {exc}")

        time.sleep(settings.poll_interval)


if __name__ == "__main__":
    run()
