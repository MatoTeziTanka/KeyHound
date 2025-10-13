#!/usr/bin/env python3
"""
KeyHound Enhanced - Structure Validation Script
Validates the professional reorganization and file references
"""

import os
import sys
import importlib.util
from pathlib import Path

def validate_directory_structure():
    """Validate the professional directory structure"""
    print("Validating KeyHound Enhanced Structure...")
    print("=" * 50)
    
    required_dirs = [
        'src',
        'src/core',
        'src/gpu', 
        'src/ml',
        'src/web',
        'src/distributed',
        'tests',
        'docs',
        'scripts',
        'config',
        'templates',
        'static'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"ERROR: Missing directories: {missing_dirs}")
        return False
    else:
        print("SUCCESS: All required directories present")
        return True

def validate_core_modules():
    """Validate core modules are accessible"""
    print("\nValidating Core Modules...")
    print("=" * 30)
    
    core_modules = [
        'src.core.bitcoin_cryptography',
        'src.core.configuration_manager',
        'src.core.error_handling',
        'src.core.memory_optimization',
        'src.core.performance_monitoring',
        'src.core.result_persistence'
    ]
    
    failed_imports = []
    for module_name in core_modules:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                failed_imports.append(module_name)
            else:
                print(f"SUCCESS: {module_name}")
        except ImportError as e:
            failed_imports.append(f"{module_name}: {e}")
    
    if failed_imports:
        print(f"ERROR: Failed imports: {failed_imports}")
        return False
    else:
        print("SUCCESS: All core modules accessible")
        return True

def validate_file_references():
    """Validate file path references are correct"""
    print("\nValidating File References...")
    print("=" * 35)
    
    # Check main.py imports
    main_py_path = Path("main.py")
    if main_py_path.exists():
        with open(main_py_path, 'r') as f:
            content = f.read()
            if "from src." in content:
                print("SUCCESS: main.py uses new import structure")
            else:
                print("ERROR: main.py needs import updates")
                return False
    else:
        print("ERROR: main.py not found")
        return False
    
    # Check keyhound_enhanced.py imports
    kh_path = Path("keyhound_enhanced.py")
    if kh_path.exists():
        with open(kh_path, 'r') as f:
            content = f.read()
            if "from src." in content:
                print("SUCCESS: keyhound_enhanced.py uses new import structure")
            else:
                print("ERROR: keyhound_enhanced.py needs import updates")
                return False
    
    return True

def validate_config_files():
    """Validate configuration files exist"""
    print("\nValidating Configuration...")
    print("=" * 32)
    
    config_files = [
        'config/default.yaml',
        'requirements.txt',
        'README.md'
    ]
    
    missing_configs = []
    for config_file in config_files:
        if not os.path.exists(config_file):
            missing_configs.append(config_file)
        else:
            print(f"SUCCESS: {config_file}")
    
    if missing_configs:
        print(f"ERROR: Missing config files: {missing_configs}")
        return False
    
    return True

def validate_test_structure():
    """Validate test files are organized"""
    print("\nValidating Test Structure...")
    print("=" * 33)
    
    test_files = [
        'tests/comprehensive_test.py',
        'tests/scaled_test.py',
        'tests/test_keyhound_enhanced.py',
        'tests/verify_found_keys.py'
    ]
    
    missing_tests = []
    for test_file in test_files:
        if not os.path.exists(test_file):
            missing_tests.append(test_file)
        else:
            print(f"SUCCESS: {test_file}")
    
    if missing_tests:
        print(f"ERROR: Missing test files: {missing_tests}")
        return False
    
    return True

def main():
    """Main validation function"""
    print("KeyHound Enhanced - Professional Structure Validation")
    print("=" * 60)
    
    validations = [
        validate_directory_structure,
        validate_core_modules,
        validate_file_references,
        validate_config_files,
        validate_test_structure
    ]
    
    all_passed = True
    for validation in validations:
        if not validation():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("VALIDATION PASSED - Professional structure is ready!")
        print("SUCCESS: All files organized correctly")
        print("SUCCESS: All imports updated")
        print("SUCCESS: Configuration files present")
        print("SUCCESS: Test structure organized")
        print("\nKeyHound Enhanced is production-ready!")
    else:
        print("VALIDATION FAILED - Issues found")
        print("Please fix the issues above before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()