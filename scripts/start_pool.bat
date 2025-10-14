@echo off
echo ============================================================
echo KeyHound Enhanced - Distributed Pool System
echo ============================================================
echo.
echo Choose an option:
echo 1. Start Pool Server (as Pool Owner)
echo 2. Join Pool as Participant
echo 3. Start Both Server and Client
echo 4. View Pool Dashboard
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto start_client
if "%choice%"=="3" goto start_both
if "%choice%"=="4" goto view_dashboard
if "%choice%"=="5" goto exit
echo Invalid choice. Please try again.
goto start

:start_server
echo.
echo Starting Pool Server...
echo.
set /p pool_owner="Enter your Pool Owner ID: "
if "%pool_owner%"=="" set pool_owner=pool_owner_2024
set /p server_port="Enter server port (default 8080): "
if "%server_port%"=="" set server_port=8080

echo Starting server as pool owner: %pool_owner%
echo Server will be available at: http://localhost:%server_port%
echo Dashboard: http://localhost:%server_port%/api/pool_dashboard
echo.
echo Press Ctrl+C to stop the server
echo.

python scripts\start_distributed_pool.py --server --pool-owner %pool_owner% --server-port %server_port%
goto end

:start_client
echo.
echo Joining Pool as Participant...
echo.
set /p user_id="Enter your User ID: "
if "%user_id%"=="" (
    echo User ID is required!
    pause
    goto start
)
set /p device_name="Enter device name (optional): "
set /p server_url="Enter pool server URL (default http://localhost:8080): "
if "%server_url%"=="" set server_url=http://localhost:8080

echo Starting client for user: %user_id%
echo Connecting to server: %server_url%
echo Device name: %device_name%
echo.
echo Your device will be automatically tested and scored.
echo Work assignments will begin automatically.
echo.
echo Press Ctrl+C to stop participation
echo.

python scripts\start_distributed_pool.py --client --user-id %user_id% --device-name "%device_name%" --server-url %server_url%
goto end

:start_both
echo.
echo Starting Both Server and Client...
echo.
set /p pool_owner="Enter your Pool Owner ID: "
if "%pool_owner%"=="" set pool_owner=pool_owner_2024
set /p user_id="Enter your User ID: "
if "%user_id%"=="" (
    echo User ID is required!
    pause
    goto start
)
set /p device_name="Enter device name (optional): "
set /p server_port="Enter server port (default 8080): "
if "%server_port%"=="" set server_port=8080

echo Starting server and client...
echo Pool Owner: %pool_owner%
echo User ID: %user_id%
echo Server Port: %server_port%
echo.
echo Server Dashboard: http://localhost:%server_port%/api/pool_dashboard
echo.
echo Press Ctrl+C to stop both server and client
echo.

python scripts\start_distributed_pool.py --both --pool-owner %pool_owner% --user-id %user_id% --device-name "%device_name%" --server-port %server_port%
goto end

:view_dashboard
echo.
echo Opening Pool Dashboard...
echo.
set /p server_url="Enter pool server URL (default http://localhost:8080): "
if "%server_url%"=="" set server_url=http://localhost:8080

echo Opening dashboard: %server_url%/api/pool_dashboard
start "" "%server_url%/api/pool_dashboard"
echo.
echo Dashboard opened in your default web browser.
echo.
pause
goto start

:exit
echo.
echo Goodbye!
echo.
goto end

:end
echo.
echo Pool system stopped.
pause
