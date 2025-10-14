#!/usr/bin/env python3
"""
KeyHound Enhanced - Simple Functionality Test
Tests basic functionality without complex imports
"""

import sys
import os
from pathlib import Path

def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        "main.py",
        "__init__.py",
        "core/keyhound_enhanced.py",
        "core/bitcoin_cryptography.py",
        "core/puzzle_data.py",
        "core/error_handling.py",
        "config/default.yaml",
        "config/environments/production.yaml",
        "config/environments/colab.yaml",
        "deployments/colab/KeyHound_Enhanced.ipynb",
        "deployments/docker/Dockerfile",
        "requirements.txt",
        "setup.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"SUCCESS: {file_path} exists")
        else:
            print(f"ERROR: {file_path} missing")
            all_exist = False
    
    return all_exist

def test_main_script():
    """Test that the main script can be executed"""
    print("\nTesting main script execution...")
    
    try:
        # Test that main.py exists and can be imported
        main_file = Path("main.py")
        if not main_file.exists():
            print("ERROR: main.py not found")
            return False
        
        # Read the file to check for syntax errors
        with open(main_file, 'r') as f:
            content = f.read()
        
        # Basic syntax check
        try:
            compile(content, str(main_file), 'exec')
            print("SUCCESS: main.py syntax is valid")
            return True
        except SyntaxError as e:
            print(f"ERROR: Syntax error in main.py: {e}")
            return False
        
    except Exception as e:
        print(f"ERROR: Main script test failed: {e}")
        return False

def test_core_modules():
    """Test core modules exist and have basic structure"""
    print("\nTesting core modules...")
    
    core_modules = [
        "core/bitcoin_cryptography.py",
        "core/puzzle_data.py", 
        "core/error_handling.py",
        "core/keyhound_enhanced.py"
    ]
    
    all_valid = True
    for module_file in core_modules:
        if Path(module_file).exists():
            print(f"SUCCESS: {module_file} exists")
            
            # Check for basic class definitions
            with open(module_file, 'r') as f:
                content = f.read()
            
            if "class" in content:
                print(f"  SUCCESS: Contains class definitions")
            else:
                print(f"  WARNING: No class definitions found")
        else:
            print(f"ERROR: {module_file} missing")
            all_valid = False
    
    return all_valid

def test_puzzle_data():
    """Test puzzle data file"""
    print("\nTesting puzzle data...")
    
    puzzle_file = Path("core/puzzle_data.py")
    if not puzzle_file.exists():
        print("ERROR: puzzle_data.py not found")
        return False
    
    try:
        with open(puzzle_file, 'r') as f:
            content = f.read()
        
        # Check for BITCOIN_PUZZLES
        if "BITCOIN_PUZZLES" in content:
            print("SUCCESS: BITCOIN_PUZZLES found in puzzle_data.py")
        else:
            print("WARNING: BITCOIN_PUZZLES not found")
        
        # Basic syntax check
        compile(content, str(puzzle_file), 'exec')
        print("SUCCESS: puzzle_data.py syntax is valid")
        return True
        
    except Exception as e:
        print(f"ERROR: puzzle_data.py test failed: {e}")
        return False

def test_dependencies():
    """Test that requirements.txt exists and has dependencies"""
    print("\nTesting dependencies...")
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("ERROR: requirements.txt not found")
        return False
    
    try:
        with open(req_file, 'r') as f:
            content = f.read()
        
        # Check for key dependencies
        key_deps = ["numpy", "ecdsa", "base58", "cryptography", "pyyaml"]
        found_deps = []
        
        for dep in key_deps:
            if dep.lower() in content.lower():
                found_deps.append(dep)
                print(f"SUCCESS: {dep} found in requirements.txt")
        
        if len(found_deps) >= 3:
            print(f"SUCCESS: {len(found_deps)}/{len(key_deps)} key dependencies found")
            return True
        else:
            print(f"WARNING: Only {len(found_deps)}/{len(key_deps)} key dependencies found")
            return False
        
    except Exception as e:
        print(f"ERROR: Dependencies test failed: {e}")
        return False

def test_deployment_files():
    """Test deployment files"""
    print("\nTesting deployment files...")
    
    deployment_files = [
        "deployments/colab/KeyHound_Enhanced.ipynb",
        "deployments/docker/Dockerfile",
        "deployments/docker/docker-compose.yml"
    ]
    
    all_exist = True
    for file_path in deployment_files:
        if Path(file_path).exists():
            print(f"SUCCESS: {file_path} exists")
        else:
            print(f"ERROR: {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Main test function"""
    print("KeyHound Enhanced - Simple Functionality Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        ("File Structure", test_file_structure),
        ("Main Script", test_main_script),
        ("Core Modules", test_core_modules),
        ("Puzzle Data", test_puzzle_data),
        ("Dependencies", test_dependencies),
        ("Deployment Files", test_deployment_files)
    ]
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                all_tests_passed = False
        except Exception as e:
            print(f"ERROR: {test_name} test failed with exception: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("ALL BASIC FUNCTIONALITY TESTS PASSED!")
        print("KeyHound Enhanced structure is correct!")
        print("All files are in place!")
        print("Ready for dependency installation and testing!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Test imports: python -c 'import core'")
        print("3. Run main: python main.py --help")
    else:
        print("SOME BASIC TESTS FAILED!")
        print("Please review the errors above!")
        print("Fix missing files before proceeding!")

if __name__ == "__main__":
    main()
