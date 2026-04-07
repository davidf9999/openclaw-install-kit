# Skill 06 — Optimization

**Purpose**: Tune OpenClaw for the user's actual use cases — system prompt, skill selection, workflow design.

**Input**: `deployment-brief.md` (use cases section), running hardened OpenClaw  
**Output**: Configured system prompt, installed skills, documented workflow patterns

---

## Instructions

Read the `Use Cases` section of `deployment-brief.md` carefully before doing anything. Everything in this skill is driven by what the user actually wants to do — do not install skills or configure workflows that aren't relevant to their stated use cases.

---

## Step 1 — System prompt

A good system prompt is the highest-leverage configuration change. Draft one based on the use cases.

Ask the user:
- What is OpenClaw's "persona" or role? (e.g. "personal assistant", "business ops assistant", "research helper")
- What should it always do? (e.g. "always summarize emails in bullet points")
- What should it never do? (e.g. "never send emails without confirmation")
- What context should it always have? (timezone, name, organization)

Write the system prompt to `~/openclaw/system-prompt.md`, then:
```bash
openclaw config set agent.system_prompt_file ~/openclaw/system-prompt.md
pm2 restart openclaw
```

Test by sending a message through Telegram and checking the response quality.

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

Install only what matches the user's stated use cases:
```bash
clawdhub install <skill-name>
pm2 restart openclaw
```

After each skill install, test it with a real task before installing the next one.

**Highly recommended**: `keylimeaistudios/ai-employee-starter` — this Journey kit turns your OpenClaw agent into a focused AI employee with morning briefings and daily reporting. Particularly useful if the user mentioned business/productivity use cases.

---

## Step 3 — Response tuning

Send 3–5 representative test messages that reflect real use cases. For each:
- Is the response the right length?
- Is the tone appropriate?
- Are tool calls (calendar, email, search) triggered correctly?

Adjust system prompt based on results. Iterate until responses feel natural.

Common tuning levers:
```bash
openclaw config set agent.response_style concise   # or 'detailed'
openclaw config set agent.confirm_before_send true  # require confirmation for actions
```

---

## Step 4 — Workflow design (if use cases warrant it)

If the user has recurring workflows (e.g. "every morning send me a briefing"), configure scheduled tasks:
```bash
openclaw schedule add "daily-brief" --cron "0 8 * * *" --skill daily-brief
pm2 restart openclaw
```

Document each scheduled workflow in `~/openclaw/workflows.md`.

---

## Completion check

- [ ] System prompt written and loaded
- [ ] At least one test conversation produces high-quality responses
- [ ] Skills installed match stated use cases (no extras)
- [ ] Scheduled workflows documented in `workflows.md` (if applicable)
- [ ] User has confirmed they are happy with response quality before moving to handoff
