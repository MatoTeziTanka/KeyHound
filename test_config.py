#!/usr/bin/env python3
"""
Test Configuration for KeyHound Enhanced

This module provides comprehensive test configuration, fixtures, and utilities
for running KeyHound Enhanced tests with different configurations and environments.

Features:
- Test environment configuration
- Mock data generation
- Test fixtures and utilities
- Performance test configurations
- Integration test setups
- CI/CD test configurations

Legendary Code Quality Standards:
- Comprehensive test configuration
- Detailed documentation and examples
- Performance optimization for tests
- Security best practices in testing
"""

import os
import sys
import json
import tempfile
import unittest
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TestConfig:
    """Test configuration settings."""
    # Test environment
    test_environment: str = "development"
    verbose: bool = True
    log_level: str = "INFO"
    
    # GPU testing
    test_gpu: bool = True
    gpu_framework: str = "cuda"
    gpu_test_keys: int = 10000
    
    # Performance testing
    performance_test_duration: int = 30
    memory_test_threshold_mb: int = 500
    
    # Bitcoin testing
    test_bitcoin_puzzles: bool = True
    test_puzzle_ids: List[int] = None
    test_brainwallet_patterns: bool = True
    max_test_patterns: int = 1000
    
    # Integration testing
    test_integration: bool = True
    test_error_handling: bool = True
    
    # Output settings
    save_test_results: bool = True
    test_output_dir: str = None
    
    def __post_init__(self):
        """Post-initialization setup."""
        if self.test_puzzle_ids is None:
            self.test_puzzle_ids = [1, 2, 3, 4, 5]  # Small puzzles for testing
        
        if self.test_output_dir is None:
            self.test_output_dir = tempfile.mkdtemp(prefix="keyhound_test_")


class TestDataGenerator:
    """Generate test data for KeyHound Enhanced tests."""
    
    @staticmethod
    def generate_test_private_keys(count: int = 100) -> List[str]:
        """Generate test private keys."""
        import secrets
        
        keys = []
        for _ in range(count):
            # Generate random 32-byte private key
            private_key = secrets.token_hex(32)
            keys.append(private_key)
        
        return keys
    
    @staticmethod
    def generate_test_passphrases(count: int = 100) -> List[str]:
        """Generate test passphrases for brainwallet testing."""
        test_passphrases = [
            "password",
            "123456",
            "password123",
            "admin",
            "qwerty",
            "letmein",
            "welcome",
            "monkey",
            "dragon",
            "master",
            "hello",
            "freedom",
            "whatever",
            "qazwsx",
            "trustno1",
            "dragon",
            "password1",
            "1234567890",
            "abc123",
            "Password1"
        ]
        
        # Extend with generated passphrases if needed
        while len(test_passphrases) < count:
            import random
            import string
            
            # Generate random passphrase
            length = random.randint(4, 12)
            passphrase = ''.join(random.choices(
                string.ascii_letters + string.digits + "!@#$%^&*",
                k=length
            ))
            test_passphrases.append(passphrase)
        
        return test_passphrases[:count]
    
    @staticmethod
    def generate_test_bitcoin_addresses(count: int = 100) -> List[str]:
        """Generate test Bitcoin addresses."""
        test_addresses = [
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Genesis block
            "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",  # Satoshi
            "12c6DSiU4Rq3P4ZxziKxzTrLWEaLMKTc1H",  # Example
            "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",  # Example
            "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # Example
        ]
        
        # Extend with generated addresses if needed
        while len(test_addresses) < count:
            import random
            import string
            
            # Generate mock address
            address = "1" + ''.join(random.choices(
                string.ascii_letters + string.digits,
                k=32
            ))
            test_addresses.append(address)
        
        return test_addresses[:count]
    
    @staticmethod
    def generate_test_config() -> Dict[str, Any]:
        """Generate test configuration."""
        return {
            "test_environment": "testing",
            "gpu_enabled": False,
            "max_threads": 4,
            "log_level": "DEBUG",
            "test_data": {
                "private_keys_count": 100,
                "passphrases_count": 50,
                "addresses_count": 25
            }
        }


class TestFixtures:
    """Test fixtures and utilities."""
    
    def __init__(self, config: TestConfig):
        """Initialize test fixtures."""
        self.config = config
        self.temp_dir = None
        self.test_data = {}
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="keyhound_fixtures_")
        
        # Generate test data
        self.test_data = {
            "private_keys": TestDataGenerator.generate_test_private_keys(100),
            "passphrases": TestDataGenerator.generate_test_passphrases(50),
            "bitcoin_addresses": TestDataGenerator.generate_test_bitcoin_addresses(25),
            "config": TestDataGenerator.generate_test_config()
        }
        
        # Save test data to files
        self._save_test_data()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _save_test_data(self):
        """Save test data to files."""
        # Save private keys
        private_keys_file = os.path.join(self.temp_dir, "private_keys.txt")
        with open(private_keys_file, 'w') as f:
            for key in self.test_data["private_keys"]:
                f.write(f"{key}\n")
        
        # Save passphrases
        passphrases_file = os.path.join(self.temp_dir, "passphrases.txt")
        with open(passphrases_file, 'w') as f:
            for passphrase in self.test_data["passphrases"]:
                f.write(f"{passphrase}\n")
        
        # Save Bitcoin addresses
        addresses_file = os.path.join(self.temp_dir, "bitcoin_addresses.txt")
        with open(addresses_file, 'w') as f:
            for address in self.test_data["bitcoin_addresses"]:
                f.write(f"{address}\n")
        
        # Save configuration
        config_file = os.path.join(self.temp_dir, "test_config.json")
        with open(config_file, 'w') as f:
            json.dump(self.test_data["config"], f, indent=2)
    
    def get_test_file_path(self, filename: str) -> str:
        """Get path to test file."""
        return os.path.join(self.temp_dir, filename)


