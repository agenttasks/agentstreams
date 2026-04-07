---
name: prompt-suggest
description: "Predict user's next likely command and display as suggestions"
trigger: "user asks for prompt suggestions, next steps, or what to do next"
---

Predict the user's next likely command or question based on conversation context.

## Rules

- Generate 1-3 suggestions
- Each suggestion: 2-8 words
- Match user's communication style (formal/informal)
- Prioritize actionable commands over questions
- Deduplicate against recent commands
- Focus on logical next steps given current work

## Output Format

Return suggestions as a JSON array:

```json
["Run the test suite", "Review the diff", "Push to remote"]
```
