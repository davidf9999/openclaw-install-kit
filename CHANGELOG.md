# Changelog

## v0.1.0-beta — 2026-04-08

First beta release.

### Validated
- Full 8-phase guided install on Ubuntu 24.04 LTS / ASUS ZenBook UX305FA (Intel Core M, fanless)
- Telegram (long-poll mode, no domain required)
- WhatsApp Path A — personal number via whatsapp-web.js bridge + Cloudflare named tunnel
- Systemd user service with linger (survives reboot and lid-close)
- Security hardening: ufw, fail2ban, file permissions, credential audit

### Included but not yet validated
- Slack, Email (IMAP/SMTP), Google Calendar, Google Contacts, GitHub, local disk
- Debian 11/12, macOS 12+, Raspberry Pi OS (ARM64), VPS deployments
- WhatsApp Path B (Meta Business API)
- Journey AI clipboard mode (kit developed in Claude Code)

### Known gaps
See [TESTING.md](TESTING.md) for full validation status and [ROADMAP.md](ROADMAP.md) for planned work.
