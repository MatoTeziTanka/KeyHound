#!/usr/bin/env python3
"""
Test individual imports to isolate issues
"""

import sys
import os

# Add keyhound to path
sys.path.insert(0, "keyhound")

print("Testing individual imports...")

try:
    print("1. Testing core imports...")
    from core.puzzle_data import BITCOIN_PUZZLES
    print("   SUCCESS: puzzle_data imported")
    
    from core.bitcoin_cryptography import BitcoinCryptography
    print("   SUCCESS: bitcoin_cryptography imported")
    
    from core.error_handling import KeyHoundLogger
    print("   SUCCESS: error_handling imported")
    
    print("2. Testing GPU imports...")
    from gpu.gpu_acceleration import GPUAccelerationManager
    print("   SUCCESS: gpu_acceleration imported")
    
    print("3. Testing main KeyHoundEnhanced...")
    from core.keyhound_enhanced import KeyHoundEnhanced
    print("   SUCCESS: KeyHoundEnhanced imported")
    
    print("\nALL IMPORTS SUCCESSFUL!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
