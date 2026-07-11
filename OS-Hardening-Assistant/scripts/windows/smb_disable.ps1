#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Disable SMBv1 protocol (WannaCry / EternalBlue mitigation).
.DESCRIPTION
    Disables the legacy and insecure SMBv1 protocol via PowerShell.
    SMBv1 is exploited by WannaCry, NotPetya, and EternalBlue.
    SMBv2 and SMBv3 remain functional.
.NOTES
    Run as Administrator in PowerShell.
    No system restart required for immediate effect, but recommended.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

Write-Host "`n[*] OS Hardening Assistant — Disable SMBv1" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor DarkGray

# Check current state
Write-Host "`n[*] Checking current SMB configuration..." -ForegroundColor Cyan
$smbV1 = Get-SmbServerConfiguration | Select-Object EnableSMB1Protocol, EnableSMB2Protocol
Write-Host "    SMBv1 Enabled: $($smbV1.EnableSMB1Protocol)"  -ForegroundColor $(if ($smbV1.EnableSMB1Protocol) { 'Red' } else { 'Green' })
Write-Host "    SMBv2 Enabled: $($smbV1.EnableSMB2Protocol)"  -ForegroundColor Green

if (-not $smbV1.EnableSMB1Protocol) {
    Write-Host "`n[OK] SMBv1 is already disabled. No changes needed." -ForegroundColor Green
    exit 0
}

# Disable SMBv1 via Set-SmbServerConfiguration
Write-Host "`n[+] Disabling SMBv1 via Set-SmbServerConfiguration..." -ForegroundColor Green
Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force

# Also disable via registry for older Windows versions
Write-Host "[+] Disabling SMBv1 via registry (legacy fallback)..." -ForegroundColor Green
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters"
Set-ItemProperty -Path $regPath -Name "SMB1" -Value 0 -Type DWord -Force

# Optionally disable the SMBv1 Windows Feature
Write-Host "[+] Removing SMBv1 Windows Feature (if applicable)..." -ForegroundColor Green
try {
    Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart -ErrorAction SilentlyContinue | Out-Null
    Write-Host "    SMBv1 Windows Feature disabled." -ForegroundColor Green
} catch {
    Write-Host "    SMBv1 Feature not found (normal on modern Windows)." -ForegroundColor DarkGray
}

# Verify
Write-Host "`n[*] Verifying SMBv1 is disabled..." -ForegroundColor Cyan
$check = Get-SmbServerConfiguration | Select-Object EnableSMB1Protocol
if (-not $check.EnableSMB1Protocol) {
    Write-Host "[OK] SMBv1 successfully disabled!" -ForegroundColor Green
} else {
    Write-Host "[!] SMBv1 may still be enabled. Check manually." -ForegroundColor Yellow
}

Write-Host "`n[!] A system restart is recommended to ensure SMBv1 is fully disabled.`n" -ForegroundColor Yellow
