# openclaw-install-kit

A [Journey kit](https://www.journeykits.ai) for installing, integrating, hardening, and handing off a self-hosted [OpenClaw](https://openclaw.ai) instance on Ubuntu — using cloud LLM APIs (no local GPU required).

Eight guided phases (including orientation). The agent guides you step by step — you run commands in your terminal, paste the output back, and the agent verifies before moving on. Produces a written runbook at the end.

---

## Why this kit?

Most existing OpenClaw setup tools are cloud-only (VPS provisioning scripts). This kit is different:

| | This kit | [clawhost](https://github.com/bfzli/clawhost) | [openclaw-lab-on-cloud](https://github.com/carlosacchi/openclaw-lab-on-cloud) |
|---|---|---|---|
| Bare metal / laptop | ✓ | — | — |
| VPS (DO/Hetzner/AWS) | ✓ | ✓ | ✓ (AWS only) |
| Discovery phase | ✓ | — | — |
| All messaging platforms | ✓ | partial | — |
| Security hardening | ✓ | basic | — |
| Optimization / prompt tuning | ✓ | — | — |
| Produces runbook | ✓ | — | — |
| Journey kit format | ✓ | — | — |
| Fanless hardware support | ✓ | — | — |

---

## Phases

| # | Skill | What happens |
|---|---|---|
| 0a | `skills/00-computing-selection.md` | Confirm or decide what machine and OS to use |
| 0b | `skills/00-orientation.md` | Brief the user — what they'll get, how it works |
| 1 | `skills/01-discovery.md` | Interview → `deployment-brief.md` |
| 2 | `skills/02-infra.md` | Node 24, ufw firewall, SSL, thermal monitoring |
| 3 | `skills/03-openclaw-core.md` | Install + systemd daemon + health check |
| 4 | `skills/04-integrations.md` | Telegram, WhatsApp, Slack, Email, Google, GitHub, local disk |
| 5 | `skills/05-security.md` | Firewall audit, credential hygiene, fail2ban, SSH |
| 6 | `skills/06-optimize.md` | System prompt, skill selection, workflow scheduling |
| 7 | `skills/07-handoff.md` | `runbook.md` generation, backup, final checklist |

---

## Requirements

- A machine running **Ubuntu 20.04+ (24.04 recommended)** or Debian 11+ — fully supported and tested
  - Raspberry Pi OS 64-bit (ARM64): supported with minor adaptations (not yet validated)
  - macOS 12+: Phase 2 commands require Homebrew substitutions; not guided step-by-step and not yet validated — see Phase 2 notes
  - Windows: not supported natively — use WSL2
  - Not sure what machine to use? Phase 0a (Computing Selection) helps you decide
- Terminal or SSH access to the target machine
- An API key from a supported LLM provider (Anthropic recommended)
- A domain name is optional — Telegram works in long-poll mode without one

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

The individual skill files are the kind of content the Claude skill-creator produces. The kit adds a composition layer on top: phase sequencing with explicit gates, a shared artifact chain (`deployment-brief.md` carries all decisions from Phase 1 through Phase 7), recovery and re-entry logic for each phase, and explicit input/output contracts between phases. The skill-creator produces the ingredients; the kit adds the orchestration.

## Kit composition chain

This kit sits in the middle of a natural three-kit sequence:

1. **`compute-selection-kit`** *(suggested — not yet published)* → machine running a compatible OS, terminal access confirmed
2. **`openclaw-install-kit`** *(this kit)* → running OpenClaw with integrations, security hardening, and a written runbook
3. **`openclaw-employee-kit`** *(see below)* → structured AI employee with scheduled briefings and reporting

## After install

The natural next step is [`keylimeaistudios/ai-employee-starter`](https://www.journeykits.ai) — a Journey kit that turns your running OpenClaw into a structured AI employee with morning briefings and daily reporting.

---

## Status

`v0.1.0` — first working draft.

**Validated on**: Ubuntu 24.04 LTS, ASUS ZenBook UX305FA (Intel Core M, fanless, x86_64). This is the only hardware and OS combination that has been real-world tested to date.

Not yet validated on: Debian, macOS, Raspberry Pi / ARM64, VPS, or any hardware other than the UX305FA. WhatsApp Path B (Meta Business API) has not been tested. See TESTING.md for the full validation status and known gaps.

Not yet published to the Journey registry. Publish planned after broader real-world validation.

Contributions and test reports welcome — see CONTRIBUTING.md.

---

## License

MIT
