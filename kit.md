---
schema: "kit/1.0"
slug: "openclaw-install"
title: "OpenClaw Installation & Setup"
summary: "Beta kit for installing, integrating, hardening, and handing off a self-hosted OpenClaw instance on a validated Ubuntu path."
version: "0.1.0"
owner: "dfront"
license: "MIT"
tags:
  - openclaw
  - self-hosted
  - install
  - ubuntu
  - AI-assistant
  - infrastructure
  - security
model:
  provider: anthropic
  name: claude-sonnet-4-6
tools:
  - bash
  - read
  - write
  - edit
skills:
  - skills/00-computing-selection.md
  - skills/00-orientation.md
  - skills/01-discovery.md
  - skills/02-infra.md
  - skills/03-openclaw-core.md
  - skills/04-integrations.md
  - skills/05-security.md
  - skills/06-optimize.md
  - skills/07-handoff.md
services:
  - name: Anthropic API
    url: https://console.anthropic.com
    purpose: LLM provider for OpenClaw gateway mode
    setup: Obtain API key from console.anthropic.com
  - name: OpenClaw
    url: https://openclaw.ai
    purpose: The platform being installed
    setup: Installed by this kit
inputs:
  - name: deployment_brief
    description: Output of skill 01-discovery — server specs, platform choices, integration list
  - name: anthropic_api_key
    description: Anthropic API key for OpenClaw gateway mode
  - name: server_access
    description: SSH access or local terminal on the target Ubuntu machine
outputs:
  - name: running_openclaw
    description: Verified running OpenClaw daemon accessible via chosen messaging platform
  - name: runbook
    description: runbook.md covering restart, backup, monitoring, and update procedures
  - name: deployment_brief
    description: deployment-brief.md capturing all decisions made during install
environment:
  os: linux-macos
  platforms:
    - claude-code
    - journey-ai
  adaptationNotes: >
    Dual-runtime design: works in two distinct execution modes.
    (1) Claude Code (tool-executing): the agent runs commands directly, reads output, and
    proceeds without user involvement in terminal steps.
    (2) Journey AI / plain chat (clipboard model): the agent gives command blocks, the user
    runs them manually in their terminal, pastes output back, and the agent verifies before
    continuing. Every command block in the skill files is formatted for this paste-and-verify
    pattern — it is harmless in Claude Code and essential in Journey AI.
    Validated so far on Ubuntu 24.04.4 LTS on ASUS ZenBook UX305FA hardware in Claude Code.
    Debian 11/12, macOS 12+, Raspberry Pi OS 64-bit (ARM64), VPS deployments, and Journey AI
    clipboard mode are documented but not yet validated end to end.
    Fanless/low-power hardware (e.g. Intel Core M) is supported with thermal monitoring notes.
selfContained: true
fileManifest:
  - path: kit.md
    role: primary
    description: Master workflow guide and kit metadata
  - path: skills/00-computing-selection.md
    role: skill
    description: Computing selection — helps user decide what machine and OS to use before installation begins
  - path: skills/00-orientation.md
    role: skill
    description: Orientation — delivered before Phase 1; sets expectations for the collaboration model
  - path: skills/01-discovery.md
    role: skill
    description: Interview phase — produces deployment-brief.md
  - path: skills/02-infra.md
    role: skill
    description: Infrastructure setup — Node.js, DNS, SSL, process manager
  - path: skills/03-openclaw-core.md
    role: skill
    description: Core OpenClaw install and gateway configuration
  - path: skills/04-integrations.md
    role: skill
    description: Messaging, calendar, email, and CRM integration
  - path: skills/05-security.md
    role: skill
    description: Security hardening — firewall, credentials, access control
  - path: skills/06-optimize.md
    role: skill
    description: Prompt engineering, skill selection, workflow tuning
  - path: skills/07-handoff.md
    role: skill
    description: Runbook generation and team onboarding
