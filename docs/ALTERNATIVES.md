# Alternatives & Competitive Landscape

This document compares `openclaw-install-kit` to other tools that partially overlap with what it does, and draws conclusions about what could be learned from each.

---

## Direct alternatives — OpenClaw-specific installers

### [clawhost](https://github.com/bfzli/clawhost)

A Node.js app that provisions OpenClaw on a VPS (DigitalOcean, Hetzner, AWS). One-click cloud deployment with SSL and DNS configuration baked in.

| | clawhost | openclaw-install-kit |
|---|---|---|
| Target | VPS only | Bare metal, VPS, laptop, Raspberry Pi |
| Format | Automated script | Guided conversation, phase-by-phase |
| Bare metal / laptop | — | ✓ |
| Hardware-adaptive config | — | ✓ (fanless, domain, hosting flags) |
| Produces runbook | — | ✓ |
| Discovery phase | — | ✓ |
| Works without domain | — | ✓ (Telegram long-poll) |
| Clipboard/chat mode | — | ✓ |

**What to learn from it:** clawhost handles the VPS path more concisely for users who just want a quick deploy on a fresh server. If this kit ever adds a "fast path for clean VPS" that skips the discovery interview for expert users, that is the experience to match.

---

### [openclaw-lab-on-cloud](https://github.com/carlosacchi/openclaw-lab-on-cloud)

Terraform + GitHub Actions deployment targeting AWS EC2. Infrastructure-as-code, declarative, reproducible.

**What to learn from it:** The IaC approach makes the VPS setup reproducible and reviewable as a diff. For users who are already Terraform-comfortable, this kit could note Terraform as an alternative to the manual Phase 2 steps — or a future `openclaw-install-kit-terraform` variant could cover that path. The current kit has no equivalent for cloud-infrastructure provisioning and that is a real gap for users who want GitOps-style repeatability.

---

## Adjacent alternatives — self-hosted AI assistant setup

### [Open WebUI](https://github.com/open-webui/open-webui)

A popular self-hosted web UI for Ollama, OpenAI, and other LLM backends. Docker-based, multi-LLM.

**Relevance:** Different product class (local/web UI vs. messaging-channel assistant), but it solves the "I want a personal AI that persists on my machine" problem for many users. Its installation is Docker-first, which is simpler than the npm + systemd path this kit uses.

**What to learn from it:** Docker packaging significantly reduces the dependency management problem (Node.js versions, nvm, global npm). A Phase 2 variant that installs OpenClaw as a Docker container — if OpenClaw supports that — would make this kit more accessible to less technical users and eliminate the nvm complexity entirely.

### [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)

Desktop app + self-hosted server for building AI workflows. Focus on UX and ease of use over configurability.

**What to learn from it:** It ships as a desktop app with a GUI installer — the user experience is closer to installing any consumer software. For non-technical users, the paste-and-verify terminal model is a significant barrier. If OpenClaw ever ships a desktop installer, the kit should detect that path and route accordingly. For now, the kit's orientation phase should be more explicit about the terminal skill level required.

---

## Format alternatives — guided install frameworks

### Journey kit format ([journeykits.ai](https://www.journeykits.ai))

This kit is itself published in the Journey kit format. Journey is a registry for packaged AI workflows, compatible with Claude, Cursor, and other AI tools.

**Relevance:** The Journey kit format is what gives this kit its composition layer — skill sequencing, input/output contracts, dual-runtime compatibility. Other kits in the registry provide comparison points.

**What to learn from it:** The Journey registry is where this kit should eventually be published (`journey install dfront/openclaw-install`). The `kit.md` schema is already written for this. Publishing there would make the kit discoverable without requiring a manual clone.

---

## Summary: what this kit does that others don't

| Capability | clawhost | openclaw-lab-on-cloud | Open WebUI | This kit |
|---|---|---|---|---|
| Bare metal / laptop support | — | — | Partial | ✓ |
| Hardware-adaptive (fanless, domain) | — | — | — | ✓ |
| Discovery interview → persisted brief | — | — | — | ✓ |
| Phase gates with completion checks | — | — | — | ✓ |
| Re-entry after context loss | — | — | — | ✓ |
| Clipboard/paste mode (any chat UI) | — | — | — | ✓ |
| Produces runbook | — | Partial (state files) | — | ✓ |
| Security hardening phase | — | Partial | — | ✓ |
| Multi-integration (WhatsApp, calendar, GitHub) | — | — | — | ✓ |
| IaC / declarative reproducibility | — | ✓ | Partial (Docker) | — |
| Docker-based install | — | — | ✓ | — |
| One-click VPS deploy | ✓ | ✓ | ✓ | — |

---

## Potential gaps to address

Based on this comparison, three gaps stand out:

**1. No fast path for clean VPS users**  
Expert users provisioning a fresh VPS don't need the discovery interview — they know their setup. A "skip to Phase 2 if you already have deployment-brief.md" shortcut would close this gap without removing the guided path for everyone else.

**2. No Docker install path**  
Docker would eliminate the nvm/Node dependency management problem. If OpenClaw supports Docker, a Phase 2 variant should exist.

**3. No IaC/Terraform path for infrastructure**  
Users who want GitOps-style reproducibility have no equivalent in this kit. A pointer to `openclaw-lab-on-cloud` for the VPS provisioning step — with this kit picking up from Phase 3 onward — would be honest and useful rather than trying to cover everything in one kit.
