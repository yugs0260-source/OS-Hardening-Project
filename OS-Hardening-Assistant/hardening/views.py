"""
views.py — All view functions for the OS Hardening Assistant.
"""

import json
import platform
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .checker import (
    check_windows_firewall, check_windows_defender,
    check_windows_updates, check_windows_users,
    check_linux_ufw, check_linux_ssh,
    check_linux_fail2ban, check_linux_updates,
    get_all_windows_checks, get_all_linux_checks,
    compute_security_score,
)
from .script_runner import get_script_content, get_all_scripts_for_platform, SCRIPT_METADATA
from .utils import (
    get_os_type, get_os_info, get_score_grade,
    build_report_context, get_hardening_checklist,
)


# ─────────────────────────────────────────────
# Home & Dashboard
# ─────────────────────────────────────────────

def index(request):
    """Home page — OS selection."""
    context = {
        'os_type': get_os_type(),
        'os_info': get_os_info(),
        'page_title': 'OS Hardening Assistant',
    }
    return render(request, 'index.html', context)


def dashboard(request):
    """Security overview dashboard."""
    os_type = get_os_type()

    if os_type == 'windows':
        checks = get_all_windows_checks()
    else:
        checks = get_all_linux_checks()

    score = compute_security_score(checks)
    grade = get_score_grade(score)

    secure_count = sum(1 for c in checks.values() if c.get('status') == 'secure')
    warning_count = sum(1 for c in checks.values() if c.get('status') == 'warning')
    danger_count = sum(1 for c in checks.values() if c.get('status') == 'danger')
    unknown_count = sum(1 for c in checks.values() if c.get('status') == 'unknown')

    context = {
        'page_title': 'Security Dashboard',
        'os_type': os_type,
        'os_info': get_os_info(),
        'checks': checks,
        'score': score,
        'grade': grade,
        'secure_count': secure_count,
        'warning_count': warning_count,
        'danger_count': danger_count,
        'unknown_count': unknown_count,
        'total_checks': len(checks),
    }
    return render(request, 'dashboard.html', context)


# ─────────────────────────────────────────────
# Windows Views
# ─────────────────────────────────────────────

def windows_home(request):
    """Windows hardening hub."""
    checks = get_all_windows_checks()
    score = compute_security_score(checks)
    grade = get_score_grade(score)
    checklist = get_hardening_checklist('windows')
    scripts = get_all_scripts_for_platform('windows')

    context = {
        'page_title': 'Windows Hardening',
        'checks': checks,
        'score': score,
        'grade': grade,
        'checklist': checklist,
        'scripts': scripts,
    }
    return render(request, 'windows/windows_home.html', context)


def win_firewall(request):
    """Windows Firewall hardening page."""
    check = check_windows_firewall()
    script = get_script_content('windows/firewall')

    context = {
        'page_title': 'Windows Firewall',
        'check': check,
        'script': script,
        'section': 'firewall',
    }
    return render(request, 'windows/firewall.html', context)


def win_defender(request):
    """Windows Defender page."""
    check = check_windows_defender()
    script = get_script_content('windows/defender')

    context = {
        'page_title': 'Windows Defender',
        'check': check,
        'script': script,
        'section': 'defender',
    }
    return render(request, 'windows/defender.html', context)


def win_updates(request):
    """Windows Updates page."""
    check = check_windows_updates()
    script = get_script_content('windows/updates')

    context = {
        'page_title': 'Windows Updates',
        'check': check,
        'script': script,
        'section': 'updates',
    }
    return render(request, 'windows/updates.html', context)


def win_users(request):
    """Windows Users page."""
    check = check_windows_users()

    context = {
        'page_title': 'User Accounts',
        'check': check,
        'section': 'users',
    }
    return render(request, 'windows/users.html', context)


def win_report(request):
    """Windows security report."""
    checks = get_all_windows_checks()
    context = build_report_context(checks, 'Windows')
    context['page_title'] = 'Windows Security Report'
    return render(request, 'windows/report.html', context)


