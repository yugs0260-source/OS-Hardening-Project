#!/usr/bin/env bash
# OS Hardening Assistant — SSH Hardening Script
# Run as: sudo bash ssh.sh
#
# WARNING: Ensure SSH key-based auth is configured BEFORE running.
# Disabling password auth without a key WILL lock you out!

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

SSHD_CONFIG="/etc/ssh/sshd_config"
BACKUP="${SSHD_CONFIG}.backup.$(date +%Y%m%d%H%M%S)"

echo -e "\n${CYAN}[*] OS Hardening Assistant — SSH Hardening${NC}"
echo "============================================================"
echo -e "${YELLOW}[!] WARNING: Ensure SSH keys are set up before proceeding!${NC}"
echo -e "${YELLOW}    Disabling password auth without keys = lockout!${NC}"

if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}[!] Must run as root.${NC}"; exit 1
fi

# Backup existing config
echo -e "\n${GREEN}[+] Backing up current sshd_config to: ${BACKUP}${NC}"
cp "$SSHD_CONFIG" "$BACKUP"

# Helper function to set or add an SSH config directive
set_ssh_option() {
    local key="$1"
    local value="$2"
    if grep -qE "^#?${key}" "$SSHD_CONFIG"; then
        sed -i "s/^#*\s*${key}.*/${key} ${value}/" "$SSHD_CONFIG"
    else
        echo "${key} ${value}" >> "$SSHD_CONFIG"
    fi
    echo -e "    ${key} = ${value}"
}

echo -e "${GREEN}[+] Applying SSH hardening settings:${NC}"
set_ssh_option "PermitRootLogin"          "no"
set_ssh_option "PasswordAuthentication"   "no"
set_ssh_option "ChallengeResponseAuthentication" "no"
set_ssh_option "X11Forwarding"            "no"
set_ssh_option "MaxAuthTries"             "3"
set_ssh_option "AllowTcpForwarding"       "no"
set_ssh_option "ClientAliveInterval"      "300"
set_ssh_option "ClientAliveCountMax"      "2"
set_ssh_option "LoginGraceTime"           "30"
set_ssh_option "PermitEmptyPasswords"     "no"
set_ssh_option "UsePAM"                   "yes"
set_ssh_option "Protocol"                 "2"

# Test the config before restarting
echo -e "\n${GREEN}[+] Testing SSH config...${NC}"
if sshd -t -f "$SSHD_CONFIG"; then
    echo -e "${GREEN}    Config test passed.${NC}"
    echo -e "${GREEN}[+] Restarting SSH service...${NC}"
    systemctl restart sshd || systemctl restart ssh
    echo -e "${GREEN}[OK] SSH hardening complete!${NC}"
else
    echo -e "${RED}[!] SSH config test FAILED! Restoring backup...${NC}"
    cp "$BACKUP" "$SSHD_CONFIG"
    echo -e "${RED}    Original config restored. No changes made.${NC}"
    exit 1
fi

echo -e "\n${CYAN}[*] Current SSH config (key settings):${NC}"
grep -E "^(PermitRootLogin|PasswordAuthentication|MaxAuthTries|X11Forwarding|Protocol)" "$SSHD_CONFIG"
echo ""
