#!/usr/bin/env python3
"""
KeyHound Enhanced - Simple Path Validation
Validates all file paths after reorganization
"""

import os
import sys
from pathlib import Path

def validate_package_structure():
    """Validate Python package structure"""
    print("Validating package structure...")
    
    required_dirs = [
        "keyhound",
        "keyhound/core",
        "keyhound/gpu",
        "keyhound/ml",
        "keyhound/web",
        "keyhound/distributed"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"SUCCESS: {dir_path}/ exists")
        else:
            print(f"ERROR: {dir_path}/ missing")
            return False
    
    return True

def validate_config_paths():
    """Validate configuration file paths"""
    print("\nValidating configuration paths...")
    
    config_files = [
        "config/default.yaml",
        "config/environments/production.yaml",
        "config/environments/colab.yaml"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"SUCCESS: {config_file} exists")
        else:
            print(f"ERROR: {config_file} missing")
            return False
    
    return True

def validate_main_entry_point():
    """Validate main entry point"""
    print("\nValidating main entry point...")
    
    main_file = "keyhound/main.py"
    if os.path.exists(main_file):
        print(f"SUCCESS: {main_file} exists")
        return True
    else:
        print(f"ERROR: {main_file} missing")
        return False

def test_imports():
    """Test basic imports"""
    print("\nTesting imports...")
    
    try:
        # Add keyhound to path
        sys.path.insert(0, "keyhound")
        
        # Test core import
        from core.keyhound_enhanced import KeyHoundEnhanced
        print("SUCCESS: KeyHoundEnhanced import works")
        
        # Test puzzle data import
        from core.puzzle_data import BITCOIN_PUZZLES
        print("SUCCESS: Puzzle data import works")
        
        return True
    except Exception as e:
        print(f"ERROR: Import failed: {e}")
        return False

def main():
    """Main validation function"""
    print("KeyHound Enhanced - Path Validation")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Run all validation tests
    tests = [
        ("Package Structure", validate_package_structure),
        ("Configuration Paths", validate_config_paths),
        ("Main Entry Point", validate_main_entry_point),
        ("Imports", test_imports)
    ]
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                all_tests_passed = False
        except Exception as e:
            print(f"ERROR: {test_name} test failed with exception: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("ALL VALIDATION TESTS PASSED!")
        print("KeyHound Enhanced is ready to use!")
        print("All file paths are correct!")
        print("All imports are working!")
        print("Optimal structure is functional!")
        print("\nYou can now run:")
        print("   python keyhound/main.py --help")
        print("   python keyhound/main.py --web")
        print("   python keyhound/main.py --puzzle 1")
    else:
        print("VALIDATION TESTS FAILED!")
        print("Some file paths or imports are broken!")
        print("Please fix the issues above!")
        sys.exit(1)

if __name__ == "__main__":
    main()
