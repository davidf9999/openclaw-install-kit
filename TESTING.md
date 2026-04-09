# Testing & Validation — openclaw-install-kit

## What has been tested (as of v0.1.0)

| What | Status |
|---|---|
| Full end-to-end install, all 8 phases | ✅ Completed once — Ubuntu 24.04 / ASUS ZenBook UX305FA / Intel Core M / fanless / x86_64 |
| Telegram integration | ✅ Verified working |
| WhatsApp Path A (personal number, whatsapp-web.js) | ✅ Verified working (including group gating, dmPolicy, Cloudflare named tunnel) |
| Cloudflare named tunnel | ✅ Verified working |
| WhatsApp Path B (Meta Business API) | ❌ Not tested — instructions based on Meta documentation only |
| Slack, Email, Discord, Signal | ❌ Not tested |
| Google Calendar | 🔶 Planned next — dedicated test account, least-privilege scopes |
| Google Contacts | 🔶 Planned next — validate with Calendar first |
| Google Gmail | 🔶 Planned next — separate stage, more sensitive scopes |
| Google Drive | ⏸ Pending path — do not treat as validated until a supported flow exists |
| GitHub integration | ❌ Not tested |
| Local disk integration | ❌ Not tested |
| Debian 11/12 | ❌ Not tested |
| macOS 12+ | ❌ Not tested — Phase 2 requires Homebrew adaptation not in this kit |
| Raspberry Pi / ARM64 | ❌ Not tested |
| VPS (DigitalOcean, Hetzner, etc.) | ✅ Validated once — DigitalOcean / Ubuntu 24.04.3 LTS / Frankfurt / Telegram working |
| Recovery after /compact (context loss) | ❌ Not tested in a real session |
| Journey AI clipboard mode | ❌ Not tested — kit developed in Claude Code tool-executing mode |

**The kit has been validated on two machine configurations.** Everything else is based on documentation review, structural analysis, or inference from the known paths.

### Google validation policy

Google integrations are intentionally staged:
- Calendar and Contacts come first
- Gmail is a separate, more sensitive follow-up stage
- Drive stays pending until there is a supported path and a successful end-to-end test

Security baseline for all Google tests:
- use a dedicated Google test account or Workspace identity when possible
- enable only the APIs/scopes actually selected in `deployment-brief.md`
- keep OAuth files under `~/.openclaw/`
- delete only the token file for the service you are retesting, not the whole workspace unless necessary

### Real-world test run log — v0.1.0 (2026-04-07)

- **OS**: Ubuntu 24.04.4 LTS
- **Hardware**: ASUS ZenBook UX305FA, Intel Core M-5Y10, 8 GB RAM, fanless, x86_64
- **Interface**: Claude Code (tool-executing mode)
- **Phases completed**: All 8 (0a–7)
- **Integrations tested**: Telegram ✅, WhatsApp Path A with Cloudflare named tunnel ✅
- **Thermal baseline**: idle ~39°C, peak ~53°C under `stress-ng --cpu 2 --timeout 30s` — within safe limits for this hardware
- **Hardware notes**: Core M is designed for burst workloads, not sustained 24/7 load. For personal assistant use (low concurrency, intermittent requests) it is comfortable. 8 GB RAM has headroom in gateway mode. If migrating to always-on VPS later, Phases 3–7 are unchanged — only Phase 2 needs VPS-specific firewall rules.
- **First phase that deviated from skill files**: Phase 3 — `openclaw onboard` behaviour and config file locations differed from initial kit assumptions; skill files were updated after this run
- **Kit updates made**: Full rewrite of skills/03, 04, 05, 06, 07 based on this run's findings

### Real-world test run log — VPS validation (2026-04-09)

- **Provider**: DigitalOcean
- **Region**: Frankfurt (`fra1`)
- **OS**: Ubuntu 24.04.3 LTS
- **Hardware**: 1 vCPU, 2 GB RAM, 50 GB disk
- **Interface**: Claude Code (tool-executing mode)
- **Phases completed**: 0a–4, with core install and Telegram validated
- **Integrations tested**: Telegram ✅
- **Dashboard access**: SSH tunnel to `http://localhost:18889/`
- **First visible deviations**:
  - `openclaw dashboard` required SSH port forwarding on the VPS
  - `openclaw gateway url` was not the correct command in this version; the dashboard command printed the tunnel instructions
  - Security audit warned about `gateway.controlUi.allowInsecureAuth=true`
  - `model-pricing` bootstrap emitted a timeout warning, but the install remained functional
