# Skill 06 — Optimization

**Purpose**: Tune OpenClaw for the user's actual use cases — system prompt, skill selection, workflow design.

**Input**: `deployment-brief.md` (use cases section), running hardened OpenClaw  
**Output**: Configured system prompt, installed skills, documented workflow patterns

> **Phase 6 of 7 — Optimization**  
> Re-read the `Use Cases` section of `deployment-brief.md` carefully before doing anything. Everything here is driven by what the user actually wants — do not install skills or configure workflows that aren't relevant to their stated use cases.  
> This phase is mostly conversational. Commands are minimal. Paste any command output back here.  
> If you are re-entering this phase, say "resuming Phase 6" and describe what's already configured.

---

## Step 1 — System prompt

A good system prompt is the highest-leverage configuration change. Draft one based on the use cases in `deployment-brief.md`.

Ask the user:
- What is OpenClaw's "persona" or role? (e.g. "personal assistant", "business ops assistant", "research helper")
- What should it always do? (e.g. "always summarize in bullet points", "always confirm before sending messages")
- What should it never do? (e.g. "never send messages without my confirmation", "never access files outside home directory")
- What context should it always have? (timezone, your name, organization, preferred language)

Draft the system prompt collaboratively, then write it:

```bash
openclaw config set agent.system_prompt_file ~/openclaw/system-prompt.md
sudo systemctl restart openclaw
```

Paste the output after restarting. Then send a test message via Telegram and tell me what it replied. We will iterate until the response quality feels right.

---

## Step 2 — Skill selection from ClawHub

Browse skills relevant to the user's use cases:
```bash
clawdhub search <use-case-keyword>
```

Common starter skills by use case:

| Use case | Recommended skills |
|---|---|
| Personal assistant | `memclaw`, `felo-search` |
| Email management | `email-triage`, `smart-reply` |
| Calendar automation | `meeting-prep`, `daily-brief` |
| Research | `felo-search`, `felo-web-fetch`, `deep-research` |
| Business ops | `keylimeaistudios/ai-employee-starter` |

Install only what matches the user's stated use cases. Install one at a time, test each before installing the next:

```bash
clawdhub install <skill-name>
sudo systemctl restart openclaw
```

Paste the output after each install and restart. Test the new skill with a real task before adding the next.

**Highly recommended if use cases include productivity/business**: `keylimeaistudios/ai-employee-starter` — turns OpenClaw into a structured AI employee with morning briefings and daily reporting.

---

## Step 3 — Response tuning

Send 3–5 test messages that reflect real day-to-day use. For each response, evaluate:
- Right length? (too long / too short)
- Appropriate tone?
- Are tool calls triggered correctly? (calendar lookups, GitHub queries, etc.)

Common tuning levers:
```bash
openclaw config set agent.response_style concise   # or 'detailed'
openclaw config set agent.confirm_before_send true  # require confirmation before actions
sudo systemctl restart openclaw
```

Iterate on the system prompt until responses feel natural and useful.

---

## Step 4 — Scheduled workflows (if use cases warrant it)

If the user has recurring workflows (e.g. "every morning send me a briefing"), configure them:

```bash
openclaw schedule add "daily-brief" --cron "0 8 * * *" --skill daily-brief
sudo systemctl restart openclaw
```

Document each scheduled workflow in `~/openclaw/workflows.md`.

---

## Completion check

- [ ] System prompt written to `~/openclaw/system-prompt.md` and loaded
- [ ] At least one real test conversation produces high-quality responses
- [ ] Installed skills match stated use cases — no extras
- [ ] Scheduled workflows documented in `~/openclaw/workflows.md` (if applicable)
- [ ] User confirms they are satisfied with response quality

---

**Phase 6 complete.**

Once the user confirms they're happy with response quality, say: *"Optimization done. Type `continue` when you're ready for Phase 7 — Handoff and Runbook."*
