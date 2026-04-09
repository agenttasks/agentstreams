Set up or manage scheduled tasks for this project. Available pre-built schedules:

- daily-review: Review all PRs opened in the last 24 hours (runs at 9am)
- dep-audit: Check for outdated or vulnerable dependencies (daily)
- ci-monitor: Check CI status for main branch (every 30 minutes)
- security-scan: Run security audit on recent changes (every 6 hours)
- cost-report: Summarize today's Claude Code usage and costs (daily)

Usage:
- List schedules: show all configured schedules
- Enable a schedule: activate one of the pre-built schedules
- Create custom: define a new recurring task with interval and prompt
- Disable a schedule: deactivate without deleting

$ARGUMENTS
