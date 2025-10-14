#!/usr/bin/env python3
"""
KeyHound Enhanced - Live Deployment Script
Deploy and test KeyHound Enhanced on a live server.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_system_requirements() -> Dict[str, Any]:
    """Check if system meets requirements for live deployment."""
    print("Checking system requirements...")
    
    requirements = {
        'python_version': sys.version_info >= (3, 8),
        'dependencies': True,
        'disk_space': True,
        'memory': True,
        'network': True
    }
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  Python version: {python_version}")
    
    if requirements['python_version']:
        print("  [OK] Python version compatible")
    else:
        print("  [FAIL] Python version too old (need 3.8+)")
    
    # Check dependencies
    required_packages = ['flask', 'psutil', 'requests', 'pyyaml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  [OK] {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  [MISSING] {package}")
    
    if missing_packages:
        requirements['dependencies'] = False
        print(f"  [FAIL] Missing packages: {missing_packages}")
        print(f"  Install with: pip install {' '.join(missing_packages)}")
    else:
        print("  [OK] All required packages available")
    
    return requirements

def test_core_functionality() -> Dict[str, Any]:
    """Test core KeyHound functionality."""
    print("\nTesting core functionality...")
    
    try:
        # Test simple keyhound
        from core.simple_keyhound import SimpleKeyHound
        
        print("  [INFO] Initializing SimpleKeyHound...")
        keyhound = SimpleKeyHound(verbose=False)
        
        # Test system info
        system_info = keyhound.get_system_info()
        print(f"  [OK] System info: {system_info}")
        
        # Test brainwallet security (quick test)
        print("  [INFO] Testing brainwallet security...")
        brainwallet_results = keyhound.test_brainwallet_security(["password", "123456", "test"])
        print(f"  [OK] Brainwallet test: {len(brainwallet_results)} patterns tested")
        
        # Test performance stats
        perf_stats = keyhound.get_performance_stats()
        print(f"  [OK] Performance stats: {perf_stats}")
        
        return {
            'success': True,
            'system_info': system_info,
            'brainwallet_results': len(brainwallet_results),
            'performance_stats': perf_stats
        }
        
    except Exception as e:
        print(f"  [FAIL] Core functionality test failed: {e}")
        return {'success': False, 'error': str(e)}

def test_web_interface() -> Dict[str, Any]:
    """Test web interface functionality."""
    print("\nTesting web interface...")
    
    try:
        # Check if web interface module exists
        from web.web_interface import start_web_interface
        print("  [OK] Web interface module available")
        
        # Test if we can import Flask components
        import flask
        print(f"  [OK] Flask version: {flask.__version__}")
        
        return {
            'success': True,
            'flask_version': flask.__version__
        }
        
    except ImportError as e:
        print(f"  [FAIL] Web interface not available: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"  [FAIL] Web interface test failed: {e}")
        return {'success': False, 'error': str(e)}

def test_remote_stats() -> Dict[str, Any]:
    """Test remote statistics dashboard."""
    print("\nTesting remote statistics dashboard...")
    
    try:
        # Check if remote stats server exists
        from web.remote_stats_server import app, get_system_stats, get_keyhound_stats
        print("  [OK] Remote stats server module available")
        
        # Test system stats function
        system_stats = get_system_stats()
        print(f"  [OK] System stats: CPU {system_stats.get('cpu_percent', 0):.1f}%, Memory {system_stats.get('memory_percent', 0):.1f}%")
        
        # Test KeyHound stats function
        keyhound_stats = get_keyhound_stats()
        print(f"  [OK] KeyHound stats: {keyhound_stats.get('status', 'unknown')}")
        
        return {
            'success': True,
            'system_stats': system_stats,
            'keyhound_stats': keyhound_stats
        }
        
    except ImportError as e:
        print(f"  [FAIL] Remote stats not available: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"  [FAIL] Remote stats test failed: {e}")
        return {'success': False, 'error': str(e)}

def start_live_services() -> Dict[str, Any]:
    """Start live services for testing."""
    print("\nStarting live services...")
    
    services = {}
    
    try:
        # Start remote stats server
        print("  [INFO] Starting remote stats server...")
        
        # Import and start the server in a thread
        from web.remote_stats_server import app, socketio
        import threading
        
        def run_server():
            socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test if server is responding
        import requests
        try:
            response = requests.get('http://localhost:8080/api/health', timeout=5)
            if response.status_code == 200:
                print("  [OK] Remote stats server started successfully")
                services['remote_stats'] = {
                    'status': 'running',
                    'url': 'http://localhost:8080',
                    'health_check': response.json()
                }
            else:
                print(f"  [FAIL] Remote stats server health check failed: {response.status_code}")
                services['remote_stats'] = {'status': 'failed'}
        except requests.exceptions.RequestException as e:
            print(f"  [FAIL] Remote stats server not responding: {e}")
            services['remote_stats'] = {'status': 'failed', 'error': str(e)}
        
        return services
        
    except Exception as e:
        print(f"  [FAIL] Failed to start live services: {e}")
        return {'error': str(e)}

def run_live_tests() -> Dict[str, Any]:
    """Run comprehensive live tests."""
    print("=" * 60)
    print("KeyHound Enhanced - Live Deployment Testing")
    print("=" * 60)
    
    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'system_requirements': check_system_requirements(),
        'core_functionality': test_core_functionality(),
        'web_interface': test_web_interface(),
        'remote_stats': test_remote_stats(),
        'live_services': {},
        'ready_for_live': False
    }
    
    # Check if all tests passed
    all_passed = (
        results['system_requirements']['python_version'] and
        results['system_requirements']['dependencies'] and
        results['core_functionality']['success'] and
        results['web_interface']['success'] and
        results['remote_stats']['success']
    )
    
    if all_passed:
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED - STARTING LIVE SERVICES")
        print("=" * 60)
        
        # Start live services
        results['live_services'] = start_live_services()
        
        if results['live_services'].get('remote_stats', {}).get('status') == 'running':
            results['ready_for_live'] = True
            print("\n🎉 KEYHOUND ENHANCED IS LIVE! 🎉")
            print(f"Remote Stats Dashboard: http://localhost:8080")
            print(f"Health Check: http://localhost:8080/api/health")
            print(f"API Stats: http://localhost:8080/api/stats")
            print("\nPress Ctrl+C to stop the services")
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(60)
                    print(f"[{time.strftime('%H:%M:%S')}] Live services running...")
            except KeyboardInterrupt:
                print("\nStopping live services...")
        else:
            print("\n❌ Failed to start live services")
    else:
        print("\n" + "=" * 60)
        print("TESTS FAILED - SYSTEM NOT READY FOR LIVE DEPLOYMENT")
        print("=" * 60)
        
        if not results['system_requirements']['python_version']:
            print("❌ Python version incompatible")
        if not results['system_requirements']['dependencies']:
            print("❌ Missing dependencies")
        if not results['core_functionality']['success']:
            print("❌ Core functionality failed")
        if not results['web_interface']['success']:
            print("❌ Web interface failed")
        if not results['remote_stats']['success']:
            print("❌ Remote stats failed")
    
    return results

def main():
    """Main entry point."""
    try:
        results = run_live_tests()
        
        # Save results
        import json
        results_file = f"live_deployment_test_{int(time.time())}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nTest results saved to: {results_file}")
        
        return 0 if results['ready_for_live'] else 1
        
    except Exception as e:
        print(f"\n[ERROR] Live deployment test failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
