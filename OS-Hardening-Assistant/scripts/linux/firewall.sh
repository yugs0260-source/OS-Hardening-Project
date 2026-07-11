#!/usr/bin/env bash
# OS Hardening Assistant — UFW Firewall Configuration
# Run as: sudo bash firewall.sh

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

echo -e "\n${CYAN}[*] OS Hardening Assistant — UFW Firewall Hardening${NC}"
echo "============================================================"

# Check root
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}[!] This script must be run as root (sudo).${NC}"
    exit 1
fi

# Install UFW if not present
if ! command -v ufw &>/dev/null; then
    echo -e "${YELLOW}[+] UFW not found. Installing...${NC}"
    apt-get update -qq
    apt-get install -y ufw
fi

# Reset to defaults
echo -e "${GREEN}[+] Resetting UFW to defaults...${NC}"
ufw --force reset

# Set default policies
echo -e "${GREEN}[+] Setting default policies: deny inbound, allow outbound...${NC}"
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (prevent lockout)
echo -e "${GREEN}[+] Allowing SSH (port 22)...${NC}"
ufw allow ssh

# Optional: allow common services (uncomment as needed)
# ufw allow http   # Port 80
# ufw allow https  # Port 443
# ufw allow 3306   # MySQL
# ufw allow 5432   # PostgreSQL

# Enable UFW
echo -e "${GREEN}[+] Enabling UFW...${NC}"
ufw --force enable

# Enable UFW at boot
systemctl enable ufw

# Show status
echo -e "\n${CYAN}[*] Current UFW Status:${NC}"
ufw status verbose

echo -e "\n${GREEN}[OK] UFW firewall hardening complete!${NC}"
echo -e "     Add additional rules with: sudo ufw allow <port>\n"
