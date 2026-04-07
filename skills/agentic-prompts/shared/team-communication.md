# Team Communication Protocol

Extracted from prompt 06 (Teammate Addendum). Defines inter-agent communication
patterns for team/swarm mode.

## SendMessage Protocol

When running as an agent in a team:

```
- Use SendMessage with `to: "<name>"` for specific teammates
- Use SendMessage with `to: "*"` sparingly for team-wide broadcasts
- Text responses alone are NOT visible to teammates — you must use SendMessage
```

## Communication Patterns

### Direct Message
Send a targeted message to a specific teammate by name:
```
SendMessage(to: "validator", message: "Please verify the auth changes in src/auth/")
```

### Broadcast
Send to all teammates (use sparingly):
```
SendMessage(to: "*", message: "Breaking change: auth middleware signature updated")
```

### When to Broadcast
- Breaking changes that affect multiple agents
- Shared resource state changes (database schema, API contract)
- Coordination signals ("research phase complete, ready for implementation")

### When NOT to Broadcast
- Status updates that only matter to one agent
- Questions directed at a specific teammate
- Routine progress reports

## Integration with Coordinator Pattern

In coordinator mode (prompt 05), the coordinator orchestrates via Agent/SendMessage
while teammates communicate peer-to-peer when needed. The coordinator:

1. Spawns workers for research, implementation, verification
2. Workers report back via task-notification XML
3. Coordinator synthesizes and directs follow-up work
4. Workers may use SendMessage for peer coordination

## Team Topology

| Role | Communication Style |
|------|-------------------|
| Coordinator | Directs workers, synthesizes results |
| Research Worker | Reports findings, does not modify files |
| Implementation Worker | Makes changes, commits |
| Verification Worker | Tests adversarially, reports verdicts |
| Peer Agent | Direct messaging for collaboration |
