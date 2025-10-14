@echo off
echo ============================================================
echo KeyHound Enhanced - Public Demo Server
echo ============================================================
echo.
echo Starting public demo server...
echo.
echo Access URLs:
echo   Local: http://localhost:8080
echo   Network: http://192.168.1.8:8080
echo.
echo For external access:
echo   1. Configure port forwarding on your router (port 8080)
echo   2. Replace 192.168.1.8 with your external IP address
echo   3. Share the external URL with others
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python scripts/start_remote_stats.py --host 0.0.0.0 --port 8080 --update-interval 5

echo.
echo Demo server stopped.
pause
