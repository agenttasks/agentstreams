Create a checkpoint of the current session state. Save a summary of:
1. Files modified in this session (git diff --name-only)
2. Current context window usage estimate
3. Key decisions made so far
4. Remaining tasks from the todo list

Write the checkpoint to .claude/checkpoints/<timestamp>.md so it can be restored later.
