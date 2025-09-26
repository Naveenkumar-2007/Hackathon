@echo off
echo 🔥 Windows Firewall Configuration for Flask Server
echo ================================================

echo.
echo 1. Adding Flask Python to Windows Firewall exceptions...
netsh advfirewall firewall add rule name="Flask Python Server" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="Flask Python Server Out" dir=out action=allow protocol=TCP localport=8000

echo.
echo 2. Adding Python.exe to firewall exceptions...
netsh advfirewall firewall add rule name="Python.exe" dir=in action=allow program="%SystemRoot%\System32\python.exe"
netsh advfirewall firewall add rule name="Anaconda Python" dir=in action=allow program="C:\Users\navee\anaconda3\python.exe"

echo.
echo 3. Allowing localhost connections...
netsh advfirewall firewall add rule name="Localhost Connections" dir=in action=allow protocol=TCP localport=1-65535 remoteip=127.0.0.1

echo.
echo ✅ Firewall rules added successfully!
echo 🔄 Now try running your Flask server again.

pause