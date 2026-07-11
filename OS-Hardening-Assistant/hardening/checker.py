"""
checker.py — Real-time OS security status checks.

Each function returns a dict:
{
    'status': 'secure' | 'warning' | 'danger' | 'unknown',
    'title':  str,
    'detail': str,
    'recommendation': str,
    'score': int  (0-100)
}
"""

import platform
import subprocess
import sys


def _run(cmd, shell=False, timeout=10):
    """Run a command and return (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=shell,
            timeout=timeout,
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return '', 'Command unavailable', -1


# ─────────────────────────────────────────────
# Windows Checks
# ─────────────────────────────────────────────

def check_windows_firewall():
    """Check Windows Firewall status for all profiles."""
    stdout, _, rc = _run(
        ['powershell', '-Command',
         'Get-NetFirewallProfile | Select-Object -Property Name,Enabled | ConvertTo-Json'],
        timeout=15,
    )
    if rc != 0 or not stdout:
        return {
            'status': 'unknown',
            'title': 'Windows Firewall',
            'detail': 'Could not query firewall status. Ensure PowerShell is available.',
            'recommendation': 'Run: netsh advfirewall set allprofiles state on',
            'score': 0,
        }

    import json
    try:
        profiles = json.loads(stdout)
        if isinstance(profiles, dict):
            profiles = [profiles]

        all_enabled = all(p.get('Enabled', False) for p in profiles)
        profile_info = ', '.join(
            f"{p['Name']}: {'✓' if p['Enabled'] else '✗'}" for p in profiles
        )

        if all_enabled:
            return {
                'status': 'secure',
                'title': 'Windows Firewall',
                'detail': f'All profiles enabled — {profile_info}',
                'recommendation': 'Firewall is properly configured.',
                'score': 100,
            }
        else:
            return {
                'status': 'danger',
                'title': 'Windows Firewall',
                'detail': f'Some profiles disabled — {profile_info}',
                'recommendation': 'Enable all firewall profiles immediately.',
                'score': 20,
            }
    except (json.JSONDecodeError, KeyError):
        return {
            'status': 'warning',
            'title': 'Windows Firewall',
            'detail': 'Firewall queried but result could not be parsed.',
            'recommendation': 'Verify firewall status manually in Windows Security.',
            'score': 50,
        }


def check_windows_defender():
    """Check Windows Defender / antivirus status."""
    stdout, _, rc = _run(
        ['powershell', '-Command',
         'Get-MpComputerStatus | Select-Object -Property RealTimeProtectionEnabled,AntivirusEnabled,AntispywareEnabled,NISEnabled | ConvertTo-Json'],
        timeout=15,
    )
    if rc != 0 or not stdout:
        return {
            'status': 'unknown',
            'title': 'Windows Defender',
            'detail': 'Could not query Defender status. May not be available or requires elevation.',
            'recommendation': 'Open Windows Security and verify Defender is enabled.',
            'score': 0,
        }

    import json
    try:
        status = json.loads(stdout)
        rtp = status.get('RealTimeProtectionEnabled', False)
        av = status.get('AntivirusEnabled', False)

        if rtp and av:
            return {
                'status': 'secure',
                'title': 'Windows Defender',
                'detail': 'Real-time protection enabled. Antivirus active.',
                'recommendation': 'Ensure virus definitions are up to date.',
                'score': 100,
            }
        elif av:
            return {
                'status': 'warning',
                'title': 'Windows Defender',
                'detail': 'Antivirus enabled but Real-time protection is OFF.',
                'recommendation': 'Enable real-time protection in Windows Security.',
                'score': 50,
            }
        else:
            return {
                'status': 'danger',
                'title': 'Windows Defender',
                'detail': 'Windows Defender is disabled.',
                'recommendation': 'Enable Windows Defender immediately.',
                'score': 0,
            }
    except (json.JSONDecodeError, KeyError):
        return {
            'status': 'warning',
            'title': 'Windows Defender',
            'detail': 'Defender status queried but could not be fully parsed.',
            'recommendation': 'Verify Defender status in Windows Security Center.',
            'score': 50,
        }


def check_windows_updates():
    """Check for pending Windows Updates."""
    stdout, _, rc = _run(
        ['powershell', '-Command',
         '(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0 and Type=\'Software\'").Updates.Count'],
        timeout=30,
    )
    if rc != 0 or not stdout:
        return {
            'status': 'unknown',
            'title': 'Windows Updates',
            'detail': 'Could not query Windows Update. May require elevated privileges.',
            'recommendation': 'Run Windows Update manually via Settings > Update & Security.',
            'score': 0,
        }

    try:
        count = int(stdout.strip())
        if count == 0:
            return {
                'status': 'secure',
                'title': 'Windows Updates',
                'detail': 'System is fully up to date. No pending updates.',
                'recommendation': 'Continue checking for updates regularly.',
                'score': 100,
            }
        elif count <= 5:
            return {
                'status': 'warning',
                'title': 'Windows Updates',
                'detail': f'{count} pending update(s) found.',
                'recommendation': 'Install pending updates soon via Windows Update.',
                'score': 60,
            }
        else:
            return {
                'status': 'danger',
                'title': 'Windows Updates',
                'detail': f'{count} pending updates found — system is significantly out of date.',
                'recommendation': 'Install all updates immediately to patch vulnerabilities.',
                'score': 10,
            }
    except ValueError:
        return {
            'status': 'unknown',
            'title': 'Windows Updates',
            'detail': 'Could not parse update count.',
            'recommendation': 'Check Windows Update manually.',
            'score': 0,
        }


def check_windows_users():
    """Check for local administrator accounts."""
    stdout, _, rc = _run(
        ['powershell', '-Command',
         'Get-LocalGroupMember -Group "Administrators" | Select-Object Name,PrincipalSource | ConvertTo-Json'],
        timeout=15,
    )
    if rc != 0 or not stdout:
        return {
            'status': 'unknown',
            'title': 'User Accounts',
            'detail': 'Could not enumerate local administrators.',
            'recommendation': 'Review local administrator accounts via Computer Management.',
            'score': 0,
        }

    import json
    try:
        members = json.loads(stdout)
        if isinstance(members, dict):
            members = [members]

        count = len(members)
        names = [m.get('Name', 'Unknown') for m in members]

        if count <= 2:
            return {
                'status': 'secure',
                'title': 'User Accounts',
                'detail': f'{count} administrator(s): {", ".join(names)}',
                'recommendation': 'Good. Minimize administrator account count.',
                'score': 90,
            }
        elif count <= 4:
            return {
                'status': 'warning',
                'title': 'User Accounts',
                'detail': f'{count} administrators found: {", ".join(names)}',
                'recommendation': 'Review and remove unnecessary admin accounts.',
                'score': 50,
            }
        else:
            return {
                'status': 'danger',
                'title': 'User Accounts',
                'detail': f'{count} administrators! {", ".join(names)}',
                'recommendation': 'Too many admin accounts. Remove unnecessary privileges immediately.',
                'score': 10,
            }
    except (json.JSONDecodeError, KeyError):
        return {
            'status': 'warning',
            'title': 'User Accounts',
            'detail': 'Administrator accounts found but could not be fully enumerated.',
            'recommendation': 'Manually review accounts via Computer Management.',
            'score': 40,
        }


# ─────────────────────────────────────────────
# Linux Checks
# ─────────────────────────────────────────────

def check_linux_ufw():
    """Check UFW (Uncomplicated Firewall) status."""
    stdout, _, rc = _run(['sudo', '-n', 'ufw', 'status'], timeout=10)
    if rc != 0:
        # Try without sudo
        stdout, _, rc = _run(['ufw', 'status'], timeout=10)

    if 'active' in stdout.lower():
        return {
            'status': 'secure',
            'title': 'UFW Firewall',
            'detail': 'UFW is active and running.',
            'recommendation': 'Ensure only required ports are open.',
            'score': 100,
        }
    elif 'inactive' in stdout.lower():
        return {
            'status': 'danger',
            'title': 'UFW Firewall',
            'detail': 'UFW is installed but inactive.',
            'recommendation': 'Run: sudo ufw enable',
            'score': 0,
        }
    else:
        return {
            'status': 'unknown',
            'title': 'UFW Firewall',
            'detail': 'UFW status could not be determined. May not be installed.',
            'recommendation': 'Install UFW: sudo apt install ufw && sudo ufw enable',
            'score': 0,
        }


def check_linux_ssh():
    """Check SSH hardening configuration."""
    ssh_config = '/etc/ssh/sshd_config'
    issues = []
    score = 100

    try:
        with open(ssh_config, 'r') as f:
            config_text = f.read()
    except (PermissionError, FileNotFoundError):
        return {
            'status': 'unknown',
            'title': 'SSH Configuration',
            'detail': f'Cannot read {ssh_config}. Requires root privileges.',
            'recommendation': 'Run as root or with sudo to check SSH config.',
            'score': 0,
        }

    checks = {
        'PermitRootLogin no': ('Root login allowed', 30),
        'PasswordAuthentication no': ('Password auth enabled (use keys)', 30),
        'X11Forwarding no': ('X11 forwarding enabled', 10),
        'MaxAuthTries': ('No MaxAuthTries limit set', 10),
    }

    for setting, (msg, penalty) in checks.items():
        key = setting.split()[0]
        if key not in config_text:
            issues.append(msg)
            score -= penalty

    if not issues:
        return {
            'status': 'secure',
            'title': 'SSH Configuration',
            'detail': 'SSH is properly hardened.',
            'recommendation': 'Continue using key-based authentication only.',
            'score': 100,
        }
    elif score >= 60:
        return {
            'status': 'warning',
            'title': 'SSH Configuration',
            'detail': f'Issues found: {"; ".join(issues)}',
            'recommendation': 'Review /etc/ssh/sshd_config and apply hardening.',
            'score': max(score, 0),
        }
    else:
        return {
            'status': 'danger',
            'title': 'SSH Configuration',
            'detail': f'Critical issues: {"; ".join(issues)}',
            'recommendation': 'Immediately harden SSH — disable root login and password auth.',
            'score': max(score, 0),
        }


def check_linux_fail2ban():
    """Check if fail2ban is installed and running."""
    stdout, _, rc = _run(['systemctl', 'is-active', 'fail2ban'], timeout=10)

    if stdout.strip() == 'active':
        return {
            'status': 'secure',
            'title': 'Fail2ban',
            'detail': 'Fail2ban is active and protecting against brute-force.',
            'recommendation': 'Verify jail configuration with: sudo fail2ban-client status',
            'score': 100,
        }
    elif rc == 0 and stdout.strip() == 'inactive':
        return {
            'status': 'warning',
            'title': 'Fail2ban',
            'detail': 'Fail2ban is installed but not running.',
            'recommendation': 'Start fail2ban: sudo systemctl start fail2ban && sudo systemctl enable fail2ban',
            'score': 30,
        }
    else:
        return {
            'status': 'danger',
            'title': 'Fail2ban',
            'detail': 'Fail2ban is not installed or not found.',
            'recommendation': 'Install fail2ban: sudo apt install fail2ban',
            'score': 0,
        }


def check_linux_updates():
    """Check for available system updates."""
    stdout, _, rc = _run(['apt', 'list', '--upgradable'], timeout=30)

    if rc != 0:
        # Try yum/dnf
        stdout, _, rc = _run(['yum', 'check-update'], timeout=30)

    if rc == -1:
        return {
            'status': 'unknown',
            'title': 'System Updates',
            'detail': 'Could not determine pending updates. Package manager unavailable.',
            'recommendation': 'Manually check for updates.',
            'score': 0,
        }

    lines = [l for l in stdout.splitlines() if '/' in l]
    count = len(lines)

    if count == 0:
        return {
            'status': 'secure',
            'title': 'System Updates',
            'detail': 'System is up to date.',
            'recommendation': 'Continue applying updates regularly.',
            'score': 100,
        }
    elif count <= 10:
        return {
            'status': 'warning',
            'title': 'System Updates',
            'detail': f'{count} package(s) can be upgraded.',
            'recommendation': 'Run: sudo apt update && sudo apt upgrade',
            'score': 60,
        }
    else:
        return {
            'status': 'danger',
            'title': 'System Updates',
            'detail': f'{count} packages need updating — system is significantly outdated.',
            'recommendation': 'Run: sudo apt update && sudo apt upgrade -y immediately.',
            'score': 10,
        }


# ─────────────────────────────────────────────
# Aggregated checks
# ─────────────────────────────────────────────

def get_all_windows_checks():
    """Return all Windows security checks."""
    return {
        'firewall': check_windows_firewall(),
        'defender': check_windows_defender(),
        'updates': check_windows_updates(),
        'users': check_windows_users(),
    }


def get_all_linux_checks():
    """Return all Linux security checks."""
    return {
        'firewall': check_linux_ufw(),
        'ssh': check_linux_ssh(),
        'fail2ban': check_linux_fail2ban(),
        'updates': check_linux_updates(),
    }


def compute_security_score(checks: dict) -> int:
    """Compute overall security score (0-100) from a checks dict."""
    scores = [v.get('score', 0) for v in checks.values()]
    if not scores:
        return 0
    return round(sum(scores) / len(scores))
