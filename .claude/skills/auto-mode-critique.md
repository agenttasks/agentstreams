---
name: auto-mode-critique
description: "Review auto-mode classifier rules for quality, clarity, completeness, and conflicts"
trigger: "user asks to review or critique their auto-mode rules, permission settings, or classifier configuration"
---

Review user-written auto-mode classifier rules for quality.

## Evaluation Criteria

1. **Clarity**: Are rules unambiguous? Could they be interpreted multiple ways?
2. **Completeness**: Do rules cover the intended scope without gaps?
3. **Conflicts**: Do any rules contradict each other?
4. **Actionability**: Can the classifier reliably apply these rules?

## Process

1. Read the auto-mode rules from settings.json (allow, soft_deny, environment sections)
2. Evaluate each rule against the four criteria
3. Flag potential issues with specific examples
4. Suggest improvements with concrete rewrites

## Guidelines

- Give concise, constructive feedback
- Rule sections use REPLACE semantics (not merge)
- Focus on rules that could cause false approvals or false blocks
- Consider edge cases the user may not have anticipated