# ─────────────────────────────────────────────
# Linux Views
# ─────────────────────────────────────────────

def linux_home(request):
    """Linux hardening hub."""
    checks = get_all_linux_checks()
    score = compute_security_score(checks)
    grade = get_score_grade(score)
    checklist = get_hardening_checklist('linux')
    scripts = get_all_scripts_for_platform('linux')

    context = {
        'page_title': 'Linux Hardening',
        'checks': checks,
        'score': score,
        'grade': grade,
        'checklist': checklist,
        'scripts': scripts,
    }
    return render(request, 'linux/linux_home.html', context)


def lnx_firewall(request):
    """Linux UFW Firewall page."""
    check = check_linux_ufw()
    script = get_script_content('linux/firewall')

    context = {
        'page_title': 'UFW Firewall',
        'check': check,
        'script': script,
        'section': 'firewall',
    }
    return render(request, 'linux/firewall.html', context)


def lnx_updates(request):
    """Linux Updates page."""
    check = check_linux_updates()
    script = get_script_content('linux/update')

    context = {
        'page_title': 'System Updates',
        'check': check,
        'script': script,
        'section': 'updates',
    }
    return render(request, 'linux/updates.html', context)


def lnx_ssh(request):
    """Linux SSH Hardening page."""
    check = check_linux_ssh()
    script = get_script_content('linux/ssh')

    context = {
        'page_title': 'SSH Hardening',
        'check': check,
        'script': script,
        'section': 'ssh',
    }
    return render(request, 'linux/ssh.html', context)


def lnx_fail2ban(request):
    """Linux Fail2ban page."""
    check = check_linux_fail2ban()
    script = get_script_content('linux/fail2ban')

    context = {
        'page_title': 'Fail2ban',
        'check': check,
        'script': script,
        'section': 'fail2ban',
    }
    return render(request, 'linux/fail2ban.html', context)


def lnx_report(request):
    """Linux security report."""
    checks = get_all_linux_checks()
    context = build_report_context(checks, 'Linux')
    context['page_title'] = 'Linux Security Report'
    return render(request, 'linux/report.html', context)


# ─────────────────────────────────────────────
# Global Report
# ─────────────────────────────────────────────

def global_report(request):
    """Combined cross-platform security report."""
    os_type = get_os_type()

    if os_type == 'windows':
        checks = get_all_windows_checks()
        platform_name = 'Windows'
    else:
        checks = get_all_linux_checks()
        platform_name = 'Linux'

    context = build_report_context(checks, platform_name)
    context['page_title'] = 'Security Report'
    return render(request, 'report.html', context)


# ─────────────────────────────────────────────
# API Endpoints (AJAX)
# ─────────────────────────────────────────────

@require_GET
def check_status_api(request):
    """AJAX endpoint to refresh status for a specific check."""
    check_name = request.GET.get('check', '')
    os_type = get_os_type()

    check_map = {
        'windows': {
            'firewall': check_windows_firewall,
            'defender': check_windows_defender,
            'updates': check_windows_updates,
            'users': check_windows_users,
        },
        'linux': {
            'firewall': check_linux_ufw,
            'ssh': check_linux_ssh,
            'fail2ban': check_linux_fail2ban,
            'updates': check_linux_updates,
        },
    }

    platform_checks = check_map.get(os_type, {})

    if check_name == 'all':
        if os_type == 'windows':
            results = get_all_windows_checks()
        else:
            results = get_all_linux_checks()
        score = compute_security_score(results)
        return JsonResponse({'results': results, 'score': score})

    check_fn = platform_checks.get(check_name)
    if not check_fn:
        return JsonResponse({'error': f'Unknown check: {check_name}'}, status=400)

    result = check_fn()
    return JsonResponse({'result': result})


@require_GET
def get_script_api(request):
    """AJAX endpoint to retrieve script content."""
    script_key = request.GET.get('key', '')
    if not script_key:
        return JsonResponse({'error': 'No script key provided'}, status=400)

    result = get_script_content(script_key)
    return JsonResponse(result)
