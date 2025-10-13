#!/usr/bin/env python3
"""Test script to check KeyHound Enhanced dependencies."""

import sys

def test_dependencies():
    """Test if required dependencies are available."""
    print(f"Python version: {sys.version}")
    print("\nTesting dependencies...")
    
    dependencies = [
        ("flask", "Flask web framework"),
        ("flask_socketio", "Flask-SocketIO for real-time communication"),
        ("numpy", "NumPy for numerical computing"),
        ("psutil", "PSUtil for system monitoring"),
        ("colorama", "Colorama for colored output"),
        ("tqdm", "TQDM for progress bars"),
        ("cryptography", "Cryptography for Bitcoin operations"),
        ("hashlib", "Hashlib for hashing (built-in)"),
        ("json", "JSON handling (built-in)"),
        ("threading", "Threading (built-in)"),
        ("multiprocessing", "Multiprocessing (built-in)"),
        ("sqlite3", "SQLite3 (built-in)"),
        ("pickle", "Pickle (built-in)"),
        ("datetime", "Datetime (built-in)"),
        ("pathlib", "Pathlib (built-in)"),
        ("typing", "Typing (built-in)"),
    ]
    
    missing_deps = []
    available_deps = []
    
    for dep, description in dependencies:
        try:
            __import__(dep)
            available_deps.append(f"[OK] {dep} - {description}")
        except ImportError:
            missing_deps.append(f"[MISSING] {dep} - {description}")
    
    print("\nAvailable dependencies:")
    for dep in available_deps:
        print(f"  {dep}")
    
    if missing_deps:
        print("\nMissing dependencies:")
        for dep in missing_deps:
            print(f"  {dep}")
        
        print("\nTo install missing dependencies, run:")
        print("pip install -r requirements.txt")
        
        return False
    else:
        print("\n[SUCCESS] All core dependencies are available!")
        return True

def test_optional_dependencies():
    """Test optional dependencies for enhanced features."""
    print("\nTesting optional dependencies...")
    
    optional_deps = [
        ("tensorflow", "TensorFlow for machine learning"),
        ("sklearn", "scikit-learn for ML algorithms"),
        ("nltk", "NLTK for natural language processing"),
        ("zmq", "ZeroMQ for distributed computing"),
        ("redis", "Redis for distributed computing"),
        ("cupy", "CuPy for GPU acceleration"),
        ("pyopencl", "PyOpenCL for GPU acceleration"),
        ("numba", "Numba for JIT compilation"),
    ]
    
    available_optional = []
    missing_optional = []
    
    for dep, description in optional_deps:
        try:
            __import__(dep)
            available_optional.append(f"[OK] {dep} - {description}")
        except ImportError:
            missing_optional.append(f"[MISSING] {dep} - {description}")
    
    if available_optional:
        print("\nAvailable optional dependencies:")
        for dep in available_optional:
            print(f"  {dep}")
    
    if missing_optional:
        print("\nMissing optional dependencies (will limit some features):")
        for dep in missing_optional:
            print(f"  {dep}")
    
    return len(available_optional)

if __name__ == "__main__":
    print("KeyHound Enhanced - Dependency Test")
    print("=" * 50)
    
    core_available = test_dependencies()
    optional_count = test_optional_dependencies()
    
    print(f"\nSummary:")
    print(f"  Core dependencies: {'[OK] All available' if core_available else '[MISSING] Some missing'}")
    print(f"  Optional dependencies: {optional_count} available")
    
    if core_available:
        print(f"\n[READY] KeyHound Enhanced is ready to run!")
        if optional_count > 0:
            print(f"[ENHANCED] Enhanced features available with {optional_count} optional dependencies")
        else:
            print(f"[BASIC] Running in basic mode - install optional dependencies for enhanced features")
    else:
        print(f"\n[ERROR] Please install missing core dependencies first")
