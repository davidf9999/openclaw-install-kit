# Design Notes — Kit UX for Journey AI Publication

## Runtime reality (confirmed via research)

Journey AI is a **prompt-orchestrated conversational agent**, not a tool-executing agent like Claude Code.

| Capability | Reality |
|---|---|
| Phase sequencing | Conversational, LLM-driven — not deterministic |
| Phase UI | None — must be simulated in text |
| Command execution | Clipboard/paste only — no direct shell access |
| State management | Prompt-based, fragile — must be reinforced explicitly |
| User role | Active operator (not passive observer) |

**Mental model**: design as a highly structured, intelligent installation guide that talks back — not an autonomous DevOps agent.

This is a significant design constraint. The current kit is written with Claude Code in mind (tool-executing agent). It needs to work as a guided co-pilot on Journey AI.

---

## What this means for the kit (structural implications)

### 1. Every bash block must become a paste-and-verify loop

Current pattern (Claude Code, wrong for Journey AI):
```
[agent runs command, reads output, continues]
```

Required pattern (Journey AI):
```
Run this command and paste the output here:
    sudo apt update
[user pastes output]
[agent reads output and proceeds]
```

Every skill file needs this treatment for every command block.

### 2. Phase transitions must be explicit gates

The agent cannot reliably enforce phase boundaries on its own. Each phase must end with:
- A clear completion checklist (paste the output of X, confirm Y)
- An explicit handoff: "Phase 2 complete. Type 'continue' when you're ready for Phase 3."

### 3. Each skill must be semi-idempotent

Users may refresh, lose context, or re-enter a phase. Each skill should:
- Restate what phase it is and what the goal is
- Re-read `deployment-brief.md` before acting
- Not assume prior conversation context is intact

### 4. State must be simulated in text

The platform has no FSM runtime. But the kit's contract-first, explicit-transition design is actually a good fit — it just needs to be enforced inside the prompt itself, not assumed from the platform.

---

## Gap 1 — No orientation before Phase 1

The current kit drops the user directly into the discovery interview. A new user has no idea:
- What OpenClaw is or what they'll end up with
- How long the install takes
- What they need to have ready
- That they will be running commands manually throughout

**Recommendation**: Add a `skills/00-orientation.md` that the agent delivers before asking any questions:

> "This kit installs OpenClaw on your Ubuntu machine and connects it to your messaging platforms. It has 7 phases and takes 30–60 minutes of active work. You will run all terminal commands yourself — I'll give you each block, explain what it does, and read back the output you paste. Before we start, have ready: terminal access to your Ubuntu machine, and an Anthropic API key."

---

## Gap 2 — The sudo / terminal handoff is undocumented

The kit never tells the user they are the ones running commands. This is structural — Journey AI has no shell access. It must be set as an expectation upfront (orientation) and reinforced at the top of each infra skill.

---

## Gap 3 — WhatsApp complexity not flagged in discovery

Skill 01 lists WhatsApp alongside Telegram with no complexity warning. WhatsApp requires either Meta Business API approval (1–3 days) or a persistent browser bridge (`whatsapp-web.js`).

**Recommendation**: Add callout in skill 01 next to WhatsApp:

> "Requires Meta Business API approval (1–3 days) or a third-party bridge. Start with Telegram if you want something working today."

---

## Gap 4 — Completion checks reference future phases

Each skill's completion check should only verify what that skill itself set up. Audit needed across all 7 skills.

---

## What works well — keep these

- `deployment-brief.md` as a shared artifact between phases. Each skill reads it and adapts. This is exactly the right pattern for a stateless conversational runtime.
- Explicit input/output contracts per skill.
- Hardware-specific flags (fanless, domain, use mode) that propagate cleanly through phases.
- Safety notes that are specific and actionable.
- The contract-first, explicit-transition design is a natural fit for prompt-space FSM emulation.
