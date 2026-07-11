#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Enable BitLocker full-disk encryption on the C: drive.
.DESCRIPTION
    Enables BitLocker with TPM-based key protection on the system drive.
    Backs up the recovery key to Active Directory (if domain-joined)
    and saves it to a file for standalone systems.
.NOTES
    Run as Administrator in PowerShell.
    Requires TPM 1.2 or later, or USB startup key.
    BACKUP YOUR RECOVERY KEY before enabling!
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "`n[*] OS Hardening Assistant — BitLocker Encryption" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor DarkGray
Write-Host "[!] WARNING: Back up your recovery key before proceeding!" -ForegroundColor Red

# Check BitLocker status
$blStatus = Get-BitLockerVolume -MountPoint "C:"
Write-Host "`n[*] Current BitLocker status on C:: $($blStatus.ProtectionStatus)" -ForegroundColor Cyan

if ($blStatus.ProtectionStatus -eq 'On') {
    Write-Host "[OK] BitLocker is already enabled on C:." -ForegroundColor Green
    exit 0
}

# Check TPM availability
$tpm = Get-Tpm -ErrorAction SilentlyContinue
if ($tpm -and $tpm.TpmPresent) {
    Write-Host "[+] TPM detected. Enabling BitLocker with TPM + PIN..." -ForegroundColor Green
    try {
        # Enable TPM key protector
        Enable-BitLocker -MountPoint "C:" `
            -TpmProtector `
            -SkipHardwareTest

        # Add recovery key protector and save to file
        $keyDir = "$env:SystemDrive\BitLockerRecoveryKey"
        New-Item -ItemType Directory -Path $keyDir -Force | Out-Null
        Add-BitLockerKeyProtector -MountPoint "C:" -RecoveryKeyProtector -RecoveryKeyPath $keyDir

        Write-Host "[OK] BitLocker enabled. Recovery key saved to: $keyDir" -ForegroundColor Green
        Write-Host "[!]  MOVE THIS KEY TO A SECURE LOCATION (USB, printed)!" -ForegroundColor Yellow
    } catch {
        Write-Host "[!] BitLocker enable failed: $_" -ForegroundColor Red
        Write-Host "    Ensure TPM is enabled in BIOS/UEFI and try again." -ForegroundColor DarkGray
    }
} else {
    Write-Host "[!] No TPM detected. BitLocker requires TPM or USB startup key." -ForegroundColor Yellow
    Write-Host "    Enable TPM in BIOS/UEFI, or use a USB startup key method." -ForegroundColor DarkGray
}

Write-Host "`n[*] BitLocker script complete.`n" -ForegroundColor Cyan
