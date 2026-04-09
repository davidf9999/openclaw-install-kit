# VPS Checklist

DigitalOcean validation plan for `openclaw-install-kit`.

## Goal

Validate the repo on a typical hosted path with minimum scope, minimum cost, and a clean result that can be cited in `TESTING.md`.

## Recommended Scope

- Provider: DigitalOcean
- Image: Ubuntu 24.04 LTS x64
- Plan: Basic
- Size: 2 GB RAM
- Disk: 50 GB
- Execution mode: Claude Code
- Required integration: Telegram
- Optional integration: WhatsApp Path A
- Defer: Google, GitHub, Slack, Email, local disk

## Success Criteria

- VPS provisioned and reachable over SSH
- Phase 0a through Phase 3 complete cleanly
- Telegram works end to end
- Optional: WhatsApp Path A works
- Enough notes captured to update `TESTING.md`

## Provisioning

1. Sign in to DigitalOcean.
2. Create a Droplet.
3. Choose:
   - Region closest to you
   - Image: `Ubuntu 24.04 LTS x64`
   - Plan: `Basic`
   - Size: `2 GB RAM`
   - Disk: `50 GB`
4. Add your SSH public key during provisioning.
5. Use a hostname like `openclaw-vps-test-01`.
6. Disable extras you do not need.
7. Create the Droplet.

## Pre-Run Inputs

Have these ready before starting:

- Anthropic API key
- Telegram bot token
- Optional: WhatsApp Path A setup items
- Local SSH key already added to the Droplet
- Claude Code ready on your local machine

Optional automation files in this repo:

- `scripts/vps-preflight.sh`
- `scripts/vps-postflight.sh`
- `templates/deployment-brief-vps-telegram.md`

## Automation Scope

The helper scripts are intentionally narrow:

- `scripts/vps-preflight.sh` captures baseline machine facts and a copy-paste test header
- `scripts/vps-postflight.sh` captures service state and log evidence at the end
- The actual install steps stay visible and manual for the first VPS validation run

Why:

- it keeps the validation path observable
- it makes VPS-specific failures easier to spot
- it avoids hiding the exact install behavior behind a bootstrap wrapper

If you later do a second VPS pass, a `vps-bootstrap.sh` may be worth adding. For the first pass, the current split is deliberate.

## Initial VPS Verification

From your local machine:

```bash
ssh root@<VPS_IP>
```

Then verify basics.

Manual way:

```bash
lsb_release -a
uname -a
free -h
df -h /
```

Automated way:

```bash
bash scripts/vps-preflight.sh DigitalOcean <region> "Telegram only"
```

Record:

- Exact Ubuntu version
- RAM
- Disk
- Region/provider
- Public IP

## Recommended Deployment Brief Values

For this validation run, keep discovery minimal.

Fastest path:
- copy `templates/deployment-brief-vps-telegram.md`
- adjust only date, exact Ubuntu version, and any scope changes

Example:

```bash
cp templates/deployment-brief-vps-telegram.md deployment-brief.md
```

Then edit the copied file if needed.

Recommended values:

- Hosting: VPS
- OS: Ubuntu 24.04
- Fanless: no
- Domain: none
- Use mode: personal/dev
- LLM provider: Anthropic
- Messaging: Telegram
- Additional integrations: none

Optional second pass:

- WhatsApp Path A only

## Execution Order

1. Phase 0a
   - Confirm machine choice and SSH access
2. Phase 0b
   - Orientation
3. Phase 1
   - Create `deployment-brief.md` with the minimal VPS + Telegram scope
4. Phase 2
   - System update
   - Node 24 via nvm
   - UFW baseline
   - Skip SSL because `Domain: none`
   - Create working directory
5. Phase 3
   - Install `openclaw`
   - Run onboard
   - Confirm `systemctl --user`
   - Confirm linger
   - Confirm dashboard URL
6. Phase 4
   - Telegram only
   - Verify bot response
   - Approve pairing
   - Lock down DM access
7. Optional
   - WhatsApp Path A only if Telegram is already stable

## What To Capture During The Run

Record these as you go:

- Any command that failed first time
- Any VPS-specific deviation from the laptop flow
- Whether firewall guidance was correct on a fresh DigitalOcean server
- Whether `systemctl --user` and linger behaved as expected on a VPS
- Actual total install time
- Whether Telegram was simpler on VPS than on laptop
- Any place where the wording still assumes local hardware

At the end of the run, collect postflight evidence automatically:

```bash
bash scripts/vps-postflight.sh
```

## Minimal Test Log Template

Copy this into your notes while running:

```md
## VPS test run
- Date:
- Provider: DigitalOcean
- Plan: Basic / 2 GB RAM / 50 GB disk
- OS: Ubuntu 24.04.x LTS
- Region:
- Public IP:
- Interface: Claude Code
- Scope tested: Telegram only / Telegram + WhatsApp Path A
- Phase 0a: pass/fail
- Phase 0b: pass/fail
- Phase 1: pass/fail
- Phase 2: pass/fail
- Phase 3: pass/fail
- Phase 4: pass/fail
- Issues encountered:
- Docs updated afterward:
```

## Decision Gates

- If Phases 0a through 3 are clean and Telegram works:
  - Count this as a successful VPS validation
  - Update `TESTING.md`
- If Phase 2 or 3 breaks in a VPS-specific way:
  - Stop and fix docs before testing extra integrations
- Do not add Google, GitHub, Slack, or email during this run unless the core path is already clean

## After The Run

1. Save:
   - Exact Ubuntu version
   - Droplet size
   - Whether Telegram worked
   - Any corrections needed
   - Output from `scripts/vps-postflight.sh`
2. Update:
   - `TESTING.md`
   - `README.md` if VPS becomes validated
   - `ROADMAP.md` if scope assumptions changed
3. Destroy the Droplet unless you want another integration pass

## Optional Second Session

If the first pass is clean:

- Test WhatsApp Path A
- Do not test WhatsApp Path B yet
- Do not expand to Google unless you intentionally want an integration-focused follow-up run

## Recommended Stopping Point

For the first VPS run, stop when:

- Phase 3 is complete
- Telegram is fully working

That alone materially strengthens the repo's validation story.
