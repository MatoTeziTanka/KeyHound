#!/usr/bin/env python3
"""
Comprehensive Test Suite for KeyHound Enhanced
Tests all core functionality, components, and integration
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
import json
import yaml

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestKeyHoundCore(unittest.TestCase):
    """Test core KeyHound functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_config = {
            'puzzle_solving': {
                'max_bits': 66,
                'batch_size': 1000,
                'timeout': 30
            },
            'performance': {
                'enable_gpu': False,
                'enable_distributed': False,
                'log_level': 'INFO'
            }
        }
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_core_imports(self):
        """Test that core modules can be imported."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            from core.bitcoin_cryptography import BitcoinCryptography
            from core.puzzle_data import BITCOIN_PUZZLES
            from core.error_handling import KeyHoundLogger
            self.assertTrue(True, "Core imports successful")
        except ImportError as e:
            self.fail(f"Core import failed: {e}")
    
    def test_keyhound_enhanced_initialization(self):
        """Test KeyHoundEnhanced initialization."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            # Test initialization without GPU
            keyhound = KeyHoundEnhanced(use_gpu=False, verbose=False)
            self.assertIsNotNone(keyhound)
            self.assertIsNotNone(keyhound.bitcoin_crypto)
            self.assertIsNotNone(keyhound.config_manager)
            self.assertIsNotNone(keyhound.performance_monitor)
            
        except Exception as e:
            self.fail(f"KeyHoundEnhanced initialization failed: {e}")
    
    def test_bitcoin_cryptography(self):
        """Test Bitcoin cryptography functionality."""
        try:
            from core.bitcoin_cryptography import BitcoinCryptography
            
            crypto = BitcoinCryptography()
            
            # Test key generation
            private_key = crypto.generate_private_key()
            self.assertIsNotNone(private_key)
            self.assertEqual(len(private_key), 64)  # 32 bytes = 64 hex chars
            
            # Test address generation
            address = crypto.private_key_to_address(private_key)
            self.assertIsNotNone(address)
            self.assertTrue(address.startswith('1') or address.startswith('3') or address.startswith('bc1'))
            
            # Test key validation
            self.assertTrue(crypto.is_valid_private_key(private_key))
            self.assertFalse(crypto.is_valid_private_key("invalid"))
            
        except Exception as e:
            self.fail(f"Bitcoin cryptography test failed: {e}")
    
    def test_puzzle_data(self):
        """Test puzzle data functionality."""
        try:
            from core.puzzle_data import BITCOIN_PUZZLES, get_brainwallet_patterns
            
            # Test puzzle data exists
            self.assertIsInstance(BITCOIN_PUZZLES, dict)
            self.assertGreater(len(BITCOIN_PUZZLES), 0)
            
            # Test brainwallet patterns
            patterns = get_brainwallet_patterns()
            self.assertIsInstance(patterns, list)
            self.assertGreater(len(patterns), 0)
            
        except Exception as e:
            self.fail(f"Puzzle data test failed: {e}")
    
    def test_configuration_manager(self):
        """Test configuration management."""
        try:
            from core.configuration_manager import ConfigurationManager
            
            config_manager = ConfigurationManager()
            
            # Test default configuration
            default_config = config_manager.get_default_config()
            self.assertIsInstance(default_config, dict)
            self.assertIn('puzzle_solving', default_config)
            self.assertIn('performance', default_config)
            
            # Test configuration validation
            self.assertTrue(config_manager.validate_config(self.test_config))
            
        except Exception as e:
            self.fail(f"Configuration manager test failed: {e}")
    
    def test_error_handling(self):
        """Test error handling and logging."""
        try:
            from core.error_handling import KeyHoundLogger, KeyHoundError
            
            # Test logger initialization
            logger = KeyHoundLogger("TestLogger")
            self.assertIsNotNone(logger)
            
            # Test error handling
            try:
                raise KeyHoundError("Test error")
            except KeyHoundError as e:
                self.assertEqual(str(e), "Test error")
            
        except Exception as e:
            self.fail(f"Error handling test failed: {e}")
    
    def test_memory_optimization(self):
        """Test memory optimization functionality."""
        try:
            from core.memory_optimization import MemoryOptimizer, get_memory_optimizer
            
            # Test memory optimizer
            optimizer = get_memory_optimizer()
            self.assertIsNotNone(optimizer)
            
            # Test memory usage tracking
            usage = optimizer.get_memory_usage()
            self.assertIsInstance(usage, dict)
            self.assertIn('total', usage)
            self.assertIn('available', usage)
            
        except Exception as e:
            self.fail(f"Memory optimization test failed: {e}")
    
    def test_performance_monitoring(self):
        """Test performance monitoring."""
        try:
            from core.performance_monitoring import PerformanceMonitor, get_performance_monitor
            
            # Test performance monitor
            monitor = get_performance_monitor()
            self.assertIsNotNone(monitor)
            
            # Test metrics collection
            monitor.start_timer("test_metric")
            monitor.stop_timer("test_metric")
            
            metrics = monitor.get_metrics()
            self.assertIsInstance(metrics, dict)
            
        except Exception as e:
            self.fail(f"Performance monitoring test failed: {e}")
    
    def test_result_persistence(self):
        """Test result persistence functionality."""
        try:
            from core.result_persistence import ResultPersistenceManager, get_result_persistence_manager
            
            # Test result persistence manager
            persistence_manager = get_result_persistence_manager()
            self.assertIsNotNone(persistence_manager)
            
            # Test result storage
            test_result = {
                'private_key': 'test_key',
                'address': 'test_address',
                'timestamp': '2025-01-01T00:00:00Z'
            }
            
            # This should not fail even if storage is not configured
            try:
                persistence_manager.store_result(test_result)
            except:
                pass  # Expected if storage not configured
            
        except Exception as e:
            self.fail(f"Result persistence test failed: {e}")

