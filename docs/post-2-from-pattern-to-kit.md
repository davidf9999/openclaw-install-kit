# From Failed Permission System to Open-Source Installation Kit

Four months of building a Google Drive permission system taught me the wrong way to solve a problem. But one pattern that emerged from it turned out to be worth keeping: a structured, phase-by-phase approach to installing and configuring software with an AI as your co-pilot.

That pattern is now an open-source project. It is called `openclaw-install-kit`.

---

### What it does

`openclaw-install-kit` is a guided installation kit for [OpenClaw](https://openclaw.ai) — a self-hosted personal AI assistant that connects to your messaging apps, calendar, GitHub, and local files, powered by a cloud LLM (Anthropic, OpenAI, etc.). No GPU, no local model.

The kit takes you from a bare Ubuntu or Debian machine to a running, hardened, documented assistant in eight phases:

- Hardware and OS selection
- Infrastructure preparation
- OpenClaw install and daemon setup
- Messaging and service integrations (Telegram, WhatsApp, GitHub, calendar, and more)
- Security hardening
- Persona and prompt tuning
- Handoff and runbook generation

At the end you have a running assistant, a written runbook, and a backup.

---

### What makes it a "journey kit" rather than a README

Most install guides are a list of commands. They assume a clean machine, a specific OS, and that nothing will go wrong.

This kit is different in three ways.

**First**, it starts with a discovery interview. Before running a single command, it asks what hardware you have, whether it is fanless, whether you have a domain, which messaging platforms you want, and which integrations matter. It writes those answers to a `deployment-brief.md` that every subsequent phase reads and adapts to. A fanless laptop gets thermal monitoring built in. A machine without a domain skips SSL entirely.

**Second**, every phase has an explicit completion check before the next phase begins. You cannot accidentally start integration setup before the daemon is verified running.

**Third**, it is designed to survive interruptions. Each phase can be re-entered after a session break or context loss. The `deployment-brief.md` on disk is the persistent state — not the conversation history.

---

### How it works in practice

If you are using Claude Code, the agent runs commands directly on your machine. If you are using any chat interface — Claude.ai, ChatGPT, Journey AI — you copy each command, run it in your terminal, paste the output back, and the agent verifies before moving on. The same kit works in both modes.

---

### Honest status

This kit has been tested end-to-end on exactly one machine: Ubuntu 24.04 on an ASUS ZenBook UX305FA (Intel Core M, fanless). Telegram and WhatsApp with a Cloudflare tunnel are verified working. Everything else — Debian, macOS, Raspberry Pi, VPS, Google Calendar, GitHub, other integrations — is documented but not yet validated by a real install.

That is why I am publishing it now rather than waiting.

---

### What I am looking for

If you run this kit — on any hardware, any OS, any set of integrations — I want to hear what happened.

Specifically:
- Which phase was the first to deviate from the skill file?
- What did you have to figure out that the kit missed?
- Did the re-entry behavior work when you picked it up after a break?

There are issue templates for both install failures and test reports. The `TESTING.md` has a log of the one real run so far, with a template for adding yours.

The repo is at [github.com/davidf9999/openclaw-install-kit](https://github.com/davidf9999/openclaw-install-kit).

If you have tried to set up a personal AI assistant and hit a wall somewhere in the process — that wall is exactly what this kit is trying to map.

---

*This is the follow-up to ["Why I Spent Four Months Reinventing Google's Wheel"](post-1-reinventing-googles-wheel.md).*
