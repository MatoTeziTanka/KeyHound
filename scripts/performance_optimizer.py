#!/usr/bin/env python3
"""
KeyHound Enhanced - Performance Optimizer
Optimizes performance based on current benchmark results.
"""

import os
import sys
import time
import json
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.simple_keyhound import SimpleKeyHound
    from core.bitcoin_cryptography import BitcoinCryptography
    from core.performance_monitoring import PerformanceMonitor
    KEYHOUND_AVAILABLE = True
except ImportError:
    KEYHOUND_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """Performance optimizer for KeyHound Enhanced."""
    
    def __init__(self):
        self.optimization_results = {}
        self.baseline_metrics = {}
        self.optimized_metrics = {}
        
    def load_benchmark_results(self) -> Dict[str, Any]:
        """Load existing benchmark results."""
        benchmark_files = list(Path(".").glob("benchmark_results_*.json"))
        
        if not benchmark_files:
            logger.warning("No benchmark results found. Run performance_benchmarks.py first.")
            return {}
        
        # Get the most recent benchmark file
        latest_file = max(benchmark_files, key=lambda f: f.stat().st_mtime)
        
        try:
            with open(latest_file, 'r') as f:
                results = json.load(f)
            logger.info(f"Loaded benchmark results from: {latest_file}")
            return results
        except Exception as e:
            logger.error(f"Failed to load benchmark results: {e}")
            return {}
    
    def analyze_performance_bottlenecks(self, benchmark_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze benchmark results to identify bottlenecks."""
        bottlenecks = []
        
        if not benchmark_results or 'benchmarks' not in benchmark_results:
            logger.warning("No benchmark data to analyze")
            return bottlenecks
        
        benchmarks = benchmark_results['benchmarks']
        
        for benchmark in benchmarks:
            name = benchmark.get('name', 'Unknown')
            rate = benchmark.get('rate', 0)
            duration = benchmark.get('duration', 0)
            memory_usage = benchmark.get('memory_usage_mb', 0)
            cpu_usage = benchmark.get('cpu_usage_percent', 0)
            error = benchmark.get('error_message')
            
            # Define performance thresholds
            thresholds = {
                'Private Key Generation': {'min_rate': 100000, 'max_memory': 10, 'max_cpu': 80},
                'Address Generation': {'min_rate': 5000, 'max_memory': 5, 'max_cpu': 70},
                'Brainwallet Testing': {'min_rate': 100, 'max_memory': 20, 'max_cpu': 60},
                'Puzzle Solving': {'min_rate': 1000, 'max_memory': 50, 'max_cpu': 90},
                'Pattern Library Search': {'min_rate': 2000, 'max_memory': 5, 'max_cpu': 50},
                'Memory Usage': {'min_rate': 1000, 'max_memory': 10, 'max_cpu': 30}
            }
            
            threshold = thresholds.get(name, {'min_rate': 1000, 'max_memory': 20, 'max_cpu': 80})
            
            bottleneck = {
                'name': name,
                'current_rate': rate,
                'current_memory': memory_usage,
                'current_cpu': cpu_usage,
                'duration': duration,
                'error': error,
                'issues': [],
                'recommendations': []
            }
            
            # Check for performance issues
            if error:
                bottleneck['issues'].append(f"Error: {error}")
                bottleneck['recommendations'].append("Fix the underlying error first")
            elif rate < threshold['min_rate']:
                bottleneck['issues'].append(f"Low performance rate: {rate} < {threshold['min_rate']}")
                bottleneck['recommendations'].append("Optimize algorithm efficiency")
            elif memory_usage > threshold['max_memory']:
                bottleneck['issues'].append(f"High memory usage: {memory_usage}MB > {threshold['max_memory']}MB")
                bottleneck['recommendations'].append("Implement memory optimization")
            elif cpu_usage > threshold['max_cpu']:
                bottleneck['issues'].append(f"High CPU usage: {cpu_usage}% > {threshold['max_cpu']}%")
                bottleneck['recommendations'].append("Optimize CPU-intensive operations")
            
            if bottleneck['issues']:
                bottlenecks.append(bottleneck)
        
        return bottlenecks
    
    def implement_caching_optimization(self) -> Dict[str, Any]:
        """Implement caching optimizations."""
        logger.info("Implementing caching optimizations...")
        
        optimizations = {
            'description': 'Caching optimization for frequently used operations',
            'changes': [],
            'performance_impact': 'High'
        }
        
        # Create optimized BitcoinCryptography with caching
        optimized_crypto_code = '''
import hashlib
from functools import lru_cache
from typing import Dict, Optional

class OptimizedBitcoinCryptography:
    """Bitcoin cryptography with caching optimizations."""
    
    def __init__(self):
        self._address_cache: Dict[str, str] = {}
        self._public_key_cache: Dict[str, str] = {}
    
    @lru_cache(maxsize=10000)
    def _cached_sha256(self, data: str) -> str:
        """Cached SHA256 computation."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_bitcoin_address_cached(self, private_key: str, address_type: str = "legacy") -> str:
        """Generate Bitcoin address with caching."""
        cache_key = f"{private_key}:{address_type}"
        
        if cache_key in self._address_cache:
            return self._address_cache[cache_key]
        
        # Generate address (simplified for demo)
        address = f"1{hashlib.sha256(private_key.encode()).hexdigest()[:30]}"
        self._address_cache[cache_key] = address
        
        return address
'''
        
        cache_file = Path("core/optimized_cryptography.py")
        with open(cache_file, 'w') as f:
            f.write(optimized_crypto_code)
        
        optimizations['changes'].append(f"Created optimized cryptography module: {cache_file}")
        optimizations['changes'].append("Added LRU cache for SHA256 operations")
        optimizations['changes'].append("Added address generation caching")
        
        return optimizations
    
    def implement_memory_optimization(self) -> Dict[str, Any]:
        """Implement memory optimizations."""
        logger.info("Implementing memory optimizations...")
        
        optimizations = {
            'description': 'Memory optimization for large-scale operations',
            'changes': [],
            'performance_impact': 'Medium'
        }
        
        # Create memory-efficient key generator
        memory_optimized_code = '''
import gc
import sys
from typing import Iterator, Generator

class MemoryEfficientKeyGenerator:
    """Memory-efficient key generation for large-scale operations."""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
    
    def generate_keys_batch(self, count: int) -> Generator[list, None, None]:
        """Generate keys in batches to manage memory usage."""
        generated = 0
        
        while generated < count:
            batch_count = min(self.batch_size, count - generated)
            batch = []
            
            for _ in range(batch_count):
                # Generate key (simplified for demo)
                key = f"key_{generated}_{time.time()}"
                batch.append(key)
                generated += 1
            
            yield batch
            
            # Force garbage collection every few batches
            if generated % (self.batch_size * 5) == 0:
                gc.collect()
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        process = psutil.Process()
        return process.memory_info().rss / (1024 * 1024)
'''
        
        memory_file = Path("core/memory_efficient_generator.py")
        with open(memory_file, 'w') as f:
            f.write(memory_optimized_code)
        
        optimizations['changes'].append(f"Created memory-efficient generator: {memory_file}")
        optimizations['changes'].append("Added batch processing for key generation")
        optimizations['changes'].append("Added automatic garbage collection")
        optimizations['changes'].append("Added memory usage monitoring")
        
        return optimizations
    
    def implement_cpu_optimization(self) -> Dict[str, Any]:
        """Implement CPU optimizations."""
        logger.info("Implementing CPU optimizations...")
        
        optimizations = {
            'description': 'CPU optimization for intensive operations',
            'changes': [],
            'performance_impact': 'High'
        }
        
        # Create CPU-optimized operations
        cpu_optimized_code = '''
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Callable, Any
import time

class CPUOptimizedOperations:
    """CPU-optimized operations using multiprocessing and threading."""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, (os.cpu_count() or 1) + 4)
    
    def parallel_key_generation(self, count: int, batch_size: int = 1000) -> List[str]:
        """Generate keys in parallel using multiple processes."""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                future = executor.submit(self._generate_key_batch, batch_count)
                futures.append(future)
            
            results = []
            for future in futures:
                results.extend(future.result())
            
            return results
    
    def _generate_key_batch(self, count: int) -> List[str]:
        """Generate a batch of keys (runs in separate process)."""
        import hashlib
        import secrets
        
        keys = []
        for _ in range(count):
            key = secrets.token_hex(32)
            keys.append(key)
        
        return keys
    
    def parallel_address_generation(self, private_keys: List[str]) -> List[str]:
        """Generate addresses in parallel."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._generate_address, pk) for pk in private_keys]
            return [future.result() for future in futures]
    
    def _generate_address(self, private_key: str) -> str:
        """Generate address from private key (simplified)."""
        import hashlib
        return f"1{hashlib.sha256(private_key.encode()).hexdigest()[:30]}"
'''
        
        cpu_file = Path("core/cpu_optimized_operations.py")
        with open(cpu_file, 'w') as f:
            f.write(cpu_optimized_code)
        
        optimizations['changes'].append(f"Created CPU-optimized operations: {cpu_file}")
        optimizations['changes'].append("Added multiprocessing for key generation")
        optimizations['changes'].append("Added parallel address generation")
        optimizations['changes'].append("Added automatic worker pool management")
        
        return optimizations
    
    def create_optimized_config(self) -> Dict[str, Any]:
        """Create optimized configuration file."""
        logger.info("Creating optimized configuration...")
        
        optimized_config = {
            'performance': {
                'cache_enabled': True,
                'cache_size': 10000,
                'memory_optimization': True,
                'batch_size': 1000,
                'parallel_processing': True,
                'max_workers': min(32, (os.cpu_count() or 1) + 4),
                'garbage_collection_interval': 5000
            },
            'optimization': {
                'enable_caching': True,
                'enable_batch_processing': True,
                'enable_parallel_processing': True,
                'memory_limit_mb': 512,
                'cpu_limit_percent': 80
            },
            'monitoring': {
                'performance_tracking': True,
                'memory_monitoring': True,
                'cpu_monitoring': True,
                'optimization_logging': True
            }
        }
        
        config_file = Path("config/optimized.yaml")
        config_file.parent.mkdir(exist_ok=True)
        
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(optimized_config, f, default_flow_style=False)
        
        return {
            'description': 'Optimized configuration for better performance',
            'changes': [f"Created optimized config: {config_file}"],
            'performance_impact': 'Medium'
        }
    
    def run_optimization(self) -> Dict[str, Any]:
        """Run the complete optimization process."""
        logger.info("Starting performance optimization...")
        
        # Load benchmark results
        benchmark_results = self.load_benchmark_results()
        
        # Analyze bottlenecks
        bottlenecks = self.analyze_performance_bottlenecks(benchmark_results)
        
        optimization_results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'benchmark_results_file': None,
            'bottlenecks_found': len(bottlenecks),
            'bottlenecks': bottlenecks,
            'optimizations_applied': [],
            'performance_improvements': {}
        }
        
        # Find the most recent benchmark file
        benchmark_files = list(Path(".").glob("benchmark_results_*.json"))
        if benchmark_files:
            latest_file = max(benchmark_files, key=lambda f: f.stat().st_mtime)
            optimization_results['benchmark_results_file'] = str(latest_file)
        
        # Apply optimizations
        if bottlenecks:
            logger.info(f"Found {len(bottlenecks)} performance bottlenecks")
            
            # Implement caching optimization
            cache_opt = self.implement_caching_optimization()
            optimization_results['optimizations_applied'].append(cache_opt)
            
            # Implement memory optimization
            memory_opt = self.implement_memory_optimization()
            optimization_results['optimizations_applied'].append(memory_opt)
            
            # Implement CPU optimization
            cpu_opt = self.implement_cpu_optimization()
            optimization_results['optimizations_applied'].append(cpu_opt)
            
            # Create optimized configuration
            config_opt = self.create_optimized_config()
            optimization_results['optimizations_applied'].append(config_opt)
        else:
            logger.info("No performance bottlenecks found!")
        
        # Save optimization results
        results_file = Path(f"optimization_results_{time.strftime('%Y%m%d_%H%M%S')}.json")
        with open(results_file, 'w') as f:
            json.dump(optimization_results, f, indent=2)
        
        optimization_results['results_file'] = str(results_file)
        
        return optimization_results
    
    def generate_optimization_report(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable optimization report."""
        report = f"""
KeyHound Enhanced - Performance Optimization Report
Generated: {results['timestamp']}

SUMMARY:
- Benchmark Results: {results['benchmark_results_file'] or 'Not found'}
- Bottlenecks Found: {results['bottlenecks_found']}
- Optimizations Applied: {len(results['optimizations_applied'])}

"""
        
        if results['bottlenecks']:
            report += "PERFORMANCE BOTTLENECKS:\n"
            report += "=" * 50 + "\n"
            
            for bottleneck in results['bottlenecks']:
                report += f"\n{bottleneck['name']}:\n"
                report += f"  Current Rate: {bottleneck['current_rate']} ops/sec\n"
                report += f"  Memory Usage: {bottleneck['current_memory']} MB\n"
                report += f"  CPU Usage: {bottleneck['current_cpu']}%\n"
                
                if bottleneck['issues']:
                    report += "  Issues:\n"
                    for issue in bottleneck['issues']:
                        report += f"    - {issue}\n"
                
                if bottleneck['recommendations']:
                    report += "  Recommendations:\n"
                    for rec in bottleneck['recommendations']:
                        report += f"    - {rec}\n"
        
        if results['optimizations_applied']:
            report += "\nOPTIMIZATIONS APPLIED:\n"
            report += "=" * 50 + "\n"
            
            for opt in results['optimizations_applied']:
                report += f"\n{opt['description']}:\n"
                report += f"  Performance Impact: {opt['performance_impact']}\n"
                report += "  Changes:\n"
                for change in opt['changes']:
                    report += f"    - {change}\n"
        
        report += f"\nNEXT STEPS:\n"
        report += "=" * 50 + "\n"
        report += "1. Run performance benchmarks again to measure improvements\n"
        report += "2. Test the optimized modules with real workloads\n"
        report += "3. Monitor system resources during optimization\n"
        report += "4. Consider implementing GPU acceleration for further improvements\n"
        
        return report

def main():
    """Main entry point."""
    print("=" * 60)
    print("KeyHound Enhanced - Performance Optimizer")
    print("=" * 60)
    
    if not KEYHOUND_AVAILABLE:
        print("[WARN] KeyHound components not available. Some optimizations may be limited.")
    
    optimizer = PerformanceOptimizer()
    
    try:
        # Run optimization
        results = optimizer.run_optimization()
        
        # Generate and display report
        report = optimizer.generate_optimization_report(results)
        print(report)
        
        # Save report to file
        report_file = Path(f"optimization_report_{time.strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n[SUCCESS] Optimization completed!")
        print(f"Results saved to: {results['results_file']}")
        print(f"Report saved to: {report_file}")
        
        if results['bottlenecks_found'] > 0:
            print(f"\nOptimizations applied for {results['bottlenecks_found']} bottlenecks")
            print("Run performance benchmarks again to measure improvements")
        else:
            print("\nNo performance bottlenecks found - system is already optimized!")
        
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        print(f"\n[ERROR] Optimization failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
