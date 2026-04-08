# Skill 04 — Integrations

**Purpose**: Connect OpenClaw to the messaging platforms and services chosen during discovery.

**Input**: `deployment-brief.md`, running OpenClaw daemon (from skill 03)  
**Output**: Each chosen platform verified as sending/receiving messages through OpenClaw

> **Phase 4 of 8 — Integrations**  
> Re-read `deployment-brief.md` before starting. Only set up platforms listed there — do not prompt the user to add more.  
> You will run all commands yourself. Paste each output back here so I can verify before we continue.  
> If you are re-entering this phase, say "resuming Phase 4" and tell me which integrations are already working.

---

## Instructions

Load nvm before running any openclaw commands:
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
```

Only set up platforms listed in `deployment-brief.md`. Skip all other sections.

Always start with Telegram (simplest, no SSL required in long-poll mode). Add others only after Telegram is verified working.

After every `openclaw config set` block, restart the daemon:
```bash
systemctl --user restart openclaw-gateway
```

---

## Telegram (start here)

Telegram is configured during onboard (skill 03). If you completed QuickStart onboard with a Telegram token, skip to **Verify** below.

### If Telegram was not set up during onboard

1. Open Telegram → search `@BotFather` → send `/newbot`
2. Follow prompts → get your **Bot Token**
   - ⚠️ Copy the token text directly from the BotFather chat — do NOT use the copy button
   - ⚠️ Paste ONLY the token (e.g. `123456789:ABCdef...`) — not the bot username

```bash
read -rsp $'Paste bot token (input hidden, press Enter):\n' TG_TOKEN && printf '\n'
openclaw config set channels.telegram.botToken "$TG_TOKEN"
unset TG_TOKEN && history -c && history -w
systemctl --user restart openclaw-gateway
```

### Verify Telegram is connected

Check channel status:
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw status --deep 2>&1 | grep -A1 Telegram
```

Paste the output. Look for `Telegram │ OK` in the deep probe section. If you see `401 Unauthorized`, the token is wrong — go to @BotFather → `/mybots` → your bot → **API Token** → **Revoke current token** → get a new one and re-run `openclaw config set`.

### Pair with the bot

Send any message to your bot in Telegram. It will respond with a **pairing request**. Approve it:

```bash
openclaw pairing approve telegram <code-shown-in-bot-message>
```

After pairing, the bot will respond to your messages. Send "hello" to confirm.

### Lock down DM access (recommended)

By default, any Telegram user who finds your bot can send pairing requests. Restrict it to yourself:

```bash
openclaw config set channels.telegram.dmPolicy allowlist
openclaw config set channels.telegram.allowFrom '["YOUR_TELEGRAM_USER_ID"]'
systemctl --user restart openclaw-gateway
```

To find your Telegram user ID: message @userinfobot in Telegram.

---

## WhatsApp (if selected — complex, do after Telegram)

Check `deployment-brief.md` for which WhatsApp path was chosen during discovery. The two paths are completely different.

---

### Path A — Personal number (whatsapp-web.js bridge)

Uses your existing WhatsApp account. No Meta approval needed. Requires a public HTTPS URL for the webhook — use Cloudflare Tunnel if you have no domain.

> ⚠️ Less stable than the API path — may break on WhatsApp updates. Requires keeping a browser session alive. Fine for personal use.

**Step 1 — Install Cloudflare Tunnel** (skip if you already have a domain + SSL):
```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o /tmp/cloudflared.deb
sudo dpkg -i /tmp/cloudflared.deb
cloudflared tunnel --url http://localhost:18789
```
Note the `https://something.trycloudflare.com` URL — you'll need it below.

**Step 2 — Configure OpenClaw WhatsApp bridge:**
```bash
openclaw config set whatsapp.mode bridge
openclaw config set whatsapp.webhook_url https://<your-tunnel-or-domain>/webhooks/whatsapp
systemctl --user restart openclaw-gateway
```

**Step 3 — Scan QR code:**
```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw whatsapp qr
```
Scan the QR code with your phone's WhatsApp (Linked Devices → Link a Device).

**Step 4 — Verify:**
Send yourself a WhatsApp message. Gordo should respond.

---

### Path B — Separate/business number (Meta Business API)

> ⚠️ Requires a public HTTPS endpoint and Meta Business API approval (1–3 days).  
> ⚠️ **This path has not been tested in this kit.** The instructions below are based on Meta's documentation. If you encounter issues, please open an issue with your output — your report will help validate this path.

**Pre-flight checklist — confirm before starting:**
- [ ] Meta app created at developers.facebook.com with WhatsApp product added
- [ ] App has been approved for the WhatsApp Business API (check App Dashboard → Status)
- [ ] You have a **Phone Number ID** (not the phone number itself — a numeric ID from the API setup)
- [ ] You have a **Permanent Access Token** (not a temporary token — generate a System User token)
- [ ] You have a public HTTPS domain for the webhook (required; Meta will not accept IP addresses or HTTP)

