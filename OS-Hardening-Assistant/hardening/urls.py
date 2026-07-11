"""URL configuration for the hardening app."""

from django.urls import path
from . import views

app_name = 'hardening'

urlpatterns = [
    # Home
    path('', views.index, name='index'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Windows hardening
    path('windows/', views.windows_home, name='windows_home'),
    path('windows/firewall/', views.win_firewall, name='win_firewall'),
    path('windows/defender/', views.win_defender, name='win_defender'),
    path('windows/updates/', views.win_updates, name='win_updates'),
    path('windows/users/', views.win_users, name='win_users'),
    path('windows/report/', views.win_report, name='win_report'),

    # Linux hardening
    path('linux/', views.linux_home, name='linux_home'),
    path('linux/firewall/', views.lnx_firewall, name='lnx_firewall'),
    path('linux/updates/', views.lnx_updates, name='lnx_updates'),
    path('linux/ssh/', views.lnx_ssh, name='lnx_ssh'),
    path('linux/fail2ban/', views.lnx_fail2ban, name='lnx_fail2ban'),
    path('linux/report/', views.lnx_report, name='lnx_report'),

    # Combined report
    path('report/', views.global_report, name='global_report'),

    # API endpoints (AJAX)
    path('api/check-status/', views.check_status_api, name='check_status_api'),
    path('api/get-script/', views.get_script_api, name='get_script_api'),
]
