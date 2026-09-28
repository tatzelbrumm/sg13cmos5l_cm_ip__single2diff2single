# Recovering Verbatim Chat Content After Context Compaction

What actually worked, live, on 2026-09-28: this assistant's own session (`a1f2b024-...`)
got its context compacted mid-conversation, and the user asked for the discarded turns
back, verbatim, for the chatlog. Here's what didn't work, what did, and why.

## The problem

Context compaction replaces this assistant's in-context view of the conversation with a
prose summary, and — at least in this environment — it also rewrites the *local* session
transcript file on disk
(`/root/.claude/projects/<project>/<session-id>.jsonl` in the cloud container). After
compaction, that file no longer contains the original pre-compaction turns in their raw
form; it jumps straight from wherever the summary was inserted onward. This was confirmed
by inspecting the file directly (`wc -l`, dumping every record's `type`/`role`/text
preview) — the raw entries for the compacted stretch simply aren't there.

## Dead ends checked (worth ruling out fast, not worth lingering on)

- **No other transcript file anywhere on the container.** `find / -iname "*.jsonl"` and a
  search for the session-id string turned up nothing else — no rotated backup, no second
  copy.
- **MCP debug logs are not conversation logs.** `~/.cache/claude-cli-nodejs/.../mcp-logs-*/*.jsonl`
  exist, but they're transport handshake noise (connection setup, headers) — no message
  content at all.
- **A browser, if one happens to be open, is a legitimate fallback** (the built-in browser
  pane or Claude in Chrome, pointed at the chat's own claude.ai URL) — but don't assume
  one is available. Check first (`tabs_context` / `tabs_context_mcp`): if the pane isn't
  open (`browserOpen: false`) or the Chrome extension isn't connected, this path is a
  dead end for that moment, and it's slower and clunkier than the real fix below even
  when it does work — screenshots/DOM reads instead of structured turn text.

## The actual fix: `read_conversation`

If this is a claude.ai-backed conversation (this project's sessions are), the
`mcp__claude_ai__read_conversation` tool reads the chat's **own stored turn history
straight from claude.ai's servers** — completely independent of this assistant's local
context window or its local session JSONL. Compacting *this assistant's* context does
not touch that server-side copy at all. This is the one source that's *guaranteed* to
still have the content, when a local JSONL or an open browser tab might not.

```
read_conversation(conversation_id="current", max_turns=N, page_token="tK")
```

- `conversation_id="current"` works from inside the same chat; otherwise pass the
  chat's claude.ai URL/UUID.
- Turns are 0-indexed, alternating Human/Assistant — but a mid-turn interjection or a
  `[Request interrupted by user]` moment can insert extra turns (an empty Assistant turn,
  a follow-up Human turn), so don't assume a fixed stride of 2.
- Tool calls render as `<tool name="...">...<parameter name="...">...</parameter></tool>`
  blocks with their real, verbatim input parameters — enough to write accurate
  elided-action summaries — but **not** their results/output. If you need a tool's
  *output* (not just what was asked of it), it has to already be quoted in the
  surrounding reply text, or it's gone the same way the raw JSONL is.
- User and assistant text comes through HTML-entity-escaped (`&lt;`, `&gt;`, `&amp;`) —
  un-escape before pasting into the chatlog.

## Paging mechanics that actually matter

- Start with a modest `max_turns` (5–10). A single turn can be enormous if it contains a
  large tool input (a `Write` call embedding hundreds of lines, a long `device_bash`
  heredoc) — one such turn alone can blow past the tool's own output cap.
- When that happens, the tool doesn't fail outright — it writes the full result to a
  local file under
  `/root/.claude/projects/<project>/<session-id>/tool-results/mcp-claude_ai-read_conversation-*.txt`
  and tells you to read it in chunks. For anything under ~2000 lines, a single `Read`
  call on that path is easier than re-fetching with a smaller `max_turns`.
- Follow `next_page_token`/`prev_page_token` (`tK`/`bK`) rather than guessing turn
  numbers — the token already encodes where the next page starts.
- Grep the saved tool-result files for a known phrase (e.g. the first few words of the
  message you're trying to relocate) instead of reading every page in full when you
  already roughly know what you're looking for.

## The takeaway

Don't spend time hunting for a raw JSONL backup or trying to get a browser tab open
first. If the task is "recover the verbatim content of *this* chat after compaction,"
`read_conversation` is the fast, reliable, first move — go there directly.

## Known limitation

This only helps for a claude.ai-backed conversation. It won't recover anything from a
session that isn't stored that way (e.g. pure API/CLI usage without this tool wired up),
and it obviously can't recover content from before compaction if that content was never
actually sent as a real turn in the first place (a tool's raw *output*, as opposed to
what was asked of it or what ended up quoted back in a reply).
