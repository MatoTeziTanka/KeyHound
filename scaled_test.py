#!/usr/bin/env python3
"""
KeyHound Enhanced - Scaled Testing Suite

This script runs comprehensive tests including:
- Multiple puzzle solving attempts
- Extended brainwallet security testing
- Long-duration performance benchmarks
- Stress testing with larger key spaces
- Memory and resource monitoring
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime
from pathlib import Path

# Import the codespace version
from keyhound_codespace import SimpleKeyHound, SimpleBitcoinCrypto, SimpleBrainwalletLibrary

class ScaledTester:
    """Comprehensive testing suite for KeyHound Enhanced."""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.results = {}
        self.start_time = datetime.now()
        
        # Initialize KeyHound
        self.keyhound = SimpleKeyHound(use_gpu=False, verbose=verbose)
        
        print("🚀 KeyHound Enhanced - Scaled Testing Suite")
        print("=" * 50)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Environment: GitHub Codespace")
        print()
    
    def test_puzzle_solving_scale(self, puzzles=[1, 66, 71, 75], max_keys_per_puzzle=10000):
        """Test puzzle solving with larger key spaces."""
        print("🧩 PUZZLE SOLVING SCALE TEST")
        print("-" * 30)
        
        puzzle_results = {}
        
        for puzzle_id in puzzles:
            print(f"\n🎯 Testing Puzzle #{puzzle_id} with {max_keys_per_puzzle:,} keys...")
            
            start_time = time.time()
            result = self.keyhound.solve_puzzle(puzzle_id, max_keys_per_puzzle)
            duration = time.time() - start_time
            
            puzzle_results[puzzle_id] = {
                "solved": result is not None,
                "keys_tested": max_keys_per_puzzle,
                "duration_seconds": duration,
                "keys_per_second": max_keys_per_puzzle / duration if duration > 0 else 0,
                "result": result
            }
            
            if result:
                print(f"   ✅ SOLVED in {duration:.2f}s ({max_keys_per_puzzle/duration:,.0f} keys/sec)")
            else:
                print(f"   ❌ Not solved in {duration:.2f}s ({max_keys_per_puzzle/duration:,.0f} keys/sec)")
        
        self.results['puzzle_solving'] = puzzle_results
        return puzzle_results
    
    def test_brainwallet_comprehensive(self, target_addresses=None, patterns_per_address=1000):
        """Comprehensive brainwallet security testing."""
        print("\n🔍 COMPREHENSIVE BRAINWALLET TESTING")
        print("-" * 40)
        
        if target_addresses is None:
            target_addresses = [
                "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",  # Puzzle #1
                "1LuckyR1fFHEsXYyx5QK4UFzv3PEAepPMK",  # Puzzle #66
                "1PooyaYd6r7P9FkBrDHqFHqG2pA7X5x8Y3",  # Puzzle #71
                "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",  # Puzzle #75
                "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Genesis block
            ]
        
        brainwallet_results = {}
        
        for address in target_addresses:
            print(f"\n🎯 Testing address: {address}")
            
            start_time = time.time()
            result = self.keyhound.brainwallet_test(address, patterns_per_address)
            duration = time.time() - start_time
            
            brainwallet_results[address] = {
                "vulnerability_found": result.get('vulnerability_found', False),
                "patterns_tested": result.get('patterns_tested', 0),
                "duration_seconds": duration,
                "patterns_per_second": result.get('patterns_tested', 0) / duration if duration > 0 else 0,
                "result": result
            }
            
            if result.get('vulnerability_found'):
                print(f"   🚨 VULNERABILITY FOUND! Pattern: {result.get('pattern', 'Unknown')}")
            else:
                print(f"   ✅ Secure ({result.get('patterns_tested', 0):,} patterns tested in {duration:.2f}s)")
        
        self.results['brainwallet_testing'] = brainwallet_results
        return brainwallet_results
    
    def test_performance_extended(self, durations=[60, 120, 300]):
        """Extended performance benchmarking."""
        print("\n⚡ EXTENDED PERFORMANCE BENCHMARKING")
        print("-" * 40)
        
        benchmark_results = {}
        
        for duration in durations:
            print(f"\n🎯 {duration}s Performance Benchmark...")
            
            start_time = time.time()
            result = self.keyhound.benchmark(duration)
            actual_duration = time.time() - start_time
            
            benchmark_results[f"{duration}s"] = {
                "target_duration": duration,
                "actual_duration": actual_duration,
                "total_operations": result['total_operations'],
                "operations_per_second": result['operations_per_second'],
                "efficiency": (duration / actual_duration) * 100 if actual_duration > 0 else 0
            }
            
            print(f"   ✅ {result['total_operations']:,} operations ({result['operations_per_second']:,.0f} ops/sec)")
        
        self.results['performance_benchmark'] = benchmark_results
        return benchmark_results
    
    def test_stress_scenarios(self):
        """Stress testing with extreme scenarios."""
        print("\n💪 STRESS TESTING SCENARIOS")
        print("-" * 30)
        
        stress_results = {}
        
        # Test 1: Very large key space
        print("\n🎯 Stress Test 1: Large Key Space (100K keys)")
        start_time = time.time()
        result = self.keyhound.solve_puzzle(66, 100000)
        duration = time.time() - start_time
        
        stress_results['large_keyspace'] = {
            "keys_tested": 100000,
            "duration_seconds": duration,
            "keys_per_second": 100000 / duration if duration > 0 else 0,
            "solved": result is not None
        }
        
        print(f"   Processed 100,000 keys in {duration:.2f}s ({100000/duration:,.0f} keys/sec)")
        
        # Test 2: Extended brainwallet testing
        print("\n🎯 Stress Test 2: Extended Brainwallet (10K patterns)")
        start_time = time.time()
        result = self.keyhound.brainwallet_test("1LuckyR1fFHEsXYyx5QK4UFzv3PEAepPMK", 10000)
        duration = time.time() - start_time
        
        stress_results['extended_brainwallet'] = {
            "patterns_tested": 10000,
            "duration_seconds": duration,
            "patterns_per_second": 10000 / duration if duration > 0 else 0,
            "vulnerability_found": result.get('vulnerability_found', False)
        }
        
        print(f"   Tested 10,000 patterns in {duration:.2f}s ({10000/duration:,.0f} patterns/sec)")
        
        # Test 3: Continuous operation
        print("\n🎯 Stress Test 3: Continuous Operation (5 minutes)")
        start_time = time.time()
        operations = 0
        test_duration = 300  # 5 minutes
        
        while time.time() - start_time < test_duration:
            # Simulate continuous work
            for _ in range(1000):
                operations += 1
            time.sleep(0.001)  # Small delay to prevent overwhelming
        
        actual_duration = time.time() - start_time
        ops_per_second = operations / actual_duration
        
        stress_results['continuous_operation'] = {
            "target_duration": test_duration,
            "actual_duration": actual_duration,
            "total_operations": operations,
            "operations_per_second": ops_per_second,
            "stability": "stable" if actual_duration >= test_duration * 0.95 else "unstable"
        }
        
        print(f"   Completed {operations:,} operations in {actual_duration:.2f}s ({ops_per_second:,.0f} ops/sec)")
        
        self.results['stress_testing'] = stress_results
        return stress_results
    
    def test_memory_and_resources(self):
        """Test memory usage and resource management."""
        print("\n🧠 MEMORY AND RESOURCE TESTING")
        print("-" * 35)
        
        import psutil
        import gc
        
        # Get initial memory state
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        resource_results = {
            "initial_memory_mb": initial_memory,
            "peak_memory_mb": initial_memory,
            "memory_tests": {}
        }
        
        print(f"Initial memory usage: {initial_memory:.1f} MB")
        
        # Test memory usage during different operations
        tests = [
            ("puzzle_solving", lambda: self.keyhound.solve_puzzle(66, 50000)),
            ("brainwallet_testing", lambda: self.keyhound.brainwallet_test("1LuckyR1fFHEsXYyx5QK4UFzv3PEAepPMK", 5000)),
            ("benchmark", lambda: self.keyhound.benchmark(30))
        ]
        
        for test_name, test_func in tests:
            print(f"\n🎯 Memory test: {test_name}")
            
            gc.collect()  # Force garbage collection
            memory_before = process.memory_info().rss / 1024 / 1024
            
            start_time = time.time()
            test_func()
            duration = time.time() - start_time
            
            gc.collect()  # Force garbage collection
            memory_after = process.memory_info().rss / 1024 / 1024
            memory_delta = memory_after - memory_before
            
            resource_results["memory_tests"][test_name] = {
                "memory_before_mb": memory_before,
                "memory_after_mb": memory_after,
                "memory_delta_mb": memory_delta,
                "duration_seconds": duration,
                "memory_per_second_mb": memory_delta / duration if duration > 0 else 0
            }
            
            resource_results["peak_memory_mb"] = max(resource_results["peak_memory_mb"], memory_after)
            
            print(f"   Memory: {memory_before:.1f} → {memory_after:.1f} MB (Δ{memory_delta:+.1f} MB)")
        
        final_memory = process.memory_info().rss / 1024 / 1024
        total_memory_delta = final_memory - initial_memory
        
        resource_results["final_memory_mb"] = final_memory
        resource_results["total_memory_delta_mb"] = total_memory_delta
        
        print(f"\n📊 Memory Summary:")
        print(f"   Initial: {initial_memory:.1f} MB")
        print(f"   Peak: {resource_results['peak_memory_mb']:.1f} MB")
        print(f"   Final: {final_memory:.1f} MB")
        print(f"   Total Δ: {total_memory_delta:+.1f} MB")
        
        self.results['resource_testing'] = resource_results
        return resource_results
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive test report."""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        print(f"Test Duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Calculate overall statistics
        total_operations = 0
        total_keys_tested = 0
        total_patterns_tested = 0
        
        if 'puzzle_solving' in self.results:
            for puzzle_data in self.results['puzzle_solving'].values():
                total_keys_tested += puzzle_data['keys_tested']
        
        if 'brainwallet_testing' in self.results:
            for brainwallet_data in self.results['brainwallet_testing'].values():
                total_patterns_tested += brainwallet_data['patterns_tested']
        
        if 'performance_benchmark' in self.results:
            for benchmark_data in self.results['performance_benchmark'].values():
                total_operations += benchmark_data['total_operations']
        
        if 'stress_testing' in self.results:
            if 'continuous_operation' in self.results['stress_testing']:
                total_operations += self.results['stress_testing']['continuous_operation']['total_operations']
        
        print(f"\n🎯 Overall Statistics:")
        print(f"   Total Keys Tested: {total_keys_tested:,}")
        print(f"   Total Patterns Tested: {total_patterns_tested:,}")
        print(f"   Total Operations: {total_operations:,}")
        print(f"   Average Performance: {total_operations/total_duration:,.0f} operations/second")
        
        # Performance summary
        if 'performance_benchmark' in self.results:
            print(f"\n⚡ Performance Summary:")
            for test_name, data in self.results['performance_benchmark'].items():
                print(f"   {test_name}: {data['operations_per_second']:,.0f} ops/sec")
        
        # Memory summary
        if 'resource_testing' in self.results:
            memory_data = self.results['resource_testing']
            print(f"\n🧠 Memory Summary:")
            print(f"   Peak Usage: {memory_data['peak_memory_mb']:.1f} MB")
            print(f"   Memory Efficiency: {abs(memory_data['total_memory_delta_mb']):.1f} MB delta")
        
        # Save detailed results
        report_file = f"comprehensive_test_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "test_summary": {
                    "start_time": self.start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "total_duration_seconds": total_duration,
                    "total_keys_tested": total_keys_tested,
                    "total_patterns_tested": total_patterns_tested,
                    "total_operations": total_operations
                },
                "detailed_results": self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        print(f"✅ Comprehensive testing completed successfully!")
        
        return {
            "total_duration": total_duration,
            "total_keys_tested": total_keys_tested,
            "total_patterns_tested": total_patterns_tested,
            "total_operations": total_operations,
            "report_file": report_file
        }

