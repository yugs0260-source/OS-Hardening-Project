#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Enable Windows Defender real-time protection and update definitions.
.DESCRIPTION
    Enables Windows Defender antivirus real-time protection, cloud protection,
    automatic sample submission, and triggers a virus definition update.
.NOTES
    Run as Administrator in PowerShell.
    May not work if a third-party AV has disabled Defender.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

Write-Host "`n[*] OS Hardening Assistant — Windows Defender Hardening" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor DarkGray

# Enable real-time protection
Write-Host "`n[+] Enabling real-time protection..." -ForegroundColor Green
Set-MpPreference -DisableRealtimeMonitoring $false

# Enable cloud-delivered protection
Write-Host "[+] Enabling cloud-delivered protection..." -ForegroundColor Green
Set-MpPreference -MAPSReporting Advanced
Set-MpPreference -SubmitSamplesConsent SendAllSamples

# Enable behavior monitoring
Write-Host "[+] Enabling behavior monitoring..." -ForegroundColor Green
Set-MpPreference -DisableBehaviorMonitoring $false

# Enable network protection
Write-Host "[+] Enabling network protection..." -ForegroundColor Green
Set-MpPreference -EnableNetworkProtection Enabled

# Update virus definitions
Write-Host "[+] Updating virus definitions..." -ForegroundColor Green
Update-MpSignature

# Run a quick scan (optional — comment out if not desired)
# Write-Host "[+] Running quick scan..." -ForegroundColor Green
# Start-MpScan -ScanType QuickScan

# Show status
Write-Host "`n[*] Current Defender Status:" -ForegroundColor Cyan
Get-MpComputerStatus | Select-Object `
    RealTimeProtectionEnabled, `
    AntivirusEnabled, `
    AntispywareEnabled, `
    NISEnabled, `
    AntivirusSignatureLastUpdated | Format-List

Write-Host "[OK] Windows Defender hardening complete!`n" -ForegroundColor Green
