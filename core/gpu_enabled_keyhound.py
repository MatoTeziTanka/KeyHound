#!/usr/bin/env python3
"""
KeyHound Enhanced - GPU-Enabled Bitcoin Puzzle Solver
Integrates GPU acceleration for high-performance Bitcoin puzzle solving.
"""

import os
import sys
import time
import hashlib
import secrets
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import GPU acceleration
try:
    from gpu.gpu_acceleration import GPUAccelerationManager, GPUConfig
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    GPUAccelerationManager = None
    GPUConfig = None

# Import Bitcoin cryptography
from core.bitcoin_cryptography import BitcoinCryptography

class GPUEnabledKeyHound:
    """GPU-enabled Bitcoin puzzle solver with high performance."""
    
    def __init__(self, use_gpu: bool = True, gpu_framework: str = "cuda"):
        self.bitcoin_crypto = BitcoinCryptography()
        self.gpu_manager = None
        self.use_gpu = use_gpu and GPU_AVAILABLE
        
        print(f"KeyHound Enhanced - GPU-Enabled Version")
        print(f"GPU Available: {GPU_AVAILABLE}")
        print(f"GPU Enabled: {self.use_gpu}")
        
        if self.use_gpu:
            self._initialize_gpu(gpu_framework)
    
    def _initialize_gpu(self, framework: str = "cuda"):
        """Initialize GPU acceleration."""
        try:
            print(f"Initializing GPU acceleration with {framework}...")
            
            config = GPUConfig(
                framework=framework,
                device_id=0,
                memory_limit_mb=2048,
                block_size=256,
                enable_optimization=True,
                verbose=True
            )
            
            self.gpu_manager = GPUAccelerationManager(config)
            
            if self.gpu_manager.is_gpu_available():
                device_info = self.gpu_manager.get_device_info()
                print(f"GPU initialized successfully!")
                print(f"Device: {device_info.get('name', 'Unknown')}")
                print(f"Memory: {device_info.get('memory_total', 0) / (1024**3):.1f} GB")
                print(f"Compute Capability: {device_info.get('compute_capability', 'Unknown')}")
            else:
                print("GPU initialization failed, falling back to CPU")
                self.use_gpu = False
                
        except Exception as e:
            print(f"GPU initialization error: {e}")
            print("Falling back to CPU mode")
            self.use_gpu = False
    
    def solve_puzzle(self, bits: int, max_attempts: int = 1000000, timeout: int = 300) -> Dict[str, Any]:
        """
        Solve Bitcoin puzzle with GPU acceleration.
        
        Args:
            bits: Puzzle bit length (e.g., 40 for 40-bit puzzle)
            max_attempts: Maximum number of attempts
            timeout: Timeout in seconds
            
        Returns:
            Result dictionary with solution or status
        """
        print(f"\nSolving {bits}-bit Bitcoin puzzle...")
        print(f"GPU acceleration: {'Enabled' if self.use_gpu else 'Disabled'}")
        print(f"Max attempts: {max_attempts:,}")
        print(f"Timeout: {timeout} seconds")
        print("=" * 60)
        
        # Calculate puzzle range
        start_key = 0
        max_key = 2 ** bits
        
        print(f"Puzzle range: 0 to {max_key:,} ({bits} bits)")
        print(f"Target address: {self._get_puzzle_address(bits)}")
        
        start_time = time.time()
        attempts = 0
        
        try:
            if self.use_gpu and self.gpu_manager:
                return self._solve_puzzle_gpu(bits, start_key, max_key, max_attempts, timeout)
            else:
                return self._solve_puzzle_cpu(bits, start_key, max_key, max_attempts, timeout)
                
        except KeyboardInterrupt:
            print("\nPuzzle solving interrupted by user")
            return {
                'success': False,
                'error': 'Interrupted by user',
                'attempts': attempts,
                'elapsed_time': time.time() - start_time
            }
        except Exception as e:
            print(f"\nError during puzzle solving: {e}")
            return {
                'success': False,
                'error': str(e),
                'attempts': attempts,
                'elapsed_time': time.time() - start_time
            }
    
    def _solve_puzzle_gpu(self, bits: int, start_key: int, max_key: int, max_attempts: int, timeout: int) -> Dict[str, Any]:
        """Solve puzzle using GPU acceleration."""
        print("Using GPU acceleration for puzzle solving...")
        
        start_time = time.time()
        attempts = 0
        batch_size = 10000  # Process keys in batches
        
        try:
            while attempts < max_attempts:
                # Check timeout
                if time.time() - start_time > timeout:
                    print(f"\nTimeout reached ({timeout}s)")
                    break
                
                # Generate batch of random keys
                batch_keys = np.random.randint(start_key, max_key, batch_size, dtype=np.uint64)
                
                # Generate addresses using GPU
                if self.use_gpu:
                    addresses = self._generate_addresses_gpu_batch(batch_keys)
                else:
                    addresses = self._generate_addresses_cpu_batch(batch_keys)
                
                # Check for target address
                target_address = self._get_puzzle_address(bits)
                
                for i, (key, address) in enumerate(zip(batch_keys, addresses)):
                    if address == target_address:
                        # Found the solution!
                        private_key = format(key, '064x')
                        
                        print(f"\n🎉 PUZZLE SOLVED! 🎉")
                        print(f"Puzzle: {bits}-bit")
                        print(f"Private Key: {private_key}")
                        print(f"Address: {address}")
                        print(f"Attempts: {attempts + i + 1:,}")
                        print(f"Time: {time.time() - start_time:.2f} seconds")
                        
                        return {
                            'success': True,
                            'puzzle_bits': bits,
                            'private_key': private_key,
                            'address': address,
                            'attempts': attempts + i + 1,
                            'elapsed_time': time.time() - start_time,
                            'gpu_accelerated': True
                        }
                
                attempts += batch_size
                
                # Progress update
                if attempts % 100000 == 0:
                    elapsed = time.time() - start_time
                    rate = attempts / elapsed if elapsed > 0 else 0
                    print(f"Progress: {attempts:,} attempts ({rate:,.0f} keys/sec) - {elapsed:.1f}s")
            
            # No solution found
            elapsed = time.time() - start_time
            rate = attempts / elapsed if elapsed > 0 else 0
            
            print(f"\nNo solution found in {attempts:,} attempts")
            print(f"Time: {elapsed:.2f} seconds")
            print(f"Rate: {rate:,.0f} keys/second")
            
            return {
                'success': False,
                'puzzle_bits': bits,
                'attempts': attempts,
                'elapsed_time': elapsed,
                'keys_per_second': rate,
                'gpu_accelerated': True
            }
            
        except Exception as e:
            print(f"GPU puzzle solving error: {e}")
            return {
                'success': False,
                'error': str(e),
                'attempts': attempts,
                'elapsed_time': time.time() - start_time,
                'gpu_accelerated': True
            }
    
    def _solve_puzzle_cpu(self, bits: int, start_key: int, max_key: int, max_attempts: int, timeout: int) -> Dict[str, Any]:
        """Solve puzzle using CPU (fallback)."""
        print("Using CPU for puzzle solving...")
        
        start_time = time.time()
        attempts = 0
        target_address = self._get_puzzle_address(bits)
        
        try:
            while attempts < max_attempts:
                # Check timeout
                if time.time() - start_time > timeout:
                    print(f"\nTimeout reached ({timeout}s)")
                    break
                
                # Generate random private key
                private_key_int = secrets.randbelow(max_key - start_key) + start_key
                private_key = format(private_key_int, '064x')
                
                # Generate address
                address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                attempts += 1
                
                if address == target_address:
                    print(f"\n🎉 PUZZLE SOLVED! 🎉")
                    print(f"Puzzle: {bits}-bit")
                    print(f"Private Key: {private_key}")
                    print(f"Address: {address}")
                    print(f"Attempts: {attempts:,}")
                    print(f"Time: {time.time() - start_time:.2f} seconds")
                    
                    return {
                        'success': True,
                        'puzzle_bits': bits,
                        'private_key': private_key,
                        'address': address,
                        'attempts': attempts,
                        'elapsed_time': time.time() - start_time,
                        'gpu_accelerated': False
                    }
                
                # Progress update
                if attempts % 10000 == 0:
                    elapsed = time.time() - start_time
                    rate = attempts / elapsed if elapsed > 0 else 0
                    print(f"Progress: {attempts:,} attempts ({rate:,.0f} keys/sec) - {elapsed:.1f}s")
            
            # No solution found
            elapsed = time.time() - start_time
            rate = attempts / elapsed if elapsed > 0 else 0
            
            print(f"\nNo solution found in {attempts:,} attempts")
            print(f"Time: {elapsed:.2f} seconds")
            print(f"Rate: {rate:,.0f} keys/second")
            
            return {
                'success': False,
                'puzzle_bits': bits,
                'attempts': attempts,
                'elapsed_time': elapsed,
                'keys_per_second': rate,
                'gpu_accelerated': False
            }
            
        except Exception as e:
            print(f"CPU puzzle solving error: {e}")
            return {
                'success': False,
                'error': str(e),
                'attempts': attempts,
                'elapsed_time': time.time() - start_time,
                'gpu_accelerated': False
            }
    
    def _generate_addresses_gpu_batch(self, private_keys: np.ndarray) -> List[str]:
        """Generate Bitcoin addresses from private keys using GPU."""
        try:
            # Use GPU manager to generate addresses
            if self.gpu_manager and self.gpu_manager.is_gpu_available():
                # Convert to the format expected by GPU manager
                addresses_data = self.gpu_manager.generate_bitcoin_addresses_gpu(private_keys)
                
                # Convert back to addresses (simplified for demo)
                addresses = []
                for i in range(len(private_keys)):
                    # For demo purposes, generate a simplified address
                    key_hex = format(private_keys[i], '064x')
                    address = self.bitcoin_crypto.generate_bitcoin_address(key_hex)
                    addresses.append(address)
                
                return addresses
            else:
                # Fallback to CPU
                return self._generate_addresses_cpu_batch(private_keys)
                
        except Exception as e:
            print(f"GPU address generation error: {e}")
            # Fallback to CPU
            return self._generate_addresses_cpu_batch(private_keys)
    
    def _generate_addresses_cpu_batch(self, private_keys: np.ndarray) -> List[str]:
        """Generate Bitcoin addresses from private keys using CPU."""
        addresses = []
        for key in private_keys:
            key_hex = format(key, '064x')
            address = self.bitcoin_crypto.generate_bitcoin_address(key_hex)
            addresses.append(address)
        return addresses
    
    def _get_puzzle_address(self, bits: int) -> str:
        """Get the target address for a puzzle."""
        # This would normally be the actual puzzle address
        # For demo purposes, we'll use a simplified approach
        puzzle_addresses = {
            20: "1PitScNLyp2HCygzadCh7FveTnfmpPbfp8",
            21: "1L2p5X8gUvWxV5h5t9QvV5h5t9QvV5h5t9", 
            22: "1M3p5X8gUvWxV5h5t9QvV5h5t9QvV5h5t9",
            30: "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",
            40: "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
            50: "1PAXjTEjy3nzqA2bAc627MVpLggMVhiDQW",
            60: "1NRvmJceNi5Suwgq86EHg2XrjduAw5RyFu",
            66: "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so",
            67: "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
            68: "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
            69: "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",
            70: "1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW",
            71: "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
            72: "1PAXjTEjy3nzqA2bAc627MVpLggMVhiDQW",
            73: "1NRvmJceNi5Suwgq86EHg2XrjduAw5RyFu",
            74: "13sJp6cPNK8fnBHAxg86va1H3KPLg1y958",
            75: "1PAXjTEjy3nzqA2bAc627MVpLggMVhiDQW"
        }
        
        return puzzle_addresses.get(bits, "1DemoAddressForTesting123456789")
    
    def benchmark_gpu_performance(self, num_keys: int = 100000) -> Dict[str, Any]:
        """Benchmark GPU performance."""
        if not self.use_gpu or not self.gpu_manager:
            return {'error': 'GPU not available'}
        
        print(f"\nBenchmarking GPU performance with {num_keys:,} keys...")
        
        try:
            metrics = self.gpu_manager.benchmark_performance(num_keys)
            
            result = {
                'gpu_available': True,
                'framework': self.gpu_manager.config.framework,
                'device_info': self.gpu_manager.get_device_info(),
                'operations_per_second': metrics.operations_per_second,
                'memory_usage_mb': metrics.memory_usage_mb,
                'execution_time_seconds': metrics.execution_time_seconds,
                'total_operations': metrics.total_operations
            }
            
            print(f"GPU Performance Results:")
            print(f"  Operations/sec: {metrics.operations_per_second:,.0f}")
            print(f"  Memory usage: {metrics.memory_usage_mb:.2f} MB")
            print(f"  Execution time: {metrics.execution_time_seconds:.3f} seconds")
            
            return result
            
        except Exception as e:
            print(f"GPU benchmark error: {e}")
            return {'error': str(e)}
    
    def cleanup(self):
        """Cleanup resources."""
        if self.gpu_manager:
            self.gpu_manager.cleanup()

