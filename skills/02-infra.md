# Skill 02 — Infrastructure

**Purpose**: Prepare the Ubuntu machine to run OpenClaw — Node.js, process manager, SSL, thermal monitoring.

**Input**: `deployment-brief.md` (from skill 01)  
**Output**: Verified ready machine — Node 24 installed, PM2 running, SSL in place (if domain available), `lm-sensors` installed if fanless

---

## Instructions

Read `deployment-brief.md` before starting. Adapt steps based on:
- `Fanless: yes` → install and configure `lm-sensors`
- `Domain: none` → skip SSL/certbot; use Telegram long-poll mode instead of webhooks
- `Hosting: VPS` → add firewall rules early; bare metal may already have them

Run all commands on the target machine (SSH in or use local terminal).

---

## Step 1 — System update

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git build-essential ufw lm-sensors
```

If fanless hardware, run sensors-detect now:
```bash
sudo sensors-detect --auto
sensors  # verify temperature readings are visible
```

Note current idle CPU temp. If already above 60°C at idle, flag to user before continuing.

---

## Step 2 — Node.js via nvm

Do not use apt's Node.js package (usually outdated).

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
nvm alias default 24
node --version   # must be v24.x.x
npm --version
```

---

## Step 3 — Install stress-ng (for thermal testing later)

```bash
sudo apt install -y stress-ng
```

PM2 is not needed — OpenClaw registers itself as a systemd service via `openclaw onboard --install-daemon` (skill 03).

---

## Step 4 — Firewall baseline

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

---

## Step 5 — SSL (only if domain is available)

Skip this step if `deployment-brief.md` shows `Domain: none`. Telegram long-poll mode does not require SSL.

```bash
sudo apt install -y certbot
sudo certbot certonly --standalone -d <your-domain>
# Note cert paths:
# /etc/letsencrypt/live/<your-domain>/fullchain.pem
# /etc/letsencrypt/live/<your-domain>/privkey.pem
```

Set up auto-renewal:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
sudo certbot renew --dry-run  # verify renewal works
```

---

## Step 6 — Directory structure

```bash
mkdir -p ~/openclaw
cd ~/openclaw
```

This will be the OpenClaw working directory for the rest of the kit.

---

## Completion check

Before marking this phase done:
- [ ] `node --version` returns v24.x.x
- [ ] `pm2 --version` returns a version
- [ ] `sudo ufw status` shows active with SSH + 80 + 443 open
- [ ] If fanless: `sensors` returns temperature readings
- [ ] If domain available: `sudo certbot renew --dry-run` succeeds
- [ ] `~/openclaw` directory exists
