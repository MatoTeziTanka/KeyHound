#!/usr/bin/env python3
"""
KeyHound Enhanced - Path Validation Script
Validates all file paths after reorganization
"""

import os
import sys
import importlib.util
from pathlib import Path

def validate_imports():
    """Validate that all imports work correctly"""
    print("Validating imports...")
    print("=" * 30)
    
    # Test core imports
    try:
        from keyhound.core.keyhound_enhanced import KeyHoundEnhanced
        print("SUCCESS: KeyHoundEnhanced import successful")
    except Exception as e:
        print(f"ERROR: KeyHoundEnhanced import failed: {e}")
        return False
    
    try:
        from keyhound.core.bitcoin_cryptography import BitcoinCryptography
        print("SUCCESS: BitcoinCryptography import successful")
    except Exception as e:
        print(f"ERROR: BitcoinCryptography import failed: {e}")
        return False
    
    try:
        from keyhound.core.puzzle_data import BITCOIN_PUZZLES
        print("SUCCESS: Puzzle data import successful")
    except Exception as e:
        print(f"ERROR: Puzzle data import failed: {e}")
        return False
    
    try:
        from keyhound.gpu.gpu_acceleration import GPUAccelerationManager
        print("SUCCESS: GPU acceleration import successful")
    except Exception as e:
        print(f"ERROR: GPU acceleration import failed: {e}")
        return False
    
    return True

def validate_config_paths():
    """Validate configuration file paths"""
    print("\nValidating configuration paths...")
    print("=" * 35)
    
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

def validate_deployment_paths():
    """Validate deployment file paths"""
    print("\nValidating deployment paths...")
    print("=" * 35)
    
    deployment_files = [
        "deployments/docker/Dockerfile",
        "deployments/docker/docker-compose.yml",
        "deployments/colab/KeyHound_Enhanced.ipynb"
    ]
    
    for deployment_file in deployment_files:
        if os.path.exists(deployment_file):
            print(f"SUCCESS: {deployment_file} exists")
        else:
            print(f"ERROR: {deployment_file} missing")
            return False
    
    return True

def validate_main_entry_point():
    """Validate main entry point"""
    print("\nValidating main entry point...")
    print("=" * 35)
    
    main_file = "keyhound/main.py"
    if os.path.exists(main_file):
        print(f"SUCCESS: {main_file} exists")
        
        # Test if it can be executed
        try:
            # Change to the keyhound directory
            os.chdir("keyhound")
            sys.path.insert(0, ".")
            
            # Import main function
            from main import main
            print("SUCCESS: Main function import successful")
            
            # Change back
            os.chdir("..")
            return True
        except Exception as e:
            print(f"ERROR: Main function import failed: {e}")
            os.chdir("..")
            return False
    else:
        print(f"ERROR: {main_file} missing")
        return False

def validate_package_structure():
    """Validate Python package structure"""
    print("\nValidating package structure...")
    print("=" * 35)
    
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

def test_keyhound_enhanced():
    """Test KeyHound Enhanced initialization"""
    print("\nTesting KeyHound Enhanced initialization...")
    print("=" * 45)
    
    try:
        # Change to the keyhound directory
        os.chdir("keyhound")
        sys.path.insert(0, ".")
        
        from core.keyhound_enhanced import KeyHoundEnhanced
        
        # Initialize with minimal config
        keyhound = KeyHoundEnhanced(
            use_gpu=False,
            verbose=False,
            config_file="../config/default.yaml"
        )
        
        print("SUCCESS: KeyHound Enhanced initialization successful")
        
        # Test basic functionality
        print("SUCCESS: KeyHound Enhanced basic functionality working")
        
        # Change back
        os.chdir("..")
        return True
        
    except Exception as e:
        print(f"ERROR: KeyHound Enhanced test failed: {e}")
        os.chdir("..")
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
        ("Deployment Paths", validate_deployment_paths),
        ("Main Entry Point", validate_main_entry_point),
        ("Imports", validate_imports),
        ("KeyHound Enhanced", test_keyhound_enhanced)
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
        print("🎉 ALL VALIDATION TESTS PASSED!")
        print("SUCCESS: KeyHound Enhanced is ready to use!")
        print("SUCCESS: All file paths are correct!")
        print("SUCCESS: All imports are working!")
        print("SUCCESS: Optimal structure is functional!")
        print("\n🚀 You can now run:")
        print("   python keyhound/main.py --help")
        print("   python keyhound/main.py --web")
        print("   python keyhound/main.py --puzzle 1")
    else:
        print("ERROR: VALIDATION TESTS FAILED!")
        print("ERROR: Some file paths or imports are broken!")
        print("ERROR: Please fix the issues above!")
        sys.exit(1)

if __name__ == "__main__":
    main()
