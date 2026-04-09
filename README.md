# openclaw-install-kit

A skill chain for installing, integrating, hardening, and handing off a self-hosted [OpenClaw](https://openclaw.ai) instance on Ubuntu — packaged as a [Journey kit](https://www.journeykits.ai) and written for **cloud LLM APIs (Anthropic, OpenAI, etc.)**.

## Who This Is For

This is for people who want to run OpenClaw on their own machine or VPS and are willing to follow a guided terminal workflow. You do not need to be a developer, but you should be comfortable copying commands into a terminal, reading output, and making a few account/setup decisions along the way.

Good fits include:
- hobbyists and tinkerers installing OpenClaw for the first time
- self-hosting users who want a structured, safer path than a one-line install script
- developers who want a reproducible install and handoff flow
- people who want Telegram first, then add other integrations later

## Prerequisites

- A machine running Ubuntu 24.04 is the best-supported path today
- Terminal access on that machine, or SSH access to a VPS
- Node 24 or the ability to install it during setup
- An Anthropic, OpenAI, or other supported cloud LLM API key
- Telegram if you want the simplest first integration
- Optional: a domain name, if you plan to expose webhooks or use integrations that require public HTTPS

If you are not sure whether your setup fits, start with the discovery phase. It will help you decide what machine to use and which integrations to include.

> **No GPU. No local model. No Ollama.**  
> This kit connects OpenClaw to a cloud LLM provider. If you want to run a local model (Llama, Mistral, Ollama, etc.) instead of a cloud API, this kit is not what you need — see the [OpenClaw local LLM docs](https://docs.openclaw.ai) for that path.

> **Cost**: API calls are billed per token by your provider. Light personal use typically costs a few dollars per month. Set a spend limit on your API account before starting.

> **Privacy**: Every message processed by OpenClaw — including messages sent by your contacts via Telegram, WhatsApp, etc. — is sent to your cloud LLM provider. Your contacts' messages are included. Review your provider's privacy policy before connecting platforms where others message you.

> **WhatsApp Path A (personal number)**: Using whatsapp-web.js violates WhatsApp's Terms of Service. Meta has banned accounts for this. Risk is lower for personal single-user use, but it is real. Only use this path if you accept that risk.

Eight guided phases (including orientation). The agent guides you step by step — you run commands in your terminal, paste the output back, and the agent verifies before moving on. Produces a written runbook at the end.

> **Beta status**
> This kit is usable today, but it is still a beta release rather than a broadly validated polished public release.
> The tested path is narrow and explicitly documented below.

**Current best-fit use case**
- You are thinking in terms of skills or a skill chain, not just a single install script
- You want a structured OpenClaw install on Ubuntu 24.04
- You are using Claude Code or another guided terminal workflow
- You want Telegram first, with WhatsApp Path A as the next best-tested extension
- You care about durability, security hardening, and a real runbook at the end

---

## Why this kit?

Most existing OpenClaw setup tools are cloud-only (VPS provisioning scripts). This kit is different:

| | This kit | [clawhost](https://github.com/bfzli/clawhost) | [openclaw-lab-on-cloud](https://github.com/carlosacchi/openclaw-lab-on-cloud) |
|---|---|---|---|
| Bare metal / laptop | ✓ | — | — |
| VPS (DO/Hetzner/AWS) | ✓ | ✓ | ✓ (AWS only) |
| Cloud LLM only (no local model) | ✓ | ✓ | ✓ |
| Discovery phase | ✓ | — | — |
| All messaging platforms | ✓ | partial | — |
| Security hardening | ✓ | basic | — |
| Optimization / prompt tuning | ✓ | — | — |
| Produces runbook | ✓ | — | — |
| Journey kit format | ✓ | — | — |
| Fanless hardware support | ✓ | — | — |

> Using **openclaw-lab-on-cloud** to provision your AWS EC2 instance? That tool handles OS and networking — start this kit at Phase 3.  
> For a detailed comparison including Open WebUI, AnythingLLM, and what each alternative taught us, see [docs/ALTERNATIVES.md](docs/ALTERNATIVES.md).

---

## Phases

| # | Skill | What happens |
|---|---|---|
| 0a | `skills/00-computing-selection.md` | Confirm or decide what machine and OS to use |
| 0b | `skills/00-orientation.md` | Brief the user — what they'll get, how it works |
| 1 | `skills/01-discovery.md` | Interview → `deployment-brief.md` |
| 2 | `skills/02-infra.md` | Node 24, ufw firewall, SSL, thermal monitoring |
| 3 | `skills/03-openclaw-core.md` | Install + systemd daemon + health check |
| 4 | `skills/04-integrations.md` | Telegram, WhatsApp, Slack, Email, Google Calendar/Contacts, Gmail, Drive, GitHub, local disk |
| 5 | `skills/05-security.md` | Firewall audit, credential hygiene, fail2ban, SSH |
| 6 | `skills/06-optimize.md` | System prompt, skill selection, workflow scheduling |
| 7 | `skills/07-handoff.md` | `runbook.md` generation, backup, final checklist |

---

## Requirements

- A machine running **Ubuntu 20.04+ (24.04 recommended)** or Debian 11+
  - Ubuntu 24.04 is the tested path
  - Debian 11+: documented, but not yet validated end to end
  - Raspberry Pi OS 64-bit (ARM64): documented with minor adaptations, not yet validated
  - macOS 12+: Phase 2 commands require Homebrew substitutions; not guided step-by-step and not yet validated — see Phase 2 notes
  - Windows: not supported natively — use WSL2
  - Not sure what machine to use? Phase 0a (Computing Selection) helps you decide
- Terminal or SSH access to the target machine
- An API key from a supported LLM provider (Anthropic recommended)
- A domain name is optional — Telegram works in long-poll mode without one
- Google is staged: Calendar/Contacts first, Gmail next, Drive only after a supported path is confirmed

---

## Known Supported Path

This is the path I currently recommend as the default first run:

- Ubuntu 24.04 LTS
- ASUS ZenBook UX305FA class hardware or similar x86_64 Linux machine
- Claude Code execution mode
- Cloud LLM provider
- Telegram integration
- WhatsApp Path A only if needed: personal number via `whatsapp-web.js`

If you stay close to that path, the kit is much more likely to work end to end without adaptation.

---

## Known Not Yet Validated

- Debian
- macOS
- Raspberry Pi / ARM64
- Journey AI clipboard mode
- WhatsApp Path B (Meta Business API)
- Slack, Email, Google, GitHub, and local disk integrations

These paths may still be reasonable, but today they should be treated as unvalidated rather than fully supported.

---

## Quick start

### Install via Journey

```bash
# From Claude Code
journey install dfront/openclaw-install
```

### Or clone and use directly

```bash
git clone https://github.com/davidf9999/openclaw-install-kit
cd openclaw-install-kit
# Open kit.md and follow the phases in order
```

---

## What gets generated on your machine (not committed)

The following files are produced during install and gitignored — they stay on your server:

- `deployment-brief.md` — your infrastructure and integration decisions
- `runbook.md` — restart, update, backup, and troubleshooting reference
- `system-prompt.md` — your OpenClaw assistant's persona and instructions
- `workflows.md` — scheduled tasks configuration

---

## How this kit works across different interfaces

This kit is designed for two execution modes:

**Claude Code (tool-executing)**: The agent runs all terminal commands directly. You review output and approve actions. Fastest path — used during the kit's own development.

**Journey AI or any chat interface (clipboard model)**: The agent has no terminal access. Each skill gives you a command block, asks you to run it and paste the output back, and verifies the result before moving on. Every command in the skill files is formatted for this pattern.

Both modes are supported throughout. You do not need to choose — just use whichever interface you have.

## How this kit relates to the Claude skill-creator

The individual skill files are the kind of content the Claude skill-creator produces. The kit adds a composition layer on top: phase sequencing with explicit gates, a shared artifact chain (`deployment-brief.md` carries all decisions from Phase 1 through Phase 7), recovery and re-entry logic for each phase, and explicit input/output contracts between phases. Put differently: the skill-creator produces the ingredients; this repo turns them into a skill chain.

## Kit composition chain

This kit sits in the middle of a natural three-kit sequence:

1. **`compute-selection-kit`** *(suggested — not yet published)* → machine running a compatible OS, terminal access confirmed
2. **`openclaw-install-kit`** *(this kit)* → running OpenClaw with integrations, security hardening, and a written runbook
3. **`openclaw-employee-kit`** *(see below)* → structured AI employee with scheduled briefings and reporting

## After install

The natural next step is [`keylimeaistudios/ai-employee-starter`](https://www.journeykits.ai) — a Journey kit that turns your running OpenClaw into a structured AI employee with morning briefings and daily reporting.

---

## Status

`v0.1.0-beta` — first working draft, suitable for early external review.

**Validated on**:
- Ubuntu 24.04 LTS, ASUS ZenBook UX305FA (Intel Core M, fanless, x86_64)
- DigitalOcean VPS, Ubuntu 24.04.3 LTS, Frankfurt, 1 vCPU / 2 GB RAM, Telegram working

Not yet validated on: Debian, macOS, Raspberry Pi / ARM64, WhatsApp Path B (Meta Business API), Slack, Email, Google Calendar/Contacts, Google Gmail, Google Drive, GitHub, local disk, or Journey AI clipboard mode. See TESTING.md for the full validation status and known gaps.

Not yet published to the Journey registry. Recommended next step: one more integration-focused validation run, or a second VPS pass with one extra integration, before calling it polished/public.

Contributions and test reports welcome — see CONTRIBUTING.md.

For the VPS validation workflow, see [docs/VPS-CHECKLIST.md](docs/VPS-CHECKLIST.md). It points to the helper scripts in `scripts/` and the VPS-specific deployment brief template in `templates/`.

---

## License

MIT
