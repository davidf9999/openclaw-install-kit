# Skill 02 — Infrastructure

**Purpose**: Prepare the Ubuntu machine to run OpenClaw — Node.js, thermal monitoring, firewall, and working directory.

**Input**: `deployment-brief.md` (from skill 01)  
**Output**: Verified ready machine — Node 24 installed, firewall active, `lm-sensors` installed if fanless, `~/openclaw` directory exists

> **Phase 2 of 7 — Infrastructure**  
> Re-read `deployment-brief.md` before starting. Adapt steps based on `Fanless`, `Domain`, and `Hosting` fields.  
> You will run all commands yourself in your terminal. After each command block, paste the output back here so I can verify before we continue.  
> If you are re-entering this phase, say "resuming Phase 2" and paste the output of `node --version` so I can see where we left off.

---

## Instructions

Read `deployment-brief.md` before starting. Adapt steps based on:
- `Fanless: yes` → install and configure `lm-sensors`, check idle temps before continuing
- `Domain: none` → skip SSL/certbot entirely; Telegram long-poll mode does not need it
- `Hosting: VPS` → add firewall rules early; bare metal may already have them

---

## Step 1 — System update

Run this in your terminal and paste the output:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install -y curl git build-essential ufw lm-sensors stress-ng
```

This updates your system and installs required tools including `lm-sensors` (temperature monitoring) and `stress-ng` (thermal load testing for Phase 5).

**If fanless hardware**, also run:

```bash
sudo sensors-detect --auto && sensors
```

Paste the `sensors` output. I will check your idle CPU temperature before we continue. **If idle temp is above 60°C, stop and tell me — we need to address that before installing anything.**

---

## Step 2 — Node.js via nvm

Do not use the system apt Node.js package — it is usually outdated. Install via nvm:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
nvm alias default 24
```

Then verify:

```bash
node --version && npm --version
```

Paste the output. I need to see `v24.x.x` before we continue.

---

## Step 3 — Firewall baseline

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

Paste the `ufw status verbose` output.

---

## Step 4 — SSL (skip if `Domain: none`)

**Skip this step** if `deployment-brief.md` shows `Domain: none`. Telegram long-poll mode does not require SSL or a public endpoint.

If you do have a domain:

```bash
sudo apt install -y certbot
sudo certbot certonly --standalone -d <your-domain>
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
sudo certbot renew --dry-run
```

Paste the `certbot renew --dry-run` output to confirm auto-renewal works.

---

## Step 5 — Working directory

```bash
mkdir -p ~/openclaw && ls -la ~/openclaw
```

Paste the output to confirm the directory exists.

---

## Completion check

Before marking this phase done, paste the output of each:

- [ ] `node --version` → must show `v24.x.x`
- [ ] `sudo ufw status` → must show active with SSH + 80 + 443 open
- [ ] If fanless: `sensors` → temperature readings visible, idle temp below 60°C
- [ ] If domain: `sudo certbot renew --dry-run` → succeeds
- [ ] `ls ~/openclaw` → directory exists (may be empty)

---

**Phase 2 complete.**

Once all checks pass, say: *"Infrastructure is ready. Type `continue` when you're ready to start Phase 3 — OpenClaw Core Install."*
