# Skill 06 — Optimization

**Purpose**: Tune OpenClaw for the user's actual use cases — persona, system prompt, skill selection, workflow design.

**Input**: `deployment-brief.md` (use cases section), running hardened OpenClaw  
**Output**: Configured assistant persona, installed skills, documented workflow patterns

> **Phase 6 of 8 — Optimization**  
> Re-read the `Use Cases` section of `deployment-brief.md` carefully before doing anything. Everything here is driven by what the user actually wants — do not install skills or configure workflows that aren't relevant to their stated use cases.  
> This phase is mostly conversational and file editing. Paste any command output back here.  
> If you are re-entering this phase, say "resuming Phase 6" and describe what's already configured.

---

## How OpenClaw personality works

OpenClaw uses a **workspace file system** for persona and memory — not a single config flag. The relevant files live in `~/.openclaw/workspace/`:

| File | Purpose |
|---|---|
| `IDENTITY.md` | Assistant name, creature, vibe, emoji, behavior rules |
| `USER.md` | User's name, timezone, preferences, context |
| `SOUL.md` | Core values and behavioral guidelines (good defaults — edit carefully) |
| `BOOTSTRAP.md` | First-run onboarding script — **delete this after setup** |

Edit these files directly. Changes take effect after restarting the gateway and clearing the session.

---

## Step 1 — Set timezone and time format

```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw config set agents.defaults.userTimezone "Your/Timezone"
openclaw config set agents.defaults.timeFormat auto
```

Common timezone values: `Asia/Jerusalem`, `America/New_York`, `Europe/London`, `Asia/Tokyo`.

---

## Step 2 — Configure IDENTITY.md

Ask the user:
- What should the assistant be called?
- What's its vibe — concise/detailed, casual/formal, cautious/bold?
- What should it always do? (e.g. "always confirm before acting")
- What should it never do? (e.g. "never access files outside home directory")
- What languages should it respond in?

Then edit `~/.openclaw/workspace/IDENTITY.md` with the answers. Example structure:

```markdown
# IDENTITY.md

- **Name:** [name]
- **Creature:** AI assistant
- **Vibe:** [tone description]
- **Emoji:** [signature emoji]

## Behavior defaults
- [list key behavioral rules]

## Language
- [language preferences]
```

Filled-in example for a personal assistant (adapt to your own preferences):

```markdown
# IDENTITY.md

- **Name:** Pixel
- **Creature:** AI assistant
- **Vibe:** Casual but not sloppy. Friendly, direct, no filler. Accurate and concise by default.
- **Emoji:** 🤖

## Behavior defaults
- Always confirm before taking any action that changes state (sending messages, writing files,
  modifying calendar events, making API calls). State what you're about to do and wait for approval.
- Read-only queries (checking calendar, listing files, searching) do not need confirmation.
- Never access paths outside the home directory.
- Never send messages on the user's behalf without explicit confirmation.

## Language
- Respond in the same language the user writes in.
- Default: English.
```

---

## Step 3 — Configure USER.md

Edit `~/.openclaw/workspace/USER.md` with the user's details:

```markdown
# USER.md

- **Name:** [full name]
- **What to call them:** [first name or nickname]
- **Timezone:** [e.g. Asia/Jerusalem]
- **Languages:** [list]
- **GitHub:** [username if applicable]

## Access granted
[list integrations configured in skill 04]

## Context
[machine info, use case, preferences]
```

---

## Step 4 — Review SOUL.md

Read `~/.openclaw/workspace/SOUL.md` with the user. The defaults are good — only edit if the user wants to change core behavioral principles. If editing, tell the user what you changed.

---

## Step 5 — Delete BOOTSTRAP.md

The bootstrap file drives the "blank slate" first-run experience. Once identity is configured, delete it:

```bash
rm -f ~/.openclaw/workspace/BOOTSTRAP.md
```

---

## Step 6 — Apply changes

After editing workspace files, restart the gateway and clear the session so the new files are picked up:

```bash
systemctl --user restart openclaw-gateway
```

Then send a message via Telegram asking the assistant its name. If it still shows the old identity, the session may be cached — check the dashboard for a "new session" or "clear session" option, or remove session files:

```bash
rm ~/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null
systemctl --user restart openclaw-gateway
```

---

## Step 7 — Skill selection

Browse available skills:
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
clawdhub search <use-case-keyword>
```

If Google integrations are in scope, prefer service-specific workflows over generic all-in-one bundles. Keep Calendar/Contacts, Gmail, and Drive separate until each service is validated and the user has confirmed the intended account boundary.

Common starter skills by use case:

| Use case | Recommended skills |
|---|---|
| Personal assistant | `memclaw`, `felo-search` |
| Email management | `email-triage`, `smart-reply` |
| Calendar automation | `meeting-prep`, `daily-brief` |
| Research | `felo-search`, `felo-web-fetch`, `deep-research` |
| Business ops | `keylimeaistudios/ai-employee-starter` |

Install one at a time, test each before installing the next:

```bash
clawdhub install <skill-name>
systemctl --user restart openclaw-gateway
```

---

## Step 8 — Response tuning

Send 3–5 test messages via Telegram that reflect real day-to-day use. Evaluate each response:
- Right length and tone?
- Confirmation before actions?
- Tool calls triggered correctly?

Iterate on `IDENTITY.md` and `SOUL.md` until responses feel right.

---

## Step 9 — Scheduled workflows (if applicable)

```bash
openclaw schedule add "daily-brief" --cron "0 8 * * *" --skill daily-brief
systemctl --user restart openclaw-gateway
```

Document each workflow in `~/openclaw/workflows.md`.

---

## Completion check

- [ ] `IDENTITY.md` filled in — name, vibe, behavior rules
- [ ] `USER.md` filled in — name, timezone, languages, context
- [ ] `BOOTSTRAP.md` deleted
- [ ] Timezone set via `openclaw config set agents.defaults.userTimezone`
- [ ] At least one real test conversation produces high-quality responses
- [ ] Installed skills match stated use cases — no extras
- [ ] Scheduled workflows documented (if applicable)
- [ ] User confirms they are satisfied with response quality

---

**Phase 6 complete.**

Once the user confirms they're happy with response quality, say: *"Optimization done. Type `continue` when you're ready for Phase 7 — Handoff and Runbook."*
