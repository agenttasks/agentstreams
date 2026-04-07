---
name: away-summary
description: "Generate 1-3 sentence recap when returning to a session after stepping away"
trigger: "user returns to session after being away, or asks what happened while they were gone"
---

Generate a brief recap of what happened in the session.

## Rules

- Exactly 1-3 short sentences
- Start with the high-level task — what the user is building or debugging
- Include the concrete next step
- Skip status reports and commit recaps
- Focus on what matters, not implementation details

## Example

"You're adding OAuth support to the API gateway. The token validation middleware
is implemented and tests pass. Next: wire up the refresh token endpoint."
