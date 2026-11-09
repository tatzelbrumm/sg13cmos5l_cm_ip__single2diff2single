# Export the visible conversation from a Claude Code session transcript (.jsonl):
# user messages (typed, and those sent while the assistant was working = queued_command attachments of human origin),
# assistant text, one bracketed line per tool call. Not included: reasoning, system text (hook feedback, task
# notifications, reminders), tool output, messages from other sessions.
import json, re, sys
src, = sys.argv[1:]
out, seen = [], set()
def strip_sys(s):
    return re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.S).strip()
def add_user(t, ts, note=''):
    key = t.strip()
    if not key or key.startswith(('<task-notification>', 'Stop hook feedback', '[SYSTEM NOTIFICATION')): return
    if key in seen: return          # a queued message can also appear as a normal user entry
    seen.add(key)
    out.append(f"**User:** ({ts}{note})\n\n{key}\n")
for line in open(src):
    try: e = json.loads(line)
    except Exception: continue
    if e.get('isSidechain'): continue
    ts = e.get('timestamp', '')
    if e.get('type') == 'attachment':
        a = e.get('attachment') or {}
        if a.get('type') == 'queued_command' and (a.get('origin') or {}).get('kind') == 'human':
            add_user(a.get('prompt', ''), a.get('timestamp', ts), ', sent while the assistant was working')
        continue
    if e.get('type') not in ('user', 'assistant') or e.get('isMeta'): continue
    c = e.get('message', {}).get('content')
    if e['type'] == 'user':
        texts = [c] if isinstance(c, str) else [b.get('text', '') for b in (c or []) if isinstance(b, dict) and b.get('type') == 'text']
        add_user("\n".join(strip_sys(x) for x in texts), ts)
    else:
        for b in c or []:
            if b.get('type') == 'text' and b['text'].strip():
                out.append(f"**Assistant:** ({ts})\n\n{b['text'].strip()}\n")
            elif b.get('type') == 'tool_use':
                i = b.get('input', {})
                d = i.get('description') or i.get('file_path') or i.get('query') or i.get('session_id') or i.get('task_id') or ''
                out.append(f"*[tool call: {b['name']}{' — ' + d if d else ''}]*\n")
print("\n".join(out))
