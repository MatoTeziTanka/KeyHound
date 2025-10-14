#!/usr/bin/env python3
"""
KeyHound Enhanced - Remote Statistics Server Startup Script
Starts the remote statistics dashboard server.
"""

import os
import sys
import argparse
import codecs
from pathlib import Path

# Fix Windows Unicode encoding issues
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Main entry point for starting remote stats server."""
    parser = argparse.ArgumentParser(
        description='Start KeyHound Remote Statistics Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/start_remote_stats.py                    # Start on default port 8080
  python scripts/start_remote_stats.py --port 9000       # Start on port 9000
  python scripts/start_remote_stats.py --host 0.0.0.0    # Allow external access
  python scripts/start_remote_stats.py --update-interval 5 # Update every 5 seconds
        """
    )
    
    parser.add_argument('--host', default='0.0.0.0',
                       help='Host to bind to (default: 0.0.0.0 for external access)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Port to bind to (default: 8080)')
    parser.add_argument('--update-interval', type=int, default=10,
                       help='Update interval in seconds (default: 10)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("KeyHound Enhanced - Remote Statistics Server")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Update Interval: {args.update_interval} seconds")
    print(f"Debug Mode: {args.debug}")
    print()
    
    # Check if web dependencies are available
    try:
        import flask
        import flask_socketio
        print("[OK] Web dependencies available")
    except ImportError as e:
        print(f"[FAIL] Web dependencies missing: {e}")
        print("Install with: pip install flask flask-socketio")
        sys.exit(1)
    
    # Check if KeyHound components are available
    try:
        from core.simple_keyhound import SimpleKeyHound
        print("[OK] KeyHound components available")
    except ImportError as e:
        print(f"[WARN] KeyHound components limited: {e}")
        print("Some features may not be available")
    
    print()
    print("Starting remote statistics server...")
    print(f"Dashboard will be available at: http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        from web.remote_stats_server import RemoteStatsServer
        
        server = RemoteStatsServer(
            host=args.host,
            port=args.port,
            update_interval=args.update_interval
        )
        server.run(debug=args.debug)
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
