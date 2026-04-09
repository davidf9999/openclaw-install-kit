#!/usr/bin/env bash
set -euo pipefail

# Gather baseline machine facts for a VPS validation run.

PROVIDER="${1:-DigitalOcean}"
REGION="${2:-unknown}"
SCOPE="${3:-Telegram only}"

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
hostname_value="$(hostname 2>/dev/null || true)"
user_value="$(whoami 2>/dev/null || true)"
kernel="$(uname -a 2>/dev/null || true)"
os_release="$(lsb_release -a 2>/dev/null || true)"
ram="$(free -h 2>/dev/null || true)"
disk_root="$(df -h / 2>/dev/null || true)"
public_ip="$(
  curl -4 -fsS https://ifconfig.me 2>/dev/null \
  || curl -4 -fsS https://api.ipify.org 2>/dev/null \
  || printf 'unknown'
)"

cat <<EOF
# VPS Preflight

Collected: ${timestamp}
Provider: ${PROVIDER}
Region: ${REGION}
Hostname: ${hostname_value}
User: ${user_value}
Public IP: ${public_ip}
Scope: ${SCOPE}

## OS
${os_release}

## Kernel
${kernel}

## RAM
${ram}

## Disk
${disk_root}

## Suggested TESTING.md snippet
- Date: ${timestamp}
- Provider: ${PROVIDER}
- Region: ${REGION}
- Public IP: ${public_ip}
- Scope tested: ${SCOPE}
EOF
