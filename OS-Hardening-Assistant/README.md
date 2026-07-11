# OS Hardening Assistant

A Django-based web application for hardening Windows and Linux operating systems. Provides a security checklist dashboard, real-time OS status checks, one-click hardening scripts, and printable security reports.

## Features

- 🛡️ **OS Detection** — Auto-detects Windows or Linux
- 🔥 **Firewall Hardening** — Windows Firewall / UFW configuration
- 🦠 **Antivirus** — Windows Defender status and configuration
- 🔄 **Updates** — Automated update checks and enforcement
- 👥 **User Auditing** — Privileged account review
- 🔐 **SSH Hardening** (Linux) — Secure SSH configuration
- 🚫 **Fail2ban** (Linux) — Brute-force protection
- 📊 **Reports** — Printable security posture reports
- 📋 **Scripts** — Ready-to-run PowerShell and Bash hardening scripts

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/OS-Hardening-Assistant.git
cd OS-Hardening-Assistant

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
OS-Hardening-Assistant/
├── os_hardening/        # Django project settings
├── hardening/           # Main Django app
├── templates/           # HTML templates
├── static/              # CSS, JS, images, icons
├── scripts/             # PowerShell & Bash hardening scripts
└── reports/             # Generated reports & logs
```

## Script Usage

> ⚠️ **Warning**: Hardening scripts modify system configuration. Always test in a non-production environment first. Run PowerShell scripts as Administrator and Bash scripts with sudo.

### Windows (PowerShell — Run as Administrator)
```powershell
.\scripts\windows\firewall.ps1
.\scripts\windows\defender.ps1
.\scripts\windows\updates.ps1
.\scripts\windows\bitlocker.ps1
.\scripts\windows\smb_disable.ps1
```

### Linux (Bash — Run with sudo)
```bash
sudo bash scripts/linux/firewall.sh
sudo bash scripts/linux/update.sh
sudo bash scripts/linux/ssh.sh
sudo bash scripts/linux/fail2ban.sh
sudo bash scripts/linux/cleanup.sh
```

## License

MIT License — see [LICENSE](LICENSE) for details.
