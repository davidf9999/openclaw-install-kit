# Skill 05 — Security Hardening

**Purpose**: Harden the OpenClaw installation — firewall audit, credential hygiene, access control, and secrets check.

**Input**: Running OpenClaw with integrations (from skill 04)  
**Output**: Completed security checklist, all findings resolved or explicitly accepted

---

## Instructions

Work through each section. For each finding, either fix it or document why it is acceptable (note in the checklist). Do not skip sections.

---

## Step 1 — Firewall audit

```bash
sudo ufw status verbose
```

Verify only necessary ports are open:
- SSH (22 or custom port)
- 80/tcp (for certbot renewal challenge)
- 443/tcp (if using webhooks)
- OpenClaw gateway port (if exposing externally — evaluate if this is necessary)

Close anything else:
```bash
sudo ufw deny <port>    # close any unexpected open ports
```

If SSH is on default port 22 and the machine is internet-facing, consider changing it:
```bash
sudo nano /etc/ssh/sshd_config   # change Port to e.g. 2222
sudo ufw allow 2222/tcp
sudo ufw delete allow ssh
sudo systemctl restart sshd
```

---

## Step 2 — Credential audit

```bash
# Check .env permissions
stat ~/openclaw/.env
# Expected: mode 600, owned by your user

# Check for keys in shell history
grep -i 'api.key\|token\|secret\|password' ~/.bash_history | head -20
```

If any secrets appear in bash history:
```bash
history -c && history -w    # clear history
```

Check no secrets are in the systemd service environment:
```bash
sudo systemctl show openclaw | grep -i env
```

Secrets should not appear in the service environment. If they do, move them to `.env` and update OpenClaw config to read from file.

---

## Step 3 — File permissions

```bash
# Core files should not be world-readable
chmod 600 ~/openclaw/.env
chmod 600 ~/openclaw/credentials.json 2>/dev/null || true
chmod 600 ~/openclaw/token.json 2>/dev/null || true
chmod 700 ~/openclaw

# Verify
ls -la ~/openclaw/
```

---

## Step 4 — Fail2ban (internet-facing machines only)

Skip if machine is on a local network only.

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo fail2ban-client status sshd
```

---

## Step 5 — SSH hardening (internet-facing machines only)

```bash
sudo nano /etc/ssh/sshd_config
```

Ensure these are set:
```
PermitRootLogin no
PasswordAuthentication no    # only if you have SSH key auth set up
PubkeyAuthentication yes
MaxAuthTries 3
```

```bash
sudo systemctl restart sshd
```

**Warning**: Do not disable `PasswordAuthentication` unless you have confirmed your SSH key works in a separate session first.

---

## Step 6 — Webhook endpoint review (if applicable)

If any integrations use public webhook endpoints:

```bash
# List any ports OpenClaw is listening on externally
ss -tlnp | grep openclaw
```

Verify each exposed endpoint:
- Requires a secret/verify token (not open to the public)
- Is behind SSL (HTTPS only)
- Has rate limiting configured (check OpenClaw gateway settings)

---

## Step 7 — Thermal check (fanless hardware)

If `Fanless: yes` in deployment-brief.md:

```bash
sensors
```

Record baseline temperature under load:
```bash
# Run a short load test
stress-ng --cpu 2 --timeout 30s &
watch -n2 sensors
```

If temps exceed 85°C under load, configure OpenClaw to limit concurrent agent tasks:
```bash
openclaw config set gateway.max_concurrent_tasks 2
sudo systemctl restart openclaw
```

---

## Completion checklist

- [ ] Firewall: only necessary ports open
- [ ] `.env` permissions: 600
- [ ] No secrets in bash history or PM2 env
- [ ] `credentials.json` / `token.json` permissions: 600 (if applicable)
- [ ] Fail2ban active (internet-facing only)
- [ ] SSH hardened (internet-facing only)
- [ ] Webhook endpoints require verify tokens
- [ ] Thermal baseline recorded (fanless hardware only)

Document any accepted risks with a brief rationale.
