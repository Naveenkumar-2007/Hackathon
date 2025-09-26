# Windows Network Diagnostics for Flask Server
# Run this script to diagnose and fix networking issues

Write-Host "🔍 WINDOWS NETWORK DIAGNOSTICS FOR FLASK SERVER" -ForegroundColor Green
Write-Host "=" * 60

# Check current firewall status
Write-Host "`n1. Checking Windows Firewall status..." -ForegroundColor Yellow
try {
    $firewallStatus = Get-NetFirewallProfile | Select-Object Name, Enabled
    $firewallStatus | Format-Table -AutoSize
} catch {
    Write-Host "Unable to check firewall status" -ForegroundColor Red
}

# Check if ports are blocked
Write-Host "`n2. Checking port availability..." -ForegroundColor Yellow
$ports = @(5000, 8000, 9000, 3000, 3001)
foreach ($port in $ports) {
    try {
        $connection = Test-NetConnection -ComputerName "127.0.0.1" -Port $port -InformationLevel Quiet
        if ($connection) {
            Write-Host "Port $port : OPEN" -ForegroundColor Green
        } else {
            Write-Host "Port $port : CLOSED/FILTERED" -ForegroundColor Red
        }
    } catch {
        Write-Host "Port $port : ERROR TESTING" -ForegroundColor Red
    }
}

# Check localhost resolution
Write-Host "`n3. Testing localhost resolution..." -ForegroundColor Yellow
try {
    $localhost = Resolve-DnsName -Name "localhost" -Type A
    Write-Host "localhost resolves to: $($localhost.IPAddress)" -ForegroundColor Green
} catch {
    Write-Host "localhost resolution failed" -ForegroundColor Red
}

# Check for Python processes
Write-Host "`n4. Checking for running Python processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python* -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "Running Python processes:" -ForegroundColor Green
    $pythonProcesses | Select-Object Id, ProcessName, Path | Format-Table -AutoSize
} else {
    Write-Host "No Python processes running" -ForegroundColor Yellow
}

# Network adapter information
Write-Host "`n5. Network adapter information..." -ForegroundColor Yellow
try {
    $adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object Name, InterfaceDescription, LinkSpeed
    $adapters | Format-Table -AutoSize
} catch {
    Write-Host "Unable to get network adapter info" -ForegroundColor Red
}

Write-Host "`n" + "=" * 60
Write-Host "🔧 SUGGESTED FIXES:" -ForegroundColor Cyan
Write-Host "1. Run PowerShell as Administrator" -ForegroundColor White
Write-Host "2. Temporarily disable Windows Defender Firewall" -ForegroundColor White
Write-Host "3. Add Python to firewall exceptions" -ForegroundColor White
Write-Host "4. Use different port (9000-9100 range)" -ForegroundColor White
Write-Host "5. Check antivirus software blocking connections" -ForegroundColor White
Write-Host "=" * 60

# Quick firewall fix commands
Write-Host "`n🚀 QUICK FIX COMMANDS (Run as Administrator):" -ForegroundColor Green
Write-Host "netsh advfirewall firewall add rule name='Flask Server' dir=in action=allow protocol=TCP localport=8000-9100" -ForegroundColor Cyan
Write-Host "netsh advfirewall firewall add rule name='Python Local' dir=in action=allow program='C:\Users\navee\anaconda3\python.exe'" -ForegroundColor Cyan

Write-Host "`nPress any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")