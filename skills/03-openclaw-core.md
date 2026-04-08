# Skill 03 — OpenClaw Core Install

**Purpose**: Install OpenClaw, configure the gateway with API keys, register as a systemd daemon, and verify it responds.

**Input**: `deployment-brief.md`, verified infra from skill 02  
**Output**: Running OpenClaw user systemd service, verified responsive, dashboard accessible

> **Phase 3 of 8 — OpenClaw Core Install**  
> Re-read `deployment-brief.md` before starting.  
> You will run all commands yourself in your terminal. Paste each output back here so I can verify before moving to the next step.  
> If you are re-entering this phase, say "resuming Phase 3" and paste `systemctl --user status openclaw-gateway`.

---

## Important: load nvm before every openclaw command

OpenClaw is installed via nvm's Node 24. In any new terminal session, run this first:

```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
```

You only need to do this once per terminal session. All openclaw commands below assume nvm is loaded.

---

## Step 1 — Install OpenClaw

> **No account required**: OpenClaw is installed as an npm package and connects directly to your LLM provider API key. You do not need to register or create an OpenClaw account.

```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
npm install -g openclaw
openclaw --version
```

Paste the output. I need to see a version number before we continue.

> **Version note**: This kit was developed and tested against OpenClaw **2026.4.5**. If your version differs, things will likely still work, but flag any unexpected behavior — it may indicate a version mismatch.

---

## Step 2 — Run onboard

The onboard wizard collects your API keys, configures the gateway, and registers OpenClaw as a **user-level systemd service**.

```bash
openclaw onboard --install-daemon
```

**QuickStart flow** — when prompted, choose:
- **Setup mode**: QuickStart (configure details later)
- **Channel**: Telegram (Bot API) — simplest starting point
- **Telegram bot token**: paste your token from @BotFather
  - ⚠️ Copy the token text directly from the BotFather chat message — do NOT use the copy button (clipboard issues on some systems)
  - ⚠️ Paste ONLY the token (e.g. `123456789:ABCdef...`) — do not include the bot username
- **DM policy warning**: noted — you will lock it down via pairing after install
- **Web search provider**: Skip for now
- **Hooks**: Skip for now

Do not pass your API key as a CLI argument — paste it when prompted interactively.

When onboard finishes, tell me what it printed at the end.

---

## Step 3 — Verify user systemd service

OpenClaw registers as a **user-level** service, not a system service. Always use `systemctl --user`:

```bash
systemctl --user status openclaw-gateway
```

Paste the output. Expected: `active (running)`.

If not running, check logs:
```bash
journalctl --user -u openclaw-gateway -n 50 --no-pager
```

Verify it starts on boot:
```bash
systemctl --user is-enabled openclaw-gateway
```

Expected: `enabled`

Also enable **linger** so the service starts at boot even before you log in:
```bash
sudo loginctl enable-linger $USER
```

---

## Step 4 — Verify config file permissions

OpenClaw stores config (including your API key) in `~/.openclaw/openclaw.json`:

```bash
stat ~/.openclaw/openclaw.json
ls -la ~/.openclaw/
```

Paste the output. Expected: `~/.openclaw/openclaw.json` with mode `600`, `~/.openclaw/` directory with mode `700`.

If not `600`:
```bash
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw
```

Do not `cat` the config file — it contains your API key.

---

## Step 5 — Get dashboard URL and verify gateway

The gateway port is assigned dynamically (not always 3000). Get the correct URL:

```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw gateway url
```

This opens the dashboard in your browser and prints the tokenized URL. **Bookmark this URL** — you'll use it to access the dashboard going forward.

Paste the URL printed (it's safe to share — it's a local URL).

---

## Step 6 — Check logs

```bash
cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -30
```

Paste the output. Look for:
- A line like `starting channels and sidecars`
- No `ERROR` or `FATAL` lines

---

## Completion check

Confirm each by pasting command output:

- [ ] `openclaw --version` returns a version
- [ ] `systemctl --user status openclaw-gateway` shows `active (running)`
- [ ] `systemctl --user is-enabled openclaw-gateway` returns `enabled`
- [ ] `loginctl show-user $USER | grep Linger` returns `Linger=yes`
- [ ] `openclaw gateway url` opens dashboard successfully
- [ ] `~/.openclaw/openclaw.json` exists with permissions `600`
- [ ] `~/.openclaw/` has permissions `700`
- [ ] No fatal errors in today's log file

---

**Phase 3 complete.**

Once all checks pass, say: *"OpenClaw is running. Type `continue` when you're ready to start Phase 4 — Integrations."*
