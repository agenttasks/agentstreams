---
name: skillify
description: "Interactive interview that captures repeatable processes into SKILL.md files"
trigger: "user wants to create a new skill, capture a workflow, or document a repeatable process"
---

Interview the user about a repeatable process and generate a SKILL.md file.

## Interview Process

1. Ask what process to capture as a skill
2. Ask clarifying questions about:
   - When this process should be triggered
   - What steps are involved
   - What tools or commands are used
   - What the expected outcome is
   - Any constraints or edge cases
3. Confirm the skill scope with the user
4. Generate the SKILL.md file in `.claude/skills/`

## SKILL.md Format

```markdown
---
name: [skill name]
description: [short description]
---

[Detailed instructions for executing the skill]
```

## Guidelines

- Keep the skill focused on a single, repeatable process
- Include specific commands, file paths, and code patterns
- Document prerequisites and assumptions
- Use clear, imperative instructions
- Make the skill generic enough for similar projects
