# My OpenClaw Install — ASUS UX305F / Ubuntu

This is your personal step-by-step guide, derived from the kit but tailored to your specific machine.

**Machine**: ASUS UX305F (Intel Core M, 8GB RAM, fanless)  
**OS**: Ubuntu (22.04+ recommended — run `lsb_release -a` to confirm)  
**Mode**: Cloud LLM only (Anthropic API, no local model)  
**Run from**: Claude Code on your local machine, operating against the UX305F

---

## Before you start

You will need:
- [ ] Terminal access to the UX305F (either directly or via SSH)
- [ ] An Anthropic API key — get one at https://console.anthropic.com if you don't have one
- [ ] The kit files from this repo open alongside in your editor

Have these ready but **do not paste them into a terminal yet** — the onboard wizard will prompt for them securely.

---

## Phase 1 — Discovery (skills/01-discovery.md)

Run this phase as a conversation with Claude Code. Claude will ask you questions and produce `deployment-brief.md`.

**Your answers (fill these in before starting — makes the conversation faster):**
- Machine: ASUS UX305F, Intel Core M, 8GB RAM
- OS: Ubuntu (check with `lsb_release -a`)
- Fanless: **yes** — thermal monitoring required
- Use mode: personal / development (not always-on production — Core M is not ideal for 24/7)
- LLM provider: Anthropic
- Primary messaging: Telegram (start here, add others later)
- Domain: do you have one? (yes/no — if no, Telegram long-poll mode will be used)

Expected output: `deployment-brief.md` in your working directory.

---

## Phase 2 — Infrastructure (skills/02-infra.md)

Run these commands on the UX305F:

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git build-essential ufw lm-sensors stress-ng

# 2. Check your temps NOW (fanless — important baseline)
sudo sensors-detect --auto
sensors
# Note the idle temp before anything else runs
```

If idle CPU temp is above 60°C — stop and ask Claude Code before continuing.

```bash
# 3. Install Node.js via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
nvm alias default 24
node --version    # must show v24.x.x

# 4. Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose

# 5. Working directory
mkdir -p ~/openclaw
```

**SSL / domain**: only needed if you have a domain and want webhook-based integrations.
Telegram works fine without it (long-poll mode). Skip certbot if no domain.

---

## Phase 3 — OpenClaw Core (skills/03-openclaw-core.md)

```bash
# Install
npm install -g openclaw
openclaw --version

# Onboard (interactive — have your Anthropic API key ready to paste)
cd ~/openclaw
openclaw onboard --install-daemon
```

When prompted:
- Provider: **Anthropic**
- Model: `claude-sonnet-4-6` (good balance); `claude-opus-4-6` if you want best quality
- Port: accept default (3000)
- Install daemon: **yes** (registers as systemd service)

```bash
# Verify it's running
sudo systemctl status openclaw
curl -s http://localhost:3000/health

# Secure the .env
chmod 600 ~/openclaw/.env
```

---

## Phase 4 — Integrations (skills/04-integrations.md)

**Start with Telegram only.** Add others after Telegram is verified.

1. Open Telegram → search `@BotFather` → `/newbot` → get your Bot Token
2. Configure:

```bash
openclaw config set telegram.token <your-bot-token>
openclaw config set telegram.mode longpoll
sudo systemctl restart openclaw
```

3. Send `/start` to your bot in Telegram. It should respond.

Add other platforms (WhatsApp, Slack, Google, etc.) only after confirming Telegram works.

---

## Phase 5 — Security (skills/05-security.md)

Run through the full security checklist in `skills/05-security.md`.

Key things for your specific machine:
```bash
# Credential check
stat ~/openclaw/.env        # should be 600
chmod 600 ~/openclaw/.env   # if not

# Thermal load test (fanless — do not skip)
stress-ng --cpu 2 --timeout 30s &
watch -n2 sensors
# Kill if temps exceed 85°C: kill %1
```

If sustained temps exceed 85°C under load:
```bash
openclaw config set gateway.max_concurrent_tasks 2
sudo systemctl restart openclaw
```

---

## Phase 6 — Optimization (skills/06-optimize.md)

Work through this with Claude Code. You'll:
- Write a system prompt for your assistant
- Install relevant skills from ClawHub
- Test with real use-case messages
- Tune until responses feel right

---

## Phase 7 — Handoff (skills/07-handoff.md)

Claude Code will generate `~/openclaw/runbook.md` for you — your ongoing reference for restarts, updates, backups, and troubleshooting.

---

## Quick reference (after install)

| Action | Command |
|---|---|
| Check status | `sudo systemctl status openclaw` |
| Restart | `sudo systemctl restart openclaw` |
| View logs | `sudo journalctl -u openclaw -n 50` |
| Check temp | `sensors` |
| Update openclaw | `npm update -g openclaw && sudo systemctl restart openclaw` |

---

## Notes specific to your hardware

- The UX305F's Core M is fanless and designed for burst workloads, not 24/7 sustained load. For personal assistant use it's fine. If you ever run heavy concurrent workflows, watch `sensors`.
- 8GB RAM is comfortable for gateway mode — you have headroom.
- If you ever want to move to a VPS for always-on reliability, the kit supports DigitalOcean/Hetzner via skill 02 — the rest of the phases are identical.
