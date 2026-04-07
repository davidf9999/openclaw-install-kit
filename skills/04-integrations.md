# Skill 04 — Integrations

**Purpose**: Connect OpenClaw to the messaging platforms and services chosen during discovery.

**Input**: `deployment-brief.md`, running OpenClaw daemon (from skill 03)  
**Output**: Each chosen platform verified as sending/receiving messages through OpenClaw

> **Phase 4 of 7 — Integrations**  
> Re-read `deployment-brief.md` before starting. Only set up platforms listed there — do not prompt the user to add more.  
> You will run all commands yourself. Paste each output back here so I can verify before we continue.  
> If you are re-entering this phase, say "resuming Phase 4" and tell me which integrations are already working.

---

## Instructions

Only set up platforms listed under `Messaging Platforms` and `Integrations` in `deployment-brief.md`. Skip all other sections.

Always start with Telegram (simplest, no SSL required in long-poll mode). Add others only after Telegram is verified working.

After every `openclaw config set` block, restart the daemon:
```bash
sudo systemctl restart openclaw
```

---

## Telegram (start here)

### Create bot
1. Open Telegram on your phone or desktop
2. Search for `@BotFather`
3. Send `/newbot` — follow the prompts, choose a name and username
4. BotFather will give you a **Bot Token** (looks like `123456789:ABCdef...`)
5. Optionally send `/setprivacy` to BotFather → select your bot → choose `Disable` (allows reading group messages)

Tell me when you have your Bot Token (don't paste the token itself — just confirm you have it).

### Configure in OpenClaw

```bash
openclaw config set telegram.token <paste-token-here>
openclaw config set telegram.mode longpoll
sudo systemctl restart openclaw
```

Replace `<paste-token-here>` with your actual token. After running, paste the output.

### Verify

Open Telegram and send `/start` to your new bot. It should respond within a few seconds.

Tell me what the bot replied (or if it didn't respond, paste the last 30 lines of logs):
```bash
sudo journalctl -u openclaw -n 30 --no-pager
```

---

## WhatsApp (if selected — complex, do after Telegram)

> ⚠️ **WhatsApp requires a public HTTPS endpoint (SSL + domain).** If `Domain: none` in your deployment brief, this integration cannot be completed until a domain and SSL are in place. Skip for now and return later.
>
> WhatsApp also requires a **Meta Business account** with an approved app — the approval process can take 1–3 days.

1. Go to developers.facebook.com → Create a new app → Add the WhatsApp product
2. Get your **Phone Number ID** and **Permanent Access Token** from the app dashboard
3. Set a webhook URL: `https://<your-domain>/webhooks/whatsapp`

```bash
openclaw config set whatsapp.phone_number_id <id>
openclaw config set whatsapp.access_token <token>
openclaw config set whatsapp.webhook_verify_token <random-string-you-choose>
sudo systemctl restart openclaw
```

Register the webhook in the Meta dashboard using the verify token you chose.

Paste the output of `sudo journalctl -u openclaw -n 30 --no-pager` after restarting.

---

## Slack (if selected)

1. Go to api.slack.com/apps → Create New App → choose **From scratch**
2. Enable **Socket Mode** (avoids the need for a public URL)
3. Add OAuth scopes under **OAuth & Permissions**: `chat:write`, `im:history`, `im:read`
4. Install to workspace → get **Bot Token** (`xoxb-...`) and **App-Level Token** (`xapp-...`)

```bash
openclaw config set slack.bot_token <xoxb-...>
openclaw config set slack.app_token <xapp-...>
sudo systemctl restart openclaw
```

Send a DM to your bot in Slack to verify. Tell me what it replied.

---

## Email — IMAP/SMTP (if selected)

Use an app-specific password if using Gmail or Outlook — not your main account password.

```bash
openclaw config set email.imap_host <host>
openclaw config set email.imap_port 993
openclaw config set email.smtp_host <host>
openclaw config set email.smtp_port 587
openclaw config set email.username <your-address>
openclaw config set email.password <app-password>
sudo systemctl restart openclaw
```

Paste the output after restarting.

---

## Google Workspace — Calendar and Contacts (if selected)

**Only proceed if listed in `deployment-brief.md`. Enable only the specific APIs selected — do not enable Gmail or Drive unless the brief says so.**

1. Go to console.cloud.google.com → Create a new project
2. Enable APIs: **Google Calendar API**, **People API** (for Contacts) — only these unless brief says otherwise
3. Create **OAuth 2.0 credentials** → Application type: Desktop app
4. Download `credentials.json` → place in `~/openclaw/`

```bash
chmod 600 ~/openclaw/credentials.json
openclaw auth google
```

A browser window will open. Authorize the requested scopes. A `token.json` will be saved.

```bash
chmod 600 ~/openclaw/token.json
sudo systemctl restart openclaw
```

Paste the output of the restart. Then test with:
```bash
openclaw query "what's on my calendar today?"
```

Paste the response.

**Common failure**: If calendar or contacts access fails later, return to GCP console, verify the correct APIs are enabled, delete `token.json`, and re-run `openclaw auth google`.

---

## GitHub (if selected)

1. Go to github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with scopes: `repo`, `read:user`, `read:org` (adjust to your needs)
3. Copy the token

```bash
openclaw config set github.token <your-token>
sudo systemctl restart openclaw
```

Test:
```bash
openclaw query "list my open GitHub pull requests"
```

Paste the response.

---

## Local disk access (if selected)

OpenClaw can read and write files on the local machine. Scope must be restricted to the home directory.

```bash
openclaw config set filesystem.allowed_paths "~"
openclaw config set filesystem.enabled true
sudo systemctl restart openclaw
```

Test:
```bash
openclaw query "list files in my home directory"
```

Paste the response. Verify it shows your home directory contents and does not access paths outside `~`.

---

## Completion check

For each platform in `deployment-brief.md`, confirm:

- [ ] Telegram: bot responds to `/start`
- [ ] WhatsApp: webhook verified in Meta dashboard, test message received (skip if no domain)
- [ ] Slack: bot responds to DM
- [ ] Email: OpenClaw can read and send a test message
- [ ] Google Calendar: calendar event readable via OpenClaw query
- [ ] Google Contacts: contact lookup works
- [ ] GitHub: PR/repo query returns expected results
- [ ] Local disk: file listing works, scoped to `~`

Run this and paste the output — confirm no auth errors:
```bash
sudo journalctl -u openclaw -n 50 --no-pager
```

---

**Phase 4 complete.**

Once all integrations in your deployment brief are verified, say: *"Integrations done. Type `continue` when you're ready to start Phase 5 — Security Hardening."*
