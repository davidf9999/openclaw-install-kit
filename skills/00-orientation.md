# Skill 00 — Orientation

**Purpose**: Orient the user before Phase 1 begins. Deliver this briefing once, at the very start of the kit.

**Input**: None  
**Output**: User understands what they're installing, how long it takes, what they need, and how this collaboration works

---

## Deliver this briefing

Say the following to the user (adapt naturally to the conversation — don't read it verbatim):

---

Welcome. This kit will install **OpenClaw** on your Ubuntu machine and set it up as a personal AI assistant connected to your chosen messaging platforms and services.

**What you'll end up with:**
- OpenClaw running as a background service on your machine
- Connected to at least one messaging app (e.g. Telegram) — so you can talk to it like a chat
- Integrated with whatever services you choose: calendar, GitHub, WhatsApp, local files, etc.
- A written runbook for restarts, updates, and backups

**How long it takes:**
- 7 phases, roughly 30–60 minutes of active work
- Most of that is you running commands and me guiding and verifying

**How we work together:**
- I will give you command blocks to run in your terminal
- You run them and paste the output back here
- I read the output, confirm everything looks right, and give you the next step
- I cannot run commands on your machine directly — you are always in control

**Before we start, make sure you have:**
- [ ] A terminal open on the Ubuntu machine (local or SSH)
- [ ] An Anthropic API key — get one at https://console.anthropic.com if needed
- [ ] A rough idea of which apps you want to connect (we'll make this concrete in Phase 1)

---

Once the user confirms they're ready, proceed to **Phase 1 — Discovery** (`skills/01-discovery.md`).
