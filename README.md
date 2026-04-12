# openclaw-install-kit

A skill chain for installing, integrating, hardening, and handing off a self-hosted [OpenClaw](https://openclaw.ai) instance on Ubuntu, using cloud LLM APIs such as Anthropic or OpenAI. No local GPU, local model, or Ollama setup is required.

This repo is structured as a Journey-compatible kit, but the Journey registry install path is not published or tested yet. For now, use the direct clone flow below.

---

## Requirements

- A target machine you can access by local terminal or SSH
- Ubuntu 24.04 LTS for the best-supported path
  - Ubuntu 20.04+ and Debian 11+ are documented but less validated
  - macOS and Raspberry Pi OS have notes in the skill files but are not validated end to end
  - Windows is not supported natively; use WSL2 with Ubuntu
- An AI coding agent CLI on your local machine, such as Claude Code or Codex CLI
- An Anthropic, OpenAI, or other supported cloud LLM API key
- Telegram if you want the simplest first integration
- Optional: a domain name if you plan to expose webhooks or use integrations that require public HTTPS

You do not need Node installed before starting. The kit checks and installs the required runtime during the infrastructure phase.

---

## Quick start

Clone the kit:

```bash
git clone https://github.com/davidf9999/openclaw-install-kit
cd openclaw-install-kit
```

Start your AI coding agent CLI in this directory. Any agent that can read files, guide terminal commands, and maintain context should work in principle; this kit has only been tested with Claude Code and Codex CLI.

For example:

```bash
claude
# or
codex
```

Prompt the agent:

```text
Use kit.md in this repository to guide me through installing OpenClaw.
```

The kit will ask where to install OpenClaw, help decide whether to use a local machine or VPS, gather missing deployment details, manage resume state, and work through the phases in order.

---

## Important Notes

**Beta status**: This kit is usable today, but it is still an early beta. The validated path is narrow and documented below.

**Cloud LLM only**: This kit connects OpenClaw to a cloud LLM provider. If you want a local model such as Llama, Mistral, or Ollama, use the [OpenClaw local LLM docs](https://docs.openclaw.ai) instead.

**Cost**: API calls are billed by your provider. Set a spend limit before starting.

**Privacy**: Messages processed by OpenClaw are sent to your cloud LLM provider, including messages sent by contacts through Telegram, WhatsApp, or other integrations. Review your provider's privacy policy before connecting platforms where other people message you.

**WhatsApp Path A**: Using `whatsapp-web.js` with a personal WhatsApp number violates WhatsApp's Terms of Service. Meta has banned accounts for this. Only use that path if you accept the risk.

---

## Supported Status

Best-supported first run:

- Ubuntu 24.04 LTS
- x86_64 Linux machine or Ubuntu VPS
- Tool-executing agent CLI mode, tested with Claude Code and Codex CLI
- Cloud LLM provider
- Telegram integration first
- WhatsApp Path A only after Telegram works, and only if you accept the account risk

Validated so far:

- Ubuntu 24.04 LTS, ASUS ZenBook UX305FA, Intel Core M, fanless, x86_64
- DigitalOcean VPS, Ubuntu 24.04.3 LTS, Frankfurt, 1 vCPU / 2 GB RAM, Telegram working

Not yet validated end to end:

- Debian
- macOS
- Raspberry Pi / ARM64
- Journey AI clipboard mode
- WhatsApp Path B, Meta Business API
- Slack, Email, Google, GitHub, and local disk integrations

See `TESTING.md` for the full validation status and known gaps.

---

## What the Kit Does

Eight guided phases, including orientation:

| # | Skill | What happens |
|---|---|---|
| 0a | `skills/00-computing-selection.md` | Confirm or decide what machine and OS to use |
| 0b | `skills/00-orientation.md` | Brief the user on what they will get and how the install works |
| 1 | `skills/01-discovery.md` | Interview → `deployment-brief.md` |
| 2 | `skills/02-infra.md` | Node 24, firewall, SSL, thermal monitoring |
| 3 | `skills/03-openclaw-core.md` | Install OpenClaw, daemon setup, health check |
| 4 | `skills/04-integrations.md` | Telegram, WhatsApp, Slack, Email, Google, GitHub, local disk |
| 5 | `skills/05-security.md` | Firewall audit, credential hygiene, fail2ban, SSH |
| 6 | `skills/06-optimize.md` | System prompt, skill selection, workflow scheduling |
| 7 | `skills/07-handoff.md` | `runbook.md`, backup, final checklist |

The agent verifies each phase before moving on. If a session is interrupted, the kit uses generated artifacts and `install-state.md` to resume from the right place.

---

## Generated Files

The following files are produced during install and are ignored by git:

- `deployment-brief.md` — infrastructure and integration decisions
- `install-state.md` — current phase, completed outputs, blockers, and next step
- `runbook.md` — restart, update, backup, and troubleshooting reference
- `system-prompt.md` — OpenClaw assistant persona and instructions
- `workflows.md` — scheduled task configuration

These files stay on your machine or server.

---

## Agent Interfaces

This kit is designed for two execution modes:

**Tool-executing agent CLI**: Agents such as Claude Code or Codex CLI run terminal commands directly. You review output and approve actions. This is the fastest path and has been used while building and validating this kit.

**Clipboard/chat mode**: The agent has no terminal access. Each skill gives you a command block, asks you to run it and paste the output back, and verifies the result before moving on. Every command in the skill files is formatted for this pattern.

---

## Journey Status

[Journey](https://www.journeykits.ai) is a registry for reusable agent workflows called kits. This repo follows the Journey kit structure, but it is not yet published to the Journey registry.

Do not use `journey install dfront/openclaw-install` until the kit is published and that install path has been tested.

---

## Why This Kit?

Most existing OpenClaw setup tools are cloud-only VPS provisioning scripts. This kit is different:

| | This kit | [clawhost](https://github.com/bfzli/clawhost) | [openclaw-lab-on-cloud](https://github.com/carlosacchi/openclaw-lab-on-cloud) |
|---|---|---|---|
| Bare metal / laptop | ✓ | — | — |
| VPS | ✓ | ✓ | ✓ (AWS only) |
| Cloud LLM only | ✓ | ✓ | ✓ |
| Discovery phase | ✓ | — | — |
| Integration planning | ✓ | partial | — |
| Security hardening | ✓ | basic | — |
| Optimization / prompt tuning | ✓ | — | — |
| Produces runbook | ✓ | — | — |
| Journey kit format | ✓ | — | — |
| Fanless hardware support | ✓ | — | — |

Using **openclaw-lab-on-cloud** to provision an AWS EC2 instance? That tool handles OS and networking. Start this kit at Phase 3.

For a detailed comparison including Open WebUI, AnythingLLM, and what each alternative taught us, see [`docs/ALTERNATIVES.md`](docs/ALTERNATIVES.md).

---

## After Install

The natural next step is [`keylimeaistudios/ai-employee-starter`](https://www.journeykits.ai), a Journey kit that turns your running OpenClaw into a structured AI employee with morning briefings and daily reporting.

---

## Status

`v0.1.0-beta` — first working draft, suitable for early external review.

Not yet published to the Journey registry. Recommended next step: one more integration-focused validation run, or a second VPS pass with one extra integration, before calling it polished/public.

Contributions and test reports welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

For the VPS validation workflow, see [`docs/VPS-CHECKLIST.md`](docs/VPS-CHECKLIST.md). It points to the helper scripts in `scripts/` and the VPS-specific deployment brief template in `templates/`.

---

## License

MIT
