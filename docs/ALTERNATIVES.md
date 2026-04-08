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

**What to learn from it:** Docker packaging reduces the dependency management problem (Node.js versions, nvm, global npm). OpenClaw does support Docker — see [docs.openclaw.ai/install/docker](https://docs.openclaw.ai/install/docker) — but the official docs explicitly state: *"No: you are running on your own machine and just want the fastest dev loop. Use the normal install flow instead."* Docker is best suited for VPS/server deployments or sandboxed environments, not personal laptop installs. A future Phase 2 Docker variant would be valuable for VPS users who want container management over systemd.

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

## Gaps and their status

**1. No fast path for expert users** ✅ Addressed  
Phase 1 (Discovery) can now be skipped if `deployment-brief.md` already exists or the user fills in the template directly. Noted in kit.md, orientation, and the Phase 1 skill header.

**2. No Docker install path** — Partially addressed (documented, not implemented  
OpenClaw supports Docker. The official docs recommend against it for personal laptop installs ("use the normal install flow instead") but it is the right choice for VPS deployments where container management is preferred over systemd. A future Phase 2 Docker variant for VPS users would eliminate nvm complexity. Not implemented in this kit yet.

**3. No IaC/Terraform path for infrastructure** ✅ Addressed  
`openclaw-lab-on-cloud` handles Terraform-managed AWS EC2 provisioning. The kit now explicitly tells users to start at Phase 3 if they used that tool for provisioning. Noted in kit.md, the computing-selection skill, and README.