class TestRunner:
    """Advanced test runner for KeyHound Enhanced."""
    
    def __init__(self, config: TestConfig):
        """Initialize test runner."""
        self.config = config
        self.fixtures = TestFixtures(config)
        self.test_results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests with comprehensive reporting."""
        print("Starting KeyHound Enhanced Test Suite...")
        print(f"Test Environment: {self.config.test_environment}")
        print(f"Output Directory: {self.config.test_output_dir}")
        
        # Set up fixtures
        self.fixtures.setUp()
        
        try:
            # Run different test categories
            self.test_results = {
                "unit_tests": self._run_unit_tests(),
                "integration_tests": self._run_integration_tests(),
                "performance_tests": self._run_performance_tests(),
                "gpu_tests": self._run_gpu_tests() if self.config.test_gpu else None,
                "error_handling_tests": self._run_error_handling_tests() if self.config.test_error_handling else None
            }
            
            # Generate comprehensive report
            report = self._generate_test_report()
            
            # Save results if requested
            if self.config.save_test_results:
                self._save_test_results(report)
            
            return report
            
        finally:
            # Clean up fixtures
            self.fixtures.tearDown()
    
    def _run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests."""
        print("\nRunning Unit Tests...")
        
        # Import and run unit tests
        from test_keyhound_enhanced import (
            TestBitcoinCryptography,
            TestErrorHandling,
            TestBrainwalletPatterns
        )
        
        suite = unittest.TestSuite()
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBitcoinCryptography))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestErrorHandling))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBrainwalletPatterns))
        
        runner = unittest.TextTestRunner(verbosity=2 if self.config.verbose else 1)
        result = runner.run(suite)
        
        return {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "success": result.wasSuccessful()
        }
    
    def _run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests."""
        if not self.config.test_integration:
            return {"skipped": True}
        
        print("\nRunning Integration Tests...")
        
        from test_keyhound_enhanced import TestIntegration
        
        suite = unittest.TestSuite()
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
        
        runner = unittest.TextTestRunner(verbosity=2 if self.config.verbose else 1)
        result = runner.run(suite)
        
        return {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "success": result.wasSuccessful()
        }
    
    def _run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests."""
        print("\nRunning Performance Tests...")
        
        from test_keyhound_enhanced import TestPerformance
        
        suite = unittest.TestSuite()
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPerformance))
        
        runner = unittest.TextTestRunner(verbosity=2 if self.config.verbose else 1)
        result = runner.run(suite)
        
        return {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "success": result.wasSuccessful()
        }
    
    def _run_gpu_tests(self) -> Dict[str, Any]:
        """Run GPU tests."""
        print("\nRunning GPU Tests...")
        
        from test_keyhound_enhanced import TestGPUFramework
        
        suite = unittest.TestSuite()
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGPUFramework))
        
        runner = unittest.TestLoader().loadTestsFromTestCase(TestGPUFramework)
        result = runner.run(suite)
        
        return {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "success": result.wasSuccessful()
        }
    
    def _run_error_handling_tests(self) -> Dict[str, Any]:
        """Run error handling tests."""
        print("\nRunning Error Handling Tests...")
        
        # Error handling tests are included in unit tests
        return {"included_in_unit_tests": True}
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        total_tests = 0
        total_failures = 0
        total_errors = 0
        
        for category, results in self.test_results.items():
            if results and not results.get("skipped", False) and not results.get("included_in_unit_tests", False):
                total_tests += results.get("tests_run", 0)
                total_failures += results.get("failures", 0)
                total_errors += results.get("errors", 0)
        
        success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "total_failures": total_failures,
                "total_errors": total_errors,
                "success_rate": success_rate,
                "overall_success": total_failures == 0 and total_errors == 0
            },
            "test_categories": self.test_results,
            "configuration": {
                "test_environment": self.config.test_environment,
                "gpu_enabled": self.config.test_gpu,
                "performance_test_duration": self.config.performance_test_duration
            },
            "timestamp": str(time.time())
        }
        
        return report
    
    def _save_test_results(self, report: Dict[str, Any]):
        """Save test results to file."""
        results_file = os.path.join(self.config.test_output_dir, "test_results.json")
        
        with open(results_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Test results saved to: {results_file}")


def get_default_test_config() -> TestConfig:
    """Get default test configuration."""
    return TestConfig()


def get_ci_test_config() -> TestConfig:
    """Get CI/CD test configuration."""
    return TestConfig(
        test_environment="ci",
        verbose=False,
        test_gpu=False,  # Skip GPU tests in CI
        performance_test_duration=10,  # Shorter duration for CI
        max_test_patterns=100
    )


def get_performance_test_config() -> TestConfig:
    """Get performance test configuration."""
    return TestConfig(
        test_environment="performance",
        verbose=True,
        test_gpu=True,
        performance_test_duration=60,
        memory_test_threshold_mb=1000,
        max_test_patterns=10000
    )


if __name__ == "__main__":
    import time
    
    # Example usage
    config = get_default_test_config()
    runner = TestRunner(config)
    
    start_time = time.time()
    results = runner.run_all_tests()
    end_time = time.time()
    
    print(f"\nTest execution completed in {end_time - start_time:.2f} seconds")
    print(f"Overall success: {results['test_summary']['overall_success']}")
    print(f"Success rate: {results['test_summary']['success_rate']:.1f}%")
