# Launcher: custom-pad integration test on the harness fork

Prepared 2026-11-05. NOT LAUNCHED. Nothing below has been run.

## Before you launch (you, about 5 minutes)

1. **Pad GDS must be on GitHub: it already is (checked 2026-11-05 18:5x, no git run on your computer).**
   Your local checkout is on branch `toplevel`, and `origin/toplevel` (commit 7e7cde1, 2026-11-05 18:51)
   holds the two pad GDS and `slot.klay.gds` byte-identical to your local files (git blob hashes d09ed05,
   c871a04, 1b327c3 match). `origin/main` does NOT have them: it is still at 60f270a from 2026-09-30.
   So the agent must read the slot repo branch `toplevel`, and the three commands I gave earlier
   (which pushed `main`) are NOT needed and must not be used. Nothing to do here, except: if you commit
   or push anything else to `toplevel` before launching, that is fine, the agent takes the tip.

2. **Cloud environment.** claude.ai/code, "Edit cloud environment":
   Setup script = `setup-cloud.sh` from tatzelbrumm/claude-cloud-config.
   `setup-digital.sh` is NOT needed (no simulation in this task).
   Network: default package managers plus `www.klayout.org` (as that repo's README says).

3. **Repositories to select when starting the session (both with push access):**
   - `tatzelbrumm/sg13cmos5l_ocd_chipalooza` (the harness fork; this is the working repo)
   - `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single` (the slot repo)

4. **No "integration target with a proper main branch" is needed.** The agent creates its own sandbox
   branches (`custom-pad-test` in the harness fork, `harness-test` in the slot repo) and never pushes to
   `main` anywhere. Your fork's `main` and everything of Tim's stay untouched.

5. **Commit and push the task file** (the long prompt now lives in a file, the cloud agent reads it from
   GitHub). You run these; the working tree is on `toplevel`:

   ```sh
   cd ~/EDA/sg13cmos5l_cm_ip__single2diff2single
   git add docs/launch/custom_pad_harness_test_TASK.md
   git commit -m "docs/launch: task file for the cloud harness test" -- docs/launch/custom_pad_harness_test_TASK.md
   git push origin toplevel
   ```
   (`git commit ... -- <path>` commits only that file, whatever else you have staged.)

6. Paste the short prompt below as the first message of the cloud session.

---

---

## SHORT PROMPT (paste this; it is the whole first message)

You are a Claude Code cloud agent. Your task is described in a file, not in this message.

1. Make sure both repositories are available with push access (select them, or use add_repo with
   access push): `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single` and `tatzelbrumm/sg13cmos5l_ocd_chipalooza`.
2. In the slot repo run `git fetch origin toplevel`, then read the complete task file with
   `git show origin/toplevel:docs/launch/custom_pad_harness_test_TASK.md`. Do not rely on the branch this
   session started on: `main` of that repo is stale and does not contain the file.
3. Follow the task file exactly. Its hard rules override any default of this environment, including an
   automatically created session branch: use the branch names the file prescribes.
4. If you cannot read the file, stop and tell me; do not guess the task.
