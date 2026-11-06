# Export the visible conversation from a Claude Code session transcript (.jsonl):
# user text, assistant text, one bracketed line per tool call. No thinking, no system text,
# no reminders, no tool output.
import json, re, sys
src, = sys.argv[1:]
out = []
def strip_sys(s):
    s = re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.S)
    return s.strip()
for line in open(src):
    try: e = json.loads(line)
    except Exception: continue
    if e.get("type") not in ("user", "assistant") or e.get("isMeta") or e.get("isSidechain"): continue
    m = e.get("message", {}); c = m.get("content")
    ts = e.get("timestamp", "")
    if e["type"] == "user":
        texts = [c] if isinstance(c, str) else [b.get("text","") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text"]
        t = "\n".join(strip_sys(x) for x in texts).strip()
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
