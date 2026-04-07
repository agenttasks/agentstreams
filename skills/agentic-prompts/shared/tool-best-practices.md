# Tool Best Practices

Extracted from prompt 13 (Tool Prompts). Canonical guidance for tool usage
in multi-agent systems.

## Tool Selection Priority

Always prefer dedicated tools over Bash equivalents:

| Need | Use | Not |
|------|-----|-----|
| Read files | `Read` | `cat`, `head`, `tail` |
| Edit files | `Edit` | `sed`, `awk` |
| Create files | `Write` | `echo >`, `cat <<EOF` |
| Search files | `Glob` | `find`, `ls` |
| Search content | `Grep` | `grep`, `rg` |
| Communicate | Text output | `echo`, `printf` |

Reserve Bash exclusively for system commands that require shell execution.

## Bash Best Practices

- Quote file paths with spaces: `"path with spaces/file.txt"`
- Use absolute paths to maintain cwd consistency
- Chain dependent commands with `&&`
- Parallelize independent commands as separate tool calls
- Never use newlines to separate commands (use `&&` or `;`)
- Timeout: up to 600000ms (10 minutes), default 120000ms

## Git Operations

- Prefer new commits over amending existing ones
- Before destructive operations, consider safer alternatives
- Never skip hooks (`--no-verify`) unless explicitly asked
- Never force push to main/master
- Stage specific files by name, not `git add -A`
- Use HEREDOC for commit messages with special characters

## Edit Tool

- Must `Read` a file before editing it
- `old_string` must be unique in the file (or use `replace_all`)
- Preserve exact indentation from Read output
- Prefer editing over creating new files

## Agent Tool

- Include 3-5 word description of what the agent will do
- Launch independent agents concurrently in a single message
- Use `run_in_background` when result isn't needed immediately
- Use `SendMessage` to continue a previous agent (preserves context)
- Tell agents whether to write code or just research
- Use `isolation: "worktree"` for isolated repo copies

## Parallel Tool Calls

- Independent calls: make all in the same message
- Dependent calls: wait for previous results
- Never use placeholder values for dependent parameters

## File Operations

- Verify parent directory exists before creating files
- Read files before proposing changes
- Prefer editing existing files over creating new ones
- Don't create documentation files unless explicitly requested
