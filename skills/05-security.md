# Skill 05 — Security Hardening

**Purpose**: Harden the OpenClaw installation — firewall audit, credential hygiene, access control, and secrets check.

**Input**: Running OpenClaw with integrations (from skill 04)  
**Output**: Completed security checklist, all findings resolved or explicitly accepted

> **Phase 5 of 8 — Security Hardening**  
> Re-read `deployment-brief.md` before starting. Adapt steps based on whether the machine is internet-facing.  
> Run each command, paste the output, and I will tell you what to fix before we continue.  
> If you are re-entering this phase, say "resuming Phase 5."

---

## Instructions

Work through each section. For each finding, either fix it or document why it is acceptable. Do not skip sections.

---

## Step 1 — Firewall audit

```bash
sudo ufw status verbose
```

Paste the output. Verify only necessary ports are open:
- SSH (22 or your custom port)
- 80/tcp (certbot renewal challenge, only if you have a domain)
- 443/tcp (webhooks, only if you have a domain)
- OpenClaw gateway port — evaluate whether it needs to be exposed externally at all

Close anything unexpected:
```bash
sudo ufw deny <port>
```

If SSH is on default port 22 and the machine is internet-facing, consider changing it:
```bash
sudo nano /etc/ssh/sshd_config   # change Port to e.g. 2222
sudo ufw allow 2222/tcp
sudo ufw delete allow ssh
sudo systemctl restart sshd
```

**Warning**: Open a second SSH session to verify the new port works before closing your current one.

---

## Step 2 — Credential audit

OpenClaw stores config (including API keys and tokens) in `~/.openclaw/openclaw.json`, not a `.env` file.

```bash
stat ~/.openclaw/openclaw.json
```

Paste the output. Expected: mode `600`, owned by your user. If not `600`:
```bash
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw
```

Check for secrets in shell history:
```bash
grep -i 'api.key\|token\|secret\|password' ~/.bash_history | head -20
```

Paste the output. If any secrets appear, clear history:
```bash
history -c && history -w
```

Check no secrets are in the systemd service environment:
```bash
systemctl --user show openclaw-gateway | grep -i env
```

Paste the output. Secrets should not appear here. If they do, they were passed as CLI arguments or environment variables at startup — remove them from the service unit and ensure all secrets are stored only in `~/.openclaw/openclaw.json`.

---

## Step 3 — File permissions

OpenClaw config lives in `~/.openclaw/` (with the dot — distinct from `~/openclaw/` which is your working directory).

```bash
chmod 600 ~/.openclaw/credentials.json 2>/dev/null || true
chmod 600 ~/.openclaw/token.json 2>/dev/null || true
chmod 700 ~/.openclaw
ls -la ~/.openclaw/
```

Paste the `ls -la` output. `openclaw.json` should show `600`, the directory `700`. `credentials.json` and `token.json` appear only if Google integration was configured.

---

## Step 4 — Fail2ban (internet-facing machines only)

Skip this step if the machine is on a local network only (not reachable from the internet).

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo fail2ban-client status sshd
```

Paste the `fail2ban-client status sshd` output.

---

## Step 5 — SSH hardening (internet-facing machines only)

Skip if local network only.

```bash
sudo nano /etc/ssh/sshd_config
```

Ensure these are set:
```
PermitRootLogin no
PasswordAuthentication no    # only set this if you have confirmed SSH key auth works
PubkeyAuthentication yes
MaxAuthTries 3
```

```bash
sudo systemctl restart sshd
```

**Warning**: Do not disable `PasswordAuthentication` unless you have confirmed your SSH key works in a separate session first.

---

## Step 6 — Webhook endpoint review (if applicable)

Skip if `Domain: none` in deployment-brief.md.

```bash
ss -tlnp | grep openclaw
```

Paste the output. For each exposed endpoint, verify:
- Requires a secret/verify token (not open to the public)
- Is behind SSL (HTTPS only)
- Rate limiting is configured in OpenClaw gateway settings

---

## Step 7 — Thermal check (fanless hardware only)

Skip if `Fanless: no` in deployment-brief.md.

```bash
sensors
```

Paste the output. Then run a short load test:

```bash
stress-ng --cpu 2 --timeout 30s
```

While it runs (or immediately after), paste:
```bash
sensors
```

If temps exceeded 85°C under load, configure OpenClaw to limit concurrent tasks:
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw config set gateway.max_concurrent_tasks 2
systemctl --user restart openclaw-gateway
```

Record the peak temperature observed.

---

## Completion checklist

Confirm each item and paste any outstanding command output:

- [ ] Firewall: only necessary ports open — paste `sudo ufw status verbose`
- [ ] `~/.openclaw/openclaw.json` permissions: 600 — paste `stat ~/.openclaw/openclaw.json`
- [ ] No secrets in bash history — paste grep output
- [ ] No secrets in systemd env — paste `systemctl --user show openclaw-gateway | grep -i env`
- [ ] `credentials.json` / `token.json` permissions: 600 (if applicable)
- [ ] Fail2ban active (internet-facing only)
- [ ] SSH hardened (internet-facing only)
- [ ] Webhook endpoints require verify tokens (if applicable)
- [ ] Thermal baseline recorded (fanless hardware only)

Document any accepted risks with a brief rationale before continuing.

---

**Phase 5 complete.**

Once all checklist items are confirmed or explicitly accepted, say: *"Security hardening done. Type `continue` when you're ready to start Phase 6 — Optimization."*
