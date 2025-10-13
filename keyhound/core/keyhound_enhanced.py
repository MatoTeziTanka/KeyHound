#!/usr/bin/env python3
"""
KeyHound Enhanced - Comprehensive Bitcoin Cryptographic Tool

A cross-platform Python application designed to:
1. Solve Bitcoin puzzle challenges (original 1000 + private key puzzles)
2. Brainwallet security testing and vulnerability assessment
3. Academic research and cryptographic studies
4. Performance benchmarking and optimization
5. Penetration testing for brainwallet implementations

Based on Bitcoin puzzle data from privatekeys.pw/puzzles/bitcoin-puzzle-tx
"""

import hashlib
import time
import argparse
import sys
import os
import json
import threading
import logging
from typing import Optional, Tuple, List, Dict, Any
import multiprocessing as mp
from tqdm import tqdm
import colorama
from colorama import Fore, Style
import numpy as np

# Import KeyHound modules from new modular structure
from .puzzle_data import BITCOIN_PUZZLES, get_brainwallet_patterns, hex_range_to_int_range
from ..gpu.gpu_acceleration import GPUAccelerationManager, GPUConfig, GPUPerformanceMetrics
from ..gpu.gpu_framework import GPUFrameworkManager, GPUDevice, GPUPerformanceMetrics as FrameworkMetrics
from .brainwallet_patterns import BrainwalletPatternLibrary, BrainwalletPattern, PatternMatch
from .bitcoin_cryptography import BitcoinCryptography, BitcoinAddress, CryptographyError
from .memory_optimization import MemoryOptimizer, StreamingKeyProcessor, get_memory_optimizer
from .configuration_manager import ConfigurationManager, get_config_manager, ConfigSchema, ConfigValidationRule
from .result_persistence import ResultPersistenceManager, get_result_persistence_manager, ResultType, StorageConfig, StorageBackend
from .performance_monitoring import PerformanceMonitor, get_performance_monitor, MetricType, AlertLevel
from ..web.web_interface import KeyHoundWebInterface, create_web_interface, WebConfig
from ..distributed.distributed_computing import DistributedComputingManager, create_distributed_manager, NodeRole, NetworkConfig, NetworkProtocol
from ..ml.machine_learning import MachineLearningManager, create_ml_manager, ModelType
from ..web.mobile_app import KeyHoundMobileApp, create_mobile_app, MobileConfig
from .error_handling import (
    KeyHoundLogger, KeyHoundError, CryptographyError as KeyHoundCryptographyError,
    GPUError, PuzzleError, BrainwalletError, ConfigurationError,
    error_handler, performance_monitor
)

# Configure logging
keyhound_logger = KeyHoundLogger("KeyHoundEnhanced", log_level="INFO")
logger = keyhound_logger.logger

# Initialize colorama for cross-platform colored output
colorama.init()


