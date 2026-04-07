---
name: stuck-diagnostic
description: "Diagnose frozen, hung, or slow Claude Code sessions via system inspections"
trigger: "user reports session is stuck, frozen, hung, slow, or unresponsive"
---

Run diagnostic checks to identify why the session is stuck or slow.

## Checks

1. **CPU usage** of current process and children
2. **Zombie processes** — defunct child processes
3. **Stdin waits** — child processes waiting on input
4. **Disk space** — available storage
5. **Memory usage** — RAM utilization
6. **File descriptor leaks** — open FD counts
7. **Network connectivity** — API endpoint reachability
8. **Recent stderr** — error pattern analysis

## Report Format

- Process state (running, sleeping, zombie)
- Resource utilization (CPU, memory, disk)
- Child process status
- Network status
- Recommended action

If the issue is identified, suggest a fix. Otherwise recommend sharing the session
for further investigation.
