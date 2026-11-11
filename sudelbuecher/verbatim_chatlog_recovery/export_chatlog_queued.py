# Export the visible conversation from a Claude Code session transcript (.jsonl): user text (also mid-turn messages that the
# transcript keeps as `queued_command` attachments), assistant visible text, one bracketed line per tool call.
# No thinking, no system text, no reminders, no tool output.
# Based on docs/slot7_testplatform/tools/export_chatlog.py (branch claude/c5-slot7-testplatform); added 2026-11-11: queued_command
# attachments as user messages (marked), image blocks as "[image attached]", skips records off the live path (isSidechain).
import json, re, sys
src, = sys.argv[1:]
out = []
def strip_sys(s):
    s = re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.S)
    s = re.sub(r"<task-notification>.*?</task-notification>", "", s, flags=re.S)
    s = re.sub(r"\[SYSTEM NOTIFICATION - NOT USER INPUT\].*", "", s, flags=re.S)
    if s.strip() == "Tool loaded.":
        return ""
    return s.strip()
for line in open(src):
    try: e = json.loads(line)
    except Exception: continue
    ty = e.get("type"); ts = e.get("timestamp", "")
    if ty == "attachment" and (e.get("attachment") or {}).get("type") == "queued_command":
        p = e["attachment"].get("prompt")
        p = p if isinstance(p, str) else " ".join(b.get("text", "") for b in (p or []) if isinstance(b, dict))
        p = strip_sys(p)
        if p: out.append(f"**User (message sent while the assistant was working):** ({e['attachment'].get('timestamp', ts)})\n\n{p}\n")
        continue
    if ty not in ("user", "assistant") or e.get("isMeta") or e.get("isSidechain"): continue
    m = e.get("message", {}); c = m.get("content")
    if ty == "user":
        if isinstance(c, str): texts = [c]
        else: texts = [b.get("text", "") if b.get("type") == "text" else "[image attached]" for b in (c or []) if isinstance(b, dict) and b.get("type") in ("text", "image")]
        t = "\n".join(strip_sys(x) if x != "[image attached]" else x for x in texts).strip()
        if t: out.append(f"**User:** ({ts})\n\n{t}\n")
    else:
        for b in c or []:
            if b.get("type") == "text" and b["text"].strip():
                out.append(f"**Assistant:** ({ts})\n\n{b['text'].strip()}\n")
            elif b.get("type") == "tool_use":
                i = b.get("input", {})
                d = i.get("description") or i.get("file_path") or i.get("query") or ""
                out.append(f"*[tool call: {b['name']}{' — ' + d if d else ''}]*\n")
print("\n".join(out))
