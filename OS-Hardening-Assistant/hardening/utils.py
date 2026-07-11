"""
utils.py — Helper functions for the OS Hardening Assistant.
"""

import platform
import datetime


def get_os_type() -> str:
    """Return 'windows' or 'linux' based on the current host OS."""
    system = platform.system().lower()
    if 'windows' in system:
        return 'windows'
    return 'linux'


def get_os_info() -> dict:
    """Return detailed OS information."""
    return {
        'type': get_os_type(),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'node': platform.node(),
    }


def format_status_badge(status: str) -> str:
    """Return an HTML badge string for a given status."""
    badges = {
        'secure': '<span class="badge badge-secure">✓ Secure</span>',
        'warning': '<span class="badge badge-warning">⚠ Warning</span>',
        'danger': '<span class="badge badge-danger">✗ Danger</span>',
        'unknown': '<span class="badge badge-unknown">? Unknown</span>',
    }
    return badges.get(status, badges['unknown'])


def get_status_color(status: str) -> str:
    """Return a CSS color class for a status."""
    colors = {
        'secure': 'text-secure',
        'warning': 'text-warning',
        'danger': 'text-danger',
        'unknown': 'text-muted',
    }
    return colors.get(status, 'text-muted')


def get_score_grade(score: int) -> dict:
    """Return grade letter and label for a security score."""
    if score >= 90:
        return {'grade': 'A', 'label': 'Excellent', 'color': '#00f5a0'}
    elif score >= 75:
        return {'grade': 'B', 'label': 'Good', 'color': '#7fff00'}
    elif score >= 60:
        return {'grade': 'C', 'label': 'Fair', 'color': '#ffd700'}
    elif score >= 40:
        return {'grade': 'D', 'label': 'Poor', 'color': '#ff8c00'}
    else:
        return {'grade': 'F', 'label': 'Critical', 'color': '#ff3366'}


def build_report_context(checks: dict, platform_name: str) -> dict:
    """Build context dict for report templates."""
    from .checker import compute_security_score
    score = compute_security_score(checks)
    grade = get_score_grade(score)
    total = len(checks)
    secure_count = sum(1 for c in checks.values() if c.get('status') == 'secure')
    warning_count = sum(1 for c in checks.values() if c.get('status') == 'warning')
    danger_count = sum(1 for c in checks.values() if c.get('status') == 'danger')

    return {
        'platform': platform_name,
        'checks': checks,
        'score': score,
        'grade': grade,
        'total_checks': total,
        'secure_count': secure_count,
        'warning_count': warning_count,
        'danger_count': danger_count,
        'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'os_info': get_os_info(),
    }


def get_hardening_checklist(platform_name: str) -> list:
    """Return a hardening checklist for the given platform."""
    windows_checklist = [
        {'id': 'wf1', 'category': 'Firewall', 'task': 'Enable Windows Firewall for all profiles', 'priority': 'high'},
        {'id': 'wf2', 'category': 'Firewall', 'task': 'Configure inbound rules — default deny', 'priority': 'high'},
        {'id': 'wf3', 'category': 'Firewall', 'task': 'Review and remove unnecessary firewall rules', 'priority': 'medium'},
        {'id': 'wd1', 'category': 'Defender', 'task': 'Enable Windows Defender real-time protection', 'priority': 'high'},
        {'id': 'wd2', 'category': 'Defender', 'task': 'Update virus definitions', 'priority': 'high'},
        {'id': 'wd3', 'category': 'Defender', 'task': 'Enable cloud-delivered protection', 'priority': 'medium'},
        {'id': 'wu1', 'category': 'Updates', 'task': 'Install all pending Windows Updates', 'priority': 'high'},
        {'id': 'wu2', 'category': 'Updates', 'task': 'Enable automatic updates', 'priority': 'high'},
        {'id': 'wu3', 'category': 'Updates', 'task': 'Enable Windows Update for other Microsoft products', 'priority': 'medium'},
        {'id': 'wa1', 'category': 'Accounts', 'task': 'Disable default Administrator account', 'priority': 'high'},
        {'id': 'wa2', 'category': 'Accounts', 'task': 'Audit local administrator accounts', 'priority': 'high'},
        {'id': 'wa3', 'category': 'Accounts', 'task': 'Enforce strong password policy', 'priority': 'medium'},
        {'id': 'ws1', 'category': 'Services', 'task': 'Disable SMBv1 protocol', 'priority': 'high'},
        {'id': 'ws2', 'category': 'Services', 'task': 'Enable BitLocker disk encryption', 'priority': 'medium'},
        {'id': 'ws3', 'category': 'Services', 'task': 'Disable Remote Desktop if not needed', 'priority': 'medium'},
        {'id': 'ws4', 'category': 'Services', 'task': 'Disable Telnet and other legacy services', 'priority': 'high'},
    ]

    linux_checklist = [
        {'id': 'lf1', 'category': 'Firewall', 'task': 'Enable UFW with default deny inbound', 'priority': 'high'},
        {'id': 'lf2', 'category': 'Firewall', 'task': 'Allow only required ports', 'priority': 'high'},
        {'id': 'lf3', 'category': 'Firewall', 'task': 'Enable firewall logging', 'priority': 'medium'},
        {'id': 'lu1', 'category': 'Updates', 'task': 'Run apt update && apt upgrade', 'priority': 'high'},
        {'id': 'lu2', 'category': 'Updates', 'task': 'Enable unattended security upgrades', 'priority': 'high'},
        {'id': 'lu3', 'category': 'Updates', 'task': 'Remove unused packages', 'priority': 'medium'},
        {'id': 'ls1', 'category': 'SSH', 'task': 'Disable SSH root login', 'priority': 'high'},
        {'id': 'ls2', 'category': 'SSH', 'task': 'Disable SSH password authentication', 'priority': 'high'},
        {'id': 'ls3', 'category': 'SSH', 'task': 'Change SSH default port', 'priority': 'medium'},
        {'id': 'ls4', 'category': 'SSH', 'task': 'Set MaxAuthTries to 3', 'priority': 'medium'},
        {'id': 'ls5', 'category': 'SSH', 'task': 'Disable X11 forwarding', 'priority': 'low'},
        {'id': 'lb1', 'category': 'Fail2ban', 'task': 'Install and enable fail2ban', 'priority': 'high'},
        {'id': 'lb2', 'category': 'Fail2ban', 'task': 'Configure SSH jail in fail2ban', 'priority': 'high'},
        {'id': 'lb3', 'category': 'Fail2ban', 'task': 'Set ban time to at least 1 hour', 'priority': 'medium'},
        {'id': 'la1', 'category': 'Accounts', 'task': 'Audit sudo users (visudo)', 'priority': 'high'},
        {'id': 'la2', 'category': 'Accounts', 'task': 'Disable unused user accounts', 'priority': 'medium'},
        {'id': 'la3', 'category': 'Accounts', 'task': 'Enforce strong password policy', 'priority': 'medium'},
    ]

    return windows_checklist if platform_name == 'windows' else linux_checklist
