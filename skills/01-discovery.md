# Skill 01 — Discovery

**Purpose**: Interview the user and produce `deployment-brief.md` — the single source of truth consumed by all subsequent phases.

**Input**: Conversation with user  
**Output**: `deployment-brief.md` in the working directory

> **Phase 1 of 8 — Discovery**  
> This phase is entirely conversational — no terminal commands. Ask questions, collect answers, write the brief.  
> If you are re-entering this phase, ask the user to confirm whether `deployment-brief.md` already exists before asking questions again.  
>  
> **Expert fast path — skip this phase if:**  
> (a) `deployment-brief.md` already exists from a previous install, or  
> (b) the user knows their setup and is willing to fill in the template below directly.  
> In either case, verify the file exists and is complete, then proceed straight to Phase 2.

---

## Instructions

Ask the user the following questions. You do not need to ask them all at once — group them naturally. Record answers as you go. At the end, write `deployment-brief.md`.

### 1. Hardware / hosting

- What machine will OpenClaw run on?
  - Bare metal (what model/specs)?
  - VPS (which provider — DigitalOcean, Hetzner, AWS, other)?
- What OS version is installed? (Ask them to run `lsb_release -a` and paste the output)
- Is this machine fanless or passively cooled? (Important for thermal monitoring)
- Is this intended for personal/dev use or always-on production?
- Do you have a domain name or DDNS hostname for this machine?

### 2. LLM provider

- Which API provider will OpenClaw use? (Anthropic recommended; also supports OpenAI, Google, Groq)
- Do you already have an API key, or do you need to create one?

### 3. Messaging platforms

Which platforms should OpenClaw connect to? (select all that apply)
- [ ] Telegram (simplest — start here if unsure)
- [ ] WhatsApp ⚠️ *Two very different setup paths — ask which one:*
  - **Personal number** (your own WhatsApp): uses `whatsapp-web.js` browser bridge — no Meta approval needed, works today, but requires keeping a browser session alive and may break on WhatsApp updates
  - **Separate/business number**: uses Meta Business API — stable and supported, but requires Meta app approval (1–3 days) and a public HTTPS endpoint
  - Record which path was chosen in the brief — skill 04 handles them differently
- [ ] Slack
- [ ] Discord
- [ ] Signal
- [ ] Microsoft Teams
- [ ] Email (IMAP/SMTP)

For each selected platform, note whether a bot/app account already exists.

### 4. Integrations

- Google Workspace (Calendar, Gmail, Drive)? (Most complex — only include if needed. Ask which services specifically.)
- CRM? (Which one — HubSpot, Salesforce, Notion, Airtable, other?)
- GitHub? (API access to repos, issues, PRs)
- Local disk access? (Scope to home directory only — confirm boundary)
- Any other webhooks or custom integrations?

### 5. Use cases

In a few sentences: what do you want OpenClaw to do for you day-to-day?
(This shapes the optimization phase — prompt design, skill selection)

### 6. Team

- Is this for personal use only, or will others access the assistant?
- If team use: how many people, what access levels?

---

## Output format

Write `deployment-brief.md` with this structure:

```markdown
# Deployment Brief

Generated: <date>

## Hardware
- Machine: <model/specs>
- OS: <ubuntu version>
- Hosting: <bare metal | VPS provider | cloud>
- Fanless: <yes/no>
- Domain: <domain or DDNS or none>
- Use mode: <personal/dev | always-on production>

## LLM Provider
- Provider: <Anthropic | OpenAI | other>
- Key status: <have it | needs creating>

## Messaging Platforms
- Primary: <platform>
- Additional: <list>
- WhatsApp path: <personal number — Path A | business number — Path B | none>

## Integrations
- Google Workspace: <yes/no — which services>
- GitHub: <yes/no>
- Local disk: <yes/no — scope>
- CRM: <name or none>
- Other: <list>

## Use Cases
<brief description>

## Team
- Users: <count>
- Access model: <personal | multi-user>

## Notes
<any special constraints, timing, concerns raised during discovery>
```

---

## Completion check

Before marking this phase done:
- [ ] `deployment-brief.md` exists in the working directory
- [ ] All 6 sections are filled in (no blanks — use "none" or "TBD" explicitly)
- [ ] User has confirmed the brief is accurate

---

**Phase 1 complete.**

Once the user confirms the brief is accurate, say: *"Phase 1 done — deployment-brief.md is your source of truth for the rest of the install. Type `continue` when you're ready to start Phase 2 — Infrastructure."*