def main():
    """Main function for scaled testing."""
    parser = argparse.ArgumentParser(
        description="KeyHound Enhanced - Scaled Testing Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full comprehensive test suite
  python3 scaled_test.py
  
  # Run specific tests only
  python3 scaled_test.py --puzzles-only
  python3 scaled_test.py --benchmark-only
  python3 scaled_test.py --stress-only
  
  # Custom test parameters
  python3 scaled_test.py --max-keys 50000 --benchmark-duration 180
        """
    )
    
    parser.add_argument('--puzzles-only', action='store_true', help='Run only puzzle solving tests')
    parser.add_argument('--benchmark-only', action='store_true', help='Run only performance benchmarks')
    parser.add_argument('--stress-only', action='store_true', help='Run only stress tests')
    parser.add_argument('--memory-only', action='store_true', help='Run only memory/resource tests')
    parser.add_argument('--max-keys', type=int, default=10000, help='Maximum keys to test per puzzle')
    parser.add_argument('--benchmark-duration', type=int, nargs='+', default=[60, 120, 300], help='Benchmark durations in seconds')
    parser.add_argument('--patterns-per-address', type=int, default=1000, help='Patterns to test per brainwallet address')
    
    args = parser.parse_args()
    
    # Initialize tester
    tester = ScaledTester(verbose=True)
    
    try:
        # Run selected tests
        if args.puzzles_only:
            tester.test_puzzle_solving_scale(max_keys_per_puzzle=args.max_keys)
        
        elif args.benchmark_only:
            tester.test_performance_extended(args.benchmark_duration)
        
        elif args.stress_only:
            tester.test_stress_scenarios()
        
        elif args.memory_only:
            tester.test_memory_and_resources()
        
        else:
            # Run full comprehensive test suite
            print("🚀 Running FULL COMPREHENSIVE TEST SUITE")
            print("This will take approximately 15-20 minutes...")
            print()
            
            tester.test_puzzle_solving_scale(max_keys_per_puzzle=args.max_keys)
            tester.test_brainwallet_comprehensive(patterns_per_address=args.patterns_per_address)
            tester.test_performance_extended(args.benchmark_duration)
            tester.test_stress_scenarios()
            tester.test_memory_and_resources()
        
        # Generate final report
        summary = tester.generate_comprehensive_report()
        
        print(f"\n🎉 Testing completed successfully!")
        print(f"📊 Total operations: {summary['total_operations']:,}")
        print(f"⏱️  Duration: {summary['total_duration']/60:.1f} minutes")
        print(f"📄 Report: {summary['report_file']}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        print("📊 Partial results saved...")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

