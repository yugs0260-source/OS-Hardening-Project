#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Force Windows Update check and install all available updates.
.DESCRIPTION
    Uses the PSWindowsUpdate module or Windows Update COM object to check
    for and install all available updates (including drivers and optional).
.NOTES
    Run as Administrator in PowerShell.
    System may require a restart after updates are installed.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

Write-Host "`n[*] OS Hardening Assistant — Windows Update" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor DarkGray

# Enable automatic updates via registry
Write-Host "`n[+] Configuring automatic updates..." -ForegroundColor Green
$AUSettings = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
If (-not (Test-Path $AUSettings)) {
    New-Item -Path $AUSettings -Force | Out-Null
}
Set-ItemProperty -Path $AUSettings -Name "NoAutoUpdate" -Value 0 -Type DWord -Force
Set-ItemProperty -Path $AUSettings -Name "AUOptions"    -Value 4 -Type DWord -Force  # Auto download and install

# Use COM object to check for updates
Write-Host "[+] Checking for pending updates via COM object..." -ForegroundColor Green
try {
    $updateSession  = New-Object -ComObject Microsoft.Update.Session
    $updateSearcher = $updateSession.CreateUpdateSearcher()
    $searchResult   = $updateSearcher.Search("IsInstalled=0 and Type='Software'")

    $pending = $searchResult.Updates.Count
    Write-Host "    Found $pending pending update(s)." -ForegroundColor $(if ($pending -eq 0) { 'Green' } else { 'Yellow' })

    if ($pending -gt 0) {
        Write-Host "`n    Pending updates:" -ForegroundColor Cyan
        for ($i = 0; $i -lt $searchResult.Updates.Count; $i++) {
            Write-Host "      [$($i+1)] $($searchResult.Updates.Item($i).Title)" -ForegroundColor White
        }

        Write-Host "`n[+] Downloading and installing updates..." -ForegroundColor Green
        $updatesToInstall = New-Object -ComObject Microsoft.Update.UpdateColl

        for ($i = 0; $i -lt $searchResult.Updates.Count; $i++) {
            $update = $searchResult.Updates.Item($i)
            if ($update.EulaAccepted -eq $false) { $update.AcceptEula() }
            $updatesToInstall.Add($update) | Out-Null
        }

        $downloader        = $updateSession.CreateUpdateDownloader()
        $downloader.Updates = $updatesToInstall
        $downloader.Download()

        $installer         = $updateSession.CreateUpdateInstaller()
        $installer.Updates = $updatesToInstall
        $installResult     = $installer.Install()

        Write-Host "`n[OK] Installation result code: $($installResult.ResultCode)" -ForegroundColor Green
        if ($installResult.RebootRequired) {
            Write-Host "[!]  A system restart is required to complete updates." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "[!] COM update method failed: $_" -ForegroundColor Yellow
    Write-Host "    Alternative: Open Settings > Windows Update > Check for updates" -ForegroundColor DarkGray
}

Write-Host "`n[OK] Windows Update check complete!`n" -ForegroundColor Green
