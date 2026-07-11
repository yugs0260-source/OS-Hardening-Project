#!/usr/bin/env bash
# OS Hardening Assistant — System Cleanup
# Run as: sudo bash cleanup.sh

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "\n${CYAN}[*] OS Hardening Assistant — System Cleanup${NC}"
echo "============================================================"

if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}[!] Must run as root.${NC}"; exit 1
fi

# Packages to remove (attack surface reduction)
PACKAGES_TO_REMOVE=(
    "telnet"
    "rsh-client"
    "rsh-server"
    "nis"
    "xinetd"
    "inetd"
    "talk"
    "talkd"
    "finger"
)

echo -e "${GREEN}[+] Removing unnecessary/insecure packages...${NC}"
for pkg in "${PACKAGES_TO_REMOVE[@]}"; do
    if dpkg -l "$pkg" &>/dev/null 2>&1; then
        echo -e "    Removing: $pkg"
        apt-get remove -y "$pkg" 2>/dev/null || true
    else
        echo -e "    ${YELLOW}Not installed: $pkg${NC}"
    fi
done

# Remove orphaned packages
echo -e "\n${GREEN}[+] Removing orphaned packages...${NC}"
apt-get autoremove -y

# Clean package cache
echo -e "${GREEN}[+] Cleaning package cache...${NC}"
apt-get autoclean
apt-get clean

# Remove old log files (>30 days)
echo -e "${GREEN}[+] Cleaning old log files (> 30 days)...${NC}"
find /var/log -type f -name "*.log" -mtime +30 -delete 2>/dev/null || true
find /var/log -type f -name "*.gz"  -mtime +7  -delete 2>/dev/null || true

# Clear bash history for root
echo -e "${GREEN}[+] Clearing root bash history...${NC}"
history -c
cat /dev/null > ~/.bash_history

# Disable core dumps
echo -e "${GREEN}[+] Disabling core dumps...${NC}"
echo "* hard core 0" >> /etc/security/limits.conf
echo "fs.suid_dumpable = 0" >> /etc/sysctl.conf
sysctl -p /etc/sysctl.conf &>/dev/null || true

# Restrict /tmp
echo -e "${GREEN}[+] Setting /tmp permissions...${NC}"
chmod 1777 /tmp

echo -e "\n${GREEN}[OK] System cleanup complete!${NC}"
echo -e "     Removed insecure services, cleaned cache, and reduced attack surface.\n"
