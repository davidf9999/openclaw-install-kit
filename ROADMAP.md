# Roadmap

## Current: v0.1.0

One validated configuration: Ubuntu 24.04 / ASUS UX305FA. Telegram and WhatsApp Path A working.

---

## v0.2.0 — Validate remaining skill 04 integrations

The integrations below are documented in skill 04 but have **not been tested end to end**. Instructions are based on OpenClaw documentation and may contain errors similar to the initial incorrect assumptions about pm2, port 3000, and system-level systemd that were discovered during the first real install.

| Integration | Status | Notes |
|---|---|---|
| Telegram | ✅ Validated | Long-poll mode, no domain |
| WhatsApp Path A (personal number) | ✅ Validated | whatsapp-web.js + Cloudflare tunnel |
| WhatsApp Path B (Meta Business API) | ❌ Not tested | Instructions based on Meta docs only |
| Slack | ❌ Not tested | |
| Email (IMAP/SMTP) | ❌ Not tested | |
| Google Calendar | 🔶 Planned next | Validate on a dedicated Google test account first |
| Google Contacts | 🔶 Planned next | Validate alongside Calendar; keep scope separated from Gmail/Drive if needed |
| Google Gmail | 🔶 Planned next | Treat as a separate, more sensitive stage after Calendar/Contacts |
| Google Drive | ⏸ Pending path | Only validate after an official supported path is confirmed |
| GitHub | ❌ Not tested | |
| Local disk | ❌ Not tested | Scope and safety controls unverified |

**The kit welcomes test reports** — see [CONTRIBUTING.md](CONTRIBUTING.md) and [TESTING.md](TESTING.md).
For the staged Google validation sequence, see [docs/GOOGLE-TEST-PLAN.md](docs/GOOGLE-TEST-PLAN.md).

---

## v0.3.0 — Broader OS and hardware validation

- Debian 12 (should work — apt/ufw identical — needs confirmation)
- Raspberry Pi 4 / ARM64 (ARM cloudflared binary, thermal limits differ)
- macOS 12+ (Phase 2 Homebrew substitutions — needs a real guided run)
- VPS (DigitalOcean, Hetzner) — no fanless concerns, different firewall defaults

---

## Future

- **Docker install variant for VPS** — OpenClaw supports Docker; a Phase 2 Docker path would eliminate nvm/Node dependency complexity for server deployments
- **Phase 2 fast path for VPS** — for users who just provisioned a fresh cloud server and want minimal guidance
- **Log rotation** — automate cleanup of `/tmp/openclaw/` and session JSONL files

---

## Integration scope — not limited to this list

The integrations above are those explicitly guided in skill 04. They are not the full list of what OpenClaw supports.

OpenClaw's integration ecosystem includes (among others): Gmail, Google Drive, Discord, Microsoft Teams, Linear, Jira, Notion, Airtable, RSS/web search, and anything reachable via ClawHub skills or custom webhooks.

The discovery phase (skill 01) is intentionally open-ended — it asks what the user wants and adapts accordingly. If you want to connect an integration not listed in skill 04, the phase header and `deployment-brief.md` support it. You may need to write or adapt the configuration steps yourself and report back to help expand skill 04.

The current skill 04 reflects integrations that were relevant to the kit's first real install, not a deliberate limitation of scope. Google Calendar/Contacts are the next validation slice; Gmail is separate and more sensitive; Drive remains pending until a supported path is confirmed.
