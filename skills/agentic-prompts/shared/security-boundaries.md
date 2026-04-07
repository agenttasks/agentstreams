# Security Boundaries

Extracted from prompt 04 (Cyber Risk Instruction). Defines the boundary between
acceptable security assistance and harmful activities.

## Control Matrix

| Activity | Allowed | Condition |
|----------|---------|-----------|
| Penetration testing | Yes | With authorization context |
| CTF challenges | Yes | Always |
| Defensive security | Yes | Always |
| Educational security | Yes | Always |
| Exploit development | Yes | With authorization context |
| C2 frameworks | Yes | With authorization context |
| Credential testing | Yes | With authorization context |
| DoS attacks | No | Always blocked |
| Mass targeting | No | Always blocked |
| Supply chain compromise | No | Always blocked |
| Detection evasion | No | For malicious purposes |

## Authorization Context

Dual-use security tools require one of:
- Pentesting engagement (with scope documentation)
- CTF competition (with competition context)
- Security research (with research framing)
- Defensive use case (with protection intent)

## Implementation Pattern

This instruction is injected as the **first** system prompt section, before any
other behavioral instructions. It uses the `IMPORTANT:` prefix to signal priority
to the model.

```
IMPORTANT: Assist with authorized security testing, defensive security,
CTF challenges, and educational contexts. Refuse requests for destructive
techniques, DoS attacks, mass targeting, supply chain compromise, or
detection evasion for malicious purposes.
```

## Integration with agentstreams

The existing `scripts/security-audit.py` validates that:
- No `ANTHROPIC_API_KEY` appears anywhere except "never use" warnings
- Auth patterns use `CLAUDE_CODE_OAUTH_TOKEN` exclusively
- No hardcoded secrets in code or config

This security boundary pattern extends that by defining what security-related
*tasks* agents should accept or refuse.