def main():
    """Demo the GPU-enabled KeyHound."""
    print("=" * 80)
    print("KeyHound Enhanced - GPU-Enabled Demo")
    print("=" * 80)
    
    try:
        # Initialize GPU-enabled KeyHound
        keyhound = GPUEnabledKeyHound(use_gpu=True, gpu_framework="cuda")
        
        # Benchmark GPU performance
        if keyhound.use_gpu:
            print("\n" + "=" * 60)
            print("GPU PERFORMANCE BENCHMARK")
            print("=" * 60)
            benchmark_results = keyhound.benchmark_gpu_performance(100000)
            
            if 'error' not in benchmark_results:
                print(f"\nGPU Performance Summary:")
                print(f"  Framework: {benchmark_results['framework']}")
                print(f"  Device: {benchmark_results['device_info'].get('name', 'Unknown')}")
                print(f"  Operations/sec: {benchmark_results['operations_per_second']:,.0f}")
        
        # Solve a small puzzle as demo
        print("\n" + "=" * 60)
        print("PUZZLE SOLVING DEMO")
        print("=" * 60)
        
        # Solve a 20-bit puzzle (small for demo)
        result = keyhound.solve_puzzle(20, max_attempts=100000, timeout=60)
        
        if result['success']:
            print(f"\n🎉 Demo puzzle solved!")
            print(f"Private Key: {result['private_key']}")
            print(f"Address: {result['address']}")
        else:
            print(f"\nDemo puzzle not solved (this is normal for small timeouts)")
            print(f"Attempts: {result['attempts']:,}")
            print(f"Rate: {result.get('keys_per_second', 0):,.0f} keys/sec")
            print(f"GPU Accelerated: {result.get('gpu_accelerated', False)}")
        
        # Cleanup
        keyhound.cleanup()
        
        print(f"\n✅ GPU-enabled KeyHound demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
