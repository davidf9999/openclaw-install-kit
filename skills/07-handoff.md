# Skill 07 — Handoff

**Purpose**: Produce a `runbook.md` covering ongoing operations, and confirm the installation is complete.

**Input**: Completed installation (skills 01–06), `deployment-brief.md`  
**Output**: `~/openclaw/runbook.md`, final verification, summary of what was installed

---

## Instructions

Generate `runbook.md` by filling in the template below using information gathered throughout the install. Then run the final verification checklist.

---

## Generate runbook.md

Write this file to `~/openclaw/runbook.md`:

```markdown
# OpenClaw Runbook

Generated: <date>
Machine: <from deployment-brief>
OpenClaw version: <openclaw --version>

---

## Daily operations

### Check status
```bash
sudo systemctl status openclaw
sudo journalctl -u openclaw -n 50 --no-pager
```

### Restart OpenClaw
```bash
sudo systemctl restart openclaw
```

### Stop / Start
```bash
sudo systemctl stop openclaw
sudo systemctl start openclaw
```

---

## Updates

### Update OpenClaw
```bash
npm update -g openclaw
pm2 restart openclaw
openclaw --version
```

### Update skills
```bash
clawdhub update --all
pm2 restart openclaw
```

---

## Temperature monitoring (fanless hardware)

<include only if Fanless: yes in deployment-brief>

Check temps:
```bash
sensors
```

If consistently above 80°C under load:
- Reduce `gateway.max_concurrent_tasks` to 1
- Consider adding a small USB fan

---

## SSL certificate renewal

<include only if domain was configured>

Certbot renews automatically via systemd timer. To check:
```bash
sudo systemctl status certbot.timer
sudo certbot renew --dry-run
```

---

## Backup

### What to back up
- `~/openclaw/.env`
- `~/openclaw/system-prompt.md`
- `~/openclaw/credentials.json` (if Google integration)
- `~/openclaw/token.json` (if Google integration)
- `~/openclaw/workflows.md` (if scheduled workflows configured)

### Backup command
```bash
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz \
  ~/openclaw/.env \
  ~/openclaw/system-prompt.md \
  ~/openclaw/workflows.md \
  ~/openclaw/credentials.json \
  ~/openclaw/token.json \
  2>/dev/null
```

Store this file off-machine (external drive, encrypted cloud storage).

---

## Restore

```bash
# On a fresh machine after completing skills 02 and 03:
tar -xzf openclaw-backup-YYYYMMDD.tar.gz -C ~/
chmod 600 ~/openclaw/.env ~/openclaw/credentials.json ~/openclaw/token.json 2>/dev/null
pm2 restart openclaw
```

---

## Troubleshooting

| Symptom | First check |
|---|---|
| Bot not responding | `sudo systemctl status openclaw` — is it active? |
| Auth errors in logs | API key expired? Check `journalctl -u openclaw -n 50` |
| High CPU/temp | `sensors`, reduce `max_concurrent_tasks` |
| Google integration fails | `token.json` may be expired — re-run `openclaw auth google` |
| Telegram webhook not working | SSL cert valid? `curl https://<domain>/health` |

---

## Installed skills

<list each skill installed in skill 06>

---

## Scheduled workflows

<list from workflows.md, or "none">

---

## Contacts / resources

- OpenClaw docs: https://docs.openclaw.ai
- OpenClaw community: https://openclaw.ai/community
- This installation was guided by: https://www.journeykits.ai (openclaw-install kit)
```

---

## Final verification

Run through this checklist with the user present:

- [ ] `pm2 status` shows `openclaw` as `online`
- [ ] Send a test message via primary messaging platform — response received
- [ ] `sensors` baseline recorded and within acceptable range (fanless hardware)
- [ ] `runbook.md` written and readable
- [ ] Backup created and stored off-machine
- [ ] User knows how to restart the daemon
- [ ] User knows how to check logs
- [ ] User knows how to update OpenClaw

---

## Congratulations

OpenClaw is installed, integrated, hardened, and documented. 

**Natural next step**: Install `keylimeaistudios/ai-employee-starter` from the Journey registry to turn your OpenClaw agent into a structured AI employee with morning briefings, health monitoring, and daily reporting.

```bash
# From within OpenClaw or Claude Code:
# journey install keylimeaistudios/ai-employee-starter --target openclaw
```
