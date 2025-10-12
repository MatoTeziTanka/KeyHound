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

# Import KeyHound modules
from puzzle_data import BITCOIN_PUZZLES, get_brainwallet_patterns, hex_range_to_int_range
from gpu_acceleration import GPUAccelerationManager, GPUConfig, GPUPerformanceMetrics
from gpu_framework import GPUFrameworkManager, GPUDevice, GPUPerformanceMetrics as FrameworkMetrics
from brainwallet_patterns import BrainwalletPatternLibrary, BrainwalletPattern, PatternMatch
from bitcoin_cryptography import BitcoinCryptography, BitcoinAddress, CryptographyError
from memory_optimization import MemoryOptimizer, StreamingKeyProcessor, get_memory_optimizer
from configuration_manager import ConfigurationManager, get_config_manager, ConfigSchema, ConfigValidationRule
from error_handling import (
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
        
        # Initialize brainwallet pattern library
        try:
            self.pattern_library = BrainwalletPatternLibrary()
            keyhound_logger.info(f"Brainwallet pattern library loaded with {len(self.pattern_library.patterns)} patterns")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.pattern_library = None
        
        # Initialize Bitcoin cryptography
        try:
            self.bitcoin_crypto = BitcoinCryptography()
            keyhound_logger.info("Bitcoin cryptography module initialized successfully")
        except Exception as e:
            keyhound_logger.log_error(e)
            self.bitcoin_crypto = None
        
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
    
    @error_handler(keyhound_logger)
    @performance_monitor(keyhound_logger)
    def solve_bitcoin_puzzle(self, puzzle_id: int) -> Optional[str]:
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
    @performance_monitor(keyhound_logger)
    def solve_bitcoin_puzzle_streaming(self, puzzle_id: int, max_keys: int = 1000000) -> Optional[str]:
        """
        Solve Bitcoin puzzle using streaming processing for large key spaces.
        
        Args:
            puzzle_id: The puzzle ID to solve
            max_keys: Maximum number of keys to check
            
        Returns:
            Private key if found, None otherwise
        """
        if puzzle_id not in BITCOIN_PUZZLES:
            keyhound_logger.error(f"Unknown puzzle ID: {puzzle_id}")
            return None
        
        puzzle = BITCOIN_PUZZLES[puzzle_id]
        target_address = puzzle["address"]
        
        keyhound_logger.info(f"Starting streaming puzzle solving for Puzzle #{puzzle_id}")
        keyhound_logger.info(f"Target address: {target_address}")
        keyhound_logger.info(f"Key range: 1 to {max_keys}")
        
        # Use memory optimizer for streaming processing
        if self.memory_optimizer:
            def process_key(key_int):
                """Process a single key for puzzle solving."""
                try:
                    # Generate Bitcoin address
                    address = self._generate_bitcoin_address(key_int)
                    
                    # Check if address matches target
                    if address == target_address:
                        keyhound_logger.info(f"SOLUTION FOUND! Private key: {hex(key_int)}")
                        return {
                            "private_key": hex(key_int),
                            "address": address,
                            "puzzle_id": puzzle_id
                        }
                    
                    return None
                except Exception as e:
                    keyhound_logger.warning(f"Error processing key {key_int}: {e}")
                    return None
            
            # Use streaming key processor
            streaming_processor = StreamingKeyProcessor(self.memory_optimizer, batch_size=10000)
            
            # Process keys in streaming fashion
            results = list(streaming_processor.process_key_range(1, max_keys + 1, process_key))
            
            if results:
                solution = results[0]  # First solution found
                self.found_keys.append(solution)
                return solution["private_key"]
            
            # Get processing statistics
            stats = streaming_processor.get_statistics()
            keyhound_logger.info(f"Streaming processing completed: {stats['keys_processed']:,} keys processed")
            keyhound_logger.info(f"Processing rate: {stats['keys_per_second']:.0f} keys/second")
        
        else:
            keyhound_logger.warning("Memory optimizer not available, falling back to standard solving")
            return self.solve_bitcoin_puzzle(puzzle_id)
        
        keyhound_logger.info(f"No solution found in {max_keys:,} keys")
        return None
    
    @error_handler(keyhound_logger)
    @performance_monitor(keyhound_logger)
    def brainwallet_security_test(self, target_address: str, custom_patterns: List[str] = None,
                                 category: Optional[str] = None, language: Optional[str] = None,
                                 difficulty: Optional[str] = None, max_patterns: int = 10000) -> Dict[str, Any]:
        """
        Enhanced brainwallet security test using comprehensive pattern library.
        
        Args:
            target_address: Target Bitcoin address to check
            custom_patterns: Custom patterns to test (optional)
            category: Pattern category filter
            language: Language filter
            difficulty: Difficulty filter
            max_patterns: Maximum number of patterns to test
            
        Returns:
            Dictionary with comprehensive test results
        """
        print(f"{Fore.CYAN}Enhanced Brainwallet Security Test{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Target Address: {target_address}{Style.RESET_ALL}")
        
        # Get patterns to test
        patterns_to_test = []
        
        if self.pattern_library:
            # Get patterns from library with filters
            if custom_patterns:
                # Add custom patterns
                for pattern_str in custom_patterns:
                    patterns_to_test.append(BrainwalletPattern(
                        pattern=pattern_str,
                        category="custom",
                        language="custom",
                        difficulty="unknown",
                        effectiveness_score=0.5
                    ))
            
            # Get patterns from library
            library_patterns = self.pattern_library.patterns
            
            # Apply filters
            if category:
                library_patterns = [p for p in library_patterns if p.category == category]
            if language:
                library_patterns = [p for p in library_patterns if p.language == language]
            if difficulty:
                library_patterns = [p for p in library_patterns if p.difficulty == difficulty]
            
            # Sort by effectiveness score and limit
            library_patterns.sort(key=lambda x: x.effectiveness_score, reverse=True)
            patterns_to_test.extend(library_patterns[:max_patterns])
        else:
            # Fallback to basic patterns
            patterns_to_test = [BrainwalletPattern(
                pattern=p, category="basic", language="english", difficulty="unknown"
            ) for p in get_brainwallet_patterns()]
        
        print(f"{Fore.YELLOW}Testing {len(patterns_to_test)} patterns{Style.RESET_ALL}")
        
        results = {
            'target_address': target_address,
            'patterns_tested': len(patterns_to_test),
            'vulnerabilities_found': [],
            'test_duration': 0,
            'patterns_per_second': 0,
            'category_breakdown': {},
            'language_breakdown': {},
            'difficulty_breakdown': {},
            'top_effective_patterns': []
        }
        
        start_time = time.time()
        patterns_processed = 0
        
        with tqdm(patterns_to_test, desc="Testing patterns", unit="pattern") as pbar:
            for pattern in pbar:
                try:
                    # Generate brainwallet private key from pattern
                    private_key = self._generate_brainwallet_key(pattern.pattern)
                    
                    # Generate Bitcoin address
                    address = self._generate_bitcoin_address(private_key)
                    
                    # Check if it matches target
                    if address == target_address:
                        vulnerability = {
                            'pattern': pattern.pattern,
                            'private_key': private_key,
                            'address': address,
                            'category': pattern.category,
                            'language': pattern.language,
                            'difficulty': pattern.difficulty,
                            'effectiveness_score': pattern.effectiveness_score,
                            'confidence': pattern.effectiveness_score
                        }
                        results['vulnerabilities_found'].append(vulnerability)
                        
                        print(f"\n{Fore.RED}🚨 VULNERABILITY FOUND! 🚨{Style.RESET_ALL}")
                        print(f"{Fore.RED}Pattern: '{pattern.pattern}'{Style.RESET_ALL}")
                        print(f"{Fore.RED}Category: {pattern.category}{Style.RESET_ALL}")
                        print(f"{Fore.RED}Language: {pattern.language}{Style.RESET_ALL}")
                        print(f"{Fore.RED}Private Key: {private_key}{Style.RESET_ALL}")
                        print(f"{Fore.RED}Address: {address}{Style.RESET_ALL}")
                        print(f"{Fore.RED}Confidence: {pattern.effectiveness_score:.3f}{Style.RESET_ALL}")
                    
                    # Update progress
                    patterns_processed += 1
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        rate = patterns_processed / elapsed
                        pbar.set_postfix({
                            'Rate': f"{rate:.0f}/s",
                            'Vulns': len(results['vulnerabilities_found'])
                        })
                
                except Exception as e:
                    logger.error(f"Error testing pattern '{pattern.pattern}': {e}")
                    continue
        
        # Calculate final results
        results['test_duration'] = time.time() - start_time
        results['patterns_per_second'] = patterns_processed / results['test_duration'] if results['test_duration'] > 0 else 0
        
        # Analyze results by category, language, and difficulty
        if results['vulnerabilities_found']:
            categories = [v['category'] for v in results['vulnerabilities_found']]
            languages = [v['language'] for v in results['vulnerabilities_found']]
            difficulties = [v['difficulty'] for v in results['vulnerabilities_found']]
            
            results['category_breakdown'] = dict(Counter(categories))
            results['language_breakdown'] = dict(Counter(languages))
            results['difficulty_breakdown'] = dict(Counter(difficulties))
            
            # Get top effective patterns
            results['top_effective_patterns'] = sorted(
                results['vulnerabilities_found'],
                key=lambda x: x['effectiveness_score'],
                reverse=True
            )[:10]
        
        # Print comprehensive results
        print(f"\n{Fore.GREEN}Enhanced Security Test Complete{Style.RESET_ALL}")
        print(f"Patterns tested: {results['patterns_tested']}")
        print(f"Vulnerabilities found: {len(results['vulnerabilities_found'])}")
        print(f"Test duration: {results['test_duration']:.2f} seconds")
        print(f"Speed: {results['patterns_per_second']:.0f} patterns/second")
        
        if results['vulnerabilities_found']:
            print(f"\n{Fore.RED}Vulnerability Analysis:{Style.RESET_ALL}")
            print(f"Categories: {results['category_breakdown']}")
            print(f"Languages: {results['language_breakdown']}")
            print(f"Difficulties: {results['difficulty_breakdown']}")
        
        return results
    
    @error_handler(keyhound_logger)
    @performance_monitor(keyhound_logger)
    def performance_benchmark(self, test_duration: int = 60, use_gpu: bool = None) -> Dict[str, Any]:
        """
        Enhanced performance benchmark with GPU acceleration support.
        
        Args:
            test_duration: Duration in seconds to run benchmark
            use_gpu: Force GPU usage (None = use instance setting)
            
        Returns:
            Dictionary with comprehensive benchmark results
        """
        print(f"{Fore.CYAN}Enhanced Performance Benchmark{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Running for {test_duration} seconds{Style.RESET_ALL}")
        
        # Determine if we should use GPU
        benchmark_gpu = use_gpu if use_gpu is not None else self.use_gpu
        if benchmark_gpu and self.gpu_manager and self.gpu_manager.is_gpu_available():
            return self._gpu_benchmark(test_duration)
        else:
            return self._cpu_benchmark(test_duration)
    
    def _gpu_benchmark(self, test_duration: int) -> Dict[str, Any]:
        """Run GPU-accelerated benchmark using advanced framework."""
        print(f"{Fore.GREEN}GPU Benchmark Mode{Style.RESET_ALL}")
        
        results = {
            'test_duration': test_duration,
            'framework': self.gpu_framework,
            'device_info': {},
            'operations_per_second': 0,
            'total_operations': 0,
            'memory_usage_mb': 0,
            'gpu_utilization': 0,
            'memory_bandwidth_gb_s': 0
        }
        
        try:
            # Try advanced GPU framework first
            if self.gpu_framework_manager and self.gpu_framework_manager.is_initialized:
                keyhound_logger.info("Running advanced GPU framework benchmark...")
                
                # Run benchmark using advanced framework
                benchmark_results = self.gpu_framework_manager.benchmark_all_frameworks(
                    num_keys=1000000
                )
                
                # Aggregate results from all frameworks
                total_operations = 0
                total_execution_time = 0
                best_performance = 0
                best_framework = ""
                
                for framework_name, metrics in benchmark_results.items():
                    total_operations += 1000000  # Each framework tested with 1M keys
                    total_execution_time += metrics.total_execution_time
                    if metrics.operations_per_second > best_performance:
                        best_performance = metrics.operations_per_second
                        best_framework = framework_name
                
                results.update({
                    'operations_per_second': best_performance,
                    'total_operations': total_operations,
                    'execution_time_seconds': total_execution_time,
                    'gpu_frameworks': benchmark_results,
                    'best_framework': best_framework
                })
                
                # Get device info from advanced framework
                device_info = self.gpu_framework_manager.get_device_info()
                results['device_info'] = device_info.get(best_framework, {})
                
                print(f"\n{Fore.GREEN}Advanced GPU Benchmark Complete{Style.RESET_ALL}")
                print(f"Best Framework: {best_framework.upper()}")
                print(f"Device: {results['device_info'].name if hasattr(results['device_info'], 'name') else 'Unknown'}")
                print(f"Operations per second: {results['operations_per_second']:,.0f}")
            
            # Fallback to legacy GPU manager
            elif self.gpu_manager and self.gpu_manager.is_gpu_available():
                keyhound_logger.info("Running legacy GPU benchmark...")
                
                results.update({
                    'framework': self.gpu_framework,
                    'device_info': self.gpu_manager.get_device_info()
                })
                
                # Run GPU benchmark
                gpu_metrics = self.gpu_manager.benchmark_performance(num_keys=1000000)
                
                results.update({
                    'operations_per_second': gpu_metrics.operations_per_second,
                    'total_operations': gpu_metrics.total_operations,
                    'memory_usage_mb': gpu_metrics.memory_usage_mb,
                    'execution_time_seconds': gpu_metrics.execution_time_seconds
                })
                
                print(f"\n{Fore.GREEN}Legacy GPU Benchmark Complete{Style.RESET_ALL}")
                print(f"Framework: {self.gpu_framework.upper()}")
                print(f"Device: {results['device_info'].get('name', 'Unknown')}")
                print(f"Operations per second: {results['operations_per_second']:,.0f}")
            
            else:
                raise GPUError("No GPU acceleration available")
            print(f"Memory usage: {results['memory_usage_mb']:.2f} MB")
            print(f"Total operations: {results['total_operations']:,}")
            
        except Exception as e:
            logger.error(f"GPU benchmark failed: {e}")
            print(f"{Fore.YELLOW}GPU benchmark failed, falling back to CPU{Style.RESET_ALL}")
            return self._cpu_benchmark(test_duration)
        
        # Save benchmark results
        self.benchmark_results = results
        
        return results
    
    def _cpu_benchmark(self, test_duration: int) -> Dict[str, Any]:
        """Run CPU-only benchmark."""
        print(f"{Fore.BLUE}CPU Benchmark Mode{Style.RESET_ALL}")
        
        results = {
            'test_duration': test_duration,
            'framework': 'cpu',
            'operations_per_second': 0,
            'total_operations': 0,
            'cpu_threads': self.num_threads,
            'gpu_acceleration': False
        }
        
        start_time = time.time()
        operations = 0
        
        with tqdm(total=test_duration, desc="CPU Benchmarking", unit="s") as pbar:
            while time.time() - start_time < test_duration:
                # Perform cryptographic operations
                private_key = operations
                address = self._generate_bitcoin_address(private_key)
                operations += 1
                
                # Update progress
                elapsed = time.time() - start_time
                if elapsed > 0:
                    rate = operations / elapsed
                    pbar.set_postfix({
                        'Ops/s': f"{rate:.0f}",
                        'Total': f"{operations:,}"
                    })
                
                pbar.update(min(1, test_duration - elapsed))
        
        results['total_operations'] = operations
        results['operations_per_second'] = operations / test_duration
        
        print(f"\n{Fore.GREEN}CPU Benchmark Complete{Style.RESET_ALL}")
        print(f"Total operations: {results['total_operations']:,}")
        print(f"Operations per second: {results['operations_per_second']:.0f}")
        print(f"CPU threads: {results['cpu_threads']}")
        
        # Save benchmark results
        self.benchmark_results = results
        
        return results
    
    def academic_research_mode(self, research_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Academic research mode for cryptographic vulnerability studies.
        
        Args:
            research_type: Type of research to conduct
            parameters: Research parameters
            
        Returns:
            Dictionary with research results
        """
        print(f"{Fore.CYAN}Academic Research Mode: {research_type}{Style.RESET_ALL}")
        
        results = {
            'research_type': research_type,
            'parameters': parameters,
            'findings': [],
            'statistics': {},
            'recommendations': []
        }
        
        if research_type == "entropy_analysis":
            results = self._entropy_analysis(parameters)
        elif research_type == "pattern_analysis":
            results = self._pattern_analysis(parameters)
        elif research_type == "collision_study":
            results = self._collision_study(parameters)
        else:
            print(f"{Fore.RED}Unknown research type: {research_type}{Style.RESET_ALL}")
        
        return results
    
    def _entropy_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze entropy patterns in private keys."""
        print(f"{Fore.YELLOW}Conducting entropy analysis{Style.RESET_ALL}")
        # TODO: Implement entropy analysis
        return {"analysis": "Entropy analysis implementation in progress"}
    
    def _pattern_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in Bitcoin addresses and private keys."""
        print(f"{Fore.YELLOW}Conducting pattern analysis{Style.RESET_ALL}")
        # TODO: Implement pattern analysis
        return {"analysis": "Pattern analysis implementation in progress"}
    
    def _collision_study(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Study hash collisions in cryptographic operations."""
        print(f"{Fore.YELLOW}Conducting collision study{Style.RESET_ALL}")
        # TODO: Implement collision study
        return {"analysis": "Collision study implementation in progress"}
    
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


def main():
    """Main entry point for Enhanced KeyHound."""
    parser = argparse.ArgumentParser(
        description="KeyHound Enhanced - Comprehensive Bitcoin Cryptographic Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Solve Bitcoin Puzzle #71 (highest priority)
  python keyhound_enhanced.py --puzzle 71
  
  # Solve Bitcoin Puzzle #135 (BSGS algorithm)
  python keyhound_enhanced.py --puzzle 135
  
  # Brainwallet security test
  python keyhound_enhanced.py --brainwallet-test 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU
  
  # Performance benchmark
  python keyhound_enhanced.py --benchmark 60
  
  # Academic research mode
  python keyhound_enhanced.py --research entropy_analysis
  
  # List available puzzles
  python keyhound_enhanced.py --list-puzzles
        """
    )
    
    # Main operation modes
    parser.add_argument(
        '--puzzle',
        type=int,
        help='Solve specific Bitcoin puzzle by ID (e.g., 71, 135)'
    )
    
    parser.add_argument(
        '--brainwallet-test',
        type=str,
        help='Test brainwallet security for target address'
    )
    
    parser.add_argument(
        '--benchmark',
        type=int,
        default=60,
        help='Run performance benchmark for N seconds (default: 60)'
    )
    
    parser.add_argument(
        '--research',
        type=str,
        help='Run academic research mode (entropy_analysis, pattern_analysis, collision_study)'
    )
    
    parser.add_argument(
        '--list-puzzles',
        action='store_true',
        help='List all available Bitcoin puzzles'
    )
    
    # Configuration options
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Enable GPU acceleration (if available)'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        help='Number of CPU threads to use (default: all available)'
    )
    
    parser.add_argument(
        '--save-results',
        type=str,
        help='Save results to specified filename'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize KeyHound Enhanced
        keyhound = KeyHoundEnhanced(
            use_gpu=args.gpu,
            num_threads=args.threads
        )
        
        if args.list_puzzles:
            print(f"\n{Fore.CYAN}Available Bitcoin Puzzles:{Style.RESET_ALL}")
            for puzzle_id, data in BITCOIN_PUZZLES.items():
                status_color = Fore.GREEN if data['status'] == 'SOLVED' else Fore.RED
                print(f"{Fore.YELLOW}Puzzle #{puzzle_id}:{Style.RESET_ALL}")
                print(f"  Address: {data['bitcoin_address']}")
                print(f"  Key Range: {data['key_range_bits']} bits")
                print(f"  Status: {status_color}{data['status']}{Style.RESET_ALL}")
                print(f"  Priority: {data['priority']}")
                if 'public_key' in data:
                    print(f"  Algorithm: BSGS (exposed public key)")
                else:
                    print(f"  Algorithm: Brute Force")
                print()
        
        elif args.puzzle:
            result = keyhound.solve_bitcoin_puzzle(args.puzzle)
            if result:
                print(f"\n{Fore.GREEN}🎉 SUCCESS! Puzzle #{args.puzzle} solved!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}Puzzle #{args.puzzle} not solved in this session{Style.RESET_ALL}")
        
        elif args.brainwallet_test:
            results = keyhound.brainwallet_security_test(args.brainwallet_test)
            if results['vulnerabilities_found']:
                print(f"\n{Fore.RED}🚨 {len(results['vulnerabilities_found'])} vulnerabilities found!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}✅ No vulnerabilities found in tested patterns{Style.RESET_ALL}")
        
        elif args.benchmark:
            results = keyhound.performance_benchmark(args.benchmark)
            print(f"\n{Fore.GREEN}Benchmark Results:{Style.RESET_ALL}")
            print(f"Performance: {results['operations_per_second']:.0f} operations/second")
        
        elif args.research:
            results = keyhound.academic_research_mode(args.research, {})
            print(f"\n{Fore.GREEN}Research Results:{Style.RESET_ALL}")
            print(json.dumps(results, indent=2))
        
        else:
            # Interactive mode
            print(f"{Fore.CYAN}Interactive Mode - Enhanced KeyHound{Style.RESET_ALL}")
            print("Available commands:")
            print("  puzzle <id>     - Solve Bitcoin puzzle")
            print("  test <address>  - Brainwallet security test")
            print("  benchmark       - Performance benchmark")
            print("  list            - List available puzzles")
            print("  quit            - Exit")
            
            while True:
                try:
                    user_input = input("\nKeyHound> ").strip().split()
                    
                    if not user_input or user_input[0].lower() == 'quit':
                        break
                    
                    elif user_input[0].lower() == 'puzzle' and len(user_input) > 1:
                        puzzle_id = int(user_input[1])
                        keyhound.solve_bitcoin_puzzle(puzzle_id)
                    
                    elif user_input[0].lower() == 'test' and len(user_input) > 1:
                        address = user_input[1]
                        keyhound.brainwallet_security_test(address)
                    
                    elif user_input[0].lower() == 'benchmark':
                        duration = int(user_input[1]) if len(user_input) > 1 else 60
                        keyhound.performance_benchmark(duration)
                    
                    elif user_input[0].lower() == 'list':
                        for puzzle_id, data in BITCOIN_PUZZLES.items():
                            print(f"Puzzle #{puzzle_id}: {data['bitcoin_address']} ({data['key_range_bits']} bits)")
                    
                    else:
                        print(f"{Fore.RED}Unknown command. Type 'quit' to exit.{Style.RESET_ALL}")
                        
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                    break
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        
        # Save results if requested
        if args.save_results or keyhound.found_keys or keyhound.benchmark_results:
            filename = args.save_results or None
            keyhound.save_results(filename)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
