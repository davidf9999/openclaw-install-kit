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

## ~~Gap 1~~ RESOLVED — Orientation before Phase 1

`skills/00-orientation.md` (Phase 0b) now exists. It briefs the user on what OpenClaw is, how long the install takes, what they need, and that they are running all commands manually. Delivered before Phase 1.

---

## ~~Gap 2~~ RESOLVED — Terminal handoff documented

The orientation skill explicitly tells the user they run all commands and paste output back. The infra skills reinforce this with "You will run all commands yourself" in each phase header.

---

## ~~Gap 3~~ RESOLVED — WhatsApp two-path question in discovery

Skill 01 now asks which WhatsApp path: personal number (whatsapp-web.js bridge) or separate/business number (Meta Business API). Skill 04 routes to Path A or Path B accordingly, with complexity warnings on each.

---

## Gap 4 — Completion checks reference future phases

Each skill's completion check should only verify what that skill itself set up. Audit needed across all 7 skills.

---

## Dual-runtime design (intentional)

This kit is designed to work in two distinct execution modes simultaneously. This is a deliberate design choice, not an accident.

**Mode 1 — Claude Code (tool-executing)**  
The agent has `bash`, `read`, `write`, and `edit` tools. It runs commands directly, reads output, and decides what to do next without user involvement in terminal steps. This is the fastest path and was used during the kit's own development and testing.

**Mode 2 — Journey AI / plain chat (clipboard model)**  
The agent has no tool access. It can only produce text. Every command block is followed by an explicit "run this and paste the output here" instruction. The user runs the command, pastes the output into the chat, and the agent reads and verifies before continuing. This is the designed pattern for Journey AI and any plain chat interface (Claude.ai, ChatGPT, etc.).

**How the skill files support both modes simultaneously**:
- Command blocks are formatted as copy-pasteable bash (works in both modes)
- Every block is followed by "paste the output" — essential in clipboard mode, harmless in tool-executing mode (the agent already has the output)
- The "you will run all commands yourself" framing at the top of each infra skill is for clipboard-mode users; tool-executing agents ignore it
- Verification steps ("paste the output of `node --version`") serve as explicit confirmation in clipboard mode and as a structured check in tool-executing mode

**Why this matters for publishing**: A kit that only works in Claude Code limits the audience to users with that specific tool. Supporting the clipboard model means any user with any chat interface can follow the kit — with the same instructions, the same command blocks, and the same verification steps.

---

## Journey kit vs the Claude skill-creator

The individual skill files (`skills/NN-name.md`) are exactly the kind of content the Claude skill-creator produces: self-contained instructions for a specific task, formatted for an AI agent to follow. The skill-creator is the right tool for generating the content inside each file.

What the skill-creator does not produce — and what the kit adds:

| What the kit adds | Why it matters |
|---|---|
| **Phase sequencing with explicit gates** | Phases cannot be skipped; each completion check must pass before the next begins |
| **Shared artifact chain** | `deployment-brief.md` is produced once and consumed by all subsequent phases; each phase adapts its behavior based on flags in the brief |
| **Recovery / re-entry logic** | Each skill can be re-entered after a session break or context loss; the file on disk is the persistent state, not the conversation |
| **Input/output contracts** | Each skill declares what it requires and what it produces; this makes the kit auditable and testable |
| **Known failure patterns** | `kit.md` lists failure modes with resolutions; skill files include inline recovery paths |
| **Dual-runtime declaration** | `kit.md` declares platform compatibility explicitly; skill files are written to support both modes |

**The relationship in one sentence**: the skill-creator produces the ingredients (individual skills); the kit adds the orchestration (sequencing, artifact chain, recovery, contracts).

**A journey kit can be seen as a way to compose skill-creator output into a pipeline** — adding the dimensions that a single skill file cannot provide on its own.

---

## What works well — keep these

- `deployment-brief.md` as a shared artifact between phases. Each skill reads it and adapts. This is exactly the right pattern for a stateless conversational runtime.
- Explicit input/output contracts per skill.
- Hardware-specific flags (fanless, domain, use mode) that propagate cleanly through phases.
- Safety notes that are specific and actionable.
- The contract-first, explicit-transition design is a natural fit for prompt-space FSM emulation.
