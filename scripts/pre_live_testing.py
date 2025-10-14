#!/usr/bin/env python3
"""
KeyHound Enhanced - Pre-Live Testing Script
Comprehensive testing of all components before live deployment.
"""

import os
import sys
import time
import json
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PreLiveTester:
    """Comprehensive pre-live testing system."""
    
    def __init__(self):
        self.test_results = {}
        self.failed_tests = []
        self.passed_tests = []
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all pre-live tests."""
        print("=" * 60)
        print("KeyHound Enhanced - Pre-Live Testing")
        print("=" * 60)
        
        tests = [
            ("Dependency Check", self.test_dependencies),
            ("Core Components", self.test_core_components),
            ("Hardware Scorer", self.test_hardware_scorer),
            ("Pool Coordinator", self.test_pool_coordinator),
            ("Pool Server API", self.test_pool_server_api),
            ("Pool Client", self.test_pool_client),
            ("Security Features", self.test_security_features),
            ("Reward Calculations", self.test_reward_calculations),
            ("Performance Benchmarks", self.test_performance_benchmarks),
            ("Documentation", self.test_documentation),
            ("Integration Test", self.test_integration)
        ]
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_func()
                if result.get('success', False):
                    self.passed_tests.append(test_name)
                    print(f"[PASS] {test_name}")
                else:
                    self.failed_tests.append(test_name)
                    print(f"[FAIL] {test_name}: {result.get('error', 'Unknown error')}")
                
                self.test_results[test_name] = result
                
            except Exception as e:
                self.failed_tests.append(test_name)
                print(f"[ERROR] {test_name}: {e}")
                self.test_results[test_name] = {'success': False, 'error': str(e)}
        
        return self.generate_test_report()
    
    def test_dependencies(self) -> Dict[str, Any]:
        """Test all required dependencies."""
        dependencies = [
            ('flask', 'Flask'),
            ('flask_cors', 'Flask-CORS'),
            ('psutil', 'psutil'),
            ('cryptography', 'cryptography'),
            ('requests', 'requests'),
            ('yaml', 'PyYAML')
        ]
        
        missing_deps = []
        for module_name, package_name in dependencies:
            try:
                __import__(module_name)
                print(f"  [OK] {package_name}")
            except ImportError:
                missing_deps.append(package_name)
                print(f"  [MISSING] {package_name}")
        
        if missing_deps:
            return {
                'success': False,
                'error': f'Missing dependencies: {", ".join(missing_deps)}',
                'missing_deps': missing_deps
            }
        
        return {'success': True, 'message': 'All dependencies available'}
    
    def test_core_components(self) -> Dict[str, Any]:
        """Test core KeyHound components."""
        core_modules = [
            'core.simple_keyhound',
            'core.bitcoin_cryptography',
            'core.puzzle_data',
            'core.brainwallet_patterns',
            'core.error_handling'
        ]
        
        failed_imports = []
        for module in core_modules:
            try:
                __import__(module)
                print(f"  [OK] {module}")
            except ImportError as e:
                failed_imports.append(f"{module}: {e}")
                print(f"  [FAIL] {module}: {e}")
        
        if failed_imports:
            return {
                'success': False,
                'error': f'Failed imports: {"; ".join(failed_imports)}',
                'failed_imports': failed_imports
            }
        
        return {'success': True, 'message': 'All core components available'}
    
    def test_hardware_scorer(self) -> Dict[str, Any]:
        """Test hardware performance scoring system."""
        try:
            from pool.hardware_scorer import HardwarePerformanceScorer
            
            scorer = HardwarePerformanceScorer()
            
            # Test hardware specs detection
            specs = scorer.get_hardware_specs("test_user", "test_device")
            print(f"  [OK] Hardware specs detected: {specs.device_type}")
            
            # Test quick performance test (10 seconds for testing)
            print("  [INFO] Running quick performance test (10s)...")
            tests = scorer.run_quick_performance_test(10)
            print(f"  [OK] Performance tests completed: {len(tests)} tests")
            
            # Test score calculation
            score = scorer.calculate_hardware_score(specs, tests)
            print(f"  [OK] Hardware score calculated: {score.combined_score:.2f}")
            
            return {
                'success': True,
                'message': 'Hardware scorer working correctly',
                'score': score.combined_score,
                'reward_percentage': score.reward_percentage
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_pool_coordinator(self) -> Dict[str, Any]:
        """Test pool coordinator functionality."""
        try:
            from pool.pool_coordinator import DistributedPoolCoordinator
            
            # Initialize coordinator
            coordinator = DistributedPoolCoordinator("test_owner", "test_public_key")
            print("  [OK] Pool coordinator initialized")
            
            # Test participant registration
            result = coordinator.register_participant("test_user", "test_device", "test_key")
            if result.get('success'):
                print("  [OK] Participant registration working")
            else:
                return {'success': False, 'error': f'Registration failed: {result.get("error")}'}
            
            # Test work assignment
            work_result = coordinator.assign_work("test_puzzle", 40)
            if work_result.get('success'):
                print("  [OK] Work assignment working")
            else:
                return {'success': False, 'error': f'Work assignment failed: {work_result.get("error")}'}
            
            # Test statistics
            stats = coordinator.get_pool_statistics()
            print(f"  [OK] Pool statistics: {stats['total_participants']} participants")
            
            return {
                'success': True,
                'message': 'Pool coordinator working correctly',
                'participants': stats['total_participants']
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_pool_server_api(self) -> Dict[str, Any]:
        """Test pool server API functionality."""
        try:
            from pool.pool_server import PoolServerAPI
            
            # Initialize server (don't start it)
            server = PoolServerAPI("test_owner", "test_key", host='127.0.0.1', port=18080)
            print("  [OK] Pool server initialized")
            
            # Test Flask app creation
            if hasattr(server, 'app'):
                print("  [OK] Flask app created")
            else:
                return {'success': False, 'error': 'Flask app not created'}
            
            # Test route registration
            routes = [rule.rule for rule in server.app.url_map.iter_rules()]
            expected_routes = ['/api/health', '/api/register', '/api/request_work', '/api/submit_key']
            
            missing_routes = []
            for route in expected_routes:
                if route not in routes:
                    missing_routes.append(route)
            
            if missing_routes:
                return {'success': False, 'error': f'Missing routes: {missing_routes}'}
            
            print(f"  [OK] API routes registered: {len(routes)} routes")
            
            return {
                'success': True,
                'message': 'Pool server API working correctly',
                'routes': len(routes)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_pool_client(self) -> Dict[str, Any]:
        """Test pool client functionality."""
        try:
            from pool.community_pool_client import CommunityPoolClient
            
            # Initialize client (don't connect to server)
            client = CommunityPoolClient("http://localhost:18080", "test_user")
            print("  [OK] Pool client initialized")
            
            # Test hardware scorer integration
            if hasattr(client, 'hardware_scorer'):
                print("  [OK] Hardware scorer integrated")
            else:
                return {'success': False, 'error': 'Hardware scorer not integrated'}
            
            # Test KeyHound integration
            if hasattr(client, 'keyhound'):
                print("  [OK] KeyHound integration available")
            else:
                print("  [WARN] KeyHound integration not available (optional)")
            
            return {
                'success': True,
                'message': 'Pool client working correctly'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_security_features(self) -> Dict[str, Any]:
        """Test security features."""
        try:
            from pool.pool_coordinator import SecureKeyDelivery
            
            # Test encryption/decryption
            secure_delivery = SecureKeyDelivery("test_public_key")
            
            # Test key encryption
            test_key = "test_private_key_12345"
            test_metadata = {"finder": "test_user", "puzzle_id": "test_puzzle"}
            
            encrypted_key = secure_delivery.encrypt_key_for_owner(test_key, test_metadata)
            print("  [OK] Key encryption working")
            
            # Test key decryption
            decrypted_payload = secure_delivery.decrypt_key_for_owner(encrypted_key)
            print("  [OK] Key decryption working")
            
            # Verify data integrity
            if decrypted_payload['private_key'] == test_key:
                print("  [OK] Data integrity verified")
            else:
                return {'success': False, 'error': 'Data integrity check failed'}
            
            return {
                'success': True,
                'message': 'Security features working correctly'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_reward_calculations(self) -> Dict[str, Any]:
        """Test reward distribution calculations."""
        try:
            from pool.pool_coordinator import RewardDistributor, PoolParticipant
            from pool.hardware_scorer import HardwareScore
            
            distributor = RewardDistributor()
            
            # Create test participants
            participants = []
            for i in range(3):
                score = HardwareScore(
                    device_id=f"device_{i}",
                    user_id=f"user_{i}",
                    base_score=100 + i * 50,
                    efficiency_score=80 + i * 10,
                    power_score=90 + i * 5,
                    combined_score=100 + i * 50,
                    reward_percentage=0.1 + i * 0.01,
                    test_results=[],
                    last_updated="2024-01-01T00:00:00",
                    score_history=[]
                )
                
                participant = PoolParticipant(
                    user_id=f"user_{i}",
                    device_id=f"device_{i}",
                    device_name=f"device_{i}",
                    hardware_score=score,
                    joined_at="2024-01-01T00:00:00",
                    last_active="2024-01-01T00:00:00",
                    total_work_contributed=0,
                    current_reward_percentage=score.reward_percentage,
                    devices=[f"device_{i}"]
                )
                participants.append(participant)
            
            # Test reward distribution
            distribution = distributor.calculate_reward_distribution(1.0, participants, participants[0])
            print("  [OK] Reward distribution calculated")
            
            # Verify distribution totals
            total_distributed = sum(distribution.values())
            if abs(total_distributed - 1.0) < 0.001:  # Allow for floating point precision
                print("  [OK] Reward distribution totals correct")
            else:
                return {'success': False, 'error': f'Distribution total incorrect: {total_distributed}'}
            
            # Verify pool owner gets 40%
            if abs(distribution.get('pool_owner', 0) - 0.4) < 0.001:
                print("  [OK] Pool owner share correct (40%)")
            else:
                return {'success': False, 'error': f'Pool owner share incorrect: {distribution.get("pool_owner", 0)}'}
            
            return {
                'success': True,
                'message': 'Reward calculations working correctly',
                'distribution': distribution
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance benchmarking system."""
        try:
            # Check if benchmark script exists and is runnable
            benchmark_script = Path("scripts/performance_benchmarks.py")
            if not benchmark_script.exists():
                return {'success': False, 'error': 'Performance benchmarks script not found'}
            
            print("  [OK] Performance benchmarks script found")
            
            # Test if we can import the benchmark components
            try:
                from core.simple_keyhound import SimpleKeyHound
                from core.bitcoin_cryptography import BitcoinCryptography
                print("  [OK] Benchmark components available")
            except ImportError as e:
                return {'success': False, 'error': f'Benchmark components not available: {e}'}
            
            return {
                'success': True,
                'message': 'Performance benchmarking system ready'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_documentation(self) -> Dict[str, Any]:
        """Test documentation completeness."""
        required_docs = [
            'README.md',
            'docs/DISTRIBUTED_POOL_GUIDE.md',
            'docs/PUBLIC_DEMO_INSTRUCTIONS.md',
            'docs/API_REFERENCE.md'
        ]
        
        missing_docs = []
        for doc in required_docs:
            if Path(doc).exists():
                print(f"  [OK] {doc}")
            else:
                missing_docs.append(doc)
                print(f"  [MISSING] {doc}")
        
        if missing_docs:
            return {
                'success': False,
                'error': f'Missing documentation: {missing_docs}',
                'missing_docs': missing_docs
            }
        
        return {'success': True, 'message': 'All required documentation present'}
    
    def test_integration(self) -> Dict[str, Any]:
        """Test end-to-end integration."""
        try:
            print("  [INFO] Testing component integration...")
            
            # Test that all components can work together
            from pool.pool_coordinator import DistributedPoolCoordinator
            from pool.hardware_scorer import HardwarePerformanceScorer
            
            # Initialize components
            coordinator = DistributedPoolCoordinator("test_owner", "test_key")
            scorer = HardwarePerformanceScorer()
            
            # Test full workflow
            specs = scorer.get_hardware_specs("integration_test", "test_device")
            tests = scorer.run_quick_performance_test(5)  # Quick test
            score = scorer.calculate_hardware_score(specs, tests)
            
            result = coordinator.register_participant("integration_test", "test_device", "test_key")
            
            if result.get('success'):
                print("  [OK] End-to-end integration working")
                return {
                    'success': True,
                    'message': 'Integration test passed'
                }
            else:
                return {'success': False, 'error': f'Integration test failed: {result.get("error")}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        total_tests = len(self.test_results)
        passed_count = len(self.passed_tests)
        failed_count = len(self.failed_tests)
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': total_tests,
            'passed_tests': passed_count,
            'failed_tests': failed_count,
            'success_rate': (passed_count / total_tests * 100) if total_tests > 0 else 0,
            'passed_test_list': self.passed_tests,
            'failed_test_list': self.failed_tests,
            'test_results': self.test_results,
            'ready_for_live': failed_count == 0,
            'recommendations': self.generate_recommendations()
        }
        
        # Save report
        report_file = f"pre_live_test_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        if self.failed_tests:
            recommendations.append("Fix all failed tests before live deployment")
        
        if "Dependency Check" in self.failed_tests:
            recommendations.append("Install missing dependencies: pip install -r requirements.txt")
        
        if "Security Features" in self.failed_tests:
            recommendations.append("Critical: Fix security features before deployment")
        
        if "Pool Server API" in self.failed_tests:
            recommendations.append("Fix pool server API issues")
        
        if "Reward Calculations" in self.failed_tests:
            recommendations.append("Fix reward calculation system")
        
        if len(self.passed_tests) == len(self.test_results):
            recommendations.append("All tests passed! System ready for live deployment")
            recommendations.append("Consider running a small-scale test with a few participants first")
            recommendations.append("Monitor system performance and user feedback")
        
        return recommendations

def main():
    """Main entry point."""
    tester = PreLiveTester()
    report = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("PRE-LIVE TESTING REPORT")
    print("=" * 60)
    print(f"Total Tests: {report['total_tests']}")
    print(f"Passed: {report['passed_tests']}")
    print(f"Failed: {report['failed_tests']}")
    print(f"Success Rate: {report['success_rate']:.1f}%")
    print(f"Ready for Live: {'YES' if report['ready_for_live'] else 'NO'}")
    
    if report['failed_test_list']:
        print(f"\nFailed Tests:")
        for test in report['failed_test_list']:
            print(f"  - {test}")
    
    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  - {rec}")
    
    if report['ready_for_live']:
        print(f"\n🎉 SYSTEM READY FOR LIVE DEPLOYMENT! 🎉")
    else:
        print(f"\n❌ SYSTEM NOT READY - FIX FAILED TESTS FIRST ❌")
    
    return 0 if report['ready_for_live'] else 1

if __name__ == '__main__':
    sys.exit(main())