failures:
  - problem: Node.js version too old
    resolution: Use nvm to install Node 24; check with `node --version` before proceeding
  - problem: Thermal throttling on fanless hardware
    resolution: Monitor with `sensors`; throttle concurrent agent tasks if temps exceed 80°C
  - problem: Google OAuth flow fails
    resolution: Enable all required scopes in GCP console; re-run OAuth flow after scope update
  - problem: Telegram not receiving messages (webhook mode)
    resolution: Verify SSL certificate is valid and publicly accessible; use `curl` to test webhook endpoint
  - problem: Telegram not receiving messages (long-poll mode, no domain)
    resolution: Check token is correct with `openclaw status --deep`; if 401, revoke and reissue token via @BotFather; SSL is not required in this mode
---

## Goal

Install, configure, integrate, harden, and hand off a self-hosted OpenClaw instance on a validated Ubuntu path — without a local LLM. By the end of this kit the agent (or human) running it will have a verified OpenClaw daemon connected to at least one messaging platform, a security-hardened environment, and a written runbook for ongoing maintenance.

## When to Use

- You want to self-host OpenClaw on a Linux machine and are comfortable starting from the tested Ubuntu path
- You are using cloud LLM APIs (Anthropic, OpenAI, etc.) — no local GPU required
- You want a structured, phase-by-phase installation that produces documentation as it goes
- You are running this kit from Claude Code (before OpenClaw is installed)

Not suitable for:
- Local LLM / Ollama setups (different resource requirements — see openclaw docs)
- Windows native installs (use WSL2 + adapt infra phase)
- Managed/hosted OpenClaw offerings

## Release Status

This kit should currently be presented as a beta.

Known supported path:
- Ubuntu 24.04.4 LTS
- x86_64 laptop or desktop hardware
- Claude Code execution mode
- Telegram integration
- WhatsApp Path A (personal number via `whatsapp-web.js`) when needed

Documented but not yet validated:
- VPS deployments
- Debian
- macOS
- Raspberry Pi / ARM64
- Journey AI clipboard mode
- WhatsApp Path B
- Slack, Email, Google, GitHub, and local disk integrations

**Expert fast path**: If you already have a completed `deployment-brief.md` (from a prior install or written manually), skip Phase 1 and go straight to Phase 2.

**Using openclaw-lab-on-cloud or another IaC tool for provisioning?** Those tools handle OS provisioning, networking, and firewall configuration. Start this kit at Phase 3 — Phases 0–2 are already done.

## Setup

### Prerequisites
- A machine running Ubuntu 20.04+ (24.04 recommended), Debian 11+, or macOS 12+
  - Other Linux distributions that use apt and systemd will generally work
  - Raspberry Pi OS 64-bit (ARM64) is supported with minor adaptations in Phase 4
  - Windows is not supported natively — use WSL2 with Ubuntu and adapt Phase 2
- SSH access or local terminal on the target machine (confirmed before Phase 1 begins)
- An Anthropic API key (or other supported provider key)
- A domain name or DDNS hostname (required for webhook-based integrations; optional for Telegram long-poll mode)
- This kit is run from Claude Code on your machine, or can be followed manually via any chat interface (see Dual-runtime design below)

### Dual-runtime design

This kit is designed to work in two distinct execution modes:

**Claude Code (tool-executing mode)**: The agent runs all terminal commands directly. The user reviews output and approves actions. This is the fastest path and was used during the kit's initial development.

**Journey AI / plain chat (clipboard model)**: The agent has no terminal access. Each skill gives command blocks with explicit "run this and paste the output" instructions. The user runs the command, pastes the output into the chat, and the agent verifies before proceeding. This mode is safe to use with any chat-based AI interface.

Every command block in the skill files is formatted to work in both modes. The paste-and-verify pattern is essential in clipboard mode and harmless in tool-executing mode.

### Relationship to the Claude skill-creator