- **Outcome**: core hosted path works end to end; Telegram paired and replied successfully

---

This document also covers:
1. Skill-creator A/B test design (Part 0)
2. Simulated A/B tests — qualitative analysis without real users or VMs (Part 1)
3. Tests requiring real infrastructure (Part 2)
4. Ongoing validation log (Part 3)

---

## Part 0 — Skill-creator A/B test design

The Claude skill-creator can generate a "vanilla" install skill from a single prompt. Using that as the control condition for comparison is more rigorous than an imagined baseline. Here is how this can be run, and what parts can be automated.

### How to run the skill-creator A/B test

**Step 1 — Generate the vanilla skill (manual, ~2 minutes)**

Open Claude and prompt the skill-creator:
> "Create a skill that installs OpenClaw on Ubuntu, connects it to Telegram, and starts it as a background service."

Save the output as `TESTING-vanilla-skill.md` (gitignored — it's a test artifact).

**Step 2 — Compare against this kit for a given user profile (automatable)**

For each user profile in Part 1, the comparison can be run by prompting Claude:
> "I have two install guides for OpenClaw. Read both. Then walk through what would happen if [user profile description] followed each guide. For each guide, note: which steps would fail, what decisions would be made incorrectly, and what would be missing at the end."

Provide both `TESTING-vanilla-skill.md` and the relevant skills from this kit. Claude can produce a structured comparison without any real machine.

**Step 3 — Record findings in Part 3 (manual)**

Add a row to the test log with date, profiles tested, and key differences found.

### What can be automated vs what can't

| Comparison step | Automatable? | How |
|---|---|---|
| Generate vanilla skill | Yes | Single skill-creator prompt, save output |
| Structural diff (phases, gates, artifacts) | Yes | Claude prompt comparing both documents |
| User profile walkthrough | Yes (qualitative) | Claude prompt simulating each profile |
| Completion rate | No | Requires real users |
| Time to completion | No | Requires real users |
| Error rate | No | Requires real infrastructure |

The qualitative simulation in Part 1 below was written by hand. Using the skill-creator to generate the actual B-condition would make it more reproducible — someone running this test six months from now would get a current skill-creator output rather than this kit's author's memory of what one looks like.

---

## Part 1 — Simulated A/B tests (run inline)

### What a "vanilla skill" looks like

For comparison purposes, here is a representative vanilla "install OpenClaw on Ubuntu" skill — the kind the Claude skill-creator would produce from a single-sentence prompt:

```
# Install OpenClaw on Ubuntu

1. Update your system: `sudo apt update && sudo apt upgrade -y`
2. Install Node.js 20: `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs`
3. Install OpenClaw: `npm install -g openclaw`
4. Run the setup wizard: `openclaw onboard`
5. Start the gateway: `openclaw gateway start`
6. Configure Telegram: set your bot token when prompted
7. Done — your assistant is running
```

This is accurate for the happy path on a fresh VPS with Node 20. It has no branching, no hardware adaptation, no security hardening, no recovery path.

---

### Scenario 1: Experienced sysadmin, Hetzner VPS, wants Telegram only

**User profile**: Comfortable with Linux. Machine is already provisioned. Wants a quick install with no extras.

| Step | Vanilla skill | This kit |
|---|---|---|
| Node.js version | Installs Node 20 — OpenClaw requires 22.14+ | Phase 2 installs Node 24 via nvm, verifies with `node --version` |
| Token format | No warning — user pastes `123456789:ABCdef... @mybot` (includes username) | Skill 03 explicitly warns: copy text, not the button; paste token only, not the bot username |
| Daemon management | `openclaw gateway start` — dies on logout | Phase 3 sets up `systemctl --user` with linger; survives reboots and logout |
| Security | Not mentioned | Phase 5 audits firewall, file permissions, shell history, fail2ban |
| Recovery | None | Each phase is re-enterable; `deployment-brief.md` persists state |

**Outcome prediction**: Vanilla skill completes in 10 minutes on this profile. This kit takes 30 minutes. For this user, the vanilla skill works — but produces a non-hardened, non-persistent install that will silently fail on next reboot.

**Kit advantage here**: Minimal for the install itself. High for long-term reliability (systemd + linger + runbook).

---

### Scenario 2: Non-technical user, home laptop, wants WhatsApp and Calendar

**User profile**: Not comfortable with Linux terminal. Using an existing laptop (daily driver). Wants WhatsApp and Google Calendar.

| Step | Vanilla skill | This kit |
|---|---|---|
| Hardware check | None — no lid-suspend warning | Phase 0a asks; Phase 3 configures no-suspend-on-lid-close |
| WhatsApp path | No distinction — implies Meta API | Phase 1 asks: personal number or business number? Routes to correct path in Phase 4 |
| Meta API approval | Not mentioned | Phase 4 warns: 1–3 day approval wait if Meta API path; recommends personal number for immediate use |
| QR code pairing | Not covered | Phase 4 covers whatsapp-web.js QR scan, device linking, group gating configuration |
| Google Calendar | "Enable Google Calendar API" — no OAuth detail | Phase 4 covers GCP project creation, credentials.json placement, `openclaw auth google` flow, token permissions |
| WhatsApp stops responding | No recovery path | Phase 4 covers dmPolicy, group allowlist, self-chat JID configuration |
| Session persistence | Not covered | Phase 3 explains linger; Phase 7 runbook covers `systemctl --user restart openclaw-gateway` |

**Outcome prediction**: Vanilla skill fails at WhatsApp for this user — wrong path assumed, no QR code guidance, no group policy explanation. Calendar setup leaves the user lost at "enable APIs." This user needs the kit.

**Kit advantage here**: High. The branching logic (personal vs business WhatsApp), the group gating discovery, and the OAuth flow walkthrough are exactly what this profile needs.

---

### Scenario 3: Developer, fanless NUC, multiple integrations, 24/7 uptime

**User profile**: Technical. Bare metal NUC, fanless, always on. Wants Telegram + WhatsApp + GitHub + local disk.

| Step | Vanilla skill | This kit |
|---|---|---|
| Thermal monitoring | Not mentioned | Phase 2 installs lm-sensors, runs `sensors-detect`, checks idle temp before proceeding |
| Stress test | Not mentioned | Phase 5 runs `stress-ng` load test, records peak temp, optionally throttles `gateway.max_concurrent_tasks` |
| Multi-integration order | All at once | Phase 4 sequences: Telegram first (simplest, verifiable), then WhatsApp, then others |
| GitHub token scopes | Not specified | Phase 4 specifies exact scopes: `repo`, `read:user`, `read:org` |
| Local disk scope | Not specified | Phase 4 configures `filesystem.allowed_paths "~"` and verifies boundary |
| Runbook | None | Phase 7 produces `runbook.md` covering restart, backup, update, monitoring |
| Phase recovery | None | Each phase is idempotent; re-entry documented in each skill header |

**Outcome prediction**: Vanilla skill gets this user to a working install. But no thermal safety, no sequencing (integration failures compound), no runbook. The developer will figure it out — but the kit saves 2–3 hours of debugging.

**Kit advantage here**: Medium-high. Thermal monitoring and the integration sequencing are the biggest wins for this profile.

---

### Summary of simulated results

| User profile | Vanilla skill success | Kit advantage |
|---|---|---|
| Expert, VPS, Telegram only | Yes, with caveats (systemd, security) | Low for install; high for reliability |
| Non-technical, laptop, WhatsApp + Calendar | No — fails at WhatsApp path and OAuth | High — branching logic and recovery are critical |
| Developer, fanless NUC, multi-integration | Yes, with manual debugging | Medium — thermal safety and sequencing save time |

**Conclusion**: The kit's value scales with user complexity and hardware specificity. For an expert on a fresh VPS wanting only Telegram, the kit adds overhead. For a non-technical user with specific hardware and multiple integrations, the kit is the difference between success and abandonment.

---

## Part 2 — Tests requiring real infrastructure

These tests cannot be simulated. They are described here for future validation.

### Test A: Kit completion rate vs vanilla skill (real users)

**Method**: Recruit 10 users per condition. Condition A uses this kit. Condition B uses a vanilla "install OpenClaw" skill generated by Claude skill-creator.

**Metrics**:
- Primary: % reaching a working bot on at least one channel
- Secondary: Time to Phase 7 (kit) or equivalent completion (vanilla)
- Error count: how many phases required a retry or support question

**Minimum sample**: 10 per condition for directional signal; 30+ for statistical significance.

---

### Test B: Kit vs kit-without-orientation (Phase 0a impact)

**Method**: Two variants of this kit — one starting at Phase 0a (computing selection + orientation), one starting at Phase 1 (discovery).

**Metric**: Abandonment rate before Phase 2 completes. Hypothesis: orientation reduces abandonment by setting correct expectations about the manual paste-and-verify model.

---

### Test C: With vs without deployment-brief (shared artifact chain)

**Method**: Variant of the kit where phases don't read `deployment-brief.md` — the agent asks questions inline at each phase instead.

**Metric**: Number of contradictory decisions across phases (e.g., SSL set up in Phase 2 but domain is "none"), number of questions repeated across phases.

This tests whether the shared artifact chain actually reduces errors and repetition or just adds overhead.

---

### Test D: Kit correctness across OS variants (automated)

**Method**: Provision VMs for each supported OS (Ubuntu 24.04, Ubuntu 22.04, Debian 12, macOS 14). Run the kit against each. Claude Code executes commands directly.

**Metrics**:
- Which phases produce errors on non-Ubuntu systems?
- Does Phase 2 fail on macOS (apt commands)?
- Does Phase 4 cloudflared install fail on ARM64?

**Automation level**: High — Claude Code + fresh VMs. Most of this can be scripted except OAuth flows and WhatsApp QR pairing.

---

### Test E: Recovery after /compact (context loss)

**Method**: Run the kit to Phase 4. Run `/compact`. Attempt to resume. Measure whether `deployment-brief.md` is sufficient for the agent to correctly identify the current state and resume.

**Metric**: Did the agent correctly identify which phase was complete and which integrations were working, using only `deployment-brief.md` + a verification command?

This directly tests the file-as-state-persistence design.

---

### Test F: WhatsApp path selection accuracy (discovery)

**Method**: Present Phase 1 discovery to 10 users. Measure: how many chose the correct WhatsApp path (personal vs business) for their actual use case? How many needed to switch paths in Phase 4?

**Hypothesis**: The two-path question in Phase 1 reduces WhatsApp Phase 4 failures compared to a kit that defaults to one path.

---

## Part 3 — Ongoing validation as kit evolves

As new OS variants, hardware profiles, and OpenClaw versions are tested, update this document with:

- Date tested
- OS version + hardware profile
- Phase where first error was encountered
- Resolution applied
- Whether skill files were updated as a result

Template:
```
## Test run: YYYY-MM-DD
- OS: Ubuntu 24.04 / Debian 12 / macOS 14 / other
- Hardware: VPS / bare metal / fanless / ARM64
- Phase 1–3: pass / fail (note)
- Phase 4: integrations tested: [list]
- Phase 5: security check result
- Phase 6–7: pass / fail
- Kit updates made: [list skill files updated]
```

---

## Current real-world test coverage

As of v0.1.0, the kit has been fully run end-to-end on exactly one configuration:

| Field | Value |
|---|---|
| Hardware | ASUS ZenBook UX305FA |
| CPU | Intel Core M-5Y10 (fanless) |
| Architecture | x86_64 |
| OS | Ubuntu 24.04 LTS |
| Interface | Claude Code (tool-executing mode) |
| Phases completed | All 8 (0a–7) |
| Integrations verified | Telegram, WhatsApp Path A (personal number), Cloudflare named tunnel |
| Integrations not tested | WhatsApp Path B, Slack, Email, Google Calendar, Google Contacts, GitHub, local disk |

Everything else is theoretical or based on documentation review.

---

## Known gaps not yet tested

- Debian 12 (apt + ufw should work identically, not yet verified)
- macOS — Phase 2 needs Homebrew adaptation documented
- ARM64 (Raspberry Pi 4) — cloudflared binary URL needs verification
- Multi-user pairing flow — tested for single user only
- Google Calendar OAuth — tested with one GCP account; edge cases with org-managed accounts untested
- WhatsApp business API path (Path B) — not tested; only personal number (Path A) has been verified