class KeyHoundEnhanced:
    """
    Enhanced KeyHound with comprehensive Bitcoin cryptographic capabilities.
    
    Legendary Code Quality Standards:
    - Comprehensive error handling and logging
    - Type hints for all methods and properties
    - Detailed documentation and examples
    - Performance optimization and monitoring
    - GPU acceleration support
    - Advanced brainwallet pattern library
    """
    
    def __init__(self, use_gpu: bool = False, num_threads: Optional[int] = None,
                 gpu_framework: str = "cuda", verbose: bool = False,
                 config_file: Optional[str] = None, max_memory_mb: int = 1024):
        """
        Initialize the Enhanced KeyHound with legendary code quality.
        
        Args:
            use_gpu: Whether to use GPU acceleration (if available)
            num_threads: Number of CPU threads to use (default: all available)
            gpu_framework: GPU framework to use ("cuda", "opencl", or "cpu")
            verbose: Enable verbose logging and output
            config_file: Path to configuration file (optional)
            max_memory_mb: Maximum memory usage in MB
        """
        self.use_gpu = use_gpu
        self.num_threads = num_threads or mp.cpu_count()
        self.gpu_framework = gpu_framework
        self.verbose = verbose
        self.start_time = None
        self.benchmark_results = {}
        self.found_keys = []
        
        # Initialize configuration manager
        try:
            self.config_manager = get_config_manager("keyhound")
            if config_file:
                self.config_manager.load_config(config_file)
            keyhound_logger.info("Configuration manager initialized successfully")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.config_manager = None
        
        # Initialize memory optimizer
        try:
            memory_limit = self.config_manager.get("performance.memory_limit_mb", max_memory_mb) if self.config_manager else max_memory_mb
            self.memory_optimizer = get_memory_optimizer(memory_limit)
            keyhound_logger.info(f"Memory optimizer initialized with {memory_limit}MB limit")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.memory_optimizer = None
        
        # Initialize result persistence manager
        try:
            results_dir = self.config_manager.get("storage.results_dir", "./results") if self.config_manager else "./results"
            storage_config = StorageConfig(
                backend=StorageBackend.FILE_SYSTEM,
                base_path=results_dir,
                encryption_enabled=self.config_manager.get("security.encrypt_config", False) if self.config_manager else False,
                compression_enabled=True,
                backup_enabled=self.config_manager.get("storage.backup_enabled", True) if self.config_manager else True
            )
            self.result_persistence = get_result_persistence_manager(storage_config)
            keyhound_logger.info("Result persistence manager initialized successfully")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.result_persistence = None
        
        # Initialize performance monitor
        try:
            performance_db = self.config_manager.get("storage.performance_db", "./performance_metrics.db") if self.config_manager else "./performance_metrics.db"
            self.performance_monitor = get_performance_monitor(performance_db)
            
            # Set up performance alerts
            self.performance_monitor.set_alert_threshold("cpu_percent", 90.0, AlertLevel.CRITICAL)
            self.performance_monitor.set_alert_threshold("memory_percent", 90.0, AlertLevel.CRITICAL)
            self.performance_monitor.set_alert_threshold("puzzle_solving_rate", 1000.0, AlertLevel.INFO)
            
            keyhound_logger.info("Performance monitor initialized successfully")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.performance_monitor = None
        
        # Initialize Bitcoin cryptography
        try:
            self.bitcoin_crypto = BitcoinCryptography()
            keyhound_logger.info("Bitcoin cryptography module initialized successfully")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.bitcoin_crypto = None
        
        # Initialize brainwallet pattern library
        try:
            self.pattern_library = BrainwalletPatternLibrary()
            keyhound_logger.info(f"Brainwallet pattern library loaded with {len(self.pattern_library.patterns)} patterns")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.pattern_library = None
        
        # Initialize GPU acceleration manager (legacy)
        self.gpu_manager = None
        if use_gpu:
            try:
                gpu_config = GPUConfig(framework=gpu_framework, verbose=verbose)
                self.gpu_manager = GPUAccelerationManager(gpu_config)
                if self.gpu_manager.is_gpu_available():
                    keyhound_logger.info(f"Legacy GPU acceleration initialized with {gpu_framework.upper()}")
                else:
                    keyhound_logger.warning("Legacy GPU acceleration requested but not available")
                    self.gpu_manager = None
            except Exception as e:
                keyhound_logger.log_error(e)
                self.gpu_manager = None
        
        # Initialize advanced GPU framework manager
        self.gpu_framework_manager = None
        if use_gpu:
            try:
                self.gpu_framework_manager = GPUFrameworkManager(
                    preferred_framework=gpu_framework,
                    logger=keyhound_logger
                )
                if self.gpu_framework_manager.is_initialized:
                    keyhound_logger.info("Advanced GPU framework initialized successfully")
                    device_info = self.gpu_framework_manager.get_device_info()
                    for framework_name, device in device_info.items():
                        keyhound_logger.info(f"GPU Device: {device.name} ({framework_name})")
                else:
                    keyhound_logger.warning("Advanced GPU framework not available")
                    self.gpu_framework_manager = None
            except Exception as e:
                keyhound_logger.log_error(e)
                self.gpu_framework_manager = None
        
        # Update GPU availability based on framework managers
        if not self.gpu_manager and not self.gpu_framework_manager:
            self.use_gpu = False
        
        # Print initialization status
        print(f"{Fore.CYAN}KeyHound Enhanced - Comprehensive Bitcoin Cryptographic Tool{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Initializing with {self.num_threads} CPU threads{Style.RESET_ALL}")
        
        if self.use_gpu and self.gpu_framework_manager and self.gpu_framework_manager.is_initialized:
            device_info = self.gpu_framework_manager.get_device_info()
            for framework_name, device in device_info.items():
                print(f"{Fore.GREEN}GPU acceleration enabled: {device.name} ({framework_name.upper()}){Style.RESET_ALL}")
            print(f"{Fore.GREEN}Framework: {gpu_framework.upper()}{Style.RESET_ALL}")
        elif self.use_gpu and self.gpu_manager and self.gpu_manager.is_gpu_available():
            device_info = self.gpu_manager.get_device_info()
            print(f"{Fore.GREEN}Legacy GPU acceleration enabled: {device_info.get('name', 'Unknown Device')}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Framework: {gpu_framework.upper()}{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}CPU-only mode{Style.RESET_ALL}")
        
        if self.pattern_library:
            stats = self.pattern_library.get_statistics()
            print(f"{Fore.GREEN}Brainwallet patterns loaded: {stats['total_patterns']} patterns{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Languages: {stats['languages']}, Categories: {stats['categories']}{Style.RESET_ALL}")
        
        if self.memory_optimizer:
            memory_stats = self.memory_optimizer.get_memory_stats()
            print(f"{Fore.GREEN}Memory optimization enabled: {memory_stats['optimization_limits']['max_memory_mb']:.0f}MB limit{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Cache enabled: {memory_stats['cache_stats']['hits']} hits, {memory_stats['cache_stats']['misses']} misses{Style.RESET_ALL}")
        
        if self.config_manager:
            config_version = self.config_manager.get("keyhound.version", "unknown")
            environment = self.config_manager.get("keyhound.environment", "unknown")
            print(f"{Fore.GREEN}Configuration loaded: v{config_version} ({environment}){Style.RESET_ALL}")
        
        if self.result_persistence:
            storage_stats = self.result_persistence.get_storage_statistics()
            print(f"{Fore.GREEN}Result persistence enabled: {storage_stats.get('total_results', 0)} results stored{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Storage backend: {storage_stats.get('storage_backend', 'unknown')}{Style.RESET_ALL}")
        
        if self.performance_monitor:
            perf_stats = self.performance_monitor.get_performance_statistics()
            print(f"{Fore.GREEN}Performance monitoring active: {perf_stats.get('current_metrics_count', 0)} metrics{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Active alerts: {perf_stats.get('active_alerts_count', 0)}{Style.RESET_ALL}")
    
    @error_handler(keyhound_logger)
    @performance_monitor(keyhound_logger)
    def solve_puzzle(self, puzzle_id: int) -> Optional[str]:
        """
        Solve a specific Bitcoin puzzle challenge.
        
        Args:
            puzzle_id: The puzzle ID to solve
            
        Returns:
            Private key if found, None otherwise
        """
        if puzzle_id not in BITCOIN_PUZZLES:
            print(f"{Fore.RED}Error: Puzzle #{puzzle_id} not found{Style.RESET_ALL}")
            return None
        
        puzzle = BITCOIN_PUZZLES[puzzle_id]
        print(f"{Fore.CYAN}Solving Bitcoin Puzzle #{puzzle_id}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Address: {puzzle['bitcoin_address']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Key Range: {puzzle['key_range_bits']} bits{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Hex Range: {puzzle['key_range_hex']}{Style.RESET_ALL}")
        
        # Convert hex range to integer range
        start_key, end_key = hex_range_to_int_range(puzzle['key_range_hex'])
        
        if "public_key" in puzzle:
            print(f"{Fore.GREEN}Using BSGS algorithm (exposed public key){Style.RESET_ALL}")
            return self._solve_with_bsgs(puzzle['public_key'], start_key, end_key, puzzle['bitcoin_address'])
        else:
            print(f"{Fore.GREEN}Using brute force algorithm{Style.RESET_ALL}")
            return self._solve_with_brute_force(start_key, end_key, puzzle['bitcoin_address'])
    
    def _solve_with_bsgs(self, public_key: str, start_key: int, end_key: int, target_address: str) -> Optional[str]:
        """
        Solve using Baby-step Giant-step algorithm for exposed public keys.
        
        Args:
            public_key: The exposed public key
            start_key: Start of key range
            end_key: End of key range
            target_address: Target Bitcoin address
            
        Returns:
            Private key if found, None otherwise
        """
        print(f"{Fore.CYAN}BSGS Algorithm: Searching range {start_key:x} to {end_key:x}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Public Key: {public_key}{Style.RESET_ALL}")
        
        # TODO: Implement BSGS algorithm
        # For now, use brute force as placeholder
        print(f"{Fore.YELLOW}BSGS implementation in progress - using brute force fallback{Style.RESET_ALL}")
        return self._solve_with_brute_force(start_key, end_key, target_address)
    
    def _solve_with_brute_force(self, start_key: int, end_key: int, target_address: str) -> Optional[str]:
        """
        Solve using brute force algorithm.
        
        Args:
            start_key: Start of key range
            end_key: End of key range
            target_address: Target Bitcoin address
            
        Returns:
            Private key if found, None otherwise
        """
        self.start_time = time.time()
        total_keys = end_key - start_key
        
        print(f"{Fore.CYAN}Brute Force: Searching {total_keys:,} keys{Style.RESET_ALL}")
        
        with tqdm(total=total_keys, desc="Searching", unit="keys") as pbar:
            for private_key in range(start_key, end_key):
                # Generate Bitcoin address from private key
                address = self._generate_bitcoin_address(private_key)
                
                # Check if this matches our target
                if address == target_address:
                    elapsed = time.time() - self.start_time
                    print(f"\n{Fore.GREEN}🎉 PUZZLE SOLVED! 🎉{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Private Key: {hex(private_key)[2:].zfill(64)}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Address: {address}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Time elapsed: {elapsed:.2f} seconds{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Keys searched: {private_key - start_key:,}{Style.RESET_ALL}")
                    
                    # Save found key
                    self.found_keys.append({
                        'private_key': hex(private_key)[2:].zfill(64),
                        'address': address,
                        'time_elapsed': elapsed,
                        'keys_searched': private_key - start_key
                    })
                    
                    return hex(private_key)[2:].zfill(64)
                
                pbar.update(1)
                
                # Update progress bar
                if self.start_time:
                    elapsed = time.time() - self.start_time
                    if elapsed > 0:
                        rate = (private_key - start_key) / elapsed
                        pbar.set_postfix({
                            'Current': f"{private_key:x}",
                            'Rate': f"{rate:.0f}/s"
                        })
        
        print(f"\n{Fore.RED}No solution found in range{Style.RESET_ALL}")
        return None
    
    @error_handler(keyhound_logger)
    def test_brainwallet_security(self, target_address: str = None) -> Dict[str, Any]:
        """
        Test brainwallet security for common patterns.
        
        Args:
            target_address: Target Bitcoin address to check (optional)
            
        Returns:
            Dictionary with test results
        """
        print(f"{Fore.CYAN}Brainwallet Security Test{Style.RESET_ALL}")
        
        if not self.pattern_library:
            print(f"{Fore.RED}Pattern library not available{Style.RESET_ALL}")
            return {"error": "Pattern library not available"}
        
        # Get common patterns
        patterns = get_brainwallet_patterns()
        
        results = {
            'patterns_tested': len(patterns),
            'vulnerabilities_found': [],
            'test_duration': 0
        }
        
        start_time = time.time()
        
        for i, pattern in enumerate(patterns, 1):
            print(f"Testing pattern {i}/{len(patterns)}: {pattern[:20]}...")
            
            # Generate brainwallet private key
            private_key = self._generate_brainwallet_key(pattern)
            
            # Generate Bitcoin address
            address = self._generate_bitcoin_address(private_key)
            
            # Check if this matches our target
            if target_address and address == target_address:
                vulnerability = {
                    'pattern': pattern,
                    'private_key': hex(private_key)[2:].zfill(64),
                    'address': address
                }
                results['vulnerabilities_found'].append(vulnerability)
                print(f"{Fore.RED}🚨 VULNERABILITY FOUND!{Style.RESET_ALL}")
                print(f"Pattern: {pattern}")
                print(f"Private Key: {hex(private_key)[2:].zfill(64)}")
                print(f"Address: {address}")
        
        results['test_duration'] = time.time() - start_time
        
        print(f"\n{Fore.GREEN}Brainwallet security test completed{Style.RESET_ALL}")
        print(f"Patterns tested: {results['patterns_tested']}")
        print(f"Vulnerabilities found: {len(results['vulnerabilities_found'])}")
        print(f"Test duration: {results['test_duration']:.2f} seconds")
        
        return results
    
    def enable_gpu_acceleration(self):
        """Enable GPU acceleration if available."""
        if self.gpu_framework_manager and self.gpu_framework_manager.is_initialized:
            self.use_gpu = True
            print(f"{Fore.GREEN}GPU acceleration enabled{Style.RESET_ALL}")
        elif self.gpu_manager and self.gpu_manager.is_gpu_available():
            self.use_gpu = True
            print(f"{Fore.GREEN}Legacy GPU acceleration enabled{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}GPU acceleration not available{Style.RESET_ALL}")
    
    def enable_distributed_computing(self):
        """Enable distributed computing if available."""
        # TODO: Implement distributed computing initialization
        print(f"{Fore.YELLOW}Distributed computing not yet implemented{Style.RESET_ALL}")
    
    def _generate_brainwallet_key(self, passphrase: str) -> int:
        """
        Generate brainwallet private key from passphrase.
        
        Args:
            passphrase: The passphrase to convert to private key
            
        Returns:
            Private key as integer
        """
        # Use SHA-256 to generate private key from passphrase
        private_key_hash = hashlib.sha256(passphrase.encode('utf-8')).hexdigest()
        return int(private_key_hash, 16)
    
    @performance_monitor(keyhound_logger)
    def _generate_bitcoin_address(self, private_key: int) -> str:
        """
        Generate a proper Bitcoin address from a private key using secp256k1.
        
        Args:
            private_key: The private key as an integer
            
        Returns:
            Bitcoin address string
            
        Raises:
            CryptographyError: If address generation fails
        """
        try:
            # Convert private key to hex
            private_key_hex = hex(private_key)[2:].zfill(64)
            
            if self.bitcoin_crypto:
                # Use proper Bitcoin cryptography
                bitcoin_address = self.bitcoin_crypto.generate_bitcoin_address(
                    private_key_hex, 
                    address_type="legacy", 
                    network="mainnet"
                )
                return bitcoin_address.address
            else:
                # Fallback to simplified implementation
                keyhound_logger.warning("Using fallback Bitcoin address generation")
                address_hash = hashlib.sha256(private_key_hex.encode()).hexdigest()
                return f"1{address_hash[:26]}"  # Simplified Bitcoin address format
                
        except Exception as e:
            keyhound_logger.log_error(e)
            raise CryptographyError(f"Bitcoin address generation failed: {e}")
    
    def save_results(self, filename: str = None) -> str:
        """
        Save all results to a JSON file.
        
        Args:
            filename: Optional filename (default: timestamp-based)
            
        Returns:
            Filename where results were saved
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"keyhound_results_{timestamp}.json"
        
        results = {
            'timestamp': time.time(),
            'found_keys': self.found_keys,
            'benchmark_results': self.benchmark_results,
            'configuration': {
                'cpu_threads': self.num_threads,
                'gpu_acceleration': self.use_gpu
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"{Fore.GREEN}Results saved to: {filename}{Style.RESET_ALL}")
        return filename
