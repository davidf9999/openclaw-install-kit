# Skill 00 — Computing Selection

**Purpose**: Help the user decide what machine and OS to run OpenClaw on. If they already have a suitable machine ready, this phase takes 2 minutes.

**Input**: Conversation with user  
**Output**: Clear machine/OS decision confirmed before Orientation begins

> **Phase 0a of 8 — Computing Selection**  
> This phase is entirely conversational — no terminal commands yet.  
> If you already have a Linux or macOS machine with terminal access ready, say so and I will confirm it meets the requirements and move straight to Orientation.

---

## Instructions

Ask only the questions needed to reach a clear decision. If the user already has a suitable machine, confirm it and proceed. Do not ask unnecessary questions.

---

### Already have a machine?

If yes, ask them to run the following and paste the output:

```bash
# Linux / Ubuntu / Debian:
uname -a && free -h && df -h /
# macOS (free does not exist on macOS):
uname -a && sysctl hw.memsize | awk '{printf "RAM: %.1f GB\n", $2/1073741824}' && df -h /
```

Confirm: Linux or macOS, 2 GB+ RAM, 10 GB+ free disk, internet access. If it passes, skip to the Completion check.

> **macOS note**: Phase 2 (Infrastructure) is written for Ubuntu/Debian — it uses `apt`, `ufw`, and `certbot`. macOS users will need to adapt those commands using Homebrew, and `ufw` does not apply. The adaptation is not guided step-by-step in this kit. If you want a fully tested, zero-adaptation path, use Ubuntu 24.04 on a VPS or spare machine.

---

### Decision guide (if no machine decided yet)

#### 1. Always-on requirement

Will OpenClaw need to be reachable 24/7, or is it acceptable for it to go offline when the machine is off?

- **24/7 required** → VPS or cloud VM (machine stays on regardless of what you do locally)
- **Personal / best-effort** → your own machine (desktop, laptop, NUC) works fine

#### 2. Budget

| Budget | Recommendation |
|---|---|
| ~€4–10/month | Hetzner CX22, DigitalOcean Basic Droplet, or Vultr |
| Already own a machine | Run it there — no ongoing hosting cost |
| Free tier | Oracle Cloud Always-Free (ARM64 VM, 1 GB RAM — tight but functional) |

#### 3. Hardware you already own

| Hardware | Verdict |
|---|---|
| Desktop PC / NUC / mini PC | Excellent — x86_64, typically 8+ GB RAM |
| Fanless mini PC or thin laptop (e.g. ASUS ZenBook) | Works — Phase 5 includes thermal monitoring |
| Laptop used daily | Possible — requires configuring no-suspend-on-lid-close (covered in Phase 3) |
| Raspberry Pi 4 (4 GB+) | Works — ARM64; cloudflared binary URL differs in Phase 4 |
| Raspberry Pi 3 or older | Not recommended — too slow for LLM gateway workloads |
| Mac (Intel or Apple Silicon) | Works — Phase 2 uses Homebrew instead of apt; ufw steps don't apply |

#### 4. Technical comfort

- Comfortable with Linux terminal → any option works
- Less comfortable → a fresh Ubuntu 24.04 VPS is the cleanest starting point; most guides are written for it
- No Linux experience → complete a basic terminal orientation before starting this kit

---

### Recommended paths

| Situation | Recommendation |
|---|---|
| Spare PC / NUC available | Run OpenClaw there. Low cost, full control. |
| Want 24/7 uptime without managing hardware | Hetzner CX22 (€4.15/mo) or DigitalOcean ($6/mo) |
| Daily-use laptop | Possible — configure lid-close behavior in Phase 3 |
| Raspberry Pi 4 (4 GB+) | Works — note ARM64 differences in Phase 2 |
| Mac (Intel or Apple Silicon) | Works — note Homebrew substitutions in Phase 2 |
| No machine, no budget | Oracle Cloud Free Tier — limited but free |

---

### OS selection

This kit is tested on **Ubuntu 24.04 LTS**. The infra steps (Phase 2) use `apt` and `ufw`.

| OS | Status |
|---|---|
| Ubuntu 20.04, 22.04, or 24.04 | Fully supported — follow skill files as written |
| Debian 11 or 12 | Fully supported — `apt` and `ufw` work identically |
| macOS 12+ (Intel or Apple Silicon) | Supported with adaptations — Phase 2 uses Homebrew; see notes in skill 02 |
| Raspberry Pi OS 64-bit | Supported — use ARM64 binary for cloudflared in Phase 4 |
| Windows (native) | Not supported — use WSL2 with Ubuntu and adapt Phase 2 |

If you are provisioning a fresh VPS and have no OS preference: choose **Ubuntu 24.04 LTS** — it is the tested path for this kit.

---

### If setting up a new VPS

1. Create a VPS with your chosen provider (Hetzner, DigitalOcean, Vultr, or similar)
2. Choose Ubuntu 24.04 LTS
3. Add your SSH public key during provisioning
4. Once provisioned, confirm you can SSH in:

```bash
ssh root@<your-server-ip>
```

Paste the first few lines of the welcome output. Once you are connected, the machine is ready.

---

## Completion check

Before moving to Orientation:

- [ ] Machine decided: `[bare metal / VPS / laptop / Raspberry Pi / Mac / other]`
- [ ] OS confirmed: `[Ubuntu 24.04 / Debian 12 / macOS / other]`
- [ ] At least 2 GB RAM and 10 GB free disk confirmed
- [ ] Terminal or SSH access confirmed — user can run a command and paste output

---

**Phase 0a complete.**

Once the machine is confirmed ready, say: *"Computing confirmed. Type `continue` when you're ready to start Orientation."*
