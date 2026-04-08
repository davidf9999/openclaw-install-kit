# Skill 07 — Handoff

**Purpose**: Produce a `runbook.md` covering ongoing operations, and confirm the installation is complete.

**Input**: Completed installation (skills 01–06), `deployment-brief.md`  
**Output**: `~/openclaw/runbook.md`, final verification, summary of what was installed

> **Phase 7 of 8 — Handoff**  
> Re-read `deployment-brief.md` and review what was installed across phases 02–06 before generating the runbook.  
> This phase is mostly written output — minimal commands. Paste any command output back here.  
> If you are re-entering this phase, say "resuming Phase 7."

---

## Instructions

Generate `runbook.md` by filling in the template below. Use `deployment-brief.md` and information gathered during the install to fill all placeholders. Then run the final verification checklist.

---

## Generate runbook.md

Write this file to `~/openclaw/runbook.md`:

```markdown
# OpenClaw Runbook

Generated: <date>
Machine: <from deployment-brief>
OpenClaw version: <from `openclaw --version`>
Assistant name: <from IDENTITY.md>
Primary channel: <from deployment-brief>

---

## Daily operations

### Check status
```bash
systemctl --user status openclaw-gateway
```

### View logs
```bash
cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -50
# Follow live:
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

### Restart
```bash
systemctl --user restart openclaw-gateway
```

### Stop / Start
```bash
systemctl --user stop openclaw-gateway
systemctl --user start openclaw-gateway
```

### Open dashboard
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw gateway url
```

---

## Boot & always-on behavior

- **Auto-start on boot**: user linger enabled (`loginctl show-user $USER | grep Linger` → `Linger=yes`)
- **Lid closed** (laptops): stays running if `HandleLidSwitch=ignore` in `/etc/systemd/logind.conf`
- **Power outage** (laptops with battery): runs on battery until depleted

To verify linger is set:
```bash
loginctl show-user $USER | grep Linger
```

If not set:
```bash
sudo loginctl enable-linger $USER
```

---

## Updates

### Update OpenClaw
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
npm update -g openclaw
systemctl --user restart openclaw-gateway
openclaw --version
```

---

## Temperature monitoring (fanless hardware)

<include only if Fanless: yes in deployment-brief>

```bash
sensors
```

Baseline: <idle temp>°C idle, <peak temp>°C under load. Critical: 95°C.

If consistently above 80°C under sustained load:
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw config set gateway.max_concurrent_tasks 2
systemctl --user restart openclaw-gateway
```

---

## SSL certificate renewal

<include only if domain was configured>

```bash
sudo systemctl status certbot.timer
sudo certbot renew --dry-run
```

---

## Backup

### What to back up
- `~/.openclaw/openclaw.json` — full config (contains API key and bot tokens — handle securely)
- `~/.openclaw/workspace/IDENTITY.md` — assistant persona
- `~/.openclaw/workspace/USER.md` — user profile
- `~/.openclaw/workspace/SOUL.md` — assistant values
- `~/openclaw/system-prompt.md` — system prompt source (if created)
- `~/openclaw/workflows.md` — scheduled workflows (if configured)

### Backup command
```bash
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/openclaw.json \
  ~/.openclaw/workspace/IDENTITY.md \
  ~/.openclaw/workspace/USER.md \
  ~/.openclaw/workspace/SOUL.md \
  ~/openclaw/system-prompt.md \
  ~/openclaw/workflows.md \
  2>/dev/null
```

Store off-machine — external drive or encrypted cloud storage.

### Restore (on fresh machine after skills 02–03)
```bash
tar -xzf openclaw-backup-YYYYMMDD.tar.gz -C ~/
chmod 600 ~/.openclaw/openclaw.json
systemctl --user restart openclaw-gateway
```

---

## Troubleshooting

| Symptom | First check |
|---|---|
| Bot not responding | `systemctl --user status openclaw-gateway` — is it active? |
| Gateway not starting | `journalctl --user -u openclaw-gateway -n 50` |
| Telegram 401 error | Token revoked — get new token from @BotFather, run `openclaw config set channels.telegram.botToken <token>`, restart |
| Dashboard not opening | `export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh" && openclaw gateway url` |
| Bot responds but ignores commands | Check if pairing approved: `openclaw pairing list` |
| nvm / openclaw not found | Run `export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"` first |
| Google integration fails | `token.json` expired — delete `~/.openclaw/token.json`, re-run `openclaw auth google` |
| High CPU/temp | `sensors`, reduce `gateway.max_concurrent_tasks` |

---

## Key file locations

| File | Purpose |
|---|---|
| `~/.openclaw/openclaw.json` | Main config (API keys, bot tokens, gateway settings) |
| `~/.openclaw/workspace/IDENTITY.md` | Assistant persona and behavior rules |
| `~/.openclaw/workspace/USER.md` | User profile |
| `~/.openclaw/workspace/SOUL.md` | Core behavioral values |
| `~/.config/systemd/user/openclaw-gateway.service` | Systemd user service unit |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Daily log file |

---

## Installed integrations

<list each integration verified in skill 04>

## Installed skills

<list each skill installed in skill 06>

## Scheduled workflows

<list from workflows.md, or "none">

---

## Resources

- OpenClaw docs: https://docs.openclaw.ai
- Troubleshooting: https://docs.openclaw.ai/troubleshooting
- Journey kit: https://www.journeykits.ai (openclaw-install)
```

---

## Final verification

Run through this checklist. Paste output or confirm verbally:

- [ ] `systemctl --user status openclaw-gateway` shows `active (running)`
- [ ] `loginctl show-user $USER | grep Linger` returns `Linger=yes`
- [ ] Send a test message via primary messaging platform — response received
- [ ] `sensors` baseline within acceptable range (fanless hardware)
- [ ] `~/openclaw/runbook.md` written — paste `ls -la ~/openclaw/`
- [ ] Backup created and stored off-machine
- [ ] User knows how to restart the gateway
- [ ] User knows how to view logs
- [ ] User knows how to update OpenClaw

---

## Congratulations

OpenClaw is installed, integrated, hardened, and documented.

**Natural next step**: Install `keylimeaistudios/ai-employee-starter` from the Journey registry to turn your assistant into a structured AI employee with morning briefings, health monitoring, and daily reporting.

---

**Phase 7 complete. Installation complete.**

Everything is documented in `~/openclaw/runbook.md`. Reach out to the OpenClaw community if you hit issues in day-to-day use.