If any of these are not in place, stop here — the integration will not work until they are.

1. Go to developers.facebook.com → Create a new app → Add the WhatsApp product
2. Get your **Phone Number ID** and **Permanent Access Token**
3. Set a webhook URL: `https://<your-domain>/webhooks/whatsapp`

```bash
openclaw config set whatsapp.phone_number_id <id>
read -rsp $'Paste Access Token (input hidden, press Enter):\n' WA_TOKEN && printf '\n'
openclaw config set whatsapp.access_token "$WA_TOKEN"
read -rsp $'Choose a webhook verify token (input hidden, press Enter):\n' WA_VERIFY && printf '\n'
openclaw config set whatsapp.webhook_verify_token "$WA_VERIFY"
unset WA_TOKEN WA_VERIFY && history -c && history -w
systemctl --user restart openclaw-gateway
```

Register the webhook in the Meta dashboard using the verify token you chose.

Check logs after restarting:
```bash
cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -30
```

---

## Slack (if selected)

1. Go to api.slack.com/apps → Create New App → **From scratch**
2. Enable **Socket Mode** (avoids need for a public URL)
3. Add OAuth scopes: `chat:write`, `im:history`, `im:read`
4. Install to workspace → get **Bot Token** (`xoxb-...`) and **App-Level Token** (`xapp-...`)

```bash
read -rsp $'Paste Bot Token (xoxb-..., input hidden):\n' SLACK_BOT && printf '\n'
openclaw config set slack.bot_token "$SLACK_BOT"
read -rsp $'Paste App Token (xapp-..., input hidden):\n' SLACK_APP && printf '\n'
openclaw config set slack.app_token "$SLACK_APP"
unset SLACK_BOT SLACK_APP && history -c && history -w
systemctl --user restart openclaw-gateway
```

Send a DM to your bot in Slack to verify.

---

## Email — IMAP/SMTP (if selected)

Use an app-specific password if using Gmail or Outlook — not your main account password.

```bash
openclaw config set email.imap_host <host>
openclaw config set email.imap_port 993
openclaw config set email.smtp_host <host>
openclaw config set email.smtp_port 587
openclaw config set email.username <your-address>
read -rsp $'Paste app password (input hidden, press Enter):\n' EMAIL_PASS && printf '\n'
openclaw config set email.password "$EMAIL_PASS"
unset EMAIL_PASS && history -c && history -w
systemctl --user restart openclaw-gateway
```

---

## Google Workspace — Calendar and Contacts (if selected)

**Only proceed if listed in `deployment-brief.md`. Enable only the specific APIs selected.**

1. Go to console.cloud.google.com → Create a new project
2. Enable APIs: **Google Calendar API**, **People API** (for Contacts) — only these unless brief says otherwise
3. Create **OAuth 2.0 credentials** → Application type: Desktop app
4. Download `credentials.json` → place in `~/.openclaw/`

```bash
chmod 600 ~/.openclaw/credentials.json
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw auth google
```

A browser window will open. Authorize the requested scopes. A `token.json` will be saved to `~/.openclaw/`.

```bash
chmod 600 ~/.openclaw/token.json
systemctl --user restart openclaw-gateway
```

Test via the dashboard or Telegram:
> "What's on my calendar today?"

**Common failure**: If calendar access fails, return to GCP console, verify the APIs are enabled, delete `~/.openclaw/token.json`, and re-run `openclaw auth google`.

---

## GitHub (if selected)

1. Go to github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a token with scopes: `repo`, `read:user`, `read:org`

```bash
read -rsp $'Paste GitHub token (input hidden, press Enter):\n' GH_TOKEN && printf '\n'
openclaw config set github.token "$GH_TOKEN"
unset GH_TOKEN && history -c && history -w
systemctl --user restart openclaw-gateway
```

Test via Telegram or dashboard:
> "List my open GitHub pull requests"

---

## Local disk access (if selected)

```bash
openclaw config set filesystem.allowed_paths "~"
openclaw config set filesystem.enabled true
systemctl --user restart openclaw-gateway
```

Test via Telegram or dashboard:
> "List files in my home directory"

Verify it stays within `~` and does not access paths outside.

---

## Completion check

For each platform in `deployment-brief.md`, confirm:

- [ ] Telegram: `openclaw status --deep` shows `Telegram │ OK`, bot responds, pairing approved
- [ ] WhatsApp: webhook verified in Meta dashboard, test message received (skip if no domain)
- [ ] Slack: bot responds to DM
- [ ] Email: OpenClaw can read and send a test message
- [ ] Google Calendar: calendar query returns results
- [ ] Google Contacts: contact lookup works
- [ ] GitHub: PR/repo query returns expected results
- [ ] Local disk: file listing works, scoped to `~`

Check logs for auth errors:
```bash
cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i "error\|auth\|401" | tail -20
```

---

**Phase 4 complete.**

Once all integrations in your deployment brief are verified, say: *"Integrations done. Type `continue` when you're ready to start Phase 5 — Security Hardening."*
