# Skill 03 — OpenClaw Core Install

**Purpose**: Install OpenClaw, configure the gateway with API keys, register as a systemd daemon, and verify it responds.

**Input**: `deployment-brief.md`, verified infra from skill 02  
**Output**: Running OpenClaw systemd service, verified responsive, `~/openclaw/.env` in place

> **Phase 3 of 7 — OpenClaw Core Install**  
> Re-read `deployment-brief.md` before starting. All commands run in your terminal inside `~/openclaw`.  
> Paste each output back here so I can verify before moving to the next step.  
> If you are re-entering this phase, say "resuming Phase 3" and paste `sudo systemctl status openclaw`.

---

## Step 1 — Install OpenClaw

```bash
cd ~/openclaw
npm install -g openclaw
openclaw --version
```

Paste the output. I need to see a version number before we continue.

---

## Step 2 — Run onboard

The onboard wizard collects your API keys, configures the gateway, and registers OpenClaw as a **systemd service** so it survives reboots.

```bash
openclaw onboard --install-daemon
```

You will be prompted interactively for:
- **LLM provider**: select per `deployment-brief.md` (Anthropic recommended)
- **API key**: paste when prompted — it will not echo to screen. Do not pass it as a CLI argument.
- **Model**: `claude-sonnet-4-6` is a good default; `claude-opus-4-6` for maximum quality
- **Gateway port**: accept the default (usually 3000) unless it conflicts with something already running
- **Daemon install**: confirm yes — this registers the systemd unit

When onboard finishes, tell me what it printed at the end.

---

## Step 3 — Verify systemd service

```bash
sudo systemctl status openclaw
```

Paste the output. Expected: `active (running)`. If not, also paste:

```bash
sudo journalctl -u openclaw -n 50 --no-pager
```

Then verify it is enabled on boot:

```bash
sudo systemctl is-enabled openclaw
```

Expected output: `enabled`

---

## Step 4 — Verify .env

```bash
ls -la ~/openclaw/.env
```

Paste the output. The file must exist and show permissions `600`. If permissions are not `600`:

```bash
chmod 600 ~/openclaw/.env
```

Do not print or `cat` the `.env` file — it contains your API key.

---

## Step 5 — Verify gateway responds

```bash
curl -s http://localhost:3000/health
```

Paste the output. Expected: `{"status":"ok"}` or similar healthy response. Adjust the port number if you changed it during onboard.

---

## Step 6 — Check logs

```bash
sudo journalctl -u openclaw -n 50 --no-pager
```

Paste the output. Look for:
- A line like `Gateway started on port XXXX`
- No `ERROR` or `FATAL` lines

If errors appear, share them here before continuing.

---

## Completion check

Confirm each by pasting command output:

- [ ] `openclaw --version` returns a version
- [ ] `sudo systemctl status openclaw` shows `active (running)`
- [ ] `sudo systemctl is-enabled openclaw` returns `enabled`
- [ ] `curl http://localhost:3000/health` returns a healthy response
- [ ] `ls -la ~/openclaw/.env` shows the file exists with permissions `600`
- [ ] No fatal errors in `journalctl -u openclaw`

---

**Phase 3 complete.**

Once all checks pass, say: *"OpenClaw is running. Type `continue` when you're ready to start Phase 4 — Integrations."*
