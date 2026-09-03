# Codex cheat sheet

## Start and resume

```bash
cd <repository> && codex                         # interactive session
codex "Explain this repository"                 # start with prompt
codex --search                                   # enable live web search
codex --image screenshot.png "Diagnose this"    # attach image
codex resume                                     # choose saved local session
codex resume --last                              # resume latest here
codex resume --all                               # search all local sessions
codex login                                      # authenticate
codex login status                               # check authentication
codex logout                                     # remove credentials
codex doctor                                     # diagnostic report
```

## Stop or suspend

Wait for the current task to finish, then exit; the session remains resumable:

```text
/exit                                            exit cleanly
/quit                                            same as /exit
```

Temporarily suspend the still-running CLI process:

```text
Ctrl+Z                                           suspend to the shell
fg                                               return to Codex
```

```bash
codex resume --last                              resume the saved session
```

## Permissions

```bash
codex --sandbox read-only --ask-for-approval on-request
codex --sandbox workspace-write --ask-for-approval on-request
codex --sandbox workspace-write --ask-for-approval untrusted
codex --sandbox read-only --ask-for-approval never
codex --dangerously-bypass-approvals-and-sandbox # DANGEROUS: unrestricted
```

```text
/status          show model, permissions, writable roots, context
/permissions     inspect/change permissions
/model           choose model and reasoning effort
/review          review local changes
/mcp             inspect MCP connections/tools
/skills          inspect/invoke skills
/init            create repository guidance
```

Type `/` to list commands supported by the installed version.

## Non-interactive and CI

```bash
codex exec "Run the tests and summarize failures"
codex exec --sandbox workspace-write "Fix the failing tests"
codex exec --json "Analyze this repository" > codex-events.jsonl
codex exec resume --last "Continue and run tests"
codex review --uncommitted
codex review --base main
codex review --commit <sha>
```

## CLI commands

```bash
codex --help
codex <command> --help
codex completion bash
codex completion zsh
codex features list
codex debug models
codex cloud
codex cloud list --json
codex apply <task-id>
codex archive <session>
codex unarchive <session>
codex delete <session>                           # permanently deletes transcript
```

## Configuration locations

```text
~/.codex/config.toml           personal defaults
<repo>/.codex/config.toml      trusted-project overrides
<repo>/AGENTS.md               durable project instructions
<repo>/.agents/skills/         repository skills
~/.agents/skills/              personal skills
```

Minimal `~/.codex/config.toml`:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
```

```bash
codex -c 'approval_policy="on-request"' -c 'sandbox_mode="read-only"'
codex --profile <name>
```

```text
CLI/-c > project config > profile > user config > system config > defaults
```

## `AGENTS.md`

```bash
cd <repository> && codex
```

```text
/init
```

```md
# AGENTS.md

## Build and test
- Install: `npm ci`
- Test: `npm test`
- Lint: `npm run lint`

## Conventions
- Preserve unrelated user changes.
- Add focused tests for behavior changes.
- Do not modify generated files manually.
```

Put more-specific `AGENTS.md` files in subdirectories.

## MCP

MCP (Model Context Protocol) connects Codex to external tools and context through MCP servers.

```bash
codex mcp list
codex mcp get <name>
codex mcp add <name> -- <command> [args...]
codex mcp add <name> --url <https-url>
codex mcp login <name>
codex mcp logout <name>
codex mcp remove <name>
```

## npm

npm is the Node.js package manager: it installs JavaScript/TypeScript dependencies and runs project scripts from `package.json`.

```bash
npm ci                                           install the locked dependencies
npm install <package>                            add a dependency
npm run                                          list project scripts
npm test                                         run the test script
```

## Skills

```text
/skills                     list/select skills
$skill-name                 invoke skill
$skill-creator              create skill
$skill-installer <name>     install curated skill
```

```text
.agents/skills/my-skill/
└── SKILL.md
```

```md
---
name: my-skill
description: State exactly when this skill should and should not run.
---

Imperative workflow instructions.
```

## Prompt templates

```text
Explain this repository: architecture, entry points, build/test commands, and risks. Do not edit files.
```

```text
Diagnose <problem>. Reproduce it, identify the root cause, and report evidence. Do not implement a fix.
```

```text
Implement <change>. Preserve unrelated edits, add focused tests, run relevant checks, and summarize changed files.
```

```text
Review the current diff for correctness, regressions, security issues, and missing tests. Report findings first; do not edit.
```

```text
Create a plan for <goal>. Call out assumptions, risks, and decisions requiring my input. Do not edit files yet.
```

## Access boundaries

Sandbox: a local OS-enforced boundary around commands. It exposes permitted host paths; it is not a separate disk or container and has no fixed location or size.

```text
Current chat                  yes
Files allowed by sandbox      yes
Former ChatGPT chats          no, unless supplied in current context
Private services              only through authorized connector/MCP
Internet                      according to web/network permissions
```

## Official references

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Configuration basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [Skills](https://learn.chatgpt.com/docs/build-skills)
