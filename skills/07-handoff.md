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

Generate `runbook.md` by filling in the template below. Use `deployment-brief.md` and information gathered during the install to fill all placeholders. Then run the backup step and final verification checklist — in that order.

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

| Path | Contents | Notes |
|---|---|---|
| `~/.openclaw/openclaw.json` | API keys, bot tokens, all config | Sensitive — never commit or share |
| `~/.openclaw/workspace/` | IDENTITY.md, USER.md, SOUL.md | Assistant persona and user profile |
| `~/.openclaw/agents/main/sessions/` | Full chat history (`.jsonl` files) | Optional — can be large; contains conversation content |
| `~/openclaw/system-prompt.md` | System prompt source | If created in Phase 6 |
| `~/openclaw/workflows.md` | Scheduled workflows | If configured |

**Chat sessions note**: sessions contain the full conversation history with your assistant. Including them means you can restore continuity after a hardware failure. Excluding them makes the backup smaller. Decide based on privacy preference and available storage.

### Run the backup now

```bash
# With chat sessions (recommended):
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/openclaw.json \
  ~/.openclaw/workspace/ \
  ~/.openclaw/agents/main/sessions/ \
  ~/openclaw/system-prompt.md \
  ~/openclaw/workflows.md \
  2>/dev/null

# Without chat sessions:
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/openclaw.json \
  ~/.openclaw/workspace/ \
  ~/openclaw/system-prompt.md \
  ~/openclaw/workflows.md \
  2>/dev/null

echo "Backup size: $(du -sh ~/openclaw-backup-$(date +%Y%m%d).tar.gz)"
```

Paste the output — confirm the file was created and the size looks reasonable.

### Copy off-machine (do this now, not later)

Choose one of the following:

```bash
# Option A — USB drive (replace /media/yourname/drive with your mount point):
cp ~/openclaw-backup-$(date +%Y%m%d).tar.gz /media/$USER/*/

# Option B — another machine on your network via scp:
scp ~/openclaw-backup-$(date +%Y%m%d).tar.gz user@192.168.x.x:~/backups/

# Option C — cloud storage via rclone (install: sudo apt install rclone, then rclone config):
rclone copy ~/openclaw-backup-$(date +%Y%m%d).tar.gz remote:backups/

# Option D — private GitHub repo (config only, no sessions — never push openclaw.json to a public repo):
# Not recommended for openclaw.json — use options A–C for the encrypted archive instead
```

If none of these are set up yet, copy to a USB drive now and set up rclone later. The backup file is useless if it lives only on the machine it's meant to protect.

### Restore (on fresh machine after Phases 2–3)
```bash
tar -xzf openclaw-backup-YYYYMMDD.tar.gz -C ~/
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw
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
| LLM API call fails / no response | Check API key in `~/.openclaw/openclaw.json`; check provider status page; check spend limits on your API account |
| Disk filling up | `du -sh ~/.openclaw/agents/main/sessions/` — prune old session `.jsonl` files (see Log rotation section) |

---

## Log rotation

Logs are written to `/tmp/openclaw/` as daily files (`openclaw-YYYY-MM-DD.log`). Files in `/tmp` are cleared on reboot. Chat sessions accumulate in `~/.openclaw/agents/main/sessions/` as `.jsonl` files and are not automatically pruned.

To check current log and session sizes:
```bash
du -sh /tmp/openclaw/
du -sh ~/.openclaw/agents/main/sessions/
```

To prune old session files (keeps last 30 days):
```bash
find ~/.openclaw/agents/main/sessions/ -name "*.jsonl" -mtime +30 -delete
```

No automatic log rotation is configured by default. If you are running long-term and disk space is a concern, add a cron job or logrotate rule.

---

## Uninstall

To remove OpenClaw from this machine:

```bash
# Stop and disable the service
systemctl --user stop openclaw-gateway
systemctl --user disable openclaw-gateway

# Disable linger (if set)
sudo loginctl disable-linger $USER

# Remove the npm package
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
npm uninstall -g openclaw

# Remove config and workspace (IRREVERSIBLE — back up first)
# rm -rf ~/.openclaw/

# Remove the systemd unit file if it was not removed by npm uninstall
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

**Before uninstalling**: revoke all tokens you issued (Telegram bot token via @BotFather, WhatsApp session, Slack tokens, GitHub token, Google OAuth via myaccount.google.com → Security → Third-party access). Tokens left active can still be used even after the software is removed.

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
- [ ] Backup archive created — paste `ls -lh ~/openclaw-backup-*.tar.gz`
- [ ] Backup copied off-machine (USB, scp, or rclone) — confirm destination
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