The individual skill files (`skills/NN-name.md`) are the kind of content the Claude skill-creator produces — self-contained instructions for a specific task. The kit adds a composition layer on top of that content:

- **Phase sequencing with explicit gates**: phases cannot be skipped; each completion check must pass before the next phase begins
- **Shared artifact chain**: `deployment-brief.md` is produced in Phase 1 and consumed by every subsequent phase; each phase adapts its steps based on the flags it contains (fanless hardware, domain availability, WhatsApp path, etc.)
- **Recovery / re-entry logic**: every skill can be re-entered after a session break or context loss; `deployment-brief.md` on disk is the persistent state
- **Input/output contracts**: each skill declares what it requires and what it produces

The skill-creator produces content; the kit adds orchestration.

### Running the kit

Work through each skill file in order (Phase 0a → Phase 7). Each skill produces an artifact (a file or a verified state) that the next skill consumes. Do not skip phases — each one sets up prerequisites for the next.

At the end of each phase, confirm the output artifact exists before moving on.

### Kit composition chain

This kit sits in the middle of a natural three-kit sequence:

1. **`compute-selection-kit`** *(suggested, not yet published)* — Helps the user choose and provision the right machine (VPS, bare metal, cloud). Ends with: a machine running a compatible OS with terminal access confirmed.
2. **`openclaw-install-kit`** *(this kit)* — Installs, integrates, hardens, and hands off a running OpenClaw instance. Starts with: a machine ready to use.
3. **`openclaw-employee-kit`** *(see `keylimeaistudios/ai-employee-starter`)* — Turns the running OpenClaw into a structured AI employee with morning briefings and scheduled reporting.

Phase 0a of this kit covers a lightweight computing selection for users who haven't yet decided what machine to use. For users who need more detailed help provisioning infrastructure (VPS setup, DNS, SSH key management), a dedicated compute-selection-kit would cover that scope.

## Steps

0a. **Computing Selection** (`skills/00-computing-selection.md`) — Confirm or decide what machine and OS to use
0b. **Orientation** (`skills/00-orientation.md`) — Brief the user before Phase 1 begins
1. **Discovery** (`skills/01-discovery.md`) — Interview the user, produce `deployment-brief.md`
2. **Infrastructure** (`skills/02-infra.md`) — Prepare the Ubuntu machine: Node.js, firewall, thermal monitoring
3. **OpenClaw Core** (`skills/03-openclaw-core.md`) — Install OpenClaw, configure gateway, verify daemon
4. **Integrations** (`skills/04-integrations.md`) — Connect messaging platforms, calendar, email, CRM
5. **Security** (`skills/05-security.md`) — Firewall, credential hardening, access control audit
6. **Optimization** (`skills/06-optimize.md`) — Prompt tuning, skill selection, workflow design
7. **Handoff** (`skills/07-handoff.md`) — Produce `runbook.md`, team onboarding notes

## Constraints

- Requires Node.js 22.14+ (Node 24 recommended). Do not proceed with older versions.
- Gateway mode only — this kit does not cover local LLM setup.
- Google Workspace integration is the most complex step and is optional. Only include it if the user confirmed it in discovery.
- OpenClaw stores config (including API keys and bot tokens) in `~/.openclaw/openclaw.json`. This file must have permissions `600` and must never be committed to version control. The install kit sets this automatically; verify in Phase 5.
- On fanless/low-power hardware (Intel Core M, fanless NUCs): monitor CPU temperature throughout. Install `lm-sensors` during infra phase.

## Safety Notes

- Never log or echo API keys to stdout during setup steps.
- The `openclaw onboard` command prompts interactively for keys — do not pass them as CLI arguments (they appear in shell history).
- After install, verify config file permissions: `chmod 600 ~/.openclaw/openclaw.json && chmod 700 ~/.openclaw`.
- Review all webhook endpoints for public exposure before enabling integrations.
- Run the security skill (05) before exposing any integration to the internet.
