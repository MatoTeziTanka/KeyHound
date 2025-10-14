"""
KeyHound Enhanced - Hardware Performance Scorer
Comprehensive hardware performance evaluation system for distributed pool rewards.
"""

import os
import sys
import time
import json
import hashlib
import threading
import psutil
import platform
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.simple_keyhound import SimpleKeyHound
    from core.bitcoin_cryptography import BitcoinCryptography
    KEYHOUND_AVAILABLE = True
except ImportError:
    KEYHOUND_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class HardwareSpecs:
    """Hardware specifications."""
    device_id: str
    device_name: str
    device_type: str  # 'cpu', 'gpu', 'mobile', 'server'
    cpu_count: int
    cpu_frequency: float
    memory_total: int
    memory_available: int
    platform: str
    architecture: str
    gpu_count: int = 0
    gpu_memory: int = 0
    battery_powered: bool = False

@dataclass
class PerformanceTest:
    """Performance test results."""
    test_name: str
    duration: float
    operations_count: int
    operations_per_second: float
    memory_usage: float
    cpu_usage: float
    power_efficiency: float
    timestamp: str

@dataclass
class HardwareScore:
    """Hardware performance score."""
    device_id: str
    user_id: str
    base_score: float
    efficiency_score: float
    power_score: float
    combined_score: float
    reward_percentage: float
    test_results: List[PerformanceTest]
    last_updated: str
    score_history: List[Dict[str, Any]]

