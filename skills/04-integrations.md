# Skill 04 — Integrations

**Purpose**: Connect OpenClaw to the messaging platforms and services chosen during discovery.

**Input**: `deployment-brief.md`, running OpenClaw daemon (from skill 03)  
**Output**: Each chosen platform verified as sending/receiving messages through OpenClaw

---

## Instructions

Read `deployment-brief.md`. Only set up platforms listed under `Messaging Platforms` and `Integrations`. Skip sections for platforms not selected — do not prompt the user to add more.

Always start with Telegram (simplest, no SSL required in long-poll mode). Add others after Telegram is verified.

---

## Telegram (start here)

### Create bot
1. Open Telegram, search for `@BotFather`
2. Send `/newbot` — follow prompts, get a **Bot Token**
3. Send `/setprivacy` → disable (allows the bot to read group messages if needed)

### Configure in OpenClaw
```bash
openclaw config set telegram.token <paste-token>
openclaw config set telegram.mode longpoll    # use 'webhook' only if you have a domain+SSL
pm2 restart openclaw
```

### Verify
Send `/start` to your bot in Telegram. OpenClaw should respond within a few seconds.

---

## WhatsApp (if selected)

WhatsApp requires a Meta Business account and approved app.

1. Create a Meta Developer app at developers.facebook.com
2. Add the WhatsApp product, get a **Phone Number ID** and **Access Token**
3. Set a webhook URL: `https://<your-domain>/webhooks/whatsapp` (SSL required)

```bash
openclaw config set whatsapp.phone_number_id <id>
openclaw config set whatsapp.access_token <token>
openclaw config set whatsapp.webhook_verify_token <random-string-you-choose>
pm2 restart openclaw
```

Register the webhook in Meta dashboard using the verify token.

**Note**: WhatsApp requires a public HTTPS endpoint. If no domain was set up, skip for now and return after SSL is in place.

---

## Slack (if selected)

1. Create a Slack App at api.slack.com/apps
2. Enable **Socket Mode** (avoids public URL requirement)
3. Add OAuth scopes: `chat:write`, `im:history`, `im:read`
4. Install to workspace, get **Bot Token** and **App-Level Token**

```bash
openclaw config set slack.bot_token <xoxb-...>
openclaw config set slack.app_token <xapp-...>
pm2 restart openclaw
```

Send a DM to your bot in Slack to verify.

---

## Email — IMAP/SMTP (if selected)

```bash
openclaw config set email.imap_host <host>
openclaw config set email.imap_port 993
openclaw config set email.smtp_host <host>
openclaw config set email.smtp_port 587
openclaw config set email.username <address>
openclaw config set email.password <password>
pm2 restart openclaw
```

Use an app-specific password if using Gmail/Outlook (not your main account password).

---

## Google Workspace (if selected — optional, most complex)

**Only proceed if `Google Workspace: yes` in deployment-brief.md.**

1. Go to console.cloud.google.com → New Project
2. Enable APIs: Google Calendar API, Gmail API, Google Drive API (as needed)
3. Create OAuth 2.0 credentials (Desktop app type)
4. Download `credentials.json` → place in `~/openclaw/`
5. Run the OAuth flow:

```bash
openclaw auth google
```

A browser window will open. Authorize all requested scopes. A `token.json` will be saved.

```bash
chmod 600 ~/openclaw/credentials.json ~/openclaw/token.json
pm2 restart openclaw
```

**Common failure**: Missing OAuth scopes. If calendar/email access fails, return to GCP console, add missing scopes, delete `token.json`, and re-run `openclaw auth google`.

---

## CRM (if selected)

OpenClaw supports CRM connections via webhooks and API keys. Refer to your CRM's OpenClaw integration docs:
- HubSpot: `openclaw config set crm.hubspot.api_key <key>`
- Notion: `openclaw config set crm.notion.token <token>`
- Airtable: `openclaw config set crm.airtable.api_key <key>`

Always `pm2 restart openclaw` after config changes.

---

## Completion check

For each platform in `deployment-brief.md`:
- [ ] Telegram: bot responds to `/start`
- [ ] WhatsApp: webhook verified in Meta dashboard, test message received
- [ ] Slack: bot responds to DM
- [ ] Email: OpenClaw can read and send a test message
- [ ] Google: calendar event readable via OpenClaw query
- [ ] CRM: test record retrievable via OpenClaw

Run `pm2 logs openclaw --lines 50` after all integrations — confirm no auth errors.
