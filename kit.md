---
schema: "kit/1.0"
slug: "openclaw-install"
title: "OpenClaw Installation & Setup"
summary: "Guide an AI agent through installing, integrating, hardening, and handing off a self-hosted OpenClaw instance — from bare metal to production-ready."
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
  os: linux
  platforms:
    - claude-code
  adaptationNotes: >
    Designed for Journey AI's conversational runtime: the agent guides the user step by step,
    the user runs all commands manually and pastes output back for verification.
    The agent cannot execute commands directly — this is by design.
    Also compatible with Claude Code (tool-executing mode) for local installs.
    Tested on Ubuntu 22.04+ and 24.04 on bare metal and VPS.
    Fanless/low-power hardware (e.g. Intel Core M) is supported with thermal monitoring notes.
selfContained: true
fileManifest:
  - path: kit.md
    role: primary
    description: Master workflow guide and kit metadata
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
  - problem: Telegram webhook not receiving messages
    resolution: Verify SSL certificate is valid and publicly accessible; use `curl` to test webhook endpoint
---

## Goal

Install, configure, integrate, harden, and hand off a fully operational self-hosted OpenClaw instance on an Ubuntu machine — without a local LLM. By the end of this kit the agent (or human) running it will have a verified OpenClaw daemon connected to at least one messaging platform, a security-hardened environment, and a written runbook for ongoing maintenance.

## When to Use

- You want to self-host OpenClaw on a Linux machine (bare metal, VPS, or cloud instance)
- You are using cloud LLM APIs (Anthropic, OpenAI, etc.) — no local GPU required
- You want a structured, phase-by-phase installation that produces documentation as it goes
- You are running this kit from Claude Code (before OpenClaw is installed)

Not suitable for:
- Local LLM / Ollama setups (different resource requirements — see openclaw docs)
- Windows native installs (use WSL2 + adapt infra phase)
- Managed/hosted OpenClaw offerings

## Setup

### Prerequisites
- Ubuntu 20.04 or later (22.04+ recommended)
- SSH access or local terminal on the target machine
- An Anthropic API key (or other supported provider key)
- A domain name or DDNS hostname (required for webhook-based integrations; optional for Telegram long-poll mode)
- This kit is run from Claude Code on your local machine, operating against the target server

### Running the kit
Work through each skill file in order (01 → 07). Each skill produces an artifact (a file or a verified state) that the next skill consumes. Do not skip phases — each one sets up prerequisites for the next.

At the end of each phase, confirm the output artifact exists before moving on.

## Steps

0. **Orientation** (`skills/00-orientation.md`) — Brief the user before Phase 1 begins
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
- All API keys must be stored in environment variables or a secrets manager — never in plain config files committed to version control.
- On fanless/low-power hardware (Intel Core M, fanless NUCs): monitor CPU temperature throughout. Install `lm-sensors` during infra phase.

## Safety Notes

- Never log or echo API keys to stdout during setup steps.
- The `openclaw onboard` command prompts interactively for keys — do not pass them as CLI arguments (they appear in shell history).
- After install, restrict `.env` file permissions: `chmod 600 .env`.
- Review all webhook endpoints for public exposure before enabling integrations.
- Run the security skill (05) before exposing any integration to the internet.
