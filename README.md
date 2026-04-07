# openclaw-install-kit

A [Journey kit](https://www.journeykits.ai) for installing, integrating, hardening, and handing off a self-hosted [OpenClaw](https://openclaw.ai) instance on Ubuntu — using cloud LLM APIs (no local GPU required).

Run from Claude Code. Seven guided phases. Produces a written runbook at the end.

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
| 1 | `skills/01-discovery.md` | Interview → `deployment-brief.md` |
| 2 | `skills/02-infra.md` | Node 24, ufw firewall, SSL, thermal monitoring |
| 3 | `skills/03-openclaw-core.md` | Install + systemd daemon + health check |
| 4 | `skills/04-integrations.md` | Telegram, WhatsApp, Slack, Email, Google, CRM |
| 5 | `skills/05-security.md` | Firewall audit, credential hygiene, fail2ban, SSH |
| 6 | `skills/06-optimize.md` | System prompt, skill selection, workflow scheduling |
| 7 | `skills/07-handoff.md` | `runbook.md` generation, backup, final checklist |

---

## Requirements

- Ubuntu 20.04+ (22.04+ recommended)
- Terminal or SSH access to the target machine
- An API key from a supported LLM provider (Anthropic recommended)
- Claude Code on your local machine (to run the kit)
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

### Personal install guide

If you are the kit author testing on a specific machine, see [`MY-INSTALL.md`](MY-INSTALL.md) — a pre-filled guide for the ASUS UX305F / Ubuntu setup.

---

## What gets generated on your machine (not committed)

The following files are produced during install and gitignored — they stay on your server:

- `deployment-brief.md` — your infrastructure and integration decisions
- `runbook.md` — restart, update, backup, and troubleshooting reference
- `system-prompt.md` — your OpenClaw assistant's persona and instructions
- `workflows.md` — scheduled tasks configuration

---

## After install

The natural next step is [`keylimeaistudios/ai-employee-starter`](https://www.journeykits.ai) — a Journey kit that turns your running OpenClaw into a structured AI employee with morning briefings and daily reporting.

---

## Status

`v0.1.0` — first working draft, being tested on Ubuntu / ASUS UX305F. Not yet published to the Journey registry. Publish planned after real-world validation.

Contributions and issue reports welcome.

---

## License

MIT