class HardwarePerformanceScorer:
    """Hardware performance scoring system for distributed pool rewards."""
    
    def __init__(self):
        self.test_results = {}
        self.score_history = {}
        self.device_registry = {}
        
    def generate_device_id(self, user_id: str, device_name: str) -> str:
        """Generate unique device ID."""
        seed = f"{user_id}_{device_name}_{platform.node()}_{time.time()}"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]
    
    def get_hardware_specs(self, user_id: str, device_name: str = None) -> HardwareSpecs:
        """Get comprehensive hardware specifications."""
        if device_name is None:
            device_name = f"{platform.node()}_{platform.system()}"
        
        device_id = self.generate_device_id(user_id, device_name)
        
        # Detect device type
        device_type = self._detect_device_type()
        
        # Get CPU info
        cpu_count = os.cpu_count() or 1
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_frequency = cpu_freq.max if cpu_freq else 0
        except:
            cpu_frequency = 0
        
        # Get memory info
        memory = psutil.virtual_memory()
        memory_total = memory.total
        memory_available = memory.available
        
        # Get GPU info (simplified)
        gpu_count, gpu_memory = self._detect_gpu_info()
        
        # Check if battery powered
        battery_powered = self._is_battery_powered()
        
        return HardwareSpecs(
            device_id=device_id,
            device_name=device_name,
            device_type=device_type,
            cpu_count=cpu_count,
            cpu_frequency=cpu_frequency,
            memory_total=memory_total,
            memory_available=memory_available,
            platform=platform.platform(),
            architecture=platform.architecture()[0],
            gpu_count=gpu_count,
            gpu_memory=gpu_memory,
            battery_powered=battery_powered
        )
    
    def _detect_device_type(self) -> str:
        """Detect device type based on system characteristics."""
        system = platform.system().lower()
        
        if system == "windows":
            # Check for mobile indicators
            if "mobile" in platform.platform().lower():
                return "mobile"
            return "pc"
        elif system == "linux":
            # Check if it's a server or mobile
            if os.path.exists("/sys/class/power_supply/"):
                return "mobile"
            return "server"
        elif system == "darwin":
            # macOS - could be MacBook (mobile) or Mac Pro (desktop)
            if "macbook" in platform.platform().lower():
                return "mobile"
            return "pc"
        else:
            return "unknown"
    
    def _detect_gpu_info(self) -> Tuple[int, int]:
        """Detect GPU information."""
        gpu_count = 0
        gpu_memory = 0
        
        try:
            # Try to detect NVIDIA GPUs
            import subprocess
            result = subprocess.run(['nvidia-smi', '--query-gpu=count,memory.total', '--format=csv,noheader,nounits'], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                gpu_count = len(lines)
                gpu_memory = sum(int(line.split(',')[1]) for line in lines if ',' in line)
        except:
            pass
        
        return gpu_count, gpu_memory
    
    def _is_battery_powered(self) -> bool:
        """Check if device is battery powered."""
        try:
            battery = psutil.sensors_battery()
            return battery is not None
        except:
            return False
    
    def run_quick_performance_test(self, duration_seconds: int = 60) -> List[PerformanceTest]:
        """Run quick 1-minute performance test."""
        logger.info(f"Running quick performance test ({duration_seconds}s)...")
        
        tests = []
        
        # Test 1: Private Key Generation
        key_gen_test = self._test_private_key_generation(duration_seconds // 3)
        tests.append(key_gen_test)
        
        # Test 2: Address Generation
        addr_test = self._test_address_generation(duration_seconds // 3)
        tests.append(addr_test)
        
        # Test 3: Puzzle Solving Simulation
        puzzle_test = self._test_puzzle_solving(duration_seconds // 3)
        tests.append(puzzle_test)
        
        return tests
    
    def run_comprehensive_performance_test(self, duration_seconds: int = 3600) -> List[PerformanceTest]:
        """Run comprehensive 1-hour performance test."""
        logger.info(f"Running comprehensive performance test ({duration_seconds}s)...")
        
        tests = []
        
        # Extended tests for more accurate scoring
        test_duration = duration_seconds // 4
        
        # Test 1: Extended Key Generation
        key_gen_test = self._test_private_key_generation(test_duration)
        tests.append(key_gen_test)
        
        # Test 2: Extended Address Generation
        addr_test = self._test_address_generation(test_duration)
        tests.append(addr_test)
        
        # Test 3: Extended Puzzle Solving
        puzzle_test = self._test_puzzle_solving(test_duration)
        tests.append(puzzle_test)
        
        # Test 4: Memory Stress Test
        memory_test = self._test_memory_operations(test_duration)
        tests.append(memory_test)
        
        return tests
    
    def _test_private_key_generation(self, duration_seconds: int) -> PerformanceTest:
        """Test private key generation performance."""
        start_time = time.time()
        operations_count = 0
        start_memory = psutil.virtual_memory().used
        
        while time.time() - start_time < duration_seconds:
            # Generate random private key (simplified)
            import secrets
            private_key = secrets.token_hex(32)
            operations_count += 1
            
            # Monitor memory every 1000 operations
            if operations_count % 1000 == 0:
                current_memory = psutil.virtual_memory().used
                if current_memory - start_memory > 100 * 1024 * 1024:  # 100MB limit
                    break
        
        actual_duration = time.time() - start_time
        ops_per_second = operations_count / actual_duration if actual_duration > 0 else 0
        memory_usage = (psutil.virtual_memory().used - start_memory) / (1024 * 1024)  # MB
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Calculate power efficiency (operations per watt - simplified)
        power_efficiency = ops_per_second / max(1, cpu_usage) if cpu_usage > 0 else ops_per_second
        
        return PerformanceTest(
            test_name="Private Key Generation",
            duration=actual_duration,
            operations_count=operations_count,
            operations_per_second=ops_per_second,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            power_efficiency=power_efficiency,
            timestamp=datetime.now().isoformat()
        )
    
    def _test_address_generation(self, duration_seconds: int) -> PerformanceTest:
        """Test Bitcoin address generation performance."""
        start_time = time.time()
        operations_count = 0
        start_memory = psutil.virtual_memory().used
        
        # Pre-generate some private keys
        import secrets
        private_keys = [secrets.token_hex(32) for _ in range(100)]
        
        while time.time() - start_time < duration_seconds:
            # Generate address from private key (simplified)
            private_key = private_keys[operations_count % len(private_keys)]
            address = f"1{hashlib.sha256(private_key.encode()).hexdigest()[:30]}"
            operations_count += 1
        
        actual_duration = time.time() - start_time
        ops_per_second = operations_count / actual_duration if actual_duration > 0 else 0
        memory_usage = (psutil.virtual_memory().used - start_memory) / (1024 * 1024)
        cpu_usage = psutil.cpu_percent(interval=1)
        power_efficiency = ops_per_second / max(1, cpu_usage) if cpu_usage > 0 else ops_per_second
        
        return PerformanceTest(
            test_name="Address Generation",
            duration=actual_duration,
            operations_count=operations_count,
            operations_per_second=ops_per_second,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            power_efficiency=power_efficiency,
            timestamp=datetime.now().isoformat()
        )
    
    def _test_puzzle_solving(self, duration_seconds: int) -> PerformanceTest:
        """Test puzzle solving simulation."""
        start_time = time.time()
        operations_count = 0
        start_memory = psutil.virtual_memory().used
        
        # Simulate puzzle solving by generating and checking keys
        import secrets
        target_pattern = "test_pattern"
        
        while time.time() - start_time < duration_seconds:
            # Generate random key and simulate checking
            private_key = secrets.token_hex(32)
            address = f"1{hashlib.sha256(private_key.encode()).hexdigest()[:30]}"
            
            # Simulate pattern matching (simplified)
            if target_pattern in address.lower():
                operations_count += 1000  # Bonus for "finding" a match
            else:
                operations_count += 1
        
        actual_duration = time.time() - start_time
        ops_per_second = operations_count / actual_duration if actual_duration > 0 else 0
        memory_usage = (psutil.virtual_memory().used - start_memory) / (1024 * 1024)
        cpu_usage = psutil.cpu_percent(interval=1)
        power_efficiency = ops_per_second / max(1, cpu_usage) if cpu_usage > 0 else ops_per_second
        
        return PerformanceTest(
            test_name="Puzzle Solving",
            duration=actual_duration,
            operations_count=operations_count,
            operations_per_second=ops_per_second,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            power_efficiency=power_efficiency,
            timestamp=datetime.now().isoformat()
        )
    
    def _test_memory_operations(self, duration_seconds: int) -> PerformanceTest:
        """Test memory-intensive operations."""
        start_time = time.time()
        operations_count = 0
        start_memory = psutil.virtual_memory().used
        
        # Test memory allocation and deallocation
        data_blocks = []
        
        while time.time() - start_time < duration_seconds:
            # Allocate memory
            block_size = 1024 * 1024  # 1MB
            data_block = bytearray(block_size)
            data_blocks.append(data_block)
            operations_count += 1
            
            # Periodically clear blocks to prevent memory exhaustion
            if len(data_blocks) > 100:
                data_blocks = data_blocks[-50:]  # Keep only recent blocks
        
        actual_duration = time.time() - start_time
        ops_per_second = operations_count / actual_duration if actual_duration > 0 else 0
        memory_usage = (psutil.virtual_memory().used - start_memory) / (1024 * 1024)
        cpu_usage = psutil.cpu_percent(interval=1)
        power_efficiency = ops_per_second / max(1, cpu_usage) if cpu_usage > 0 else ops_per_second
        
        return PerformanceTest(
            test_name="Memory Operations",
            duration=actual_duration,
            operations_count=operations_count,
            operations_per_second=ops_per_second,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            power_efficiency=power_efficiency,
            timestamp=datetime.now().isoformat()
        )
    
    def calculate_hardware_score(self, hardware_specs: HardwareSpecs, test_results: List[PerformanceTest]) -> HardwareScore:
        """Calculate comprehensive hardware performance score."""
        
        # Base score from hardware specifications
        base_score = self._calculate_base_score(hardware_specs)
        
        # Performance score from test results
        performance_score = self._calculate_performance_score(test_results)
        
        # Efficiency score (performance per watt)
        efficiency_score = self._calculate_efficiency_score(test_results, hardware_specs)
        
        # Power score (sustained performance)
        power_score = self._calculate_power_score(test_results)
        
        # Combined score
        combined_score = (base_score * 0.2 + 
                         performance_score * 0.4 + 
                         efficiency_score * 0.2 + 
                         power_score * 0.2)
        
        # Calculate reward percentage (0.1% to 5% range)
        reward_percentage = min(5.0, max(0.1, combined_score / 1000))
        
        return HardwareScore(
            device_id=hardware_specs.device_id,
            user_id="",  # Will be set by caller
            base_score=base_score,
            efficiency_score=efficiency_score,
            power_score=power_score,
            combined_score=combined_score,
            reward_percentage=reward_percentage,
            test_results=test_results,
            last_updated=datetime.now().isoformat(),
            score_history=[]
        )
    
    def _calculate_base_score(self, specs: HardwareSpecs) -> float:
        """Calculate base score from hardware specifications."""
        score = 0
        
        # CPU score
        cpu_score = specs.cpu_count * (specs.cpu_frequency / 1000) * 10
        score += cpu_score
        
        # Memory score
        memory_gb = specs.memory_total / (1024**3)
        memory_score = memory_gb * 5
        score += memory_score
        
        # GPU score
        gpu_score = specs.gpu_count * (specs.gpu_memory / 1024) * 20
        score += gpu_score
        
        # Device type modifier
        type_modifiers = {
            'server': 1.2,
            'pc': 1.0,
            'mobile': 0.6,
            'unknown': 0.8
        }
        modifier = type_modifiers.get(specs.device_type, 1.0)
        
        # Battery penalty
        if specs.battery_powered:
            modifier *= 0.8
        
        return score * modifier
    
    def _calculate_performance_score(self, test_results: List[PerformanceTest]) -> float:
        """Calculate performance score from test results."""
        if not test_results:
            return 0
        
        total_ops_per_second = sum(test.operations_per_second for test in test_results)
        return total_ops_per_second / len(test_results)
    
    def _calculate_efficiency_score(self, test_results: List[PerformanceTest], specs: HardwareSpecs) -> float:
        """Calculate efficiency score (performance per resource)."""
        if not test_results:
            return 0
        
        total_efficiency = sum(test.power_efficiency for test in test_results)
        avg_efficiency = total_efficiency / len(test_results)
        
        # Normalize based on device type
        efficiency_multipliers = {
            'server': 1.0,
            'pc': 0.9,
            'mobile': 1.2,  # Mobile devices get bonus for efficiency
            'unknown': 0.8
        }
        
        multiplier = efficiency_multipliers.get(specs.device_type, 1.0)
        return avg_efficiency * multiplier
    
    def _calculate_power_score(self, test_results: List[PerformanceTest]) -> float:
        """Calculate sustained performance score."""
        if not test_results:
            return 0
        
        # Calculate consistency across tests
        ops_rates = [test.operations_per_second for test in test_results]
        avg_rate = sum(ops_rates) / len(ops_rates)
        
        # Calculate variance (lower is better for consistency)
        variance = sum((rate - avg_rate) ** 2 for rate in ops_rates) / len(ops_rates)
        consistency = max(0, 1 - (variance / avg_rate)) if avg_rate > 0 else 0
        
        return avg_rate * consistency

def main():
    """Main entry point for testing."""
    print("=" * 60)
    print("KeyHound Enhanced - Hardware Performance Scorer")
    print("=" * 60)
    
    scorer = HardwarePerformanceScorer()
    
    # Test with current system
    user_id = "test_user"
    device_name = "test_device"
    
    # Get hardware specs
    specs = scorer.get_hardware_specs(user_id, device_name)
    print(f"\nHardware Specs:")
    print(f"  Device ID: {specs.device_id}")
    print(f"  Device Type: {specs.device_type}")
    print(f"  CPU Count: {specs.cpu_count}")
    print(f"  CPU Frequency: {specs.cpu_frequency} MHz")
    print(f"  Memory: {specs.memory_total / (1024**3):.1f} GB")
    print(f"  GPU Count: {specs.gpu_count}")
    print(f"  GPU Memory: {specs.gpu_memory} MB")
    print(f"  Battery Powered: {specs.battery_powered}")
    
    # Run quick performance test
    print(f"\nRunning 1-minute performance test...")
    quick_tests = scorer.run_quick_performance_test(60)
    
    print(f"\nQuick Test Results:")
    for test in quick_tests:
        print(f"  {test.test_name}:")
        print(f"    Operations/sec: {test.operations_per_second:.2f}")
        print(f"    Memory Usage: {test.memory_usage:.1f} MB")
        print(f"    CPU Usage: {test.cpu_usage:.1f}%")
        print(f"    Power Efficiency: {test.power_efficiency:.2f}")
    
    # Calculate hardware score
    score = scorer.calculate_hardware_score(specs, quick_tests)
    
    print(f"\nHardware Score:")
    print(f"  Base Score: {score.base_score:.2f}")
    print(f"  Performance Score: {score.performance_score:.2f}")
    print(f"  Efficiency Score: {score.efficiency_score:.2f}")
    print(f"  Power Score: {score.power_score:.2f}")
    print(f"  Combined Score: {score.combined_score:.2f}")
    print(f"  Reward Percentage: {score.reward_percentage:.3f}%")
    
    # Save results
    results_file = f"hardware_score_{specs.device_id}_{int(time.time())}.json"
    with open(results_file, 'w') as f:
        json.dump(asdict(score), f, indent=2)
    
    print(f"\n[SUCCESS] Results saved to: {results_file}")

if __name__ == '__main__':
    main()
