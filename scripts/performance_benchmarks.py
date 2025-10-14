#!/usr/bin/env python3
"""
KeyHound Enhanced - Performance Benchmarks
==========================================

Comprehensive performance benchmarking system for KeyHound Enhanced.
Establishes baseline performance metrics and monitoring thresholds.

Author: KeyHound Enhanced Performance Team
Version: 2.0.0
"""

import os
import sys
import time
import json
import logging
import psutil
import platform
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Add KeyHound root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.simple_keyhound import SimpleKeyHound
from core.bitcoin_cryptography import BitcoinCryptography
from core.brainwallet_patterns import BrainwalletPatternLibrary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkResult:
    """Represents a benchmark test result."""
    test_name: str
    duration: float
    iterations: int
    rate_per_second: float
    memory_usage_mb: float
    cpu_usage_percent: float
    success: bool
    error_message: Optional[str] = None
    additional_metrics: Dict[str, Any] = None

@dataclass
class SystemInfo:
    """System information for benchmarking."""
    platform: str
    cpu_count: int
    memory_gb: float
    python_version: str
    gpu_available: bool
    gpu_name: Optional[str] = None

class PerformanceBenchmarker:
    """Comprehensive performance benchmarking system."""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.system_info = self._get_system_info()
        self.start_time = time.time()
        
        # Initialize KeyHound components
        try:
            self.keyhound = SimpleKeyHound(verbose=False)
            self.crypto = BitcoinCryptography()
            self.pattern_lib = BrainwalletPatternLibrary()
        except Exception as e:
            logger.error(f"Failed to initialize KeyHound components: {e}")
            sys.exit(1)
    
    def _get_system_info(self) -> SystemInfo:
        """Gather system information."""
        try:
            # Check for GPU
            gpu_available = False
            gpu_name = None
            try:
                import torch
                gpu_available = torch.cuda.is_available()
                if gpu_available:
                    gpu_name = torch.cuda.get_device_name(0)
            except ImportError:
                pass
            
            return SystemInfo(
                platform=platform.platform(),
                cpu_count=os.cpu_count() or 1,
                memory_gb=psutil.virtual_memory().total / (1024**3),
                python_version=platform.python_version(),
                gpu_available=gpu_available,
                gpu_name=gpu_name
            )
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return SystemInfo(
                platform="Unknown",
                cpu_count=1,
                memory_gb=4.0,
                python_version="Unknown",
                gpu_available=False
            )
    
    def _measure_performance(self, test_name: str, test_function, *args, **kwargs) -> BenchmarkResult:
        """Measure performance of a test function."""
        logger.info(f"Running benchmark: {test_name}")
        
        # Get initial resource usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        initial_cpu = process.cpu_percent()
        
        try:
            start_time = time.time()
            result = test_function(*args, **kwargs)
            end_time = time.time()
            
            duration = end_time - start_time
            
            # Get final resource usage
            final_memory = process.memory_info().rss / (1024 * 1024)  # MB
            final_cpu = process.cpu_percent()
            
            # Calculate metrics
            iterations = result.get('iterations', 1) if isinstance(result, dict) else 1
            rate_per_second = iterations / duration if duration > 0 else 0
            memory_usage = final_memory - initial_memory
            cpu_usage = (initial_cpu + final_cpu) / 2
            
            return BenchmarkResult(
                test_name=test_name,
                duration=duration,
                iterations=iterations,
                rate_per_second=rate_per_second,
                memory_usage_mb=memory_usage,
                cpu_usage_percent=cpu_usage,
                success=True,
                additional_metrics=result if isinstance(result, dict) else {}
            )
            
        except Exception as e:
            logger.error(f"Benchmark {test_name} failed: {e}")
            return BenchmarkResult(
                test_name=test_name,
                duration=0,
                iterations=0,
                rate_per_second=0,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                success=False,
                error_message=str(e)
            )
    
    def benchmark_private_key_generation(self) -> BenchmarkResult:
        """Benchmark private key generation."""
        def test_function():
            iterations = 10000
            start_time = time.time()
            
            for _ in range(iterations):
                private_key = self.crypto.generate_private_key()
                assert len(private_key) == 64  # 32 bytes = 64 hex chars
            
            return {'iterations': iterations}
        
        return self._measure_performance("Private Key Generation", test_function)
    
    def benchmark_address_generation(self) -> BenchmarkResult:
        """Benchmark Bitcoin address generation."""
        def test_function():
            iterations = 5000
            start_time = time.time()
            
            for _ in range(iterations):
                private_key = self.crypto.generate_private_key()
                address = self.crypto.generate_bitcoin_address(private_key)
                assert len(address) > 20  # Valid Bitcoin address length
            
            return {'iterations': iterations}
        
        return self._measure_performance("Address Generation", test_function)
    
    def benchmark_brainwallet_testing(self) -> BenchmarkResult:
        """Benchmark brainwallet pattern testing."""
        def test_function():
            test_patterns = ["password", "123456", "bitcoin", "wallet", "crypto"]
            start_time = time.time()
            
            results = self.keyhound.test_brainwallet_security(test_patterns)
            
            return {
                'iterations': len(test_patterns),
                'patterns_tested': len(results),
                'vulnerable_found': sum(1 for r in results if r.get('vulnerable'))
            }
        
        return self._measure_performance("Brainwallet Testing", test_function)
    
    def benchmark_puzzle_solving(self, bits: int = 20) -> BenchmarkResult:
        """Benchmark puzzle solving performance."""
        def test_function():
            max_attempts = 100000
            start_time = time.time()
            
            # Simulate puzzle solving without actually solving
            keys_generated = 0
            for _ in range(max_attempts):
                private_key = self.crypto.generate_private_key()
                address = self.crypto.generate_bitcoin_address(private_key)
                keys_generated += 1
            
            return {
                'iterations': keys_generated,
                'bits': bits,
                'max_attempts': max_attempts
            }
        
        return self._measure_performance(f"Puzzle Solving ({bits}-bit)", test_function)
    
    def benchmark_pattern_library_search(self) -> BenchmarkResult:
        """Benchmark pattern library operations."""
        def test_function():
            iterations = 1000
            start_time = time.time()
            
            for _ in range(iterations):
                # Test pattern search
                patterns = self.pattern_lib.get_top_patterns(10)
                assert len(patterns) == 10
            
            return {'iterations': iterations}
        
        return self._measure_performance("Pattern Library Search", test_function)
    
    def benchmark_memory_usage(self) -> BenchmarkResult:
        """Benchmark memory usage patterns."""
        def test_function():
            iterations = 100
            large_data = []
            
            for i in range(iterations):
                # Create some memory usage
                data = [self.crypto.generate_private_key() for _ in range(1000)]
                large_data.append(data)
            
            # Clean up
            del large_data
            
            return {'iterations': iterations}
        
        return self._measure_performance("Memory Usage", test_function)
    
    def benchmark_gpu_operations(self) -> Optional[BenchmarkResult]:
        """Benchmark GPU operations if available."""
        if not self.system_info.gpu_available:
            logger.info("GPU not available, skipping GPU benchmarks")
            return None
        
        def test_function():
            try:
                import torch
                
                # Test GPU tensor operations
                iterations = 1000
                device = torch.device('cuda')
                
                for _ in range(iterations):
                    # Create tensors on GPU
                    a = torch.randn(1000, 1000, device=device)
                    b = torch.randn(1000, 1000, device=device)
                    c = torch.mm(a, b)  # Matrix multiplication
                
                return {'iterations': iterations, 'gpu_name': self.system_info.gpu_name}
                
            except Exception as e:
                raise Exception(f"GPU benchmark failed: {e}")
        
        return self._measure_performance("GPU Operations", test_function)
    
    def run_comprehensive_benchmarks(self) -> Dict[str, Any]:
        """Run all benchmark tests."""
        logger.info("Starting comprehensive performance benchmarks...")
        logger.info(f"System: {self.system_info.platform}")
        logger.info(f"CPU Cores: {self.system_info.cpu_count}")
        logger.info(f"Memory: {self.system_info.memory_gb:.1f} GB")
        logger.info(f"Python: {self.system_info.python_version}")
        logger.info(f"GPU: {'Available' if self.system_info.gpu_available else 'Not Available'}")
        if self.system_info.gpu_name:
            logger.info(f"GPU Name: {self.system_info.gpu_name}")
        
        # Run all benchmarks
        benchmarks = [
            self.benchmark_private_key_generation,
            self.benchmark_address_generation,
            self.benchmark_brainwallet_testing,
            self.benchmark_puzzle_solving,
            self.benchmark_pattern_library_search,
            self.benchmark_memory_usage,
        ]
        
        # Add GPU benchmark if available
        gpu_benchmark = self.benchmark_gpu_operations()
        if gpu_benchmark:
            benchmarks.append(lambda: gpu_benchmark)
        
        # Run benchmarks
        for benchmark_func in benchmarks:
            try:
                result = benchmark_func()
                self.results.append(result)
            except Exception as e:
                logger.error(f"Benchmark failed: {e}")
        
        # Generate summary
        total_time = time.time() - self.start_time
        summary = self._generate_summary(total_time)
        
        # Log results
        self._log_results()
        
        return summary
    
    def _generate_summary(self, total_time: float) -> Dict[str, Any]:
        """Generate benchmark summary."""
        successful_results = [r for r in self.results if r.success]
        failed_results = [r for r in self.results if not r.success]
        
        # Calculate averages
        avg_rate = sum(r.rate_per_second for r in successful_results) / len(successful_results) if successful_results else 0
        avg_memory = sum(r.memory_usage_mb for r in successful_results) / len(successful_results) if successful_results else 0
        avg_cpu = sum(r.cpu_usage_percent for r in successful_results) / len(successful_results) if successful_results else 0
        
        # Performance categories
        excellent_results = [r for r in successful_results if r.rate_per_second > 10000]
        good_results = [r for r in successful_results if 1000 <= r.rate_per_second <= 10000]
        poor_results = [r for r in successful_results if r.rate_per_second < 1000]
        
        return {
            "system_info": asdict(self.system_info),
            "total_tests": len(self.results),
            "successful_tests": len(successful_results),
            "failed_tests": len(failed_results),
            "total_time": total_time,
            "average_rate_per_second": avg_rate,
            "average_memory_usage_mb": avg_memory,
            "average_cpu_usage_percent": avg_cpu,
            "performance_categories": {
                "excellent": len(excellent_results),
                "good": len(good_results),
                "poor": len(poor_results)
            },
            "results": [asdict(r) for r in self.results]
        }
    
    def _log_results(self):
        """Log benchmark results."""
        logger.info("\n" + "=" * 60)
        logger.info("PERFORMANCE BENCHMARK RESULTS")
        logger.info("=" * 60)
        
        for result in self.results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            logger.info(f"{status} {result.test_name}")
            logger.info(f"   Duration: {result.duration:.2f}s")
            logger.info(f"   Rate: {result.rate_per_second:.0f} ops/sec")
            logger.info(f"   Memory: {result.memory_usage_mb:.1f} MB")
            logger.info(f"   CPU: {result.cpu_usage_percent:.1f}%")
            if result.error_message:
                logger.info(f"   Error: {result.error_message}")
        
        # Summary
        successful = sum(1 for r in self.results if r.success)
        total = len(self.results)
        logger.info(f"\nSUMMARY: {successful}/{total} tests passed")
        
        # Performance thresholds
        logger.info("\nPERFORMANCE THRESHOLDS:")
        logger.info("  Excellent: >10,000 ops/sec")
        logger.info("  Good: 1,000-10,000 ops/sec")
        logger.info("  Poor: <1,000 ops/sec")
    
    def save_results(self, filename: str = None) -> str:
        """Save benchmark results to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        summary = self._generate_summary(time.time() - self.start_time)
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Benchmark results saved to: {filename}")
        return filename

def main():
    """Main entry point for performance benchmarking."""
    print("KeyHound Enhanced - Performance Benchmarks")
    print("=" * 50)
    
    benchmarker = PerformanceBenchmarker()
    summary = benchmarker.run_comprehensive_benchmarks()
    
    # Save results
    results_file = benchmarker.save_results()
    
    # Print final summary
    print(f"\nBenchmark completed in {summary['total_time']:.2f} seconds")
    print(f"Results: {summary['successful_tests']}/{summary['total_tests']} tests passed")
    print(f"Average performance: {summary['average_rate_per_second']:.0f} ops/sec")
    print(f"Results saved to: {results_file}")

if __name__ == "__main__":
    main()