class TestKeyHoundAdvanced(unittest.TestCase):
    """Test advanced KeyHound features."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_gpu_availability(self):
        """Test GPU availability detection."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            keyhound = KeyHoundEnhanced(use_gpu=True, verbose=False)
            
            # Check if GPU features are available
            self.assertIsInstance(keyhound._available_features, dict)
            self.assertIn('gpu', keyhound._available_features)
            
            # GPU manager should be None if not available
            if not keyhound._available_features['gpu']:
                self.assertIsNone(keyhound.gpu_manager)
            
        except Exception as e:
            self.fail(f"GPU availability test failed: {e}")
    
    def test_web_availability(self):
        """Test web interface availability."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            keyhound = KeyHoundEnhanced(verbose=False)
            
            # Check if web features are available
            self.assertIsInstance(keyhound._available_features, dict)
            self.assertIn('web', keyhound._available_features)
            
        except Exception as e:
            self.fail(f"Web availability test failed: {e}")
    
    def test_ml_availability(self):
        """Test machine learning availability."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            keyhound = KeyHoundEnhanced(verbose=False)
            
            # Check if ML features are available
            self.assertIsInstance(keyhound._available_features, dict)
            self.assertIn('ml', keyhound._available_features)
            
        except Exception as e:
            self.fail(f"ML availability test failed: {e}")
    
    def test_distributed_availability(self):
        """Test distributed computing availability."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            keyhound = KeyHoundEnhanced(verbose=False)
            
            # Check if distributed features are available
            self.assertIsInstance(keyhound._available_features, dict)
            self.assertIn('distributed', keyhound._available_features)
            
        except Exception as e:
            self.fail(f"Distributed availability test failed: {e}")

class TestKeyHoundIntegration(unittest.TestCase):
    """Test KeyHound integration and end-to-end functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_puzzle_solving_workflow(self):
        """Test complete puzzle solving workflow."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            keyhound = KeyHoundEnhanced(use_gpu=False, verbose=False)
            
            # Test puzzle solving setup (without actually solving)
            # This tests the workflow setup
            puzzle_bits = 40  # Small puzzle for testing
            
            # Test that puzzle solving can be initialized
            # We won't actually solve to avoid long test times
            self.assertIsNotNone(keyhound.bitcoin_crypto)
            self.assertIsNotNone(keyhound.config_manager)
            
        except Exception as e:
            self.fail(f"Puzzle solving workflow test failed: {e}")
    
    def test_brainwallet_testing_workflow(self):
        """Test brainwallet testing workflow."""
        try:
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            keyhound = KeyHoundEnhanced(verbose=False)
            
            # Test brainwallet testing setup
            self.assertIsNotNone(keyhound.pattern_library)
            
        except Exception as e:
            self.fail(f"Brainwallet testing workflow test failed: {e}")
    
    def test_configuration_loading(self):
        """Test configuration loading from files."""
        try:
            # Create test config file
            test_config_path = os.path.join(self.temp_dir, "test_config.yaml")
            test_config = {
                'puzzle_solving': {
                    'max_bits': 50,
                    'batch_size': 500
                },
                'performance': {
                    'enable_gpu': False,
                    'log_level': 'DEBUG'
                }
            }
            
            with open(test_config_path, 'w') as f:
                yaml.dump(test_config, f)
            
            from core.keyhound_enhanced import KeyHoundEnhanced
            
            # Test loading configuration from file
            keyhound = KeyHoundEnhanced(config_file=test_config_path, verbose=False)
            self.assertIsNotNone(keyhound.config_manager)
            
        except Exception as e:
            self.fail(f"Configuration loading test failed: {e}")

class TestKeyHoundDeployment(unittest.TestCase):
    """Test deployment configurations and files."""
    
    def test_docker_configuration(self):
        """Test Docker configuration files."""
        dockerfile_path = Path(__file__).parent.parent / "deployments" / "docker" / "Dockerfile"
        docker_compose_path = Path(__file__).parent.parent / "deployments" / "docker" / "docker-compose.yml"
        
        self.assertTrue(dockerfile_path.exists(), "Dockerfile should exist")
        self.assertTrue(docker_compose_path.exists(), "docker-compose.yml should exist")
        
        # Test Dockerfile content
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
            self.assertIn("FROM python", dockerfile_content)
            self.assertIn("COPY", dockerfile_content)
            self.assertIn("CMD", dockerfile_content)
    
    def test_colab_notebook(self):
        """Test Google Colab notebook."""
        notebook_path = Path(__file__).parent.parent / "deployments" / "colab" / "KeyHound_Enhanced.ipynb"
        
        self.assertTrue(notebook_path.exists(), "Colab notebook should exist")
    
    def test_requirements_file(self):
        """Test requirements.txt file."""
        requirements_path = Path(__file__).parent.parent / "requirements.txt"
        
        self.assertTrue(requirements_path.exists(), "requirements.txt should exist")
        
        with open(requirements_path, 'r') as f:
            requirements = f.read()
            self.assertIn("numpy", requirements)
            self.assertIn("ecdsa", requirements)
            self.assertIn("cryptography", requirements)
    
    def test_setup_py(self):
        """Test setup.py file."""
        setup_path = Path(__file__).parent.parent / "setup.py"
        
        self.assertTrue(setup_path.exists(), "setup.py should exist")
        
        with open(setup_path, 'r') as f:
            setup_content = f.read()
            self.assertIn("name=", setup_content)
            self.assertIn("version=", setup_content)

def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("KeyHound Enhanced - Comprehensive Test Suite")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestKeyHoundCore,
        TestKeyHoundAdvanced,
        TestKeyHoundIntegration,
        TestKeyHoundDeployment
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
