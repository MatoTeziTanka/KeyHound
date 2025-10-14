#!/usr/bin/env python3
"""
KeyHound Enhanced - Remote Statistics Server Test Script
Tests the remote statistics dashboard functionality.
"""

import requests
import time
import json
import sys
import codecs
from pathlib import Path

# Fix Windows Unicode encoding issues
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_remote_stats_server(host='localhost', port=8080, timeout=30):
    """Test the remote statistics server functionality."""
    print("=" * 60)
    print("KeyHound Enhanced - Remote Statistics Server Test")
    print("=" * 60)
    
    base_url = f"http://{host}:{port}"
    
    # Test 1: Health check endpoint
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"[OK] Health check passed: {health_data['status']}")
            print(f"  Uptime: {health_data['uptime']:.2f} seconds")
        else:
            print(f"[FAIL] Health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] Health check failed: {e}")
        return False
    
    # Test 2: Statistics API endpoint
    print("\n2. Testing statistics API endpoint...")
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            stats_data = response.json()
            print("[OK] Statistics API working")
            print(f"  Timestamp: {stats_data['timestamp']}")
            print(f"  KeyHound Status: {stats_data['keyhound']['status']}")
            print(f"  System CPU: {stats_data['system']['cpu_percent']:.1f}%")
            print(f"  Connected Clients: {stats_data['server']['connected_clients']}")
        else:
            print(f"[FAIL] Statistics API failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] Statistics API failed: {e}")
        return False
    
    # Test 3: Dashboard page
    print("\n3. Testing dashboard page...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("[OK] Dashboard page accessible")
            if "KeyHound Enhanced" in response.text:
                print("  [OK] Page contains expected content")
            else:
                print("  [WARN] Page may not be loading correctly")
        else:
            print(f"[FAIL] Dashboard page failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] Dashboard page failed: {e}")
        return False
    
    # Test 4: Multiple requests (performance test)
    print("\n4. Testing multiple requests...")
    start_time = time.time()
    successful_requests = 0
    total_requests = 10
    
    for i in range(total_requests):
        try:
            response = requests.get(f"{base_url}/api/stats", timeout=2)
            if response.status_code == 200:
                successful_requests += 1
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.1)  # Small delay between requests
    
    elapsed_time = time.time() - start_time
    success_rate = (successful_requests / total_requests) * 100
    
    print(f"[OK] Performance test completed")
    print(f"  Successful requests: {successful_requests}/{total_requests} ({success_rate:.1f}%)")
    print(f"  Total time: {elapsed_time:.2f} seconds")
    print(f"  Average response time: {elapsed_time/total_requests:.3f} seconds")
    
    # Test 5: JSON data validation
    print("\n5. Testing JSON data structure...")
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            stats_data = response.json()
            
            required_fields = ['timestamp', 'system', 'keyhound', 'server', 'connection_status']
            missing_fields = []
            
            for field in required_fields:
                if field not in stats_data:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"[FAIL] Missing required fields: {missing_fields}")
                return False
            else:
                print("[OK] JSON data structure is valid")
                print(f"  System fields: {list(stats_data['system'].keys())}")
                print(f"  KeyHound fields: {list(stats_data['keyhound'].keys())}")
                print(f"  Server fields: {list(stats_data['server'].keys())}")
        else:
            print(f"[FAIL] JSON validation failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] JSON validation failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("[SUCCESS] All tests passed! Remote statistics server is working correctly.")
    print(f"Dashboard URL: {base_url}")
    print("=" * 60)
    return True

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test KeyHound Remote Statistics Server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')
    parser.add_argument('--timeout', type=int, default=30, help='Test timeout in seconds (default: 30)')
    
    args = parser.parse_args()
    
    print("Testing KeyHound Remote Statistics Server...")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Timeout: {args.timeout} seconds")
    
    # Check if requests library is available
    try:
        import requests
    except ImportError:
        print("\n[ERROR] requests library not available")
        print("Install with: pip install requests")
        sys.exit(1)
    
    # Run tests
    success = test_remote_stats_server(args.host, args.port, args.timeout)
    
    if success:
        print("\n[SUCCESS] Remote statistics server test completed successfully!")
        print("\nTo start the server:")
        print("  python scripts/start_remote_stats.py")
        print("\nTo access the dashboard:")
        print(f"  http://{args.host}:{args.port}")
        sys.exit(0)
    else:
        print("\n[FAILED] Remote statistics server test failed!")
        print("\nMake sure the server is running:")
        print("  python scripts/start_remote_stats.py")
        sys.exit(1)

if __name__ == '__main__':
    main()
