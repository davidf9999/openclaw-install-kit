# Skill 00 — Orientation

**Purpose**: Orient the user before Phase 1 begins. Deliver this briefing once, at the very start of the kit.

**Input**: None  
**Output**: User understands what they're installing, how long it takes, what they need, and how this collaboration works

> **Phase 0b of 8 — Orientation**  
> Deliver this briefing once, before Phase 1 begins. If you are re-entering, skip it and go straight to Phase 1.

---

## Deliver this briefing

Say the following to the user (adapt naturally to the conversation — don't read it verbatim):

---

Welcome. This kit will install **OpenClaw** on your Linux or macOS machine and set it up as a personal AI assistant connected to your chosen messaging platforms and services.

**What you'll end up with:**
- OpenClaw running as a background service on your machine
- Connected to at least one messaging app (e.g. Telegram) — so you can talk to it like a chat
- Integrated with whatever services you choose: calendar, GitHub, WhatsApp, local files, etc.
- A written runbook for restarts, updates, and backups

**Important — this kit uses cloud LLM APIs only:**  
OpenClaw will call a cloud provider (Anthropic, OpenAI, etc.) for every response. You will need an API key and will pay per-token usage fees. **Local models (Ollama, Llama, Mistral, etc.) are not covered by this kit.** If that's what you want, stop here and see the OpenClaw local LLM documentation instead.

**Cost**: API calls are billed per token by your provider. Light personal use (tens of messages per day) typically costs a few dollars per month. Heavy use or long conversations cost more. Set a spend limit on your API account before starting — most providers offer this in the billing settings.

**Privacy**: Every message you send to OpenClaw — and every message sent to it by your contacts (WhatsApp, Telegram, etc.) — is sent to your chosen cloud LLM provider for processing. Your contacts' messages are included. If you choose Anthropic (Claude), messages are processed under Anthropic's privacy policy. Consider this before connecting platforms where others message you.

**How long it takes:**
- 8 phases, roughly 30–60 minutes of active work
- Most of that is you running commands and me guiding and verifying

**Recommended first run:**
- If you want the smoothest path, start with **Ubuntu 24.04 + Telegram only**
- Add extra integrations only after the core install is working
- WhatsApp Path A is the best-tested extension after Telegram

**How we work together:**
- I will give you command blocks to run in your terminal
- You run them and paste the output back here
- I read the output, confirm everything looks right, and give you the next step
- If you are using **Claude Code**: I can run commands directly on your machine — you will see each one and can approve or deny it
- If you are using **Journey AI or a plain chat interface**: you run all commands yourself and paste the output back — I have no direct access to your terminal

**Before we start, make sure you have:**
- [ ] A terminal open on the Ubuntu machine (local or SSH)
- [ ] An Anthropic API key — get one at https://console.anthropic.com if needed
- [ ] A rough idea of which apps you want to connect (we'll make this concrete in Phase 1)

---

**Expert fast path**: If the user already has a `deployment-brief.md` from a previous install, or knows their setup well enough to fill in the template themselves, they can skip Phase 1 entirely. Ask them to confirm the file is complete, then go directly to Phase 2.

Once the user confirms they're ready, proceed to **Phase 1 — Discovery** (`skills/01-discovery.md`).
