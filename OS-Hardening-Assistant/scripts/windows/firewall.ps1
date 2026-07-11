#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Enable and configure Windows Firewall for all profiles.
.DESCRIPTION
    Enables Windows Firewall for Domain, Private, and Public profiles.
    Sets default inbound to block and outbound to allow.
    Logs dropped packets for monitoring.
.NOTES
    Run as Administrator in PowerShell.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "`n[*] OS Hardening Assistant — Windows Firewall Hardening" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor DarkGray

# Enable firewall for all profiles
Write-Host "`n[+] Enabling firewall for all profiles..." -ForegroundColor Green
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Default inbound: block; outbound: allow
Write-Host "[+] Setting default inbound to Block, outbound to Allow..." -ForegroundColor Green
Set-NetFirewallProfile -Profile Domain,Public,Private `
    -DefaultInboundAction  Block `
    -DefaultOutboundAction Allow

# Enable logging for dropped packets
Write-Host "[+] Enabling firewall logging for dropped packets..." -ForegroundColor Green
Set-NetFirewallProfile -Profile Domain,Public,Private `
    -LogAllowed    False `
    -LogBlocked    True  `
    -LogMaxSizeKilobytes 4096

# Display current status
Write-Host "`n[*] Current Firewall Status:" -ForegroundColor Cyan
Get-NetFirewallProfile | Format-Table Name, Enabled, DefaultInboundAction, DefaultOutboundAction -AutoSize

Write-Host "`n[OK] Windows Firewall hardening complete!" -ForegroundColor Green
Write-Host "     Review rules in: Windows Security > Firewall & network protection`n" -ForegroundColor DarkGray
