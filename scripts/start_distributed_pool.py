#!/usr/bin/env python3
"""
KeyHound Enhanced - Distributed Pool Startup Script
Starts the distributed Bitcoin puzzle solving pool system.
"""

import os
import sys
import argparse
import time
from pathlib import Path

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Main entry point for starting the distributed pool."""
    parser = argparse.ArgumentParser(
        description='Start KeyHound Distributed Pool System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/start_distributed_pool.py --server                    # Start pool server
  python scripts/start_distributed_pool.py --client --user-id alice    # Start pool client
  python scripts/start_distributed_pool.py --both --user-id bob        # Start both server and client
        """
    )
    
    parser.add_argument('--server', action='store_true', help='Start pool server')
    parser.add_argument('--client', action='store_true', help='Start pool client')
    parser.add_argument('--both', action='store_true', help='Start both server and client')
    parser.add_argument('--user-id', help='User ID for pool client')
    parser.add_argument('--device-name', help='Device name for pool client')
    parser.add_argument('--server-url', default='http://localhost:8080', help='Pool server URL')
    parser.add_argument('--server-host', default='0.0.0.0', help='Server host')
    parser.add_argument('--server-port', type=int, default=8080, help='Server port')
    parser.add_argument('--pool-owner', default='pool_owner_2024', help='Pool owner ID')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("KeyHound Enhanced - Distributed Pool System")
    print("=" * 60)
    
    # Check dependencies
    try:
        import flask
        import flask_cors
        print("[OK] Web dependencies available")
    except ImportError as e:
        print(f"[FAIL] Web dependencies missing: {e}")
        print("Install with: pip install flask flask-cors")
        return 1
    
    try:
        from pool.pool_server import PoolServerAPI
        from pool.community_pool_client import CommunityPoolClient
        print("[OK] Pool components available")
    except ImportError as e:
        print(f"[FAIL] Pool components missing: {e}")
        print("Make sure all pool modules are properly installed")
        return 1
    
    success = True
    
    # Start server
    if args.server or args.both:
        print(f"\nStarting Pool Server...")
        print(f"Host: {args.server_host}")
        print(f"Port: {args.server_port}")
        print(f"Pool Owner: {args.pool_owner}")
        
        try:
            from pool.pool_server import PoolServerAPI
            
            # Create pool server
            server = PoolServerAPI(
                pool_owner_id=args.pool_owner,
                pool_owner_public_key="pool_owner_public_key_placeholder",
                host=args.server_host,
                port=args.server_port
            )
            
            print(f"[OK] Pool server initialized")
            print(f"Dashboard: http://{args.server_host}:{args.server_port}/api/pool_dashboard")
            print(f"API Base: http://{args.server_host}:{args.server_port}/api/")
            
            if not args.both:  # Only start server
                print("\nPress Ctrl+C to stop the server")
                server.run(debug=args.debug)
            else:
                # Start server in background thread
                import threading
                server_thread = threading.Thread(target=server.run, args=(args.debug,), daemon=True)
                server_thread.start()
                print("[OK] Pool server started in background")
                
                # Wait a moment for server to start
                time.sleep(3)
        
        except Exception as e:
            print(f"[FAIL] Failed to start pool server: {e}")
            success = False
    
    # Start client
    if args.client or args.both:
        if not args.user_id:
            print("[FAIL] User ID required for pool client")
            print("Use --user-id YOUR_USER_ID")
            return 1
        
        print(f"\nStarting Pool Client...")
        print(f"User ID: {args.user_id}")
        print(f"Server URL: {args.server_url}")
        
        try:
            from pool.community_pool_client import CommunityPoolClient
            
            # Create pool client
            client = CommunityPoolClient(args.server_url, args.user_id)
            
            print(f"[OK] Pool client initialized")
            print(f"Device name: {args.device_name or 'auto-detected'}")
            
            # Start participation
            client_success = client.start_pool_participation(args.device_name)
            
            if client_success:
                print(f"[OK] Pool participation started")
                print(f"Device ID: {client.device_id}")
                print("\nPress Ctrl+C to stop participation")
                
                try:
                    # Keep running until interrupted
                    while True:
                        time.sleep(60)
                        
                        # Display stats every minute
                        stats = client.get_pool_stats()
                        if stats:
                            print(f"\nPool Stats:")
                            print(f"  Total Participants: {stats.total_participants}")
                            print(f"  Active Participants: {stats.active_participants}")
                            print(f"  Keys Found: {stats.total_keys_found}")
                            print(f"  Your Rank: {stats.user_rank}")
                            print(f"  Your Reward %: {stats.user_reward_percentage:.3f}%")
                            print(f"  Work Contributed: {stats.work_contributed}")
                
                except KeyboardInterrupt:
                    print("\nStopping pool participation...")
                    client.stop_pool_participation()
                    print("[OK] Pool participation stopped")
            else:
                print("[FAIL] Failed to start pool participation")
                success = False
        
        except Exception as e:
            print(f"[FAIL] Failed to start pool client: {e}")
            success = False
    
    if success:
        print(f"\n[SUCCESS] Distributed pool system started successfully!")
        
        if args.both:
            print(f"\nSystem Status:")
            print(f"  Pool Server: Running on http://{args.server_host}:{args.server_port}")
            print(f"  Pool Client: Connected as {args.user_id}")
            print(f"  Dashboard: http://{args.server_host}:{args.server_port}/api/pool_dashboard")
            
            print(f"\nTo invite others to join:")
            print(f"  1. Share the dashboard URL")
            print(f"  2. They download the client")
            print(f"  3. They run: python scripts/start_distributed_pool.py --client --user-id THEIR_USER_ID --server-url http://{args.server_host}:{args.server_port}")
        
        return 0
    else:
        print(f"\n[FAILED] Distributed pool system startup failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
