#!/usr/bin/env bash
# OS Hardening Assistant — Install & Configure Fail2ban
# Run as: sudo bash fail2ban.sh

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "\n${CYAN}[*] OS Hardening Assistant — Fail2ban Setup${NC}"
echo "============================================================"

if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}[!] Must run as root.${NC}"; exit 1
fi

# Install fail2ban
if ! command -v fail2ban-server &>/dev/null; then
    echo -e "${GREEN}[+] Installing fail2ban...${NC}"
    apt-get update -qq
    apt-get install -y fail2ban
else
    echo -e "${GREEN}[+] fail2ban already installed.${NC}"
fi

# Create local jail configuration (override defaults)
JAIL_LOCAL="/etc/fail2ban/jail.local"

echo -e "${GREEN}[+] Writing jail.local configuration...${NC}"
cat > "$JAIL_LOCAL" <<'EOF'
[DEFAULT]
# Ban duration: 1 hour
bantime  = 3600
# Detection window: 10 minutes
findtime = 600
# Max retries before ban
maxretry = 3
# Backend (auto = systemd if available, else polling)
backend  = auto
# Ban action
banaction = iptables-multiport
# Ignore local traffic
ignoreip = 127.0.0.1/8 ::1

[sshd]
enabled  = true
port     = ssh
logpath  = %(sshd_log)s
maxretry = 3
bantime  = 7200

[sshd-ddos]
enabled  = true
port     = ssh
logpath  = %(sshd_log)s
maxretry = 6
findtime = 60
bantime  = 86400

[pam-generic]
enabled  = true
logpath  = %(syslog_authpriv)s
EOF

echo -e "${GREEN}[+] Starting and enabling fail2ban service...${NC}"
systemctl start  fail2ban
systemctl enable fail2ban

# Show status
echo -e "\n${CYAN}[*] Fail2ban service status:${NC}"
systemctl status fail2ban --no-pager -l || true

echo -e "\n${CYAN}[*] Active jails:${NC}"
fail2ban-client status 2>/dev/null || echo "    (fail2ban still starting...)"

echo -e "\n${GREEN}[OK] Fail2ban configured and running!${NC}"
echo -e "     Check SSH jail: sudo fail2ban-client status sshd"
echo -e "     Unban an IP:    sudo fail2ban-client set sshd unbanip <IP>\n"
