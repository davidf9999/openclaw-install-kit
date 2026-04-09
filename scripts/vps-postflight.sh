#!/usr/bin/env bash
set -euo pipefail

# Collect post-install evidence for a VPS validation run.

if [[ -f "$HOME/.nvm/nvm.sh" ]]; then
  export NVM_DIR="$HOME/.nvm"
  # shellcheck disable=SC1090
  source "$NVM_DIR/nvm.sh"
fi

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
log_path="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"

echo "# VPS Postflight"
echo
echo "Collected: ${timestamp}"
echo

echo "## systemctl --user status openclaw-gateway"
systemctl --user status openclaw-gateway --no-pager || true
echo

echo "## systemctl --user is-enabled openclaw-gateway"
systemctl --user is-enabled openclaw-gateway || true
echo

echo "## loginctl show-user \$USER | grep Linger"
loginctl show-user "$USER" | grep Linger || true
echo

echo "## openclaw --version"
openclaw --version || true
echo

echo "## openclaw status --deep"
openclaw status --deep || true
echo

if [[ -f "${log_path}" ]]; then
  echo "## tail -30 ${log_path}"
  tail -30 "${log_path}" || true
else
  echo "## Log file not found"
  echo "${log_path}"
fi
