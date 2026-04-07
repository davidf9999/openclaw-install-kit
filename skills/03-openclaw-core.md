# Skill 03 — OpenClaw Core Install

**Purpose**: Install OpenClaw, configure the gateway with API keys, register as a systemd daemon, and verify it responds.

**Input**: `deployment-brief.md`, verified infra from skill 02  
**Output**: Running OpenClaw systemd service, verified responsive, `~/openclaw/.env` in place

---

## Instructions

All commands run on the target machine in `~/openclaw`.

---

## Step 1 — Install OpenClaw

```bash
cd ~/openclaw
npm install -g openclaw
openclaw --version   # verify install
```

---

## Step 2 — Run onboard

The onboard wizard collects your API keys, configures the gateway, and registers OpenClaw as a **systemd service** so it survives reboots. Do not pass keys as CLI arguments.

```bash
openclaw onboard --install-daemon
```

During onboard you will be prompted for:
- **LLM provider**: select per `deployment-brief.md` (Anthropic recommended)
- **API key**: paste when prompted — it will not echo to screen
- **Model**: `claude-sonnet-4-6` is a good default; use `claude-opus-4-6` for maximum quality
- **Gateway port**: accept default (usually 3000) unless it conflicts
- **Daemon install**: confirm yes — this registers the systemd unit

---

## Step 3 — Verify systemd service

```bash
sudo systemctl status openclaw
```

Expected: `active (running)`. If not, check:
```bash
sudo journalctl -u openclaw -n 50
```

Enable on boot (should already be done by onboard, but verify):
```bash
sudo systemctl is-enabled openclaw   # should print "enabled"
```

---

## Step 4 — Verify .env

```bash
ls -la ~/openclaw/.env       # must exist
stat ~/openclaw/.env         # check permissions
```

If permissions are not 600, fix immediately:
```bash
chmod 600 ~/openclaw/.env
```

Do not print or cat the .env file.

---

## Step 5 — Verify gateway responds

```bash
curl -s http://localhost:3000/health
```

Expected: `{"status":"ok"}` or similar. Adjust port if you changed it during onboard.

---

## Step 6 — Check logs

```bash
sudo journalctl -u openclaw -n 50 --no-pager
```

Look for:
- `Gateway started on port XXXX`
- No `ERROR` or `FATAL` lines

If errors appear, note them and consult the openclaw docs before continuing.

---

## Completion check

Before marking this phase done:
- [ ] `openclaw --version` returns a version
- [ ] `sudo systemctl status openclaw` shows `active (running)`
- [ ] `sudo systemctl is-enabled openclaw` returns `enabled`
- [ ] `curl http://localhost:3000/health` returns a healthy response
- [ ] `~/openclaw/.env` exists with permissions 600
- [ ] No fatal errors in `journalctl -u openclaw`
