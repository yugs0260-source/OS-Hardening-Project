#!/usr/bin/env bash
# OS Hardening Assistant — System Update Script
# Run as: sudo bash update.sh

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "\n${CYAN}[*] OS Hardening Assistant — System Package Update${NC}"
echo "============================================================"

if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}[!] This script must be run as root (sudo).${NC}"
    exit 1
fi

# Detect package manager
if command -v apt-get &>/dev/null; then
    echo -e "${GREEN}[+] Detected APT package manager (Debian/Ubuntu)${NC}"

    echo -e "${GREEN}[+] Updating package lists...${NC}"
    apt-get update

    echo -e "${GREEN}[+] Upgrading installed packages...${NC}"
    apt-get upgrade -y

    echo -e "${GREEN}[+] Applying dist-upgrade (kernel, dependency changes)...${NC}"
    apt-get dist-upgrade -y

    echo -e "${GREEN}[+] Removing unused packages...${NC}"
    apt-get autoremove -y
    apt-get autoclean

    # Enable unattended security upgrades
    if ! dpkg -l unattended-upgrades &>/dev/null; then
        echo -e "${YELLOW}[+] Installing unattended-upgrades...${NC}"
        apt-get install -y unattended-upgrades
    fi
    echo -e "${GREEN}[+] Enabling automatic security upgrades...${NC}"
    dpkg-reconfigure --priority=low unattended-upgrades

elif command -v yum &>/dev/null; then
    echo -e "${GREEN}[+] Detected YUM package manager (RHEL/CentOS)${NC}"
    yum update -y
    yum upgrade -y

elif command -v dnf &>/dev/null; then
    echo -e "${GREEN}[+] Detected DNF package manager (Fedora/RHEL 8+)${NC}"
    dnf update -y
    dnf upgrade -y

else
    echo -e "${RED}[!] No supported package manager found.${NC}"
    exit 1
fi

echo -e "\n${GREEN}[OK] System update complete!${NC}"

# Check if reboot required (Debian/Ubuntu)
if [ -f /var/run/reboot-required ]; then
    echo -e "${YELLOW}[!] A system reboot is required to complete updates.${NC}"
    echo -e "    Run: sudo reboot\n"
else
    echo -e "    No reboot required.\n"
fi
