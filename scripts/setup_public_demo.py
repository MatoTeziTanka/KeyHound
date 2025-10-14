#!/usr/bin/env python3
"""
KeyHound Enhanced - Public Demo Setup Script
Sets up public access to the remote statistics dashboard.
"""

import os
import sys
import subprocess
import time
import requests
import argparse
import codecs
from pathlib import Path

# Fix Windows Unicode encoding issues
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_network_connectivity():
    """Check if we can reach external services."""
    print("Checking network connectivity...")
    
    try:
        # Test internet connectivity
        response = requests.get("https://httpbin.org/ip", timeout=5)
        if response.status_code == 200:
            ip_data = response.json()
            external_ip = ip_data.get('origin', 'Unknown')
            print(f"[OK] External IP: {external_ip}")
            return True
    except Exception as e:
        print(f"[WARN] Could not determine external IP: {e}")
    
    return False

def get_local_ip():
    """Get the local IP address."""
    import socket
    try:
        # Connect to a remote address to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"

def check_port_availability(port):
    """Check if a port is available."""
    import socket
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except OSError:
            return False

def setup_public_demo(port=8080, host='0.0.0.0'):
    """Set up public demo access."""
    print("=" * 60)
    print("KeyHound Enhanced - Public Demo Setup")
    print("=" * 60)
    
    # Check network connectivity
    has_internet = check_network_connectivity()
    
    # Get network information
    local_ip = get_local_ip()
    
    print(f"\nNetwork Information:")
    print(f"  Local IP: {local_ip}")
    print(f"  Internet Access: {'Yes' if has_internet else 'No'}")
    
    # Check port availability
    if not check_port_availability(port):
        print(f"[WARN] Port {port} is already in use. Trying port {port + 1}")
        port += 1
        if not check_port_availability(port):
            print(f"[ERROR] No available ports found around {port}")
            return False
    
    print(f"  Available Port: {port}")
    
    # Create public demo configuration
    demo_config = f"""
# KeyHound Enhanced - Public Demo Configuration
# Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}

# Network Configuration
HOST={host}
PORT={port}
EXTERNAL_ACCESS=true

# Demo Settings
UPDATE_INTERVAL=5
DEMO_MODE=true
PUBLIC_ACCESS=true

# Access URLs
LOCAL_URL=http://localhost:{port}
NETWORK_URL=http://{local_ip}:{port}
EXTERNAL_URL=http://{local_ip}:{port}  # Replace with your external IP

# Instructions:
# 1. Start the server: python scripts/start_remote_stats.py --port {port}
# 2. Access locally: http://localhost:{port}
# 3. Access from network: http://{local_ip}:{port}
# 4. For external access, configure port forwarding on your router
# 5. Replace EXTERNAL_URL with your actual external IP address
"""
    
    # Save demo configuration
    config_file = Path("demo_config.env")
    with open(config_file, 'w') as f:
        f.write(demo_config)
    
    print(f"\n[SUCCESS] Demo configuration saved to: {config_file}")
    
    # Create startup script for demo
    demo_startup = f"""@echo off
echo ============================================================
echo KeyHound Enhanced - Public Demo Server
echo ============================================================
echo.
echo Starting public demo server...
echo.
echo Access URLs:
echo   Local: http://localhost:{port}
echo   Network: http://{local_ip}:{port}
echo.
echo For external access:
echo   1. Configure port forwarding on your router (port {port})
echo   2. Replace {local_ip} with your external IP address
echo   3. Share the external URL with others
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python scripts/start_remote_stats.py --host {host} --port {port} --update-interval 5

echo.
echo Demo server stopped.
pause
"""
    
    startup_file = Path("scripts/start_public_demo.bat")
    with open(startup_file, 'w') as f:
        f.write(demo_startup)
    
    print(f"[SUCCESS] Demo startup script created: {startup_file}")
    
    # Create instructions file
    instructions = f"""# KeyHound Enhanced - Public Demo Instructions

## Quick Start

### 1. Start the Demo Server
```bash
# Windows (Easy)
scripts\\start_public_demo.bat

# Or manually
python scripts/start_remote_stats.py --host {host} --port {port} --update-interval 5
```

### 2. Access the Dashboard

#### Local Access
- **URL**: http://localhost:{port}
- **Description**: Access from the same machine

#### Network Access
- **URL**: http://{local_ip}:{port}
- **Description**: Access from other devices on your network

#### External Access (Public)
- **URL**: http://YOUR_EXTERNAL_IP:{port}
- **Requirements**:
  - Configure port forwarding on your router (port {port})
  - Replace `YOUR_EXTERNAL_IP` with your actual external IP
  - Ensure firewall allows connections on port {port}

## Configuration

### Port Forwarding Setup
1. Access your router's admin panel (usually 192.168.1.1 or 192.168.0.1)
2. Find "Port Forwarding" or "Virtual Server" settings
3. Add a rule:
   - **External Port**: {port}
   - **Internal IP**: {local_ip}
   - **Internal Port**: {port}
   - **Protocol**: TCP

### Firewall Configuration
1. Windows Firewall:
   - Allow Python through firewall
   - Or create inbound rule for port {port}

2. Router Firewall:
   - Ensure port {port} is open
   - Some routers have additional security settings

## Demo Features

### Real-time Statistics
- Live KeyHound performance metrics
- System resource monitoring
- Connection status indicators
- Historical performance charts

### Access Methods
- **Web Browser**: Any modern browser
- **Mobile**: Responsive design for phones/tablets
- **API**: REST endpoints for programmatic access

## Security Notes

### Demo Mode
- This is a demo server for testing
- Not recommended for production use
- No authentication required
- Data is not persistent

### Production Deployment
- Use HTTPS in production
- Implement authentication
- Add rate limiting
- Use environment variables for secrets

## Troubleshooting

### Cannot Access from External Network
1. Check port forwarding configuration
2. Verify firewall settings
3. Test with local network first
4. Check if ISP blocks incoming connections

### Connection Refused
1. Ensure server is running
2. Check if port is available
3. Verify firewall settings
4. Try a different port

### Performance Issues
1. Reduce update interval
2. Check system resources
3. Monitor network usage
4. Optimize server configuration

## Support

For issues or questions:
- Check the logs in the terminal
- Review firewall and router settings
- Test with local access first
- Ensure all dependencies are installed

---

**KeyHound Enhanced Public Demo** - Share your Bitcoin cryptography platform with the world!
"""
    
    instructions_file = Path("docs/PUBLIC_DEMO_INSTRUCTIONS.md")
    instructions_file.parent.mkdir(exist_ok=True)
    with open(instructions_file, 'w') as f:
        f.write(instructions)
    
    print(f"[SUCCESS] Demo instructions created: {instructions_file}")
    
    print(f"\n" + "=" * 60)
    print("PUBLIC DEMO SETUP COMPLETE!")
    print("=" * 60)
    print(f"\nTo start the public demo:")
    print(f"  scripts\\start_public_demo.bat")
    print(f"\nAccess URLs:")
    print(f"  Local: http://localhost:{port}")
    print(f"  Network: http://{local_ip}:{port}")
    print(f"\nFor external access:")
    print(f"  1. Configure port forwarding (port {port})")
    print(f"  2. Share: http://YOUR_EXTERNAL_IP:{port}")
    print(f"\nInstructions: docs/PUBLIC_DEMO_INSTRUCTIONS.md")
    
    return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Set up KeyHound Public Demo')
    parser.add_argument('--port', type=int, default=8080, help='Port for demo server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    
    args = parser.parse_args()
    
    success = setup_public_demo(args.port, args.host)
    
    if success:
        print(f"\n[SUCCESS] Public demo setup completed successfully!")
        print(f"Ready to share KeyHound with the world!")
        sys.exit(0)
    else:
        print(f"\n[FAILED] Public demo setup failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
