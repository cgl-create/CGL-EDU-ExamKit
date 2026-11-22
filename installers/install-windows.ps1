$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$App = Join-Path $env:LOCALAPPDATA "CGL\ExamKit\App"
New-Item -ItemType Directory -Force -Path $App | Out-Null
$Base = "https://raw.githubusercontent.com/cgl-create/CGL-EDU-ExamKit/main"
$Files = @("index.html","server.py","requirements.txt","manifest.webmanifest","sw.js","icon.svg")
foreach ($File in $Files) {
  Write-Host "Downloading $File..."
  Invoke-WebRequest -Uri "$Base/$File" -OutFile (Join-Path $App $File)
}
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) { $PyCmd = "py"; $PyArgs = @("-3") } else {
  $Python = Get-Command python -ErrorAction SilentlyContinue
  if (-not $Python) { throw "Python 3 is required. Install it from https://www.python.org/downloads/windows/ and rerun this installer." }
  $PyCmd = "python"; $PyArgs = @()
}
& $PyCmd @PyArgs -m venv (Join-Path $App ".venv")
$VenvPython = Join-Path $App ".venv\Scripts\python.exe"
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r (Join-Path $App "requirements.txt")
$Launcher = Join-Path $env:LOCALAPPDATA "CGL\ExamKit\Start-ExamKit.cmd"
@"
@echo off
cd /d "$App"
"$VenvPython" server.py
"@ | Set-Content -Encoding ASCII $Launcher
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "CGL+ ExamKit OS.lnk"
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $Launcher
$Shortcut.WorkingDirectory = $App
$Shortcut.Save()
try { New-NetFirewallRule -DisplayName "CGL+ ExamKit OS (TCP 8765)" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8765 -Profile Private -ErrorAction Stop | Out-Null } catch { Write-Warning "Could not add the private-network firewall rule. Run PowerShell as Administrator or allow Python through Windows Firewall when prompted." }
Write-Host ""
Write-Host "Installed. Start CGL+ ExamKit OS from your Desktop shortcut."
Write-Host "Open http://examkit.local:8765 (or the hostname printed by the server)."
