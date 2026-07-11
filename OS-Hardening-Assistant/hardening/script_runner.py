"""
script_runner.py — Script content reader and metadata provider.

Scripts are displayed to users for manual execution, not auto-run,
to avoid unintended system modification. Users can copy or download
scripts from the UI.
"""

import os
from pathlib import Path
from django.conf import settings


SCRIPT_METADATA = {
    # Windows scripts
    'windows/firewall': {
        'name': 'Enable & Configure Windows Firewall',
        'file': 'windows/firewall.ps1',
        'platform': 'windows',
        'shell': 'PowerShell (Run as Administrator)',
        'risk': 'low',
        'description': 'Enables Windows Firewall for all profiles (Domain, Private, Public) and sets default-deny inbound rules.',
        'icon': 'firewall',
    },
    'windows/defender': {
        'name': 'Enable Windows Defender',
        'file': 'windows/defender.ps1',
        'platform': 'windows',
        'shell': 'PowerShell (Run as Administrator)',
        'risk': 'low',
        'description': 'Enables Windows Defender real-time protection and triggers a signature update.',
        'icon': 'shield',
    },
    'windows/updates': {
        'name': 'Force Windows Update Check',
        'file': 'windows/updates.ps1',
        'platform': 'windows',
        'shell': 'PowerShell (Run as Administrator)',
        'risk': 'low',
        'description': 'Forces an immediate Windows Update check and installs available updates.',
        'icon': 'update',
    },
    'windows/bitlocker': {
        'name': 'Enable BitLocker Drive Encryption',
        'file': 'windows/bitlocker.ps1',
        'platform': 'windows',
        'shell': 'PowerShell (Run as Administrator)',
        'risk': 'medium',
        'description': 'Enables BitLocker encryption on the C: drive. Back up your recovery key!',
        'icon': 'shield',
    },
    'windows/smb_disable': {
        'name': 'Disable SMBv1 Protocol',
        'file': 'windows/smb_disable.ps1',
        'platform': 'windows',
        'shell': 'PowerShell (Run as Administrator)',
        'risk': 'low',
        'description': 'Disables the insecure SMBv1 protocol (WannaCry/EternalBlue mitigation).',
        'icon': 'terminal',
    },
    # Linux scripts
    'linux/firewall': {
        'name': 'Enable UFW Firewall',
        'file': 'linux/firewall.sh',
        'platform': 'linux',
        'shell': 'Bash (sudo)',
        'risk': 'low',
        'description': 'Enables UFW with default-deny inbound policy, allowing only SSH (port 22).',
        'icon': 'firewall',
    },
    'linux/update': {
        'name': 'Update & Upgrade System Packages',
        'file': 'linux/update.sh',
        'platform': 'linux',
        'shell': 'Bash (sudo)',
        'risk': 'low',
        'description': 'Runs apt update and apt upgrade to install all available security patches.',
        'icon': 'update',
    },
    'linux/ssh': {
        'name': 'Harden SSH Configuration',
        'file': 'linux/ssh.sh',
        'platform': 'linux',
        'shell': 'Bash (sudo)',
        'risk': 'medium',
        'description': 'Hardens /etc/ssh/sshd_config — disables root login, password auth, and X11 forwarding.',
        'icon': 'terminal',
    },
    'linux/fail2ban': {
        'name': 'Install & Configure Fail2ban',
        'file': 'linux/fail2ban.sh',
        'platform': 'linux',
        'shell': 'Bash (sudo)',
        'risk': 'low',
        'description': 'Installs fail2ban and configures SSH jail to block brute-force attacks.',
        'icon': 'shield',
    },
    'linux/cleanup': {
        'name': 'System Cleanup',
        'file': 'linux/cleanup.sh',
        'platform': 'linux',
        'shell': 'Bash (sudo)',
        'risk': 'low',
        'description': 'Removes unnecessary packages and cleans the apt cache to reduce attack surface.',
        'icon': 'terminal',
    },
}


def get_script_content(script_key: str) -> dict:
    """
    Read and return the content of a hardening script.

    Returns dict with keys: content, metadata, error
    """
    meta = SCRIPT_METADATA.get(script_key)
    if not meta:
        return {'content': None, 'metadata': None, 'error': f'Unknown script: {script_key}'}

    script_path = Path(settings.SCRIPTS_DIR) / meta['file']

    if not script_path.exists():
        return {
            'content': f'# Script file not found: {script_path}',
            'metadata': meta,
            'error': 'Script file not found on disk.',
        }

    try:
        content = script_path.read_text(encoding='utf-8')
        return {'content': content, 'metadata': meta, 'error': None}
    except OSError as e:
        return {'content': None, 'metadata': meta, 'error': str(e)}


def get_all_scripts_for_platform(platform: str) -> list:
    """Return metadata list for all scripts of a given platform."""
    return [
        {'key': k, **v}
        for k, v in SCRIPT_METADATA.items()
        if v['platform'] == platform
    ]
